#   _                                                                       _
#  (_)  ___   ___   ___  _ __   ___   __ _  _ __ ___           ___   _ __  | | _   _
#  | | / __| / _ \ / __|| '__| / _ \ / _` || '_ ` _ \         / _ \ | '_ \ | || | | |
#  | || (__ |  __/| (__ | |   |  __/| (_| || | | | | |       | (_) || | | || || |_| |
#  |_| \___| \___| \___||_|    \___| \__,_||_| |_| |_| _____  \___/ |_| |_||_| \__, |
#                                                     |_____|                  |___/
#  The Pythonic, no depencency fork of icecream


__version__ = "0.0.1"

"""

fork from IceCream - Never use print() to debug again
Original author: Ansgar Grunseid / grunseid.com / grunseid@gmail.com

Main differences with icecream:
  icecream_only doesn't depend on ANY external module
  icecream_only is a single source file package, thus easily installed
  icecream_only does not support colouring
  icecream_only can switch on/off time inclusion
  icecream_only introduces delta time that can also be switched on or off
  icecream_only uses PEP8 compatible naming (both in the interface and internal)

(c)2021 Ruud van der Ham - rt.van.der.ham@gmail.com
"""

import ast
import inspect
import pprint
import sys
import datetime
import textwrap
from pathlib import Path

# source of executing module
import __future__
import ast
import dis
import functools
import inspect
import io
import linecache
import sys
import types
from collections import defaultdict, namedtuple
from itertools import islice
from operator import attrgetter
from threading import RLock

from functools import lru_cache
from tokenize import detect_encoding
from itertools import zip_longest
from pathlib import Path

cache = lru_cache(maxsize=None)
text_type = str

try:
    _get_instructions = dis.get_instructions
except AttributeError:

    class Instruction(namedtuple("Instruction", "offset argval opname starts_line")):
        lineno = None

    from dis import HAVE_ARGUMENT, EXTENDED_ARG, hasconst, opname, findlinestarts

    def _get_instructions(co):
        code = co.co_code
        linestarts = dict(findlinestarts(co))
        n = len(code)
        i = 0
        extended_arg = 0
        while i < n:
            offset = i
            c = code[i]
            op = ord(c)
            lineno = linestarts.get(i)
            argval = None
            i = i + 1
            if op >= HAVE_ARGUMENT:
                oparg = ord(code[i]) + ord(code[i + 1]) * 256 + extended_arg
                extended_arg = 0
                i = i + 2
                if op == EXTENDED_ARG:
                    extended_arg = oparg * 65536

                if op in hasconst:
                    argval = co.co_consts[oparg]
            yield Instruction(offset, argval, opname[op], lineno)


def assert_(condition, message=""):
    if not condition:
        raise AssertionError(str(message))


def get_instructions(co):
    lineno = None
    for inst in _get_instructions(co):
        lineno = inst.starts_line or lineno
        assert_(lineno)
        inst.lineno = lineno
        yield inst


class NotOneValueFound(Exception):
    pass


def only(it):
    if hasattr(it, "__len__"):
        if len(it) != 1:
            raise NotOneValueFound(f"Expected one value, found {len(it)}")
        return list(it)[0]

    lst = tuple(islice(it, 2))
    if len(lst) == 0:
        raise NotOneValueFound("Expected one value, found 0")
    if len(lst) > 1:
        raise NotOneValueFound("Expected one value, found several")
    return lst[0]


