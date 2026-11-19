"""A warehouse for docstrings added to manufactured ast tools."""
from __future__ import annotations

from astToolFactory import settingsManufacturing
from astToolFactory.documentation import (aDocument, diminutive2etymology, Docstring, docstrings, make1docstring,
    map2PythonDelimiters, map2PythonKeywords, map2PythonOperators)
from astToolkit import Make
import ast

# NOTE "ClassDefIdentifier": {'attribute': "'attributeType' = 'defaultValue'"}

listDocstring: list[Docstring] = []

identifierToolClass: str = settingsManufacturing.identifiers['Make']

attributes = aDocument("Optional source positions. See `Make` for line numbers and byte offsets.", 'ast_attributes')
attributesInt = aDocument("Optional source positions. Supply integer end positions when setting them. See `Make`.",
    'ast_attributes_int')
attributesTypeComment = aDocument("Optional source positions and `type_comment`. See `Make` for source positions.",
    'ast_attributes_type_comment')

listDocstring.append(Docstring(f"{identifierToolClass}.alias"  # ruff: ignore[repeated-append]
    , aDocument("Make an `ast.alias` object for a single name mapping in an import statement.")
    , aDocument("An `ast.alias` represents one imported name, with an optional `as` binding.")
    , Parameters={"dotModule": aDocument(f"({diminutive2etymology['dotModule']}) Name to import. Use a dotted module path in `import` or a "
            "member name in `from ... import`. Use `'*'` for a wildcard in a `from ... import` statement. This "
            "is `ast.alias.name`.", "str")
        , "asName": aDocument(f"({diminutive2etymology['asName']}) Local identifier supplied by `as`. Omit it to use the binding "
            f"implied by the import. This is `ast.alias.asname` ({diminutive2etymology['asname']}).", "str | None = None")
        , "**keywordArguments": attributes}
    , Returns={"importAlias": aDocument("An `ast.alias` object mapping one import name with an optional local alias.", "ast.alias")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.AnnAssign"
    , aDocument(f"Make an `ast.AnnAssign` ({diminutive2etymology['AnnAssign']}) for an annotated assignment.")
    , aDocument(f"An `ast.AnnAssign` ({diminutive2etymology['AnnAssign']}) represents `name: int = 42` or an "
        "annotation without an assignment, such as `name: int`. For a name target, `Make.AnnAssign` sets "
        "`simple=1`, the form used for an unparenthesized name. Attribute and subscription targets use "
        "`simple=0`.")
    , Parameters={"target": aDocument("Assignment target in `Make.Store()` context. Use an `ast.Name`, `ast.Attribute`, or `ast.Subscript`.", "ast.Name | ast.Attribute | ast.Subscript")
        , "annotation": aDocument(f"Annotation expression following `:` (`ast.expr`, {diminutive2etymology['expr']}).", "ast.expr")
        , "value": aDocument("Value expression following `=`. Omit it for an annotation without an assignment.", "ast.expr | None = None")
        , "**keywordArguments": attributes}
    , Returns={"annotatedAssignment": aDocument("The statement for the supplied annotation and optional value.", "ast.AnnAssign")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.arg"
    , aDocument(f"Make an `ast.arg` ({diminutive2etymology['arg']}) for one parameter in a function definition.")
    , aDocument(f"An `ast.arg` ({diminutive2etymology['arg']}) represents a single parameter, including a "
        "positional-only, keyword-only, `*args`, or `**kwargs` parameter. Supply defaults separately in "
        "`Make.arguments`.")
    , Parameters={"Buffalo_buffalo_Buffalo_buffalo_buffalo_buffalo_Buffalo_buffalo": aDocument(f"Name of the parameter, stored in `ast.arg.arg` ({diminutive2etymology['arg']}).", "str")
        , "annotation": aDocument(f"Annotation expression following `:` (`ast.expr`, {diminutive2etymology['expr']}).", "ast.expr | None = None")
        , "type_comment": aDocument(f"({diminutive2etymology['type_comment']}) Type annotation text from a `# type: ...` comment on this parameter.", "str | None = None")
        , "**keywordArguments": attributesTypeComment}
    , Returns={"argumentDefinition": aDocument(f"An `ast.arg` ({diminutive2etymology['arg']}) object representing one function parameter with an "
            "optional type annotation.", "ast.arg")}
    , categories={"Parameter Naming": aDocument("For the first positional-or-keyword parameter of `functionDefinition`, "
            "`functionDefinition.args.args[0].arg` gives the parameter name. The first "
            f"`args` ({diminutive2etymology['args']}) holds the `ast.arguments` specification, and the second "
            f"holds the list of `ast.arg` ({diminutive2etymology['arg']}) objects.")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.arguments"
    , aDocument("Make an `ast.arguments` specification for a function or `lambda`.")
    , aDocument("The `ast.arguments` specification collects the parameters by calling convention and stores their "
        "default expressions in separate lists.")
    , Parameters={"posonlyargs": aDocument(f"({diminutive2etymology['posonlyargs']}) Positional-only parameters that appear before the `/` "
            f"separator (`ast.arg`, {diminutive2etymology['arg']}).", "list[ast.arg] = []")
        , "list_arg": aDocument(f"({diminutive2etymology['list_arg']}) Positional-or-keyword parameters. This is "
            f"`ast.arguments.args` ({diminutive2etymology['args']}).", "list[ast.arg] = []")
        , "vararg": aDocument(f"({diminutive2etymology['vararg']}) The single `*args` parameter that collects extra positional arguments.", "ast.arg | None = None")
        , "kwonlyargs": aDocument(f"({diminutive2etymology['kwonlyargs']}) Keyword-only parameters that appear after `*` or `*args`.", "list[ast.arg] = []")
        , "kw_defaults": aDocument(f"({diminutive2etymology['kw_defaults']}) Default expressions aligned with `kwonlyargs`. Use `None` "
            "for each required parameter and `Make.Constant(None)` for an explicit `None` default "
            f"(`ast.expr`, {diminutive2etymology['expr']}).", "Sequence[ast.expr | None] = []")
        , "kwarg": aDocument(f"({diminutive2etymology['kwarg']}) The single `**kwargs` parameter that collects extra keyword arguments.", "ast.arg | None = None")
        , "defaults": aDocument("Default expressions for the last parameters in the combined `posonlyargs` and `list_arg` lists, in that order.", "Sequence[ast.expr] = []")}
    , Returns={"functionSignature": aDocument("An `ast.arguments` object holding the complete parameter specification.", "ast.arguments")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Assert"
    , aDocument("Make an `ast.Assert` for an `assert` statement.")
    , aDocument("An `ast.Assert` represents a condition checked at runtime. A false test raises `AssertionError`. "
        "Python omits assertions when compiling with optimization enabled.")
    , Parameters={"test": aDocument(f"Expression whose truth value is checked (`ast.expr`, {diminutive2etymology['expr']}).", "ast.expr")
        , "msg": aDocument(f"({diminutive2etymology['msg']}) Expression evaluated when the test is false. Its value becomes the "
            "argument to `AssertionError`.", "ast.expr | None = None")
        , "**keywordArguments": attributes}
    , Returns={"assertStatement": aDocument("An `ast.Assert` object representing an assertion statement.", "ast.Assert")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.AST"
    , aDocument(f"Make an instance of the base class `ast.AST` ({diminutive2etymology['AST']}).")
    , aDocument("Use a specific factory such as `Make.Name`, `Make.Call`, or `Make.Assign` to represent Python syntax.")
    , Returns={"astAST": aDocument("An instance of the common base class for Python syntax objects.", "ast.AST")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Assign"
    , aDocument("Make an `ast.Assign` for an assignment statement.")
    , aDocument("An `ast.Assign` represents a simple assignment such as `x = 5`, an unpacking assignment such as "
        "`a, b = pair`, or a chained assignment such as `a = b = value`.")
    , Parameters={"targets": aDocument("One or more assignment targets in `Make.Store()` context. Use one tuple or list target for "
            f"unpacking, or separate targets for chained assignment (`ast.expr`, {diminutive2etymology['expr']}).", "Sequence[ast.expr]")
        , "value": aDocument("Expression evaluated once. Python assigns the result to each target in order.", "ast.expr")
        , "type_comment": aDocument(f"({diminutive2etymology['type_comment']}) Type annotation text from a `# type: ...` comment on the assignment.", "str | None = None")
        , "**keywordArguments": attributesTypeComment}
    , Returns={"assignment": aDocument("An `ast.Assign` object representing a variable assignment.", "ast.Assign")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.AsyncFor"
    , aDocument(f"Make an `ast.AsyncFor` ({diminutive2etymology['AsyncFor']}) for an `async for` loop.")
    , aDocument(f"An `ast.AsyncFor` ({diminutive2etymology['AsyncFor']}) consumes an asynchronous iterable. The "
        f"optional `orElse` ({diminutive2etymology['orElse']}) clause runs when the asynchronous iterator is "
        "exhausted.")
    , Parameters={"target": aDocument("Assignment target in `Make.Store()` context that receives each item "
            f"(`ast.expr`, {diminutive2etymology['expr']}).", "ast.expr")
        , "iter": aDocument(f"({diminutive2etymology['iter']}) Expression that supplies the asynchronous iterable.", "ast.expr")
        , "body": aDocument(f"Statements executed once per item (`ast.stmt`, {diminutive2etymology['stmt']}).", "Sequence[ast.stmt]")
        , "orElse": aDocument(f"({diminutive2etymology['orElse']}) Statements executed on exhaustion. `break` skips them. This is "
            f"`ast.AsyncFor.orelse` (`AsyncFor` {diminutive2etymology['AsyncFor']}, `orelse` "
            f"{diminutive2etymology['orelse']}).", "Sequence[ast.stmt] = []")
        , "type_comment": aDocument(f"({diminutive2etymology['type_comment']}) Type annotation text for the loop target, from a `# type: ...` comment.", "str | None = None")
        , "**keywordArguments": attributesTypeComment}
    , Returns={"asyncForLoop": aDocument(f"An `ast.AsyncFor` ({diminutive2etymology['AsyncFor']}) object representing an asynchronous `for` loop.", "ast.AsyncFor")}
    , categories={"Async Context": aDocument("Use `async for` inside an `async def` body. To compile it at the top level, pass "
            "`ast.PyCF_ALLOW_TOP_LEVEL_AWAIT` to `compile()`.")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.AsyncFunctionDef"
    , aDocument(f"Make an `ast.AsyncFunctionDef` ({diminutive2etymology['AsyncFunctionDef']}) for `async def`.")
    , aDocument(f"An `ast.AsyncFunctionDef` ({diminutive2etymology['AsyncFunctionDef']}) represents a coroutine "
        "function or, when its body contains `yield`, an asynchronous generator function.")
    , Parameters={"name": aDocument("Function name as a string identifier.", "str")
        , "argumentSpecification": aDocument("Complete parameter specification from `Make.arguments`. Omit it for a function with no parameters. "
            f"This is `ast.AsyncFunctionDef.args` (`AsyncFunctionDef` {diminutive2etymology['AsyncFunctionDef']}"
            f", `args` {diminutive2etymology['args']}).", "ast.arguments = Make.arguments()")
        , "body": aDocument("Statements in the function body. Supply `Make.Pass()` for a body with no other statements "
            f"(`ast.stmt`, {diminutive2etymology['stmt']}).", "Sequence[ast.stmt] = []")
        , "decorator_list": aDocument("Decorator expressions in source order. Python applies them from the last decorator to the first. "
            f"(`ast.expr`, {diminutive2etymology['expr']})", "Sequence[ast.expr] = []")
        , "returns": aDocument(f"({diminutive2etymology['returns']}) Return annotation following `->`.", "ast.expr | None = None")
        , "type_params": aDocument(f"({diminutive2etymology['type_params']}) Type parameters declared in brackets after the function "
            f"name (`ast.type_param`, {diminutive2etymology['type_param']}).", "Sequence[ast.type_param] = []")
        , "type_comment": aDocument(f"({diminutive2etymology['type_comment']}) Function signature text from a `# type: ...` comment, "
            "such as `'(int) -> str'`.", "str | None = None")
        , "**keywordArguments": attributesTypeComment}
    , Returns={"asyncFunction": aDocument(f"An `ast.AsyncFunctionDef` ({diminutive2etymology['AsyncFunctionDef']}) object representing an "
            "asynchronous function definition.", "ast.AsyncFunctionDef")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.AsyncWith"
    , aDocument(f"Make an `ast.AsyncWith` ({diminutive2etymology['AsyncWith']}) for an `async with` statement.")
    , aDocument(f"An `ast.AsyncWith` ({diminutive2etymology['AsyncWith']}) manages one or more asynchronous context "
        f"managers. Each `ast.withitem` ({diminutive2etymology['withitem']}) provides a manager expression "
        "and an optional `as` target for the value returned by `__aenter__`.")
    , Parameters={"items": aDocument(f"Context manager specifications in entry order (`ast.withitem`, {diminutive2etymology['withitem']}).", "list[ast.withitem]")
        , "body": aDocument(f"Statements executed after entering all the context managers (`ast.stmt`, {diminutive2etymology['stmt']}).", "Sequence[ast.stmt]")
        , "type_comment": aDocument(f"({diminutive2etymology['type_comment']}) Type annotation text for the `as` targets, from a `# type: ...` comment.", "str | None = None")
        , "**keywordArguments": attributesTypeComment}
    , Returns={"asyncWithStatement": aDocument(f"An `ast.AsyncWith` ({diminutive2etymology['AsyncWith']}) object representing an asynchronous "
            "context manager statement.", "ast.AsyncWith")}
    , categories={"Async Context": aDocument("Use `async with` inside an `async def` body. To compile it at the top level, pass "
            "`ast.PyCF_ALLOW_TOP_LEVEL_AWAIT` to `compile()`.")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Attribute"
    , aDocument("Make an `ast.Attribute` object for dot notation attribute access.")
    , aDocument("The `ast.Attribute` object represents attribute access using dot notation such as `object.method` "
        "or `module.Class`.")
    , Parameters={"value": aDocument("Base expression providing the object on which attribute access begins "
            f"(`ast.expr`, {diminutive2etymology['expr']}).", "ast.expr")
        , "attribute": aDocument(f"Name following `.`. This is `ast.Attribute.attr` ({diminutive2etymology['attr']}).", "str")
        , "context": aDocument("Use `Make.Load()` to read, `Make.Store()` to assign, or "
            f"`Make.Del()` ({diminutive2etymology['Del']}) to delete. This is "
            f"`ast.Attribute.ctx` ({diminutive2etymology['ctx']}) (`ast.expr_context`, {diminutive2etymology['expr_context']}).", "ast.expr_context = Make.Load()")
        , "**keywordArguments": attributes}
    , Returns={"attributeAccess": aDocument("An `ast.Attribute` object representing the attribute access.", "ast.Attribute")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.AugAssign"
    , aDocument(f"Make an `ast.AugAssign` ({diminutive2etymology['AugAssign']}) for augmented assignment.")
    , aDocument(f"An `ast.AugAssign` ({diminutive2etymology['AugAssign']}) represents an operation such as "
        "`total += item`. Python evaluates the target once and assigns the operation's result back to it. "
        f"Augmented assignment delimiters include `{map2PythonDelimiters['AugAssign'].replace(', ', '`, `')}`.")
    , Parameters={"target": aDocument("One `ast.Name`, `ast.Attribute`, or `ast.Subscript` in `Make.Store()` context.", "ast.Name | ast.Attribute | ast.Subscript")
        , "op": aDocument(f"({diminutive2etymology['op']}) Binary operator for the augmented assignment. For example, "
            "`Make.Add()` represents the operation in `+=`.", "ast.operator")
        , "value": aDocument(f"Right-hand operand of the operation (`ast.expr`, {diminutive2etymology['expr']}).", "ast.expr")
        , "**keywordArguments": attributes}
    , Returns={"augmentedAssignment": aDocument(f"An `ast.AugAssign` ({diminutive2etymology['AugAssign']}) object representing a compound assignment statement.", "ast.AugAssign")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Await"
    , aDocument(f"Make an `ast.Await` ({diminutive2etymology['Await']}) expression.")
    , aDocument(f"An `ast.Await` ({diminutive2etymology['Await']}) can suspend a coroutine until an awaitable produces a result.")
    , Parameters={"value": aDocument("Expression that evaluates to an awaitable, such as a call to an `async def` function "
            f"(`ast.expr`, {diminutive2etymology['expr']}).", "ast.expr")
        , "**keywordArguments": attributes}
    , Returns={"awaitExpression": aDocument(f"An `ast.Await` ({diminutive2etymology['Await']}) object representing a suspension point in a coroutine.", "ast.Await")}
    , categories={"Async Context": aDocument(f"Use `await` ({diminutive2etymology['await']}) inside an `async def` body. To compile it at the top "
            "level, pass `ast.PyCF_ALLOW_TOP_LEVEL_AWAIT` to `compile()`.")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.BinOp"
    , aDocument(f"Make an `ast.BinOp` ({diminutive2etymology['BinOp']}) for a binary operation.")
    , aDocument(f"An `ast.BinOp` ({diminutive2etymology['BinOp']}) represents one operation on two operands, such as "
        "`a + b` or `a | b`. Use an operator class's `join()` to build a left-associated series of "
        "operations.")
    , Parameters={"left": aDocument(f"({diminutive2etymology['left']}) Left operand (`ast.expr`, {diminutive2etymology['expr']}).", "ast.expr")
        , "op": aDocument(f"({diminutive2etymology['op']}) Binary operator, such as `Make.Add()`, "
            f"`Make.Sub()` ({diminutive2etymology['Sub']}), or "
            f"`Make.MatMult()` ({diminutive2etymology['MatMult']}).", "ast.operator")
        , "right": aDocument(f"({diminutive2etymology['right']}) Right operand.", "ast.expr")
        , "**keywordArguments": attributes}
    , Returns={"binaryOperation": aDocument(f"An `ast.BinOp` ({diminutive2etymology['BinOp']}) object representing a two-operand arithmetic, "
            "bitwise, or other binary operation.", "ast.BinOp")}
    , categories={"See Also": aDocument("`Make.Add.join`\n"
            "    Build a series of additions.")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.boolop"
    , aDocument(f"Make an instance of the base class `ast.boolop` ({diminutive2etymology['boolop']}).")
    , aDocument(f"Use `Make.And()` or `Make.Or()` to supply a concrete operator to `Make.BoolOp` ({diminutive2etymology['BoolOp']}).")
    , Returns={"baseBooleanOperator": aDocument(f"A base `ast.boolop` ({diminutive2etymology['boolop']}) object.", "ast.boolop")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.BoolOp"
    , aDocument(f"Make an `ast.BoolOp` ({diminutive2etymology['BoolOp']}) for an `and` or `or` expression.")
    , aDocument(f"An `ast.BoolOp` ({diminutive2etymology['BoolOp']}) stores all operands in an unparenthesized chain "
        "such as `a and b and c`. Python evaluates them from left to right until the result is determined "
        "and returns the last operand evaluated.")
    , Parameters={"op": aDocument(f"({diminutive2etymology['op']}) Operator for the entire chain. Use `Make.And()` or `Make.Or()` "
            f"(`ast.boolop`, {diminutive2etymology['boolop']}).", "ast.boolop")
        , "values": aDocument(f"Two or more operand expressions in evaluation order (`ast.expr`, {diminutive2etymology['expr']}).", "Sequence[ast.expr]")
        , "**keywordArguments": attributes}
    , Returns={"booleanOperation": aDocument("The expression combining all operands in order.", "ast.BoolOp")}
    , categories={"See Also": aDocument("`Make.And.join`\n"
            "    Join expressions with `and`.\n"
            "`Make.Or.join`\n"
            "    Join expressions with `or`.")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Break"
    , aDocument("Make an `ast.Break` object for a `break` statement.")
    , aDocument("A `break` statement exits the nearest enclosing loop and skips its `else` clause.")
    , Returns={"breakStatement": aDocument("An `ast.Break` object representing a loop termination statement.", "ast.Break")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Call"
    , aDocument("Make an `ast.Call` for a call expression.")
    , aDocument("An `ast.Call` represents a call such as `callback(a, *items, key=val, **options)`.")
    , Parameters={"callee": aDocument("Expression that evaluates to the callable. This is "
            f"`ast.Call.func` ({diminutive2etymology['func']}) (`ast.expr`, {diminutive2etymology['expr']}).", "ast.expr")
        , "listParameters": aDocument("Positional argument expressions in call order. Use `Make.Starred` for each `*iterable` argument. "
            f"This is `ast.Call.args` ({diminutive2etymology['args']}).", "Sequence[ast.expr] = []")
        , "list_keyword": aDocument(f"({diminutive2etymology['list_keyword']}) Keyword arguments in call order. Use "
            "`Make.keyword(None, value)` for `**mapping`. This is `ast.Call.keywords`.", "list[ast.keyword] = []")
        , "**keywordArguments": attributes}
    , Returns={"functionCall": aDocument("An `ast.Call` object representing a call expression with positional and keyword arguments.", "ast.Call")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.ClassDef"
    , aDocument(f"Make an `ast.ClassDef` ({diminutive2etymology['ClassDef']}) for a class statement.")
    , aDocument(f"An `ast.ClassDef` ({diminutive2etymology['ClassDef']}) can include base classes, class keywords, "
        "decorators, and a list of type parameters for a generic class.")
    , Parameters={"name": aDocument("Class name as a string identifier.", "str")
        , "bases": aDocument("Sequence of base class expressions for inheritance. An empty sequence produces a class with no "
            f"explicit bases (`ast.expr`, {diminutive2etymology['expr']}).", "Sequence[ast.expr] = []")
        , "list_keyword": aDocument(f"({diminutive2etymology['list_keyword']}) Class keywords such as `metaclass=ABCMeta`. This is "
            f"`ast.ClassDef.keywords` ({diminutive2etymology['ClassDef']}).", "list[ast.keyword] = []")
        , "body": aDocument("Statements in the class body. Supply `Make.Pass()` for a class body with no other statements "
            f"(`ast.stmt`, {diminutive2etymology['stmt']}).", "Sequence[ast.stmt] = []")
        , "decorator_list": aDocument("Decorator expressions in source order. Python applies them from the last decorator to the first.", "Sequence[ast.expr] = []")
        , "type_params": aDocument(f"({diminutive2etymology['type_params']}) Type parameters declared in brackets after the class name. "
            f"(`ast.type_param`, {diminutive2etymology['type_param']})", "Sequence[ast.type_param] = []")
        , "**keywordArguments": attributes}
    , Returns={"classDefinition": aDocument(f"An `ast.ClassDef` ({diminutive2etymology['ClassDef']}) object representing a complete class declaration.", "ast.ClassDef")}
    , categories={"Examples": aDocument("    ```python\n"
            "    from astToolkit import Make\n"
            "\n"
            "    # Creates AST equivalent to: class Vehicle: pass\n"
            "    simpleClass = Make.ClassDef('Vehicle', body=[Make.Pass()])\n"
            "\n"
            "    # Creates AST equivalent to: class Bicycle(Vehicle, metaclass=ABCMeta): pass\n"
            "    inheritedClass = Make.ClassDef(\n"
            "        'Bicycle',\n"
            "        bases=[Make.Name('Vehicle')],\n"
            "        list_keyword=[Make.keyword('metaclass', Make.Name('ABCMeta'))],\n"
            "        body=[Make.Pass()]\n"
            "    )\n"
            "    ```")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.cmpop"
    , aDocument(f"Make an instance of the base class `ast.cmpop` ({diminutive2etymology['cmpop']}).")
    , aDocument(f"Use a concrete comparison operator such as `Make.Eq()` ({diminutive2etymology['Eq']}) or "
        f"`Make.Lt()` ({diminutive2etymology['Lt']}) in `Make.Compare`.")
    , Returns={"comparisonOperator": aDocument(f"A base `ast.cmpop` ({diminutive2etymology['cmpop']}) object.", "ast.cmpop")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Compare"
    , aDocument("Make an `ast.Compare` object for a comparison expression, including chained comparisons.")
    , aDocument("An `ast.Compare` represents a comparison such as `x == 0` or a chain such as `0 <= x < 100`. A "
        "chain compares adjacent operands from left to right, evaluates each intermediate operand once, and "
        "stops at the first false comparison.")
    , Parameters={"left": aDocument(f"({diminutive2etymology['left']}) Leftmost operand (`ast.expr`, {diminutive2etymology['expr']}).", "ast.expr")
        , "ops": aDocument(f"({diminutive2etymology['ops']}) One or more comparison operators, with one operator per entry in "
            f"`comparators` (`ast.cmpop`, {diminutive2etymology['cmpop']}).", "Sequence[ast.cmpop]")
        , "comparators": aDocument("Operands following `left`, in source order. For `a < b <= c`, supply `[b, c]`.", "Sequence[ast.expr]")
        , "**keywordArguments": attributes}
    , Returns={"comparison": aDocument("An `ast.Compare` object representing a comparison or chained comparison expression.", "ast.Compare")}
    , categories={"Examples": aDocument("    ```python\n"
            "    from astToolkit import Make\n"
            "\n"
            "    # Creates AST equivalent to: `temperature == 72`\n"
            "    temperatureCheck = Make.Compare(\n"
            "        left=Make.Name('temperature'),\n"
            "        ops=[Make.Eq()],\n"
            "        comparators=[Make.Constant(72)]\n"
            "    )\n"
            "\n"
            "    # Creates AST equivalent to: `0 <= inventory < 100`\n"
            "    inventoryRange = Make.Compare(\n"
            "        left=Make.Constant(0),\n"
            "        ops=[Make.LtE(), Make.Lt()],\n"
            "        comparators=[Make.Name('inventory'), Make.Constant(100)]\n"
            "    )\n"
            "    ```")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.comprehension"
    , aDocument("Make an `ast.comprehension` for one `for` clause and its filters.")
    , aDocument("The `generators` list of a comprehension or generator expression holds these clauses. Write them "
        "in source order, from the outermost to the innermost loop.")
    , Parameters={"target": aDocument("Assignment target in `Make.Store()` context that receives each item "
            f"(`ast.expr`, {diminutive2etymology['expr']}).", "ast.expr")
        , "iter": aDocument(f"({diminutive2etymology['iter']}) Expression supplying the iterable or asynchronous iterable.", "ast.expr")
        , "ifs": aDocument(f"({diminutive2etymology['ifs']}) Filter expressions following this `for` clause. All must be truthy "
            "for an item to proceed. An empty sequence applies no filter.", "Sequence[ast.expr]")
        , "is_async": aDocument(f"({diminutive2etymology['is_async']}) Use `1` for `async for` or `0` for `for`.", "int = 0")}
    , Returns={"comprehensionClause": aDocument("An `ast.comprehension` object representing one `for` clause with optional filters.", "ast.comprehension")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Constant"
    , aDocument("Make an `ast.Constant` object for a literal value in Python source.")
    , aDocument("An `ast.Constant` stores a literal's Python value. Use "
        f"`Make.UnaryOp` ({diminutive2etymology['UnaryOp']}) for a sign attached to a numeric literal in "
        "source.")
    , Parameters={"value": aDocument("Literal value, such as an integer, float, complex number, string, bytes, `True`, `False`, `None`, or `Ellipsis`.", "ast_ConstantValue")
        , "kind": aDocument("Use `'u'` for a `u`-prefixed string literal. Omit `kind` for other literals.", "str | None = None")
        , "**keywordArguments": attributes}
    , Returns={"constantValue": aDocument("An `ast.Constant` object holding the specified literal value.", "ast.Constant")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Continue"
    , aDocument("Make an `ast.Continue` object for a `continue` statement.")
    , aDocument("A `continue` statement skips the rest of the current iteration of the nearest enclosing loop.")
    , Returns={"continueStatement": aDocument("An `ast.Continue` object representing a loop continuation statement.", "ast.Continue")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Del"
    , aDocument(f"Make an `ast.Del` ({diminutive2etymology['Del']}) context for a deletion target.")
    , aDocument(f"Use `Make.Del()` ({diminutive2etymology['Del']}) as `context` on an expression passed to "
        "`Make.Delete`, such as an attribute in `del bicycle.wheel`.")
    , Returns={"deleteContext": aDocument("Expression context for deletion.", "ast.Del")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Delete"
    , aDocument("Make an `ast.Delete` for a `del` statement.")
    , aDocument("A `del` statement can remove a name binding, an attribute, an item, or a slice.")
    , Parameters={"targets": aDocument(f"One or more targets in `Make.Del()` ({diminutive2etymology['Del']}) context, in deletion order. "
            f"(`ast.expr`, {diminutive2etymology['expr']})", "Sequence[ast.expr]")
        , "**keywordArguments": attributes}
    , Returns={"deleteStatement": aDocument("The `del` statement for the supplied targets.", "ast.Delete")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Dict"
    , aDocument(f"Make an `ast.Dict` ({diminutive2etymology['Dict']}) for a dictionary display.")
    , aDocument(f"An `ast.Dict` ({diminutive2etymology['Dict']}) represents entries such as "
        "`{'name': value, **options}`. Each key has a corresponding expression in `values`. Later entries "
        "replace earlier entries with the same key.")
    , Parameters={"keys": aDocument(f"Key expressions. Use `None` as the key for each `**mapping` entry (`ast.expr`, {diminutive2etymology['expr']}).", "Sequence[ast.expr | None] = []")
        , "values": aDocument("Value expressions paired with `keys`. For an unpacking entry, provide the mapping expression.", "Sequence[ast.expr] = []")
        , "**keywordArguments": attributes}
    , Returns={"dictionaryLiteral": aDocument(f"`AST` ({diminutive2etymology['AST']}) object representing a dictionary literal with specified key-value pairs.", "ast.Dict")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.DictComp"
    , aDocument(f"Make an `ast.DictComp` ({diminutive2etymology['DictComp']}) expression.")
    , aDocument(f"An `ast.DictComp` ({diminutive2etymology['DictComp']}) represents key-value generation such as "
        "`{recipe: difficulty for recipe in cookbook}`. For dictionary unpacking, such as "
        "`{**mapping for mapping in mappings}`, pass the mapping expression as `key` and `None` as `value` [1].")
    , Parameters={"key": aDocument("Expression for each key, or for the mapping to unpack when `value` is `None` "
            f"(`ast.expr`, {diminutive2etymology['expr']}).", "ast.expr")
        , "value": aDocument("Expression for each value. Use `None` to represent `**` unpacking. The factory forwards `None` to "
            f"`ast.DictComp` ({diminutive2etymology['DictComp']}) even though its annotation lists only "
            "`ast.expr`.", "ast.expr | None")
        , "generators": aDocument("`for` clauses and filters in source order.", "list[ast.comprehension]")
        , "**keywordArguments": attributes}
    , Returns={"dictionaryComprehension": aDocument(f"`AST` ({diminutive2etymology['AST']}) object representing a dictionary comprehension expression.", "ast.DictComp")}
    , categories={"See Also": aDocument("`Make.comprehension`\n"
            "    Create one `for` clause and its filters.")
        , "Examples": aDocument("    ```python\n"
            "    from astToolkit import Make\n"
            "\n"
            "    # Creates AST equivalent to: `{recipe: difficulty for recipe in cookbook}`\n"
            "    recipeDifficulty = Make.DictComp(\n"
            "        key=Make.Name('recipe'),\n"
            "        value=Make.Name('difficulty'),\n"
            "        generators=[Make.comprehension(\n"
            "            target=Make.Name('recipe', Make.Store()),\n"
            "            iter=Make.Name('cookbook'),\n"
            "            ifs=[]\n"
            "        )]\n"
            "    )\n"
            "    ```")
        , "References": aDocument("[1] Unpacking in comprehensions\n"
            "    https://docs.python.org/3.15/reference/expressions.html#unpacking-in-comprehensions")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Eq"
    , aDocument(f"Make an `ast.Eq` ({diminutive2etymology['Eq']}) comparison operator.")
    , aDocument(f"Use `ast.Eq` ({diminutive2etymology['Eq']}) in the `ops` ({diminutive2etymology['ops']}) of "
        f"`Make.Compare` to represent `{map2PythonOperators['Eq']}`.")
    , Returns={"equalityOperator": aDocument(f"The operator to put in `ast.Compare.ops` ({diminutive2etymology['ops']}).", "ast.Eq")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.excepthandler"
    , aDocument(f"Make an instance of the base class `ast.excepthandler` ({diminutive2etymology['excepthandler']}).")
    , aDocument(f"Use `Make.ExceptHandler` ({diminutive2etymology['ExceptHandler']}) to make a concrete handler for "
        f"`Make.Try` or `Make.TryStar` ({diminutive2etymology['TryStar']}).")
    , Parameters={"**keywordArguments": attributes}
    , Returns={"exceptionHandler": aDocument(f"Abstract `AST` ({diminutive2etymology['AST']}) object for exception handling clause classification.", "ast.excepthandler")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.ExceptHandler"
    , aDocument(f"Make an `ast.ExceptHandler` ({diminutive2etymology['ExceptHandler']}) clause.")
    , aDocument("The enclosing `ast.Try` represents `except`. The enclosing "
        f"`ast.TryStar` ({diminutive2etymology['TryStar']}) represents `except*` and handles matching "
        "members of an exception group.")
    , Parameters={"type": aDocument("Exception type expression or tuple of types. Omit it for a bare `except` "
            f"(`ast.expr`, {diminutive2etymology['expr']}).", "ast.expr | None = None")
        , "name": aDocument("Identifier after `as`, if supplied.", "str | None = None")
        , "body": aDocument(f"Statements executed when the handler matches (`ast.stmt`, {diminutive2etymology['stmt']}).", "Sequence[ast.stmt] = []")
        , "**keywordArguments": attributes}
    , Returns={"exceptionHandler": aDocument(f"`AST` ({diminutive2etymology['AST']}) object representing an except clause in try-except statements.", "ast.ExceptHandler")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.expr"
    , aDocument(f"Make an instance of the base class `ast.expr` ({diminutive2etymology['expr']}).")
    , aDocument("Use a concrete expression factory, such as `Make.Name` or `Make.Call`, to represent syntax that "
        f"evaluates to a value. Use `Make.Expr` ({diminutive2etymology['Expr']}) to place an expression "
        "where Python expects a statement.")
    , Parameters={"**keywordArguments": attributes}
    , Returns={"expression": aDocument("An instance of the common base class for expressions.", "ast.expr")}
    , categories={"See Also": aDocument("`Make.Expr`\n"
            "    Use an expression as a statement.")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Expr"
    , aDocument(f"Make an `ast.Expr` ({diminutive2etymology['Expr']}) for an expression statement.")
    , aDocument(f"Use an `ast.Expr` ({diminutive2etymology['Expr']}) to put an expression in a statement list, such "
        "as a call made for its side effects or a string used as a docstring.")
    , Parameters={"value": aDocument(f"Expression evaluated as a standalone statement (`ast.expr`, {diminutive2etymology['expr']}).", "ast.expr")
        , "**keywordArguments": attributes}
    , Returns={"expressionStatement": aDocument("A statement containing the supplied expression.", "ast.Expr")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.expr_context"
    , aDocument(f"Make an instance of the base class `ast.expr_context` ({diminutive2etymology['expr_context']}).")
    , aDocument(f"Use `Make.Load()`, `Make.Store()`, or `Make.Del()` ({diminutive2etymology['Del']}) to mark an "
        "expression as a read, an assignment target, or a deletion target.")
    , Returns={"expressionContext": aDocument(f"Abstract `AST` ({diminutive2etymology['AST']}) context object for expression usage classification.", "ast.expr_context")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Expression"
    , aDocument("Make an `ast.Expression` for compilation in `eval` mode.")
    , aDocument("An `ast.Expression` is the outermost object returned by `ast.parse(..., mode='eval')`.")
    , Parameters={"body": aDocument(f"Single expression to evaluate (`ast.expr`, {diminutive2etymology['expr']}).", "ast.expr")}
    , Returns={"expression": aDocument("The expression and its `eval`-mode container.", "ast.Expression")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.For"
    , aDocument("Make an `ast.For` for a `for` loop.")
    , aDocument(f"An `ast.For` consumes an iterable. The optional `orElse` ({diminutive2etymology['orElse']}) clause "
        "runs when the iterator is exhausted.")
    , Parameters={"target": aDocument("Assignment target in `Make.Store()` context that receives each item "
            f"(`ast.expr`, {diminutive2etymology['expr']}).", "ast.expr")
        , "iter": aDocument(f"({diminutive2etymology['iter']}) Expression that supplies the iterable.", "ast.expr")
        , "body": aDocument(f"Statements executed once per item (`ast.stmt`, {diminutive2etymology['stmt']}).", "Sequence[ast.stmt]")
        , "orElse": aDocument(f"({diminutive2etymology['orElse']}) Statements executed on exhaustion. `break` skips them. This is "
            f"`ast.For.orelse` ({diminutive2etymology['orelse']}).", "Sequence[ast.stmt] = []")
        , "type_comment": aDocument(f"({diminutive2etymology['type_comment']}) Type annotation text for the loop target, from a `# type: ...` comment.", "str | None = None")
        , "**keywordArguments": attributesTypeComment}
    , Returns={"forLoop": aDocument(f"`AST` ({diminutive2etymology['AST']}) object representing a for loop iteration construct.", "ast.For")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.FormattedValue"
    , aDocument("Make an `ast.FormattedValue` for a replacement field in an f-string.")
    , aDocument(f"Use `Make.JoinedStr` ({diminutive2etymology['JoinedStr']}) to combine replacement fields and "
        "literal text into an f-string.")
    , Parameters={"value": aDocument(f"Expression inside the braces (`ast.expr`, {diminutive2etymology['expr']}).", "ast.expr")
        , "conversion": aDocument("Use `-1` for no explicit conversion, or `ord('s')`, `ord('r')`, or `ord('a')` for `!s`, `!r`, or `!a`.", "int")
        , "format_spec": aDocument(f"({diminutive2etymology['format_spec']}) Format specification following `:` as an "
            f"`ast.JoinedStr` ({diminutive2etymology['JoinedStr']}). Omit it when the field has no format "
            "specification.", "ast.expr | None = None")
        , "**keywordArguments": attributes}
    , Returns={"formattedValue": aDocument(f"`AST` ({diminutive2etymology['AST']}) object representing a formatted value within an f-string expression.", "ast.FormattedValue")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.FunctionDef"
    , aDocument(f"Make an `ast.FunctionDef` ({diminutive2etymology['FunctionDef']}) for a function.")
    , aDocument(f"An `ast.FunctionDef` ({diminutive2etymology['FunctionDef']}) can include a parameter "
        "specification, decorators, a return annotation, and type parameters for a generic function.")
    , Parameters={"name": aDocument("Function name as string identifier.", "str")
        , "argumentSpecification": aDocument("Complete parameter specification from `Make.arguments`. Omit it for a function with no parameters. "
            f"This is `ast.FunctionDef.args` (`FunctionDef` {diminutive2etymology['FunctionDef']}, `args` "
            f"{diminutive2etymology['args']}).", "ast.arguments = Make.arguments()")
        , "body": aDocument("Statements in the function body. Supply `Make.Pass()` for a body with no other statements "
            f"(`ast.stmt`, {diminutive2etymology['stmt']}).", "Sequence[ast.stmt] = []")
        , "decorator_list": aDocument("Decorator expressions in source order. Python applies them from the last decorator to the first. "
            f"(`ast.expr`, {diminutive2etymology['expr']})", "Sequence[ast.expr] = []")
        , "returns": aDocument(f"({diminutive2etymology['returns']}) Return annotation following `->`.", "ast.expr | None = None")
        , "type_params": aDocument(f"({diminutive2etymology['type_params']}) Type parameters declared in brackets after the function "
            f"name (`ast.type_param`, {diminutive2etymology['type_param']}).", "Sequence[ast.type_param] = []")
        , "type_comment": aDocument(f"({diminutive2etymology['type_comment']}) Function signature text from a `# type: ...` comment, "
            "such as `'(int) -> str'`.", "str | None = None")
        , "**keywordArguments": attributesTypeComment}
    , Returns={"functionDefinition": aDocument(f"`AST` ({diminutive2etymology['AST']}) object representing a complete function definition with metadata.", "ast.FunctionDef")}
    , categories={"Examples": aDocument("    ```python\n"
            "    from astToolkit import Make\n"
            "\n"
            "    # Creates AST equivalent to: def cook(): pass\n"
            "    simpleFunction = Make.FunctionDef('cook', body=[Make.Pass()])\n"
            "\n"
            "    # Define bake with an annotated signature and a default temperature.\n"
            "    typedFunction = Make.FunctionDef(\n"
            "        'bake',\n"
            "        Make.arguments(\n"
            "            list_arg=[Make.arg('recipe', Make.Name('str')), Make.arg('temperature', Make.Name('int'))],\n"
            "            defaults=[Make.Constant(350)]\n"
            "        ),\n"
            "        [Make.Return(Make.Constant(True))],\n"
            "        returns=Make.Name('bool')\n"
            "    )\n"
            "    ```")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.FunctionType"
    , aDocument(f"Make an `ast.FunctionType` ({diminutive2etymology['FunctionType']}) for a function type comment.")
    , aDocument(f"An `ast.FunctionType` ({diminutive2etymology['FunctionType']}) represents text such as "
        "`(int, str) -> bool`, as returned by `ast.parse(..., mode='func_type')`. To attach the comment to "
        f"a function, supply the text as `type_comment` ({diminutive2etymology['type_comment']}) to "
        f"`Make.FunctionDef` ({diminutive2etymology['FunctionDef']}).")
    , Parameters={"argtypes": aDocument(f"({diminutive2etymology['argtypes']}) Parameter type expressions in order "
            f"(`ast.expr`, {diminutive2etymology['expr']}).", "Sequence[ast.expr]")
        , "returns": aDocument(f"({diminutive2etymology['returns']}) Return type expression following `->`.", "ast.expr")}
    , Returns={"functionType": aDocument("The parameter types and return type from a function type comment.", "ast.FunctionType")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.GeneratorExp"
    , aDocument(f"Make an `ast.GeneratorExp` ({diminutive2etymology['GeneratorExp']}) for a generator expression.")
    , aDocument(f"An `ast.GeneratorExp` ({diminutive2etymology['GeneratorExp']}) represents an expression such as "
        "`(item.name for item in items)`. Python evaluates the first iterable when creating the generator, "
        "then produces values as the generator advances.")
    , Parameters={"element": aDocument("Expression that produces a value. For `(*items for items in groups)`, use `Make.Starred` to yield "
            "each unpacked item. This is `ast.GeneratorExp.elt` (`GeneratorExp` "
            f"{diminutive2etymology['GeneratorExp']}, `elt` {diminutive2etymology['elt']}) "
            f"(`ast.expr`, {diminutive2etymology['expr']}).", "ast.expr")
        , "generators": aDocument("`for` clauses and filters in source order.", "list[ast.comprehension]")
        , "**keywordArguments": attributes}
    , Returns={"generatorExpression": aDocument(f"`AST` ({diminutive2etymology['AST']}) object representing a generator expression for lazy evaluation.", "ast.GeneratorExp")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Global"
    , aDocument("Make an `ast.Global` for a `global` declaration.")
    , aDocument("A `global` declaration directs references and assignments to the specified names to module scope "
        "throughout the enclosing code block.")
    , Parameters={"names": aDocument("Identifiers declared global.", "list[str]")
        , "**keywordArguments": attributes}
    , Returns={"globalStatement": aDocument("The declaration for the supplied names.", "ast.Global")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Gt"
    , aDocument(f"Make an `ast.Gt` ({diminutive2etymology['Gt']}) comparison operator.")
    , aDocument(f"Use `ast.Gt` ({diminutive2etymology['Gt']}) in the `ops` ({diminutive2etymology['ops']}) of "
        f"`Make.Compare` to represent `{map2PythonOperators['Gt']}`.")
    , Returns={"greaterThanOperator": aDocument(f"The operator to put in `ast.Compare.ops` ({diminutive2etymology['ops']}).", "ast.Gt")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.GtE"
    , aDocument(f"Make an `ast.GtE` ({diminutive2etymology['GtE']}) comparison operator.")
    , aDocument(f"Use `ast.GtE` ({diminutive2etymology['GtE']}) in the `ops` ({diminutive2etymology['ops']}) of "
        f"`Make.Compare` to represent `{map2PythonOperators['GtE']}`.")
    , Returns={"greaterThanOrEqualOperator": aDocument(f"The operator to put in `ast.Compare.ops` ({diminutive2etymology['ops']}).", "ast.GtE")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.If"
    , aDocument("Make an `ast.If` for an `if` statement.")
    , aDocument(f"Use another `ast.If` as the only statement in `orElse` ({diminutive2etymology['orElse']}) to "
        "represent an `elif` clause.")
    , Parameters={"test": aDocument(f"Condition expression evaluated for truth (`ast.expr`, {diminutive2etymology['expr']}).", "ast.expr")
        , "body": aDocument(f"Statements executed when `test` is truthy (`ast.stmt`, {diminutive2etymology['stmt']}).", "Sequence[ast.stmt]")
        , "orElse": aDocument(f"({diminutive2etymology['orElse']}) Statements executed when `test` is falsy. This is "
            f"`ast.If.orelse` ({diminutive2etymology['orelse']}).", "Sequence[ast.stmt] = []")
        , "**keywordArguments": attributes}
    , Returns={"conditionalStatement": aDocument(f"`AST` ({diminutive2etymology['AST']}) object representing a conditional branching statement.", "ast.If")}
    , categories={"Examples": aDocument("    ```python\n"
            "    from astToolkit import Make\n"
            "\n"
            "    # Creates AST for: if userLoggedIn:\n"
            "    #                     showDashboard()\n"
            "    simpleIf = Make.If(\n"
            "        Make.Name('userLoggedIn'),\n"
            "        [Make.Expr(Make.Call(Make.Name('showDashboard')))]\n"
            "    )\n"
            "\n"
            "    # Creates AST for: if temperature > 100:\n"
            "    #                     activateCooling()\n"
            "    #                 else:\n"
            "    #                     maintainTemperature()\n"
            "    ifElse = Make.If(\n"
            "        Make.Compare(Make.Name('temperature'), [Make.Gt()], [Make.Constant(100)]),\n"
            "        [Make.Expr(Make.Call(Make.Name('activateCooling')))],\n"
            "        [Make.Expr(Make.Call(Make.Name('maintainTemperature')))]\n"
            "    )\n"
            "\n"
            "    # Creates AST for nested if-elif-else chains\n"
            "    ifElifElse = Make.If(\n"
            "        Make.Compare(Make.Name('score'), [Make.GtE()], [Make.Constant(90)]),\n"
            "        [Make.Assign([Make.Name('grade', Make.Store())], Make.Constant('A'))],\n"
            "        [Make.If(\n"
            "            Make.Compare(Make.Name('score'), [Make.GtE()], [Make.Constant(80)]),\n"
            "            [Make.Assign([Make.Name('grade', Make.Store())], Make.Constant('B'))],\n"
            "            [Make.Assign([Make.Name('grade', Make.Store())], Make.Constant('C'))]\n"
            "        )]\n"
            "    )\n"
            "    ```")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.IfExp"
    , aDocument(f"Make an `ast.IfExp` ({diminutive2etymology['IfExp']}) for a conditional expression.")
    , aDocument(f"An `ast.IfExp` ({diminutive2etymology['IfExp']}) represents "
        "`valueIfTrue if condition else valueIfFalse`. Python evaluates the condition and then evaluates "
        "only the selected expression.")
    , Parameters={"test": aDocument(f"Condition expression evaluated for truth (`ast.expr`, {diminutive2etymology['expr']}).", "ast.expr")
        , "body": aDocument("Expression selected when `test` is truthy.", "ast.expr")
        , "orElse": aDocument(f"({diminutive2etymology['orElse']}) Expression selected when `test` is falsy. This is "
            f"`ast.IfExp.orelse` (`IfExp` {diminutive2etymology['IfExp']}, `orelse` "
            f"{diminutive2etymology['orelse']}).", "ast.expr")
        , "**keywordArguments": attributes}
    , Returns={"conditionalExpression": aDocument("The conditional expression with both alternatives.", "ast.IfExp")}
    , categories={"Examples": aDocument("    ```python\n"
            "    from astToolkit import Make\n"
            "\n"
            "    # To create the `ast.AST` representation of `maxVolume if amplified else defaultVolume`:\n"
            "    Make.IfExp(\n"
            "        test = Make.Name('amplified'),\n"
            "        body = Make.Name('maxVolume'),\n"
            "        orElse = Make.Name('defaultVolume')\n"
            "    )\n"
            "\n"
            "    # To create the `ast.AST` representation of `\"sunny\" if weather > 70 else \"cloudy\"`:\n"
            "    Make.IfExp(\n"
            "        test = Make.Compare(Make.Name('weather'), [ Make.Gt() ], [ Make.Constant(70) ]),\n"
            "        body = Make.Constant(\"sunny\"),\n"
            "        orElse = Make.Constant(\"cloudy\")\n"
            "    )\n"
            "    ```")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Import"
    , aDocument("Make an `ast.Import` for one module in an `import` statement.")
    , aDocument("`Make.Import` supplies the single `ast.alias` stored in `ast.Import.names`. A plain `import` "
        "accepts an absolute module path such as `collections.abc`. Use `Make.ImportFrom` for relative "
        "imports.")
    , Parameters={"dotModule": aDocument(f"({diminutive2etymology['dotModule']}) Absolute module name, optionally "
            "dotted. This is `ast.Import.names[0].name`.", "identifierDotAttribute")
        , "asName": aDocument(f"({diminutive2etymology['asName']}) Local identifier after `as`. When omitted, the import binds the "
            f"first component of `dotModule`. This is `ast.Import.names[0].asname` ({diminutive2etymology['asname']}).", "str | None = None")
        , "is_lazy": aDocument("Use `True` to represent the `lazy` prefix. Omit it or use `False` for a regular "
            "`import` statement. Explicit lazy imports require module scope and exclude `try` blocks [1].", "bool | None = None")
        , "**keywordArguments": attributes}
    , Returns={"importStatement": aDocument("An `ast.Import` object with one `ast.alias` object representing a single `import` statement with a "
            "single module name.", "ast.Import")}
    , categories={"See Also": aDocument("`Make.ImportFrom`\n"
            "    Import names from a module.")
        , "Examples": aDocument("    ```python\n"
            "    from astToolkit import Make\n"
            "\n"
            "    # To represent: `import os`\n"
            "    Make.Import(dotModule = 'os')\n"
            "\n"
            "    # To represent: `import re as regex`\n"
            "    Make.Import(dotModule = 're', asName = 'regex')\n"
            "\n"
            "    # To represent: `import collections.abc`\n"
            "    Make.Import(dotModule = 'collections.abc')\n"
            "\n"
            "    # To represent: `import scipy.signal.windows as SciPy`\n"
            "    Make.Import(dotModule = 'scipy.signal.windows', asName = 'SciPy')\n"
            "    ```")
        , "References": aDocument("[1] Lazy imports.\n"
            "    https://docs.python.org/3.15/reference/simple_stmts.html#lazy-imports")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.ImportFrom"
    , aDocument("Make an `ast.ImportFrom` for a `from ... import` statement.")
    , aDocument("An `ast.ImportFrom` represents one source module and one or more names from it. For a relative "
        f"import, supply the leading dots as `level` ({diminutive2etymology['level']}).")
    , Parameters={"dotModule": aDocument(f"({diminutive2etymology['dotModule']}) Module name without leading dots. Use `None` for a statement "
            "such as `from . import sibling`. This is `ast.ImportFrom.module`.", "str | None")
        , "list_alias": aDocument("Imported names and any local aliases from `Make.alias`. Use `[Make.alias('*')]` for a wildcard "
            "import. This is `ast.ImportFrom.names`.", "list[ast.alias]")
        , "level": aDocument(f"({diminutive2etymology['level']}) Number of leading dots. `0` means an absolute import, `1` means "
            "the current package, and `2` means the parent package.", "int = 0")
        , "is_lazy": aDocument("Use `True` to represent the `lazy` prefix. Omit it or use `False` for a regular `from ... import` "
            "statement. Explicit lazy imports require module scope and exclude `try` blocks, wildcard imports, "
            "and future imports [1].", "bool | None = None")
        , "**keywordArguments": attributes}
    , Returns={"fromImportStatement": aDocument(f"`AST` ({diminutive2etymology['AST']}) object representing a selective module import statement.", "ast.ImportFrom")}
    , categories={"See Also": aDocument("`Make.Import`\n"
            "    Import a module by its absolute name.")
        , "References": aDocument("[1] Lazy imports.\n"
            "    https://docs.python.org/3.15/reference/simple_stmts.html#lazy-imports")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.In"
    , aDocument("Make an `ast.In` comparison operator.")
    , aDocument(f"Use `ast.In` in the `ops` ({diminutive2etymology['ops']}) of `Make.Compare` to represent "
        f"{map2PythonKeywords['In']}. Python tests the left operand for membership in the right operand.")
    , Returns={"membershipOperator": aDocument(f"The operator to put in `ast.Compare.ops` ({diminutive2etymology['ops']}).", "ast.In")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Interactive"
    , aDocument(f"Make an `ast.Interactive` ({diminutive2etymology['Interactive']}) for compilation in `single` mode.")
    , aDocument(f"An `ast.Interactive` ({diminutive2etymology['Interactive']}) is the outermost object returned by "
        "`ast.parse(..., mode='single')`. Interactive execution displays the result of an expression "
        "statement when the result is other than `None`.")
    , Parameters={"body": aDocument(f"Statements to execute in interactive mode (`ast.stmt`, {diminutive2etymology['stmt']}).", "Sequence[ast.stmt]")}
    , Returns={"interactive": aDocument("The statements and their `single`-mode container.", "ast.Interactive")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Interpolation"
    , aDocument("Make an `ast.Interpolation` for a replacement field in a t-string.")
    , aDocument(f"Use `Make.TemplateStr` ({diminutive2etymology['TemplateStr']}) to combine replacement fields with "
        "literal text. Each field records its expression, original source text, conversion, and format "
        "specification.")
    , Parameters={"value": aDocument(f"Expression inside the braces (`ast.expr`, {diminutive2etymology['expr']}).", "ast.expr")
        , "string": aDocument("Original source text of the expression, stored in "
            f"`ast.Interpolation.str` ({diminutive2etymology['str']}). `None` asks `ast.unparse()` to regenerate "
            "the text from `value` [1]. The factory accepts `None` at runtime while its annotation lists `str`.", "str | None")
        , "conversion": aDocument("Use `-1` for no explicit conversion, or `ord('s')`, `ord('r')`, or `ord('a')` for `!s`, `!r`, or `!a`.", "int")
        , "format_spec": aDocument(f"({diminutive2etymology['format_spec']}) Format specification following `:` as an "
            f"`ast.JoinedStr` ({diminutive2etymology['JoinedStr']}). Omit it when the field has no format "
            "specification.", "ast.expr | None = None")
        , "**keywordArguments": attributes}
    , Returns={"interpolation": aDocument(f"`AST` ({diminutive2etymology['AST']}) object representing an interpolation component of a template string.", "ast.Interpolation")}
    , categories={"References": aDocument("[1] `ast.Interpolation`.\n"
            "    https://docs.python.org/3.15/library/ast.html#ast.Interpolation")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Invert"
    , aDocument("Make an `ast.Invert` operator for `~value`.")
    , aDocument(f"Use `ast.Invert` as `op` ({diminutive2etymology['op']}) in "
        f"`Make.UnaryOp` ({diminutive2etymology['UnaryOp']}). For an integer `x`, `~x` evaluates to "
        "`-(x + 1)`.")
    , Returns={"bitwiseComplementOperator": aDocument(f"`AST` ({diminutive2etymology['AST']}) object representing the '`~`' bitwise complement operator "
            f"for use in `ast.UnaryOp` ({diminutive2etymology['UnaryOp']}).", "ast.Invert")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Is"
    , aDocument("'Is', meaning 'Is identical to', is the `object` representation of Python keyword '`is`'.", AIgenerated=False)
    , aDocument(f"`ast.Is` is a subclass of `ast.cmpop` ({diminutive2etymology['cmpop']}). Use it in the `ops` ({diminutive2etymology['ops']}) of `Make.Compare` to represent {map2PythonKeywords['Is']}. Both operands must refer to the same object for the comparison to be true.\n"
        "\n"
        "What's the difference between equality and identity? The work of Jane Austen 'is Equal to' the work of Franz Kafka. The work of Mark Twain 'is Equal to' the work of Samuel Clemens. And Mark Twain 'Is identical to' Samuel Clemens because they are the same person.", AIgenerated=False)
    , Returns={"identityOperator": aDocument("The `is` operator for use in `ast.Compare`.", "ast.Is", AIgenerated=False)}
    , categories={"Examples": aDocument("    ```python\n"
            "    from astToolkit import Make\n"
            "\n"
            "    # Equivalent to valueAttributes is None.\n"
            "    Make.Compare(\n"
            "        left=Make.Name('valueAttributes'), ops=[Make.Is()], comparators=[Make.Constant(None)]\n"
            "    )\n"
            "    ```", AIgenerated=False)}
))

listDocstring.append(Docstring(f"{identifierToolClass}.IsNot"
    , aDocument("Make an `ast.IsNot` operator for `is not`.")
    , aDocument(f"Use `ast.IsNot` in the `ops` ({diminutive2etymology['ops']}) of `Make.Compare` to represent "
        f"{map2PythonKeywords['IsNot']}. Python evaluates `a is not b` as true when the operands refer to "
        "different objects. For example, `chicken is not None` checks whether `chicken` refers to an object "
        "other than the `None` singleton.")
    , Returns={"identityNegationOperator": aDocument("The identity comparison operator for use in `ast.Compare`.", "ast.IsNot")}
    , categories={"Examples": aDocument("    ```python\n"
            "    from astToolkit import Make\n"
            "\n"
            "    # Equivalent to chicken is not None.\n"
            "    Make.Compare(\n"
            "        left=Make.Name('chicken'), ops=[Make.IsNot()], comparators=[Make.Constant(None)]\n"
            "    )\n"
            "    ```")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.JoinedStr"
    , aDocument(f"Make an `ast.JoinedStr` ({diminutive2etymology['JoinedStr']}) for an f-string.")
    , aDocument(f"An `ast.JoinedStr` ({diminutive2etymology['JoinedStr']}) combines literal text and formatted "
        "values in source order. You can also use it for the format specification of a replacement field.")
    , Parameters={"values": aDocument("Use an `ast.Constant` containing a string for each literal part and an `ast.FormattedValue` for "
            f"each replacement field (`ast.expr`, {diminutive2etymology['expr']}).", "Sequence[ast.expr]")
        , "**keywordArguments": attributes}
    , Returns={"joinedString": aDocument(f"`AST` ({diminutive2etymology['AST']}) object representing an f-string literal with interpolated values.", "ast.JoinedStr")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.keyword"
    , aDocument("Make an `ast.keyword` for a keyword argument or `**` unpacking.")
    , aDocument("Use an `ast.keyword` in a call or class definition to represent forms such as `temperature=350` or `**settings`.")
    , Parameters={"Buffalo_buffalo_Buffalo_buffalo_buffalo_buffalo_Buffalo_buffalo": aDocument(f"Keyword name, stored in `ast.keyword.arg` ({diminutive2etymology['arg']}). Pass `None` explicitly for `**mapping`.", "str | None")
        , "value": aDocument("Argument value expression. For `**mapping`, this is the expression that provides the mapping "
            f"(`ast.expr`, {diminutive2etymology['expr']}).", "ast.expr")
        , "**keywordArguments": attributes}
    , Returns={"keywordArgument": aDocument(f"`AST` ({diminutive2etymology['AST']}) object representing a named argument in function calls.", "ast.keyword")}
    , categories={"Examples": aDocument("Creates AST equivalent to temperature=350.\n"
            "    ```python\n"
            "    from astToolkit import Make\n"
            "\n"
            "    namedArgument = Make.keyword('temperature', Make.Constant(350))\n"
            "    ```\n"
            "\n"
            "Creates AST equivalent to **settings (keyword arguments unpacking).\n"
            "    ```python\n"
            "    from astToolkit import Make\n"
            "\n"
            "    unpackedArguments = Make.keyword(None, Make.Name('settings'))\n"
            "    ```")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Lambda"
    , aDocument(f"Make an `ast.Lambda` ({diminutive2etymology['Lambda']}) for a `lambda` expression.")
    , aDocument("A `lambda` creates a function whose result is the value of its body expression.")
    , Parameters={"argumentSpecification": aDocument("Parameter specification from `Make.arguments`. This is `ast.Lambda.args` (`Lambda` "
            f"{diminutive2etymology['Lambda']}, `args` {diminutive2etymology['args']}).", "ast.arguments")
        , "body": aDocument(f"Expression evaluated on each call (`ast.expr`, {diminutive2etymology['expr']}).", "ast.expr")
        , "**keywordArguments": attributes}
    , Returns={"lambdaFunction": aDocument(f"`AST` ({diminutive2etymology['AST']}) object representing an anonymous lambda function expression.", "ast.Lambda")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.List"
    , aDocument("Make an `ast.List` for a list display or unpacking target.")
    , aDocument("An `ast.List` represents bracketed forms such as `[a, b]`. The context indicates how Python uses the expression.")
    , Parameters={"listElements": aDocument(f"Element expressions in order. This is `ast.List.elts` ({diminutive2etymology['elts']}) "
            f"(`ast.expr`, {diminutive2etymology['expr']}).", "Sequence[ast.expr] = []")
        , "context": aDocument("Use `Make.Load()` to build a list, `Make.Store()` for an assignment target, or "
            f"`Make.Del()` ({diminutive2etymology['Del']}) for a deletion target. This is "
            f"`ast.List.ctx` ({diminutive2etymology['ctx']}) (`ast.expr_context`, {diminutive2etymology['expr_context']}).", "ast.expr_context = Make.Load()")
        , "**keywordArguments": attributes}
    , Returns={"listLiteral": aDocument(f"`AST` ({diminutive2etymology['AST']}) object representing a list literal with specified elements.", "ast.List")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.ListComp"
    , aDocument(f"Make an `ast.ListComp` ({diminutive2etymology['ListComp']}) for a list comprehension.")
    , aDocument(f"An `ast.ListComp` ({diminutive2etymology['ListComp']}) represents a list comprehension such as "
        "`[item.name for item in items]`.")
    , Parameters={"element": aDocument("Expression that supplies each element. Use `Make.Starred` for unpacking, as in "
            "`[*items for items in groups]`. This is `ast.ListComp.elt` (`ListComp` "
            f"{diminutive2etymology['ListComp']}, `elt` {diminutive2etymology['elt']}) "
            f"(`ast.expr`, {diminutive2etymology['expr']}).", "ast.expr")
        , "generators": aDocument("`for` clauses and filters in source order.", "list[ast.comprehension]")
        , "**keywordArguments": attributes}
    , Returns={"listComprehension": aDocument(f"`AST` ({diminutive2etymology['AST']}) object representing a list comprehension expression.", "ast.ListComp")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Load"
    , aDocument("Make an `ast.Load` context for reading a value.")
    , aDocument("Use `Make.Load()` to represent an expression such as `bicycle.wheel` when it retrieves the wheel "
        "attribute. Value references made by `Make.Name` and `Make.Attribute` use this context by default.")
    , Returns={"loadContext": aDocument(f"`AST` ({diminutive2etymology['AST']}) context object indicating value retrieval operations.", "ast.Load")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Lt"
    , aDocument(f"Make an `ast.Lt` ({diminutive2etymology['Lt']}) comparison operator.")
    , aDocument(f"Use `ast.Lt` ({diminutive2etymology['Lt']}) in the `ops` ({diminutive2etymology['ops']}) of "
        f"`Make.Compare` to represent `{map2PythonOperators['Lt']}`.")
    , Returns={"lessThanOperator": aDocument(f"The operator to put in `ast.Compare.ops` ({diminutive2etymology['ops']}).", "ast.Lt")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.LtE"
    , aDocument(f"Make an `ast.LtE` ({diminutive2etymology['LtE']}) comparison operator.")
    , aDocument(f"Use `ast.LtE` ({diminutive2etymology['LtE']}) in the `ops` ({diminutive2etymology['ops']}) of "
        f"`Make.Compare` to represent `{map2PythonOperators['LtE']}`.")
    , Returns={"lessThanOrEqualOperator": aDocument(f"The operator to put in `ast.Compare.ops` ({diminutive2etymology['ops']}).", "ast.LtE")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Match"
    , aDocument(f"Make an `ast.Match` ({diminutive2etymology['Match']}) for a `match` statement.")
    , aDocument(f"An `ast.Match` ({diminutive2etymology['Match']}) evaluates the subject once and tries the cases in "
        "source order. The first case whose pattern matches and whose guard succeeds supplies the body to "
        "execute.")
    , Parameters={"subject": aDocument(f"Expression that supplies the value to match (`ast.expr`, {diminutive2etymology['expr']}).", "ast.expr")
        , "cases": aDocument("Case clauses in source order. Supply at least one "
            f"`Make.match_case` ({diminutive2etymology['match_case']}) for a complete statement.", "list[ast.match_case] = []")
        , "**keywordArguments": attributes}
    , Returns={"matchStatement": aDocument(f"`AST` ({diminutive2etymology['AST']}) object representing a complete pattern matching statement.", "ast.Match")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.match_case"
    , aDocument(f"Make an `ast.match_case` ({diminutive2etymology['match_case']}) for one `case` clause.")
    , aDocument("A case selects a body when its pattern matches and its optional guard is truthy.")
    , Parameters={"pattern": aDocument("Pattern applied to the subject of the enclosing `match`.", "ast.pattern")
        , "guard": aDocument("Condition evaluated after the pattern matches and its names are bound "
            f"(`ast.expr`, {diminutive2etymology['expr']}).", "ast.expr | None = None")
        , "body": aDocument(f"Statements executed when the case is selected (`ast.stmt`, {diminutive2etymology['stmt']}).", "Sequence[ast.stmt] = []")}
    , Returns={"matchCase": aDocument(f"`AST` ({diminutive2etymology['AST']}) object representing a single case clause in match statements.", "ast.match_case")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.MatchAs"
    , aDocument(f"Make an `ast.MatchAs` ({diminutive2etymology['MatchAs']}) for an `as` pattern or a capture.")
    , aDocument(f"An `ast.MatchAs` ({diminutive2etymology['MatchAs']}) can represent `Point(x, y) as location`, a "
        "capture such as `location`, or the wildcard `_`.")
    , Parameters={"pattern": aDocument("Pattern to match before binding `name`. Supply `name` with any explicit `pattern`.", "ast.pattern | None = None")
        , "name": aDocument("Identifier to bind to the matched subject. When both fields are `None`, the result represents `_`.", "str | None = None")
        , "**keywordArguments": attributesInt}
    , Returns={"matchAs": aDocument(f"An `ast.MatchAs` ({diminutive2etymology['MatchAs']}) object with the specified pattern and name.", "ast.MatchAs")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.MatchClass"
    , aDocument(f"Make an `ast.MatchClass` ({diminutive2etymology['MatchClass']}) for a class pattern.")
    , aDocument(f"An `ast.MatchClass` ({diminutive2etymology['MatchClass']}) represents a pattern such as "
        "`Point(x, y=0)`. Python checks the subject with `isinstance()` and matches attribute values "
        "against the supplied subpatterns.")
    , Parameters={"cls": aDocument(f"({diminutive2etymology['cls']}) Expression identifying the class, such as `Point` or "
            f"`geometry.Point` (`ast.expr`, {diminutive2etymology['expr']}).", "ast.expr")
        , "patterns": aDocument("Positional subpatterns. For most classes, `__match_args__` determines the corresponding attributes.", "Sequence[ast.pattern] = []")
        , "kwd_attrs": aDocument(f"({diminutive2etymology['kwd_attrs']}) Attribute names from keyword subpatterns, in source order.", "list[str] = []")
        , "kwd_patterns": aDocument(f"({diminutive2etymology['kwd_patterns']}) Subpatterns paired with `kwd_attrs`, in the same order.", "Sequence[ast.pattern] = []")
        , "**keywordArguments": attributesInt}
    , Returns={"matchClass": aDocument(f"An `ast.MatchClass` ({diminutive2etymology['MatchClass']}) object configured for the specified class and patterns.", "ast.MatchClass")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.MatchMapping"
    , aDocument(f"Make an `ast.MatchMapping` ({diminutive2etymology['MatchMapping']}) for a mapping pattern.")
    , aDocument(f"An `ast.MatchMapping` ({diminutive2etymology['MatchMapping']}) represents a pattern such as "
        "`{'name': name, **extra}`. A mapping can match when it contains additional keys.")
    , Parameters={"keys": aDocument(f"Literal or dotted-name key expressions (`ast.expr`, {diminutive2etymology['expr']}).", "Sequence[ast.expr] = []")
        , "patterns": aDocument("Patterns for the values associated with `keys`, in the same order.", "Sequence[ast.pattern] = []")
        , "rest": aDocument(f"({diminutive2etymology['rest']}) Capture name after `**`. When supplied, it receives a dictionary "
            "of the remaining items.", "str | None = None")
        , "**keywordArguments": attributesInt}
    , Returns={"matchMapping": aDocument(f"An `ast.MatchMapping` ({diminutive2etymology['MatchMapping']}) object for the specified key-value "
            "patterns and optional rest capture.", "ast.MatchMapping")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.MatchOr"
    , aDocument(f"Make an `ast.MatchOr` ({diminutive2etymology['MatchOr']}) for alternative patterns.")
    , aDocument(f"An `ast.MatchOr` ({diminutive2etymology['MatchOr']}) represents alternatives separated by `|`. "
        "Python tries them from left to right. Every alternative must bind the same names.")
    , Parameters={"patterns": aDocument("Two or more alternatives in matching order.", "Sequence[ast.pattern] = []")
        , "**keywordArguments": attributesInt}
    , Returns={"matchOr": aDocument(f"An `ast.MatchOr` ({diminutive2etymology['MatchOr']}) object containing the alternative patterns.", "ast.MatchOr")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.MatchSequence"
    , aDocument(f"Make an `ast.MatchSequence` ({diminutive2etymology['MatchSequence']}) for a sequence pattern.")
    , aDocument(f"An `ast.MatchSequence` ({diminutive2etymology['MatchSequence']}) represents patterns such as "
        "`[first, *rest]` or `(x, y)`. Sequence patterns exclude strings, bytes, and byte arrays.")
    , Parameters={"patterns": aDocument(f"Element patterns in order. One `ast.MatchStar` ({diminutive2etymology['MatchStar']}) can capture a "
            "variable-length portion of the sequence.", "Sequence[ast.pattern] = []")
        , "**keywordArguments": attributesInt}
    , Returns={"matchSequence": aDocument(f"An `ast.MatchSequence` ({diminutive2etymology['MatchSequence']}) object for the specified element patterns.", "ast.MatchSequence")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.MatchSingleton"
    , aDocument(f"Make an `ast.MatchSingleton` ({diminutive2etymology['MatchSingleton']}) for a singleton pattern.")
    , aDocument(f"An `ast.MatchSingleton` ({diminutive2etymology['MatchSingleton']}) compares the subject by "
        "identity with `None`, `True`, or `False`.")
    , Parameters={"value": aDocument("Singleton to match. Use `None`, `True`, or `False`.", "bool | None")
        , "**keywordArguments": attributesInt}
    , Returns={"matchSingleton": aDocument(f"An `ast.MatchSingleton` ({diminutive2etymology['MatchSingleton']}) object for the specified singleton value.", "ast.MatchSingleton")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.MatchStar"
    , aDocument(f"Make an `ast.MatchStar` ({diminutive2etymology['MatchStar']}) for a starred sequence pattern.")
    , aDocument(f"An `ast.MatchStar` ({diminutive2etymology['MatchStar']}) represents `*rest` or `*_` inside a "
        "sequence pattern. It matches the elements left after the fixed positions on either side are "
        "accounted for.")
    , Parameters={"name": aDocument("Capture name for the list of remaining elements. Use `None` for `*_`.", "str | None = None")
        , "**keywordArguments": attributesInt}
    , Returns={"matchStar": aDocument(f"An `ast.MatchStar` ({diminutive2etymology['MatchStar']}) object with the specified capture name.", "ast.MatchStar")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.MatchValue"
    , aDocument(f"Make an `ast.MatchValue` ({diminutive2etymology['MatchValue']}) for a value pattern.")
    , aDocument(f"An `ast.MatchValue` ({diminutive2etymology['MatchValue']}) compares the subject with a literal or "
        "the value of a dotted name using `==`. Use "
        f"`Make.MatchSingleton` ({diminutive2etymology['MatchSingleton']}) for `None`, `True`, and `False`.")
    , Parameters={"value": aDocument(f"Literal expression or dotted name such as `Color.RED` (`ast.expr`, {diminutive2etymology['expr']}).", "ast.expr")
        , "**keywordArguments": attributesInt}
    , Returns={"matchValue": aDocument(f"An `ast.MatchValue` ({diminutive2etymology['MatchValue']}) object for the specified value expression.", "ast.MatchValue")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.mod", aDocument(f"Create an abstract `ast.mod` ({diminutive2etymology['mod']}) `object`.", AIgenerated=False)))

listDocstring.append(Docstring(f"{identifierToolClass}.Module"
    , aDocument("Make an `ast.Module` for a sequence of top-level statements.")
    , aDocument("An `ast.Module` represents source compiled in `exec` mode. You can also store the module's "
        "`# type: ignore` comments.")
    , Parameters={"body": aDocument(f"Top-level statements in source order (`ast.stmt`, {diminutive2etymology['stmt']}).", "Sequence[ast.stmt]")
        , "type_ignores": aDocument(f"({diminutive2etymology['type_ignores']}) Line-specific "
            f"`ast.TypeIgnore` ({diminutive2etymology['TypeIgnore']}) directives for `# type: ignore` comments.", "list[ast.TypeIgnore] = []")}
    , Returns={"moduleDefinition": aDocument(f"`AST` ({diminutive2etymology['AST']}) object representing a complete Python module structure.", "ast.Module")}
    , categories={"Examples": aDocument("Creates AST equivalent to x = 42.\n"
            "    ```python\n"
            "    from astToolkit import Make\n"
            "\n"
            "    simpleModule = Make.Module([Make.Assign([Make.Name('x', Make.Store())], Make.Constant(42))])\n"
            "    ```\n"
            "\n"
            "Creates AST equivalent to module with function and assignment\n"
            "    ```python\n"
            "    from astToolkit import Make\n"
            "\n"
            "    moduleWithFunction = Make.Module([\n"
            "        Make.FunctionDef('calculate', body=[Make.Return(Make.Constant(100))]),\n"
            "        Make.Assign([Make.Name('result', Make.Store())], Make.Call(Make.Name('calculate'), []))\n"
            "    ])\n"
            "    ```")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Name"
    , aDocument("Make an `ast.Name` for an identifier in an expression.")
    , aDocument("An `ast.Name` represents a bare name such as `inventory`. The context indicates a read, an "
        "assignment target, or a deletion target.")
    , Parameters={"id": aDocument(f"({diminutive2etymology['id']}) Identifier string, such as `inventory`. Use `Make.Attribute` for a dotted reference.", "str")
        , "context": aDocument("Use `Make.Load()` to read, `Make.Store()` to assign, or "
            f"`Make.Del()` ({diminutive2etymology['Del']}) to delete. This is "
            f"`ast.Name.ctx` ({diminutive2etymology['ctx']}) (`ast.expr_context`, {diminutive2etymology['expr_context']}).", "ast.expr_context = Make.Load()")
        , "**keywordArguments": attributes}
    , Returns={"nameReference": aDocument(f"`AST` ({diminutive2etymology['AST']}) object representing an identifier reference with specified context.", "ast.Name")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.NamedExpr"
    , aDocument(f"Make an `ast.NamedExpr` ({diminutive2etymology['NamedExpr']}) for an assignment expression.")
    , aDocument(f"An `ast.NamedExpr` ({diminutive2etymology['NamedExpr']}) represents a form such as "
        "`(inventory := count)`. Python assigns the expression's value to the name and returns that same "
        "value.")
    , Parameters={"target": aDocument("Name in `Make.Store()` context that receives the value.", "ast.Name")
        , "value": aDocument("Expression evaluated for assignment and returned by the assignment expression "
            f"(`ast.expr`, {diminutive2etymology['expr']}).", "ast.expr")
        , "**keywordArguments": attributes}
    , Returns={"namedExpression": aDocument(f"`AST` ({diminutive2etymology['AST']}) object representing an assignment expression with the walrus operator.", "ast.NamedExpr")}
    , categories={"Examples": aDocument("    ```python\n"
            "    from astToolkit import Make\n"
            "\n"
            "    # Creates AST equivalent to: `(inventory := len(warehouse)) > 10`\n"
            "    inventoryCheck = Make.Compare(\n"
            "        left=Make.NamedExpr(\n"
            "            target=Make.Name('inventory', Make.Store()),\n"
            "            value=Make.Call(Make.Name('len'), [Make.Name('warehouse')])\n"
            "        ),\n"
            "        ops=[Make.Gt()],\n"
            "        comparators=[Make.Constant(10)]\n"
            "    )\n"
            "    ```")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Nonlocal"
    , aDocument("Make an `ast.Nonlocal` for a `nonlocal` declaration.")
    , aDocument("Each declared name refers to an existing binding in the nearest enclosing function scope that binds it.")
    , Parameters={"names": aDocument("Identifiers declared nonlocal.", "list[str]")
        , "**keywordArguments": attributes}
    , Returns={"nonlocalStatement": aDocument("The declaration for the supplied names.", "ast.Nonlocal")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Not"
    , aDocument("Make an `ast.Not` operator for `not value`.")
    , aDocument(f"Use `ast.Not` as `op` ({diminutive2etymology['op']}) in "
        f"`Make.UnaryOp` ({diminutive2etymology['UnaryOp']}). Python evaluates `not value` as true when "
        "`value` is falsy.")
    , Returns={"logicalNegationOperator": aDocument(f"`AST` ({diminutive2etymology['AST']}) object representing the keyword '`not`' logical negation "
            f"operator for use in `ast.UnaryOp` ({diminutive2etymology['UnaryOp']}).", "ast.Not")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.NotEq"
    , aDocument(f"Make an `ast.NotEq` ({diminutive2etymology['NotEq']}) comparison operator.")
    , aDocument(f"Use `ast.NotEq` ({diminutive2etymology['NotEq']}) in the `ops` ({diminutive2etymology['ops']}) of "
        f"`Make.Compare` to represent `{map2PythonOperators['NotEq']}`.")
    , Returns={"inequalityOperator": aDocument(f"The operator to put in `ast.Compare.ops` ({diminutive2etymology['ops']}).", "ast.NotEq")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.NotIn"
    , aDocument(f"Make an `ast.NotIn` ({diminutive2etymology['NotIn']}) operator.")
    , aDocument(f"Use `ast.NotIn` ({diminutive2etymology['NotIn']}) in the `ops` ({diminutive2etymology['ops']}) of "
        f"`Make.Compare` to represent {map2PythonKeywords['NotIn']}. Python tests the left operand for "
        "membership in the right operand.")
    , Returns={"negativeMembershipOperator": aDocument(f"The operator to put in `ast.Compare.ops` ({diminutive2etymology['ops']}).", "ast.NotIn")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.operator"
    , aDocument("Make an instance of the base class `ast.operator`.")
    , aDocument("Use a concrete binary operator such as `Make.Add()` or "
        f"`Make.BitOr()` ({diminutive2etymology['BitOr']}) in `Make.BinOp` ({diminutive2etymology['BinOp']}) "
        f"or `Make.AugAssign` ({diminutive2etymology['AugAssign']}).")
    , Returns={"binaryOperator": aDocument("An instance of the common base class for binary operators.", "ast.operator")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.ParamSpec"
    , aDocument(f"Make an `ast.ParamSpec` ({diminutive2etymology['ParamSpec']}) type parameter.")
    , aDocument(f"An `ast.ParamSpec` ({diminutive2etymology['ParamSpec']}) represents a type parameter such as `**P` "
        "in a generic declaration. It can preserve a callable's positional and keyword parameter types.")
    , Parameters={"name": aDocument("Type parameter name without the `**` prefix.", "str")
        , "default_value": aDocument("Default parameter list expression, such as `[int, str]`, when supplied "
            f"(`ast.expr`, {diminutive2etymology['expr']}).", "ast.expr | None = None")
        , "**keywordArguments": attributesInt}
    , Returns={"parameterSpecification": aDocument(f"`AST` ({diminutive2etymology['AST']}) object representing a parameter specification type parameter.", "ast.ParamSpec")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Pass"
    , aDocument("Make an `ast.Pass` for a `pass` statement.")
    , aDocument("Use `Make.Pass()` where Python requires a statement and the body needs no action.")
    , Returns={"passStatement": aDocument("A `pass` statement.", "ast.Pass")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.pattern"
    , aDocument("Make an instance of the base class `ast.pattern`.")
    , aDocument(f"Use a concrete pattern factory such as `Make.MatchClass` ({diminutive2etymology['MatchClass']}) or "
        f"`Make.MatchValue` ({diminutive2etymology['MatchValue']}) to build a case pattern.")
    , Parameters={"**keywordArguments": attributesInt}
    , Returns={"pattern": aDocument("A base `ast.pattern` object with the specified attributes.", "ast.pattern")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Raise"
    , aDocument("Make an `ast.Raise` for a `raise` statement.")
    , aDocument("An `ast.Raise` represents `raise`, `raise exc`, or `raise exc from cause`.")
    , Parameters={"exc": aDocument(f"({diminutive2etymology['exc']}) Expression that supplies an exception instance or class. Omit it "
            f"to re-raise the active exception (`ast.expr`, {diminutive2etymology['expr']}).", "ast.expr | None = None")
        , "cause": aDocument("Expression following `from`. Use `Make.Constant(None)` for `from None`, which suppresses display "
            "of the implicit exception context.", "ast.expr | None = None")
        , "**keywordArguments": attributes}
    , Returns={"raiseStatement": aDocument("The `raise` statement with the supplied exception and cause.", "ast.Raise")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Return"
    , aDocument("Make an `ast.Return` for a `return` statement.")
    , aDocument("A `return` statement exits the enclosing function. In a generator, it ends iteration.")
    , Parameters={"value": aDocument("Expression returned by the function. Omit it for a bare `return`. An asynchronous generator "
            f"requires the bare form (`ast.expr`, {diminutive2etymology['expr']}).", "ast.expr | None = None")
        , "**keywordArguments": attributes}
    , Returns={"returnStatement": aDocument(f"`AST` ({diminutive2etymology['AST']}) object representing a function return with optional value.", "ast.Return")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Set"
    , aDocument("Make an `ast.Set` for a set display.")
    , aDocument("An `ast.Set` represents set displays such as `{a, b}` or `{a, *items}`. An empty set expression "
        "unparses as `{*()}`.")
    , Parameters={"listElements": aDocument(f"Element expressions in source order. This is `ast.Set.elts` ({diminutive2etymology['elts']}) "
            f"(`ast.expr`, {diminutive2etymology['expr']}).", "Sequence[ast.expr] = []")
        , "**keywordArguments": attributes}
    , Returns={"setLiteral": aDocument(f"`AST` ({diminutive2etymology['AST']}) object representing a set literal with specified unique elements.", "ast.Set")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.SetComp"
    , aDocument(f"Make an `ast.SetComp` ({diminutive2etymology['SetComp']}) for a set comprehension.")
    , aDocument(f"An `ast.SetComp` ({diminutive2etymology['SetComp']}) represents a set comprehension such as "
        "`{item.name for item in items}`.")
    , Parameters={"element": aDocument("Expression that supplies each element. Use `Make.Starred` for unpacking, as in "
            "`{*items for items in groups}`. This is `ast.SetComp.elt` (`SetComp` "
            f"{diminutive2etymology['SetComp']}, `elt` {diminutive2etymology['elt']}) "
            f"(`ast.expr`, {diminutive2etymology['expr']}).", "ast.expr")
        , "generators": aDocument("`for` clauses and filters in source order.", "list[ast.comprehension]")
        , "**keywordArguments": attributes}
    , Returns={"setComprehension": aDocument(f"`AST` ({diminutive2etymology['AST']}) object representing a set comprehension expression.", "ast.SetComp")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Slice"
    , aDocument("Make an `ast.Slice` for a slice inside a subscription.")
    , aDocument("Use an `ast.Slice` as `slice` in `Make.Subscript` to represent forms such as `items[start:stop:step]`.")
    , Parameters={"lower": aDocument(f"({diminutive2etymology['lower']}) Start expression before the first `:`. Omit it for an open "
            f"start (`ast.expr`, {diminutive2etymology['expr']}).", "ast.expr | None = None")
        , "upper": aDocument(f"({diminutive2etymology['upper']}) Stop expression after the first `:`. For built-in sequences, the "
            "stop position is exclusive.", "ast.expr | None = None")
        , "step": aDocument("Stride expression after the second `:`. Built-in sequences use a stride of `1` when omitted.", "ast.expr | None = None")
        , "**keywordArguments": attributes}
    , Returns={"sliceExpression": aDocument(f"`AST` ({diminutive2etymology['AST']}) object representing a slice operation for sequence subscripting.", "ast.Slice")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Starred"
    , aDocument("Make an `ast.Starred` for the `*` form of an expression or target.")
    , aDocument("Use an `ast.Starred` for unpacking in calls and displays or to capture remaining items in an assignment target.")
    , Parameters={"value": aDocument("Iterable expression to unpack, or target that receives the remaining items "
            f"(`ast.expr`, {diminutive2etymology['expr']}).", "ast.expr")
        , "context": aDocument("Use `Make.Load()` for unpacking an iterable or `Make.Store()` for an assignment target. This is "
            f"`ast.Starred.ctx` ({diminutive2etymology['ctx']}) (`ast.expr_context`, {diminutive2etymology['expr_context']}).", "ast.expr_context = Make.Load()")
        , "**keywordArguments": attributes}
    , Returns={"starredExpression": aDocument(f"`AST` ({diminutive2etymology['AST']}) object representing a starred expression for unpacking operations.", "ast.Starred")}
    , categories={"Examples": aDocument("    ```python\n"
            "    from astToolkit import Make\n"
            "\n"
            "    # Call cook(*ingredients).\n"
            "    cookCall = Make.Call(Make.Name('cook'), [Make.Starred(Make.Name('ingredients'))])\n"
            "\n"
            "    # Assign first, *remaining = groceries.\n"
            "    targets = Make.Tuple(\n"
            "        [Make.Name('first', Make.Store()),\n"
            "         Make.Starred(Make.Name('remaining', Make.Store()), Make.Store())],\n"
            "        Make.Store(),\n"
            "    )\n"
            "    unpackGroceries = Make.Assign([targets], Make.Name('groceries'))\n"
            "    ```")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.stmt"
    , aDocument(f"Make an instance of the base class `ast.stmt` ({diminutive2etymology['stmt']}).")
    , aDocument("Use a concrete statement factory such as `Make.Assign` or `Make.Return` to represent an executable statement.")
    , Parameters={"**keywordArguments": attributes}
    , Returns={"statement": aDocument("An instance of the common base class for statements.", "ast.stmt")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Store"
    , aDocument("Make an `ast.Store` context for an assignment target.")
    , aDocument("Use `Make.Store()` for targets that receive a value in assignments, loops, comprehensions, or an "
        "`as` clause of a `with` statement.")
    , Returns={"storeContext": aDocument("Expression context for an assignment target.", "ast.Store")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Subscript"
    , aDocument("Make an `ast.Subscript` for a subscription such as `items[key]`.")
    , aDocument("The expression in brackets can supply a key, index, slice, or tuple of subscription arguments.")
    , Parameters={"value": aDocument(f"Expression for the object being subscripted (`ast.expr`, {diminutive2etymology['expr']}).", "ast.expr")
        , "slice": aDocument("Expression inside brackets. Use `Make.Slice` for colon-separated bounds or `Make.Tuple` for "
            "comma-separated arguments.", "ast.expr")
        , "context": aDocument("Use `Make.Load()` to read, `Make.Store()` to assign, or "
            f"`Make.Del()` ({diminutive2etymology['Del']}) to delete. This is "
            f"`ast.Subscript.ctx` ({diminutive2etymology['ctx']}) (`ast.expr_context`, {diminutive2etymology['expr_context']}).", "ast.expr_context = Make.Load()")
        , "**keywordArguments": attributes}
    , Returns={"subscriptExpression": aDocument(f"`AST` ({diminutive2etymology['AST']}) object representing a subscription operation with brackets.", "ast.Subscript")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.TemplateStr"
    , aDocument(f"Make an `ast.TemplateStr` ({diminutive2etymology['TemplateStr']}) for a t-string.")
    , aDocument("A t-string evaluates to a template containing literal text and structured interpolations. You can "
        "use each interpolation's value and formatting information when processing the template.")
    , Parameters={"values": aDocument("Use `ast.Constant` strings for literal text and `ast.Interpolation` objects for replacement "
            f"fields, in source order (`ast.expr`, {diminutive2etymology['expr']}).", "Sequence[ast.expr]")
        , "**keywordArguments": attributes}
    , Returns={"templateString": aDocument(f"`AST` ({diminutive2etymology['AST']}) object representing a template string.", "ast.TemplateStr")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Try"
    , aDocument("Make an `ast.Try` for a `try` statement.")
    , aDocument("An `ast.Try` can handle exceptions with `except`, run an `else` body after normal completion, or "
        "run a `finally` body on exit.")
    , Parameters={"body": aDocument(f"Statements in the `try` block (`ast.stmt`, {diminutive2etymology['stmt']}).", "Sequence[ast.stmt]")
        , "handlers": aDocument("`except` clauses in matching order. Use an empty list for `try ... finally` without handlers "
            f"(`ast.ExceptHandler`, {diminutive2etymology['ExceptHandler']}).", "list[ast.ExceptHandler]")
        , "orElse": aDocument(f"({diminutive2etymology['orElse']}) Statements executed if the `try` block reaches its end "
            "normally. Requires at least one handler. This is "
            f"`ast.Try.orelse` ({diminutive2etymology['orelse']}).", "Sequence[ast.stmt] = []")
        , "finalbody": aDocument(f"({diminutive2etymology['finalbody']}) `finally` statements executed when control leaves the `try` statement.", "Sequence[ast.stmt] = []")
        , "**keywordArguments": attributes}
    , Returns={"tryStatement": aDocument(f"`AST` ({diminutive2etymology['AST']}) object representing an exception handling statement with optional cleanup.", "ast.Try")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.TryStar"
    , aDocument(f"Make an `ast.TryStar` ({diminutive2etymology['TryStar']}) statement.")
    , aDocument(f"An `ast.TryStar` ({diminutive2etymology['TryStar']}) represents handlers that each receive the "
        "subgroup of exceptions matching their type. A single exception can also match an `except*` clause "
        "as a group of one.")
    , Parameters={"body": aDocument(f"Statements in the `try` block (`ast.stmt`, {diminutive2etymology['stmt']}).", "Sequence[ast.stmt]")
        , "handlers": aDocument("One or more `except*` clauses in matching order, supplied as "
            f"`ast.ExceptHandler` ({diminutive2etymology['ExceptHandler']}) objects with an exception type.", "list[ast.ExceptHandler]")
        , "orElse": aDocument(f"({diminutive2etymology['orElse']}) Statements executed if the `try` block reaches its end "
            f"normally. This is `ast.TryStar.orelse` (`TryStar` {diminutive2etymology['TryStar']}, `orelse` "
            f"{diminutive2etymology['orelse']}).", "Sequence[ast.stmt] = []")
        , "finalbody": aDocument(f"({diminutive2etymology['finalbody']}) `finally` statements executed when control leaves the `try` statement.", "Sequence[ast.stmt] = []")
        , "**keywordArguments": attributes}
    , Returns={"tryStarStatement": aDocument(f"`AST` ({diminutive2etymology['AST']}) object representing an exception group handling statement "
            "with optional cleanup.", "ast.TryStar")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Tuple"
    , aDocument("Make an `ast.Tuple` for a tuple display or unpacking target.")
    , aDocument("An `ast.Tuple` represents comma-separated forms such as `(x, y)` or `(x,)`, as well as the empty tuple `()`.")
    , Parameters={"listElements": aDocument(f"Element expressions in order. This is `ast.Tuple.elts` ({diminutive2etymology['elts']}) "
            f"(`ast.expr`, {diminutive2etymology['expr']}).", "Sequence[ast.expr] = []")
        , "context": aDocument("Use `Make.Load()` to build a tuple, `Make.Store()` for an assignment target, or "
            f"`Make.Del()` ({diminutive2etymology['Del']}) for a deletion target. This is "
            f"`ast.Tuple.ctx` ({diminutive2etymology['ctx']}) (`ast.expr_context`, {diminutive2etymology['expr_context']}).", "ast.expr_context = Make.Load()")
        , "**keywordArguments": attributes}
    , Returns={"tupleLiteral": aDocument(f"`AST` ({diminutive2etymology['AST']}) object representing a tuple literal with specified elements.", "ast.Tuple")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.type_ignore"
    , aDocument(f"Make an instance of the base class `ast.type_ignore` ({diminutive2etymology['type_ignore']}).")
    , aDocument(f"Use `Make.TypeIgnore` ({diminutive2etymology['TypeIgnore']}) for a `# type: ignore` comment in a module.")
    , Returns={"typeIgnore": aDocument("An instance of the common base class for type ignore directives.", "ast.type_ignore")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.type_param"
    , aDocument(f"Make an instance of the base class `ast.type_param` ({diminutive2etymology['type_param']}).")
    , aDocument(f"Use `Make.TypeVar` ({diminutive2etymology['TypeVar']}), "
        f"`Make.ParamSpec` ({diminutive2etymology['ParamSpec']}), or "
        f"`Make.TypeVarTuple` ({diminutive2etymology['TypeVarTuple']}) for a type parameter in a generic "
        "declaration.")
    , Parameters={"**keywordArguments": attributesInt}
    , Returns={"typeParameter": aDocument(f"Abstract `AST` ({diminutive2etymology['AST']}) object representing the base of type parameter hierarchy.", "ast.type_param")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.TypeAlias"
    , aDocument(f"Make an `ast.TypeAlias` ({diminutive2etymology['TypeAlias']}) for a `type` statement.")
    , aDocument(f"An `ast.TypeAlias` ({diminutive2etymology['TypeAlias']}) represents a declaration such as "
        "`type Vector[T] = list[T]`.")
    , Parameters={"name": aDocument("Name of the alias as an `ast.Name` in `Make.Store()` context.", "ast.Name")
        , "type_params": aDocument(f"({diminutive2etymology['type_params']}) Type parameters declared in brackets after the name. Use "
            f"an empty sequence for a non-generic alias (`ast.type_param`, {diminutive2etymology['type_param']}).", "Sequence[ast.type_param]")
        , "value": aDocument(f"Expression defining the aliased type (`ast.expr`, {diminutive2etymology['expr']}).", "ast.expr")
        , "**keywordArguments": attributesInt}
    , Returns={"typeAliasDefinition": aDocument(f"`AST` ({diminutive2etymology['AST']}) object representing a complete type alias declaration.", "ast.TypeAlias")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.TypeIgnore"
    , aDocument(f"Make an `ast.TypeIgnore` ({diminutive2etymology['TypeIgnore']}) directive.")
    , aDocument(f"Add an `ast.TypeIgnore` ({diminutive2etymology['TypeIgnore']}) to `Make.Module` to record an "
        "ignore directive at a specific source line.")
    , Parameters={"lineno": aDocument(f"({diminutive2etymology['lineno']}) One-based source line of the directive.", "int")
        , "tag": aDocument("Text following `ignore`, such as `'[assignment]'`. Use `''` for an unqualified ignore.", "str")}
    , Returns={"typeIgnoreDirective": aDocument(f"`AST` ({diminutive2etymology['AST']}) object representing a type checker ignore comment.", "ast.TypeIgnore")}
    , categories={"Examples": aDocument("Creates AST equivalent to # type: ignore (on line 42).\n"
            "    ```python\n"
            "    from astToolkit import Make\n"
            "\n"
            "    simpleIgnore = Make.TypeIgnore(42, '')\n"
            "    ```\n"
            "\n"
            "Creates AST equivalent to # type: ignore[assignment] (on line 15).\n"
            "    ```python\n"
            "    from astToolkit import Make\n"
            "\n"
            "    taggedIgnore = Make.TypeIgnore(15, '[assignment]')\n"
            "    ```")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.TypeVar"
    , aDocument(f"Make an `ast.TypeVar` ({diminutive2etymology['TypeVar']}) for a type variable.")
    , aDocument(f"An `ast.TypeVar` ({diminutive2etymology['TypeVar']}) represents a type parameter such as `T`, "
        "`T: Base`, or `T: (int, str)`.")
    , Parameters={"name": aDocument("Type variable name.", "str")
        , "bound": aDocument("Upper-bound expression, or an `ast.Tuple` of allowed types for constraints. Omit it for an "
            f"unrestricted type variable (`ast.expr`, {diminutive2etymology['expr']}).", "ast.expr | None = None")
        , "default_value": aDocument("Default type expression following `=`.", "ast.expr | None = None")
        , "**keywordArguments": attributesInt}
    , Returns={"typeVariable": aDocument(f"`AST` ({diminutive2etymology['AST']}) object representing a type variable with optional constraints.", "ast.TypeVar")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.TypeVarTuple"
    , aDocument(f"Make an `ast.TypeVarTuple` ({diminutive2etymology['TypeVarTuple']}) for a variadic type parameter.")
    , aDocument(f"An `ast.TypeVarTuple` ({diminutive2etymology['TypeVarTuple']}) represents a type parameter such as "
        "`*Ts` that accepts a sequence of type arguments.")
    , Parameters={"name": aDocument("Type parameter name without the `*` prefix.", "str")
        , "default_value": aDocument("Default type sequence expression, such as `*tuple[int, str]` or `()` "
            f"(`ast.expr`, {diminutive2etymology['expr']}).", "ast.expr | None = None")
        , "**keywordArguments": attributesInt}
    , Returns={"typeVariableTuple": aDocument(f"`AST` ({diminutive2etymology['AST']}) object representing a variadic type variable.", "ast.TypeVarTuple")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.UAdd"
    , aDocument(f"Make an `ast.UAdd` ({diminutive2etymology['UAdd']}) operator for `+value`.")
    , aDocument(f"Use `ast.UAdd` ({diminutive2etymology['UAdd']}) as `op` ({diminutive2etymology['op']}) in "
        f"`Make.UnaryOp` ({diminutive2etymology['UnaryOp']}). Unary `+` leaves a built-in numeric operand's "
        "sign as it was.")
    , Returns={"unaryPositiveOperator": aDocument(f"`AST` ({diminutive2etymology['AST']}) object representing the '`+`' unary positive operator for "
            f"use in `ast.UnaryOp` ({diminutive2etymology['UnaryOp']}).", "ast.UAdd")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.unaryop"
    , aDocument(f"Make an instance of the base class `ast.unaryop` ({diminutive2etymology['unaryop']}).")
    , aDocument(f"Use `Make.Invert()`, `Make.Not()`, `Make.UAdd()` ({diminutive2etymology['UAdd']}), or "
        f"`Make.USub()` ({diminutive2etymology['USub']}) as a concrete operator in "
        f"`Make.UnaryOp` ({diminutive2etymology['UnaryOp']}).")
    , Returns={"unaryOperator": aDocument("Abstract unary operator object that serves as the base class for all Python unary operators in "
            f"`AST` ({diminutive2etymology['AST']}) structures.", "ast.unaryop")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.UnaryOp"
    , aDocument(f"Make an `ast.UnaryOp` ({diminutive2etymology['UnaryOp']}) for an operation on one operand.")
    , aDocument(f"An `ast.UnaryOp` ({diminutive2etymology['UnaryOp']}) represents prefix operations such as `-value`"
        ", `not value`, and `~value`.")
    , Parameters={"op": aDocument(f"({diminutive2etymology['op']}) Unary operator, such as "
            f"`Make.UAdd()` ({diminutive2etymology['UAdd']}), `Make.USub()` ({diminutive2etymology['USub']}), "
            f"`Make.Not()`, or `Make.Invert()` (`ast.unaryop`, {diminutive2etymology['unaryop']}).", "ast.unaryop")
        , "operand": aDocument(f"Expression operated on (`ast.expr`, {diminutive2etymology['expr']}).", "ast.expr")
        , "**keywordArguments": attributes}
    , Returns={"unaryOperation": aDocument(f"`AST` ({diminutive2etymology['AST']}) object representing a unary operation on a single expression.", "ast.UnaryOp")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.USub"
    , aDocument(f"Make an `ast.USub` ({diminutive2etymology['USub']}) operator for `-value`.")
    , aDocument(f"Use `ast.USub` ({diminutive2etymology['USub']}) as `op` ({diminutive2etymology['op']}) in "
        f"`Make.UnaryOp` ({diminutive2etymology['UnaryOp']}) to represent arithmetic negation.")
    , Returns={"unaryNegativeOperator": aDocument(f"`AST` ({diminutive2etymology['AST']}) object representing the '`-`' unary negation operator for "
            f"use in `ast.UnaryOp` ({diminutive2etymology['UnaryOp']}).", "ast.USub")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.While"
    , aDocument("Make an `ast.While` for a `while` loop.")
    , aDocument("A `while` loop checks the condition before each iteration and runs the body while the condition is truthy.")
    , Parameters={"test": aDocument(f"Condition expression evaluated before each iteration (`ast.expr`, {diminutive2etymology['expr']}).", "ast.expr")
        , "body": aDocument(f"Statements executed while `test` is truthy (`ast.stmt`, {diminutive2etymology['stmt']}).", "Sequence[ast.stmt]")
        , "orElse": aDocument(f"({diminutive2etymology['orElse']}) Statements executed when the test is falsy. `break` skips them. "
            f"This is `ast.While.orelse` ({diminutive2etymology['orelse']}).", "Sequence[ast.stmt] = []")
        , "**keywordArguments": attributes}
    , Returns={"whileLoop": aDocument(f"`AST` ({diminutive2etymology['AST']}) object representing a condition-based iteration statement.", "ast.While")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.With"
    , aDocument("Make an `ast.With` for a `with` statement.")
    , aDocument("A `with` statement enters context managers in source order and exits them in reverse order. Each "
        "item can assign the result of `__enter__` to an `as` target.")
    , Parameters={"items": aDocument(f"Context manager specifications from `Make.withitem` ({diminutive2etymology['withitem']}), in entry order.", "list[ast.withitem]")
        , "body": aDocument(f"Statements executed after entering all the context managers (`ast.stmt`, {diminutive2etymology['stmt']}).", "Sequence[ast.stmt]")
        , "type_comment": aDocument(f"({diminutive2etymology['type_comment']}) Type annotation text for the `as` targets, from a `# type: ...` comment.", "str | None = None")
        , "**keywordArguments": attributesTypeComment}
    , Returns={"withStatement": aDocument(f"`AST` ({diminutive2etymology['AST']}) object representing a context manager statement for resource management.", "ast.With")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.withitem"
    , aDocument(f"Make an `ast.withitem` ({diminutive2etymology['withitem']}) for one context manager in a `with` statement.")
    , aDocument(f"Use an `ast.withitem` ({diminutive2etymology['withitem']}) for forms such as `manager` or "
        f"`manager as resource` in `Make.With` or `Make.AsyncWith` ({diminutive2etymology['AsyncWith']}).")
    , Parameters={"context_expr": aDocument(f"({diminutive2etymology['context_expr']}) Expression that supplies the context manager "
            f"(`ast.expr`, {diminutive2etymology['expr']}).", "ast.expr")
        , "optional_vars": aDocument(f"({diminutive2etymology['optional_vars']}) Assignment target after `as`, in `Make.Store()` context. "
            "Omit it to leave the result of entering the manager unbound.", "ast.expr | None = None")}
    , Returns={"contextItem": aDocument(f"`AST` ({diminutive2etymology['AST']}) object representing a single context manager in with statements.", "ast.withitem")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Yield"
    , aDocument(f"Make an `ast.Yield` ({diminutive2etymology['Yield']}) for a `yield` expression.")
    , aDocument("A `yield` expression suspends the generator and produces a value. On resumption, the expression "
        "evaluates to the value sent into the generator, or to `None` when advanced normally.")
    , Parameters={"value": aDocument("Expression whose value the generator yields. Omit it for a bare `yield`, which yields `None` "
            f"(`ast.expr`, {diminutive2etymology['expr']}).", "ast.expr | None = None")
        , "**keywordArguments": attributes}
    , Returns={"yieldExpression": aDocument(f"`AST` ({diminutive2etymology['AST']}) object representing a yield expression for generator functions.", "ast.Yield")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.YieldFrom"
    , aDocument(f"Make an `ast.YieldFrom` ({diminutive2etymology['YieldFrom']}) for a `yield from` expression.")
    , aDocument("A `yield from` expression delegates to another iterable. When iteration ends, the expression takes "
        "the iterator's `StopIteration.value` as its result. Use it in a synchronous generator.")
    , Parameters={"value": aDocument(f"Expression supplying the iterable to delegate to (`ast.expr`, {diminutive2etymology['expr']}).", "ast.expr")
        , "**keywordArguments": attributes}
    , Returns={"yieldFromExpression": aDocument(f"`AST` ({diminutive2etymology['AST']}) object representing a yield from expression for generator delegation.", "ast.YieldFrom")}
))

for subclass in ast.boolop.__subclasses__():
    identifierClass = subclass.__name__
    listDocstring.append(Docstring(f"{identifierToolClass}.{identifierClass}"
        , aDocument(f"Make an `ast.{identifierClass}` operator for {map2PythonKeywords[identifierClass]}.", AIgenerated=False)
        , aDocument(f"This subclass of `ast.{identifierClass}` adds `join()`, which combines expressions into one "
            f"`ast.BoolOp` ({diminutive2etymology['BoolOp']}).", AIgenerated=False)))

for subclass in ast.operator.__subclasses__():
    identifierClass = subclass.__name__
    etymology = diminutive2etymology.get(identifierClass)
    nameOperator = f'`ast.{identifierClass}`'
    if etymology:
        nameOperator += f' ({etymology})'
    listDocstring.append(Docstring(f"{identifierToolClass}.{identifierClass}"
        , aDocument(f"Make an {nameOperator} operator for `{map2PythonOperators[identifierClass]}`.", AIgenerated=False)
        , aDocument(f"This subclass of {nameOperator} adds `join()`, which combines expressions into nested "
            f"`ast.BinOp` ({diminutive2etymology['BinOp']}) operations.", AIgenerated=False)))

for data in listDocstring:
    docstrings[identifierToolClass][data.identifier.removeprefix(f"{identifierToolClass}.")] = Make.Expr(
        Make.Constant(make1docstring(data, lineWidth=94)))
del listDocstring

data = Docstring(identifierToolClass
    , aDocument(f"Create an `ast.AST` ({diminutive2etymology['AST']}) object or an instance of a subclass.", AIgenerated=False)
    , aDocument(f"I describe `keywordArguments` of `{identifierToolClass}` methods here.", AIgenerated=False)
    , {'col_offset': aDocument(f"({diminutive2etymology['col_offset']}) Zero-based UTF-8 byte offset where the source begins.",
            'int', AIgenerated=False)
        , 'end_col_offset': aDocument(f"({diminutive2etymology['end_col_offset']}) Zero-based UTF-8 byte offset just after "
            "the end of the source on `end_lineno`.", 'int | None', AIgenerated=False)
        , 'end_lineno': aDocument(f"({diminutive2etymology['end_lineno']}) One-based line number where the source ends.",
            'int | None', AIgenerated=False)
        , 'lineno': aDocument(f"({diminutive2etymology['lineno']}) One-based line number where the source begins.",
            'int', AIgenerated=False)}
    , categories={'Source Positions and Syntax Fields': aDocument(f"""What is an attribute? In Python, an attribute is a named
        property of an object. In the `ast` ({diminutive2etymology['ast']}) universe, one word may have many different
        meanings. Pay close attention to capitalization, leading underscores, and context.

        The syntax fields appear in `_fields`, and their types appear in `_field_types`. For example, the `attr`
        ({diminutive2etymology['attr']}) field of `ast.Attribute` holds the name after the dot. Other uses of the word
        attribute include `getattr`, `setattr`, and `ast.MatchClass.kwd_attrs` ({diminutive2etymology['kwd_attrs']}).

        The source positions, when available, appear in `_attributes`. They refer to the original source, including
        when the text contains characters that use multiple UTF-8 bytes. For an exception to the usual placement of
        source positions in `**keywordArguments`, see `Make.TypeIgnore` ({diminutive2etymology['TypeIgnore']}), which has
        a named `lineno` ({diminutive2etymology['lineno']}) field.""", AIgenerated=False)}
)
docstrings[identifierToolClass][identifierToolClass] = Make.Expr(
    Make.Constant(make1docstring(data, lineWidth=98)))
del data

data = Docstring(settingsManufacturing.identifiers['boolopJoinMethod']
    , aDocument("I use this method to join expressions with a Boolean operator.")
    , aDocument(f"`Make.And.join()` and `Make.Or.join()` use one `ast.BoolOp` ({diminutive2etymology['BoolOp']}) "
        "for two or more expressions.")
    , {'ast_operator': aDocument(f"Boolean operator class, `ast.And` or `ast.Or` "
            f"(`ast.boolop`, {diminutive2etymology['boolop']}).", 'type[ast.boolop]')
        , 'expressions': aDocument(f"Operands in evaluation order (`ast.expr`, {diminutive2etymology['expr']}).",
            'Sequence[ast.expr]')
        , '**keywordArguments': aDocument("Source positions for the constructed expression.", 'ast_attributes')}
    , {'joinedExpression': aDocument(f"One `ast.BoolOp` ({diminutive2etymology['BoolOp']}) for two or more operands, "
        "the original operand for a single input, or an empty string literal for an empty input.", 'ast.expr')}
)
docstrings[identifierToolClass][settingsManufacturing.identifiers['boolopJoinMethod']] = Make.Expr(
    Make.Constant(make1docstring(data, lineWidth=94)))
del data

data = Docstring('join_boolop'
    , aDocument(f"Join expressions in one `ast.BoolOp` ({diminutive2etymology['BoolOp']}).", AIgenerated=False)
    , aDocument(f"Like `str.join()` ({diminutive2etymology['str']}) but for `AST` ({diminutive2etymology['AST']}) "
        "expressions.", AIgenerated=False)
    , {'expressions': aDocument(f"Operands in evaluation order (`ast.expr`, {diminutive2etymology['expr']}).",
            'Sequence[ast.expr]', AIgenerated=False)
        , '**keywordArguments': aDocument("Source positions for the constructed expression. A single input keeps "
            "its existing positions.", 'ast_attributes', AIgenerated=False)}
    , {'joinedExpression': aDocument(f"One `ast.BoolOp` ({diminutive2etymology['BoolOp']}) for two or more operands, "
        "the original operand for a single input, or an empty string literal for an empty input.",
        'ast.expr', AIgenerated=False)}
    , {'Examples': aDocument("""    ```python
    import ast
    from astToolkit import Make

    # Both expressions represent Lions and tigers and bears.
    ast.BoolOp(
        op=ast.And(),
        values=[Make.Name('Lions'), Make.Name('tigers'), Make.Name('bears')],
    )
    Make.And.join([Make.Name('Lions'), Make.Name('tigers'), Make.Name('bears')])
    ```""", AIgenerated=False)}
)
docstrings[identifierToolClass]['join_boolop'] = Make.Expr(
    Make.Constant(make1docstring(data, lineWidth=90)))
del data

data = Docstring('_operatorJoinMethod'
    , aDocument("I use this method to join expressions with a binary operator.")
    , aDocument(f"Operator classes such as `Make.Add` use this method to join expressions into left-associated "
        f"`ast.BinOp` ({diminutive2etymology['BinOp']}) operations.")
    , {'ast_operator': aDocument("Binary operator class such as `ast.Add` or `ast.BitOr`.", 'type[ast.operator]')
        , 'expressions': aDocument(f"Operands in evaluation order (`ast.expr`, {diminutive2etymology['expr']}).",
            'Iterable[ast.expr]')
        , '**keywordArguments': aDocument("Source positions for every constructed expression.", 'ast_attributes')}
    , {'joinedExpression': aDocument(f"Nested `ast.BinOp` ({diminutive2etymology['BinOp']}) operations for two or "
        "more operands, the original operand for a single input, or an empty string literal for an empty input.",
        'ast.expr')}
)
docstrings[identifierToolClass]['_operatorJoinMethod'] = Make.Expr(
    Make.Constant(make1docstring(data, lineWidth=94)))
del data

data = Docstring('join_operator'
    , aDocument(f"Join expressions in left-associated `ast.BinOp` ({diminutive2etymology['BinOp']}) operations.",
        AIgenerated=False)
    , aDocument(f"Like `str.join()` ({diminutive2etymology['str']}) but for `AST` ({diminutive2etymology['AST']}) "
        "expressions. Joining `a`, `b`, and `c` with `Make.Sub.join()` represents `(a - b) - c`.", AIgenerated=False)
    , {'expressions': aDocument(f"Operands in evaluation order (`ast.expr`, {diminutive2etymology['expr']}).",
            'Iterable[ast.expr]', AIgenerated=False)
        , '**keywordArguments': aDocument("Source positions for every constructed expression. A single input keeps "
            "its existing positions.", 'ast_attributes', AIgenerated=False)}
    , {'joinedExpression': aDocument(f"Nested `ast.BinOp` ({diminutive2etymology['BinOp']}) operations for two or "
        "more operands, the original operand for a single input, or an empty string literal for an empty input.",
        'ast.expr', AIgenerated=False)}
    , {'Examples': aDocument("""    ```python
    import ast
    from astToolkit import Make

    # Both expressions represent (Crosby | Stills) | Nash.
    ast.BinOp(
        left=ast.BinOp(left=Make.Name('Crosby'), op=ast.BitOr(), right=Make.Name('Stills')),
        op=ast.BitOr(),
        right=Make.Name('Nash'),
    )
    Make.BitOr.join([Make.Name('Crosby'), Make.Name('Stills'), Make.Name('Nash')])
    ```""", AIgenerated=False)}
)
docstrings[identifierToolClass]['join_operator'] = Make.Expr(
    Make.Constant(make1docstring(data, lineWidth=90)))
del data