class Source(object):
    def __init__(self, filename, lines):

        self.filename = filename
        text = "".join(lines)

        if not isinstance(text, text_type):
            encoding = self.detect_encoding(text)
            text = text.decode(encoding)
            lines = [line.decode(encoding) for line in lines]

        self.text = text
        self.lines = [line.rstrip("\r\n") for line in lines]

        ast_text = text
        self._nodes_by_line = defaultdict(list)
        self.tree = None
        self._qualnames = {}

        try:
            self.tree = ast.parse(ast_text, filename=filename)
        except SyntaxError:
            pass
        else:
            for node in ast.walk(self.tree):
                for child in ast.iter_child_nodes(node):
                    child.parent = node
                if hasattr(node, "lineno"):
                    self._nodes_by_line[node.lineno].append(node)

            visitor = QualnameVisitor()
            visitor.visit(self.tree)
            self._qualnames = visitor.qualnames

    @classmethod
    def for_frame(cls, frame, use_cache=True):
        return cls.for_filename(frame.f_code.co_filename, frame.f_globals or {}, use_cache)

    @classmethod
    def for_filename(cls, filename, module_globals=None, use_cache=True):
        if isinstance(filename, Path):
            filename = str(filename)

        source_cache = cls._class_local("__source_cache", {})
        if use_cache:
            try:
                return source_cache[filename]
            except KeyError:
                pass

        if not use_cache:
            linecache.checkcache(filename)

        lines = tuple(linecache.getlines(filename, module_globals))
        result = source_cache[filename] = cls._for_filename_and_lines(filename, lines)
        return result

    @classmethod
    def _for_filename_and_lines(cls, filename, lines):
        source_cache = cls._class_local("__source_cache_with_lines", {})
        try:
            return source_cache[(filename, lines)]
        except KeyError:
            pass

        result = source_cache[(filename, lines)] = cls(filename, lines)
        return result

    @classmethod
    def lazycache(cls, frame):
        if hasattr(linecache, "lazycache"):
            linecache.lazycache(frame.f_code.co_filename, frame.f_globals)

    @classmethod
    def executing(cls, frame_or_tb):
        if isinstance(frame_or_tb, types.TracebackType):
            tb = frame_or_tb
            frame = tb.tb_frame
            lineno = tb.tb_lineno
            lasti = tb.tb_lasti
        else:
            frame = frame_or_tb
            lineno = frame.f_lineno
            lasti = frame.f_lasti

        code = frame.f_code
        key = (code, id(code), lasti)
        executing_cache = cls._class_local("__executing_cache", {})

        try:
            args = executing_cache[key]
        except KeyError:

            def find(source, retry_cache):
                node = stmts = None
                tree = source.tree
                if tree:
                    try:
                        stmts = source.statements_at_line(lineno)
                        if stmts:
                            if code.co_filename.startswith("<ipython-input-") and code.co_name == "<module>":
                                tree = _extract_ipython_statement(stmts, tree)
                            node = NodeFinder(frame, stmts, tree, lasti).result
                    except Exception as e:
                        if retry_cache and isinstance(e, (NotOneValueFound, AssertionError)):
                            return find(source=cls.for_frame(frame, use_cache=False), retry_cache=False)

                    if node:
                        new_stmts = {statement_containing_node(node)}
                        assert_(new_stmts <= stmts)
                        stmts = new_stmts

                return source, node, stmts

            args = find(source=cls.for_frame(frame), retry_cache=True)
            executing_cache[key] = args

        return Executing(frame, *args)

    @classmethod
    def _class_local(cls, name, default):
        result = cls.__dict__.get(name, default)
        setattr(cls, name, result)
        return result

    @cache
    def statements_at_line(self, lineno):
        return {statement_containing_node(node) for node in self._nodes_by_line[lineno]}

    @cache
    def asttokens(self):
        from asttokens import ASTTokens

        return ASTTokens(self.text, tree=self.tree, filename=self.filename)

    @staticmethod
    def decode_source(source):
        if isinstance(source, bytes):
            encoding = Source.detect_encoding(source)
            source = source.decode(encoding)
        return source

    @staticmethod
    def detect_encoding(source):
        return detect_encoding(io.BytesIO(source).readline)[0]

    def code_qualname(self, code):
        assert_(code.co_filename == self.filename)
        return self._qualnames.get((code.co_name, code.co_firstlineno), code.co_name)


class Executing(object):
    def __init__(self, frame, source, node, stmts):
        self.frame = frame
        self.source = source
        self.node = node
        self.statements = stmts

    def code_qualname(self):
        return self.source.code_qualname(self.frame.f_code)

    def text(self):
        return self.source.asttokens().get_text(self.node)

    def text_range(self):
        return self.source.asttokens().get_text_range(self.node)


class QualnameVisitor(ast.NodeVisitor):
    def __init__(self):
        super(QualnameVisitor, self).__init__()
        self.stack = []
        self.qualnames = {}

    def add_qualname(self, node, name=None):
        name = name or node.name
        self.stack.append(name)
        if getattr(node, "decorator_list", ()):
            lineno = node.decorator_list[0].lineno
        else:
            lineno = node.lineno
        self.qualnames.setdefault((name, lineno), ".".join(self.stack))

    def visit_FunctionDef(self, node, name=None):
        self.add_qualname(node, name)
        self.stack.append("<locals>")
        if isinstance(node, ast.Lambda):
            children = [node.body]
        else:
            children = node.body
        for child in children:
            self.visit(child)
        self.stack.pop()
        self.stack.pop()

        for field, child in ast.iter_fields(node):
            if field == "body":
                continue
            if isinstance(child, ast.AST):
                self.visit(child)
            elif isinstance(child, list):
                for grandchild in child:
                    if isinstance(grandchild, ast.AST):
                        self.visit(grandchild)

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_Lambda(self, node):
        self.visit_FunctionDef(node, "<lambda>")

    def visit_ClassDef(self, node):
        self.add_qualname(node)
        self.generic_visit(node)
        self.stack.pop()


future_flags = sum(getattr(__future__, fname).compiler_flag for fname in __future__.all_feature_names)


def compile_similar_to(source, matching_code):
    return compile(source, matching_code.co_filename, "exec", flags=future_flags & matching_code.co_flags, dont_inherit=True)


sentinel = "io8urthglkjdghvljusketgIYRFYUVGHFRTBGVHKGF78678957647698"


class NodeFinder(object):
    def __init__(self, frame, stmts, tree, lasti):
        self.frame = frame
        self.tree = tree
        self.code = code = frame.f_code
        self.is_pytest = any("pytest" in name.lower() for group in [code.co_names, code.co_varnames] for name in group)

        if self.is_pytest:
            self.ignore_linenos = frozenset(assert_linenos(tree))
        else:
            self.ignore_linenos = frozenset()

        instruction = self.get_actual_current_instruction(lasti)
        op_name = instruction.opname
        self.lasti = instruction.offset

        if op_name.startswith("CALL_"):
            typ = ast.Call
        elif op_name.startswith(("BINARY_SUBSCR", "SLICE+")):
            typ = ast.Subscript
        elif op_name.startswith("BINARY_"):
            typ = ast.BinOp
        elif op_name.startswith("UNARY_"):
            typ = ast.UnaryOp
        elif op_name in ("LOAD_ATTR", "LOAD_METHOD", "LOOKUP_METHOD"):
            typ = ast.Attribute
        elif op_name in ("COMPARE_OP", "IS_OP", "CONTAINS_OP"):
            typ = ast.Compare
        else:
            raise RuntimeError(op_name)

        with lock:
            exprs = {
                node for stmt in stmts for node in ast.walk(stmt) if isinstance(node, typ) if not (hasattr(node, "ctx") and not isinstance(node.ctx, ast.Load))
            }

            self.result = only(list(self.matching_nodes(exprs)))

    def clean_instructions(self, code):
        return [inst for inst in get_instructions(code) if inst.opname != "EXTENDED_ARG" if inst.lineno not in self.ignore_linenos]

    def get_original_clean_instructions(self):
        result = self.clean_instructions(self.code)
        if not any(inst.opname == "JUMP_IF_NOT_DEBUG" for inst in self.compile_instructions()):
            result = [inst for inst in result if inst.opname != "JUMP_IF_NOT_DEBUG"]

        return result

    def matching_nodes(self, exprs):
        original_instructions = self.get_original_clean_instructions()
        original_index = only(i for i, inst in enumerate(original_instructions) if inst.offset == self.lasti)
        for i, expr in enumerate(exprs):
            setter = get_setter(expr)
            replacement = ast.BinOp(left=expr, op=ast.Pow(), right=ast.Str(s=sentinel))
            ast.fix_missing_locations(replacement)
            setter(replacement)
            try:
                instructions = self.compile_instructions()
            finally:
                setter(expr)
            indices = [i for i, instruction in enumerate(instructions) if instruction.argval == sentinel]

            for index_num, sentinel_index in enumerate(indices):
                sentinel_index -= index_num * 2

                assert_(instructions.pop(sentinel_index).opname == "LOAD_CONST")
                assert_(instructions.pop(sentinel_index).opname == "BINARY_POWER")

            for index_num, sentinel_index in enumerate(indices):
                sentinel_index -= index_num * 2
                new_index = sentinel_index - 1

                if new_index != original_index:
                    continue

                original_inst = original_instructions[original_index]
                new_inst = instructions[new_index]
                if (
                    original_inst.opname == new_inst.opname in ("CONTAINS_OP", "IS_OP")
                    and original_inst.arg != new_inst.arg
                    and (original_instructions[original_index + 1].opname != instructions[new_index + 1].opname == "UNARY_NOT")
                ):
                    instructions.pop(new_index + 1)

                for inst1, inst2 in zip_longest(original_instructions, instructions):
                    assert_(
                        inst1.opname == inst2.opname
                        or all("JUMP_IF_" in inst.opname for inst in [inst1, inst2])
                        or all(inst.opname in ("JUMP_FORWARD", "JUMP_ABSOLUTE") for inst in [inst1, inst2])
                        or (inst1.opname == "PRINT_EXPR" and inst2.opname == "POP_TOP")
                        or (inst1.opname in ("LOAD_METHOD", "LOOKUP_METHOD") and inst2.opname == "LOAD_ATTR")
                        or (inst1.opname == "CALL_METHOD" and inst2.opname == "CALL_FUNCTION"),
                        (inst1, inst2, ast.dump(expr), expr.lineno, self.code.co_filename),
                    )

                yield expr

    def compile_instructions(self):
        module_code = compile_similar_to(self.tree, self.code)
        code = only(self.find_codes(module_code))
        return self.clean_instructions(code)

    def find_codes(self, root_code):
        checks = [attrgetter("co_firstlineno"), attrgetter("co_name"), attrgetter("co_freevars"), attrgetter("co_cellvars")]
        if not self.is_pytest:
            checks += [attrgetter("co_names"), attrgetter("co_varnames")]

        def matches(c):
            return all(f(c) == f(self.code) for f in checks)

        code_options = []
        if matches(root_code):
            code_options.append(root_code)

        def finder(code):
            for const in code.co_consts:
                if not inspect.iscode(const):
                    continue

                if matches(const):
                    code_options.append(const)
                finder(const)

        finder(root_code)
        return code_options

    def get_actual_current_instruction(self, lasti):
        instructions = list(get_instructions(self.code))
        index = only(i for i, inst in enumerate(instructions) if inst.offset == lasti)

        while True:
            instruction = instructions[index]
            if instruction.opname != "EXTENDED_ARG":
                return instruction
            index += 1


def get_setter(node):
    parent = node.parent
    for name, field in ast.iter_fields(parent):
        if field is node:
            return lambda new_node: setattr(parent, name, new_node)
        elif isinstance(field, list):
            for i, item in enumerate(field):
                if item is node:

                    def setter(new_node):
                        field[i] = new_node

                    return setter


lock = RLock()


@cache
def statement_containing_node(node):
    while not isinstance(node, ast.stmt):
        node = node.parent
    return node


def assert_linenos(tree):
    for node in ast.walk(tree):
        if hasattr(node, "parent") and hasattr(node, "lineno") and isinstance(statement_containing_node(node), ast.Assert):
            yield node.lineno


def _extract_ipython_statement(stmts, tree):
    stmt = list(stmts)[0]
    while not isinstance(stmt.parent, ast.Module):
        stmt = stmt.parent
    tree = ast.parse("")
    tree.body = [stmt]
    ast.copy_location(tree, stmt)
    return tree


# end of source of executing module


def stderr_print(*args):
    print(*args, file=sys.stderr)


def isLiteral(s):
    try:
        ast.literal_eval(s)
    except Exception:
        return False
    return True


class NoSourceAvailableError(OSError):
    infoMessage = (
        "Failed to access the underlying source code for analysis. Was y() "
        "invoked in an interpreter (e.g. python -i), a frozen application "
        "(e.g. packaged with PyInstaller), or did the underlying source code "
        "change during execution?"
    )


def callOrValue(obj):
    return obj() if callable(obj) else obj


class Source(Source):
    def get_text_with_indentation(self, node):
        result = self.asttokens().get_text(node)
        if "\n" in result:
            result = " " * node.first_token.start[1] + result
            result = textwrap.dedent(result)
        result = result.strip()
        return result


def prefixLinesAfterFirst(prefix, s):
    lines = s.splitlines(True)

    for i in range(1, len(lines)):
        lines[i] = prefix + lines[i]

    return "".join(lines)


def indented_lines(prefix, string):
    lines = string.splitlines()
    return [prefix + lines[0]] + [" " * len(prefix) + line for line in lines[1:]]


def format_pair(prefix, arg, value):
    arg_lines = indented_lines(prefix, arg)
    value_prefix = arg_lines[-1] + ": "

    looksLikeAString = value[0] + value[-1] in ["''", '""']
    if looksLikeAString:  # Align the start of multiline strings.
        value = prefixLinesAfterFirst(" ", value)

    value_lines = indented_lines(value_prefix, value)
    lines = arg_lines[:-1] + value_lines
    return "\n".join(lines)


PREFIX = "ic| "
LINE_WRAP_WIDTH = 70  # Characters.
CONTEXT_DELIMITER = ": "
OUTPUT_FUNCTION = lambda self, *args: stderr_print(*args)
ARG_TO_STRING_FUNCTION = lambda self, obj: pprint.pformat(obj).replace("\\n", "\n")
INCLUDE_CONTEXT = False
INCLUDE_TIME = False
INCLUDE_TIME0 = False

ENABLED = True
PAIR_DELIMITER = ", "

starttime = datetime.datetime.now()


class IC:

    prefix = PREFIX
    line_wrap_width = LINE_WRAP_WIDTH
    context_delimiter = CONTEXT_DELIMITER
    output_function = OUTPUT_FUNCTION
    arg_to_string_function = ARG_TO_STRING_FUNCTION
    include_context = INCLUDE_CONTEXT
    include_time = INCLUDE_TIME
    include_time0 = INCLUDE_TIME0
    enabled = ENABLED
    pair_delimiter = PAIR_DELIMITER

    def __init__(self, prefix=None, output_function=None, arg_to_string_function=None, include_context=None, include_time=None, include_time0=None):
        self.configure(
            prefix=prefix,
            output_function=output_function,
            arg_to_string_function=arg_to_string_function,
            include_context=include_context,
            include_time=include_time,
            include_time0=include_time0,
        )

    def __call__(self, *args):
        if self.enabled:
            call_frame = inspect.currentframe().f_back
            try:
                out = self._format(call_frame, *args)
            except NoSourceAvailableError as err:
                prefix = callOrValue(self.prefix)
                out = prefix + "Error: " + err.infoMessage
            self.output_function(out)

        if not args:  # E.g. ic().
            passthrough = None
        elif len(args) == 1:  # E.g. ic(1).
            passthrough = args[0]
        else:  # E.g. y(1, 2, 3).
            passthrough = args

        return passthrough

    def format(self, *args):
        call_frame = inspect.currentframe().f_back
        out = self._format(call_frame, *args)
        return out

    def _format(self, call_frame, *args):
        prefix = callOrValue(self.prefix)

        call_node = Source.executing(call_frame).node
        if call_node is None:
            raise NoSourceAvailableError()

        if len(args) == 0 or self.include_context:
            parts = [self._format_context(call_frame, call_node)]
        else:
            parts = []
        if self.include_time:
            parts.append(f'@ {datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]}')

        if self.include_time0:
            t0 = (datetime.datetime.now() - starttime).total_seconds()
            parts.append(f"\u0394 {t0:.3f}")

        context = " ".join(parts)

        if args:
            return self._format_args(call_frame, call_node, prefix, context, args)
        else:
            return prefix + context

    def _format_args(self, call_frame, call_node, prefix, context, args):
        source = Source.for_frame(call_frame)
        sanitized_args = [source.get_text_with_indentation(arg) for arg in call_node.args]

        pairs = list(zip(sanitized_args, args))

        out = self._construct_argument_output(prefix, context, pairs)
        return out

    def _construct_argument_output(self, prefix, context, pairs):
        def arg_prefix(arg):
            return f"{arg}: "

        pairs = [(arg, self.arg_to_string_function(val)) for arg, val in pairs]
        pairs_processed = [val if isLiteral(arg) else (arg_prefix(arg) + val) for arg, val in pairs]

        all_args_on_one_line = self.pair_delimiter.join(pairs_processed)
        multiline_args = len(all_args_on_one_line.splitlines()) > 1

        context_delimiter = self.context_delimiter if context else ""
        all_pairs = prefix + context + context_delimiter + all_args_on_one_line
        first_line_too_long = len(all_pairs.splitlines()[0]) > self.line_wrap_width

        if multiline_args or first_line_too_long:
            if context:
                lines = [prefix + context] + [format_pair(len(prefix) * " ", arg, value) for arg, value in pairs]
            else:
                arg_lines = [format_pair("", arg, value) for arg, value in pairs]
                lines = indented_lines(prefix, "\n".join(arg_lines))
        else:
            lines = [prefix + context + context_delimiter + all_args_on_one_line]

        return "\n".join(lines)

    def _format_context(self, call_frame, call_node):
        filename, line_number, parent_function = self._get_context(call_frame, call_node)

        if parent_function != "<module>":
            parent_function = f"{parent_function}()"

        context = f"{filename}:{line_number} in {parent_function}"
        return context

    def _get_context(self, call_frame, call_node):
        line_number = call_node.lineno
        frame_info = inspect.getframeinfo(call_frame)
        parent_function = frame_info.function

        filename = Path(frame_info.filename).name

        return filename, line_number, parent_function

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def configure(self, prefix=None, output_function=None, arg_to_string_function=None, include_context=None, include_time=None, include_time0=None):
        if prefix is not None:
            self.prefix = prefix

        if output_function is not None:
            self.output_function = output_function

        if arg_to_string_function is not None:
            self.arg_to_string_function = arg_to_string_function

        if include_context is not None:
            self.include_context = include_context

        if include_time is not None:
            self.include_time = include_time

        if include_time0 is not None:
            self.include_time0 = include_time0


ic = IC()
y = IC(prefix="y| ")
