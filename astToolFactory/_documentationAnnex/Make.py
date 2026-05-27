"""A warehouse for docstrings added to manufactured ast tools.

NOTE Use special indentation in this file.
    1. The generated files use spaces, not tabs, so use spaces here.
    2. As of this writing, I only know how to _manually_ align the indentation of the docstrings with the associated code. So,
        indent one or two levels as appropriate.
"""
from __future__ import annotations

from astToolFactory import settingsManufacturing
from astToolFactory.documentation import aDocument, diminutive2etymology, Docstring, docstrings, make1docstring
from astToolkit import Make
import ast

# NOTE "ClassDefIdentifier": {'attribute': "'attributeType' = 'defaultValue'"}

listDocstring: list[Docstring] = []

identifierToolClass: str = settingsManufacturing.identifiers['Make']

listDocstring.append(Docstring(f"{identifierToolClass}.alias"  # noqa: FURB113
    , aDocument("Make an `ast.alias` object for a single name mapping in an import statement.")
    , aDocument(f"""The `ast.alias` object represents one name mapping in an `import` or `from ... import` statement. `dotModule` accepts the name being imported; the optional `asName` ({diminutive2etymology['asName']}) provides an alternative local identifier for the imported name.""")
    , {'dotModule': aDocument("The module, submodule, class, or function name to import. Dot notation is permitted for submodule paths. This parameter corresponds to `ast.alias.name`.", 'str')
        , 'asName': aDocument(f"({diminutive2etymology['asName']}) Optional alternative identifier for the imported name in local scope. This parameter corresponds to `ast.alias.asname`.", 'str | None = None')}
    , {'importAlias': aDocument("An `ast.alias` object mapping one import name with an optional local alias.", 'ast.alias')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.AnnAssign"
    , aDocument(f"Make an `ast.AnnAssign` ({diminutive2etymology['AnnAssign']}) object for a type-annotated variable assignment.")
    , aDocument("""The `ast.AnnAssign` object represents an annotated variable assignment such as `name: int = 42` or `config: dict[str, Any]`. The `annotation` provides the type expression; the optional `value` provides an initial value.""")
    , {'target': aDocument("Assignment target. May be an `ast.Name`, `ast.Attribute`, or `ast.Subscript`.", 'ast.Name | ast.Attribute | ast.Subscript')
        , 'annotation': aDocument("Type annotation expression specifying the variable type.", 'ast.expr')
        , 'value': aDocument("Optional initial value expression for the annotated variable.", 'ast.expr | None = None')}
    , {'annotatedAssignment': aDocument(f"An `ast.AnnAssign` ({diminutive2etymology['AnnAssign']}) object representing a type-annotated variable assignment.", 'ast.AnnAssign')}
    , {'Implementation Details': aDocument("""`Make.AnnAssign` automatically computes `ast.AnnAssign.simple` as `int(isinstance(target, ast.Name))`. This field is not exposed as a parameter. The Python grammar requires `simple` to be 1 when the target is a bare `ast.Name` and 0 for `ast.Attribute` or `ast.Subscript` targets.""")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.arg"
    , aDocument(f"Make an `ast.arg` ({diminutive2etymology['arg']}) object for a single parameter in a function signature.")
    , aDocument("""The `ast.arg` object represents one parameter in a function definition, including positional, keyword-only, `*args`, and `**kwargs` parameters. The parameter name is provided as `Buffalo_buffalo_Buffalo_buffalo_buffalo_buffalo_Buffalo_buffalo`, which corresponds to `ast.arg.arg`.""")
    , {'Buffalo_buffalo_Buffalo_buffalo_buffalo_buffalo_Buffalo_buffalo': aDocument("Parameter name as a string. This parameter corresponds to `ast.arg.arg`.", 'str')
        , 'annotation': aDocument("Optional type annotation expression for the parameter.", 'ast.expr | None = None')}
    , {'argumentDefinition': aDocument(f"An `ast.arg` ({diminutive2etymology['arg']}) object representing one function parameter with an optional type annotation.", 'ast.arg')}
    , {'Parameter Naming': aDocument(f"""`ast.arg` uses `ast.arg.arg` (a string field) to hold the parameter name. In `Make`, this field is named `Buffalo_buffalo_Buffalo_buffalo_buffalo_buffalo_Buffalo_buffalo` to avoid collision with the `ast.arg` class itself. In an `ast.FunctionDef` ({diminutive2etymology['FunctionDef']}), the dereference chain is `ast.FunctionDef.args.args[n].arg.arg`—four identifiers that resolve to: the `ast.arguments` object, the list of positional parameters, one `ast.arg` object, and the parameter name string.""")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.arguments"
    , aDocument("Make an `ast.arguments` object for the complete parameter specification of a function definition.")
    , aDocument("""The `ast.arguments` object collects all parameter categories for a function definition: positional-only parameters, regular positional parameters, a variadic parameter, keyword-only parameters, a keyword variadic parameter, and their associated default values.""")
    , {'posonlyargs': aDocument(f"({diminutive2etymology['posonlyargs']}) Positional-only parameters that appear before the `/` separator.", 'list[ast.arg] | None = None')
        , 'list_arg': aDocument(f"({diminutive2etymology['list_arg']}) Regular positional parameters. This parameter corresponds to `ast.arguments.args`.", 'list[ast.arg] | None = None')
        , 'vararg': aDocument(f"({diminutive2etymology['vararg']}) The single `*args` parameter that collects extra positional arguments.", 'ast.arg | None = None')
        , 'kwonlyargs': aDocument(f"({diminutive2etymology['kwonlyargs']}) Keyword-only parameters that appear after `*` or `*args`.", 'list[ast.arg] | None = None')
        , 'kw_defaults': aDocument(f"({diminutive2etymology['kw_defaults']}) Default value expressions for keyword-only parameters. `None` at a position indicates that the corresponding keyword-only parameter is required.", 'Sequence[ast.expr | None] | None = None')
        , 'kwarg': aDocument(f"({diminutive2etymology['kwarg']}) The single `**kwargs` parameter that collects extra keyword arguments.", 'ast.arg | None = None')
        , 'defaults': aDocument("Default value expressions for the trailing N regular positional parameters. The length must be less than or equal to the number of regular positional parameters.", 'Sequence[ast.expr] | None = None')}
    , {'functionSignature': aDocument("An `ast.arguments` object holding the complete parameter specification.", 'ast.arguments')}
    , {'Field Mapping': aDocument("""`Make.arguments` renames `ast.arguments.args` to `list_arg` to avoid shadowing the Python built-in identifier `args`. Internally, `Make.arguments` passes `list_arg` as the `args` keyword argument to `ast.arguments`.""")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Assert"
    , aDocument("Make an `ast.Assert` object for an `assert` statement.")
    , aDocument(f"""The `ast.Assert` object represents an `assert` statement. When the `test` expression evaluates to `False`, the Python interpreter raises `AssertionError`. The optional `msg` ({diminutive2etymology['msg']}) expression provides the error message attached to that `AssertionError`.""")
    , {'test': aDocument("Boolean expression to evaluate. When `test` is falsy, `AssertionError` is raised.", 'ast.expr')
        , 'msg': aDocument(f"({diminutive2etymology['msg']}) Optional expression providing the `AssertionError` message.", 'ast.expr | None = None')}
    , {'assertStatement': aDocument("An `ast.Assert` object representing an assertion statement.", 'ast.Assert')}
    , {'Runtime Behavior': aDocument("""Python's `-O` (optimize) flag removes `assert` statements from compiled bytecode entirely. Code that uses `assert` for input validation rather than debugging will silently skip those checks when Python runs under optimization.""")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.AST"
    , aDocument(f"Make a base `ast.AST` ({diminutive2etymology['AST']}) object.")
    , aDocument(f"""The `ast.AST` ({diminutive2etymology['AST']}) object is the base class for all AST node types. In most cases, use a specific factory method such as `Make.Name`, `Make.Call`, or `Make.Assign` rather than `Make.AST`.""")
    , {}
    , {'baseNode': aDocument(f"A base `ast.AST` ({diminutive2etymology['AST']}) object.", 'ast.AST')}
    , {'AST Architecture': aDocument(f"""`ast.AST` ({diminutive2etymology['AST']}) provides two class-level tuples that govern each subclass: `_fields`, which lists the names of domain-specific child nodes, and `_attributes`, which lists the four source-position attributes (`lineno`, `col_offset`, `end_lineno`, `end_col_offset`). This factory method creates a minimal instance with no `_fields` populated and no attributes set.""")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Assign"
    , aDocument("Make an `ast.Assign` object for a variable assignment without a type annotation.")
    , aDocument("""The `ast.Assign` object represents a simple assignment such as `x = 5` or a chained assignment such as `a = b = value`. A single-element `targets` sequence is the common case; multiple targets create a chained assignment where each target receives the same evaluated `value`.""")
    , {'targets': aDocument("Sequence of assignment targets. Each target receives the evaluated `value`. Multiple targets create a chained assignment.", 'Sequence[ast.expr]')
        , 'value': aDocument("Expression whose result is assigned to every target.", 'ast.expr')}
    , {'assignment': aDocument("An `ast.Assign` object representing a variable assignment.", 'ast.Assign')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.AsyncFor"
    , aDocument(f"Make an `ast.AsyncFor` ({diminutive2etymology['AsyncFor']}) object for an `async for` loop.")
    , aDocument(f"""The `ast.AsyncFor` object represents an `async for` loop that iterates over an asynchronous iterable. The loop body executes once per item yielded by the `iter` ({diminutive2etymology['iter']}) expression. The optional `orElse` ({diminutive2etymology['orElse']}) body executes when the iterator is exhausted without a `break` statement.""")
    , {'target': aDocument("Loop variable expression that receives each yielded item.", 'ast.expr')
        , 'iter': aDocument(f"({diminutive2etymology['iter']}) Asynchronous iterable expression being consumed by the loop.", 'ast.expr')
        , 'body': aDocument("Sequence of statements executed once per item from the async iterable.", 'Sequence[ast.stmt]')
        , 'orElse': aDocument(f"({diminutive2etymology['orElse']}) Optional statements executed when the async iterator is exhausted without a `break` statement. This parameter corresponds to `ast.AsyncFor.orelse`.", 'Sequence[ast.stmt] | None = None')}
    , {'asyncForLoop': aDocument(f"An `ast.AsyncFor` ({diminutive2etymology['AsyncFor']}) object representing an asynchronous `for` loop.", 'ast.AsyncFor')}
    , {'Async Context': aDocument("""`ast.AsyncFor` nodes are valid only inside an `ast.AsyncFunctionDef` body. Placing an `ast.AsyncFor` node inside a synchronous function body produces a `SyntaxError` at compile time.""")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.AsyncFunctionDef"
    , aDocument(f"Make an `ast.AsyncFunctionDef` ({diminutive2etymology['AsyncFunctionDef']}) object for an `async def` function declaration.")
    , aDocument(f"""The `ast.AsyncFunctionDef` object represents an `async def` function definition. The function body may contain `await` expressions, `async for` loops, and `async with` statements. The `type_params` ({diminutive2etymology['type_params']}) parameter supports generic `async def` functions introduced in Python 3.12.""")
    , {'name': aDocument("Function name as a string identifier.", 'str')
        , 'argumentSpecification': aDocument("Complete parameter specification for the function. Defaults to an empty `ast.arguments` object when `None`.", 'ast.arguments | None = None')
        , 'body': aDocument("Sequence of statements forming the function body.", 'Sequence[ast.stmt] | None = None')
        , 'decorator_list': aDocument("Sequence of decorator expressions applied to the function, in declaration order.", 'Sequence[ast.expr] | None = None')
        , 'returns': aDocument(f"({diminutive2etymology['returns']}) Optional return type annotation expression.", 'ast.expr | None = None')
        , 'type_params': aDocument(f"({diminutive2etymology['type_params']}) Optional sequence of type parameters for generic `async def` functions. Requires Python 3.12 or later.", 'Sequence[ast.type_param] | None = None')}
    , {'asyncFunction': aDocument(f"An `ast.AsyncFunctionDef` ({diminutive2etymology['AsyncFunctionDef']}) object representing an asynchronous function definition.", 'ast.AsyncFunctionDef')}
    , {'Field Mapping': aDocument("""`Make.AsyncFunctionDef` renames `ast.AsyncFunctionDef.args` to `argumentSpecification` to avoid shadowing the Python built-in identifier `args`. Internally, `Make.AsyncFunctionDef` passes `argumentSpecification` as the `args` keyword argument to `ast.AsyncFunctionDef`.""")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.AsyncWith"
    , aDocument(f"Make an `ast.AsyncWith` ({diminutive2etymology['AsyncWith']}) object for an `async with` statement.")
    , aDocument("""The `ast.AsyncWith` object represents an `async with` statement that manages one or more asynchronous context managers. Each element of `items` specifies one context manager expression and an optional variable binding for the value returned by the context manager's `__aenter__` coroutine.""")
    , {'items': aDocument("Sequence of `ast.withitem` objects, each specifying one async context manager expression and an optional `as` variable binding.", 'list[ast.withitem]')
        , 'body': aDocument("Sequence of statements executed within the async context manager scope.", 'Sequence[ast.stmt]')}
    , {'asyncWithStatement': aDocument(f"An `ast.AsyncWith` ({diminutive2etymology['AsyncWith']}) object representing an asynchronous context manager statement.", 'ast.AsyncWith')}
    , {'Async Context': aDocument("""`ast.AsyncWith` nodes are valid only inside an `ast.AsyncFunctionDef` body. Placing an `ast.AsyncWith` node inside a synchronous function body produces a `SyntaxError` at compile time.""")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Attribute"
    , aDocument("Make an `ast.Attribute` object for dot notation attribute access.")
    , aDocument("""The `ast.Attribute` object represents attribute access using dot notation such as `object.method` or `module.Class`. The `*attribute` variadic parameter accepts multiple names to chain attribute accesses, producing `value.first.second.third` from a single `Make.Attribute` call.""")
    , {'value': aDocument("Base expression providing the object on which attribute access begins.", 'ast.expr')
        , 'attribute': aDocument("One or more attribute name strings to access in sequence. Multiple names generate a chain of nested `ast.Attribute` objects.", 'str')
        , 'context': aDocument(f"({diminutive2etymology['ctx']}) Expression context for the final attribute in the chain. Use `ast.Load()` to read, `ast.Store()` to assign, or `ast.Del()` ({diminutive2etymology['Del']}) to delete. Defaults to `ast.Load()`. This parameter corresponds to `ast.Attribute.ctx`.", 'ast.expr_context | None = None')}
    , {'attributeAccess': aDocument("An `ast.Attribute` object representing the final attribute in the chain.", 'ast.Attribute')}
    , {'Chained Attribute Access': aDocument("""`Make.Attribute(value, 'first', 'second', context=ctx)` produces `ast.Attribute(ast.Attribute(value, 'first', ctx=ast.Load()), 'second', ctx=ctx)`. Only the final `ast.Attribute` node in the chain uses the supplied `context`; all intermediate nodes use `ast.Load()`.""")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.AugAssign"
    , aDocument(f"Make an `ast.AugAssign` ({diminutive2etymology['AugAssign']}) object for a compound assignment operation.")
    , aDocument(f"""The `ast.AugAssign` object represents compound assignment operators such as `+=`, `-=`, `*=`, and `/=`. The `op` ({diminutive2etymology['op']}) specifies which binary operation is applied to the current `target` value combined with the `value` expression before the result is stored back into `target`.""")
    , {'target': aDocument("Assignment target being modified. Must be an `ast.Name`, `ast.Attribute`, or `ast.Subscript`.", 'ast.Name | ast.Attribute | ast.Subscript')
        , 'op': aDocument(f"({diminutive2etymology['op']}) Binary operator instance defining the augmentation, such as `ast.Add()` for `+=` or `ast.Mult()` ({diminutive2etymology['Mult']}) for `*=`.", 'ast.operator')
        , 'value': aDocument("Expression whose result is combined with the current target value using `op` before the result is assigned back to `target`.", 'ast.expr')}
    , {'augmentedAssignment': aDocument(f"An `ast.AugAssign` ({diminutive2etymology['AugAssign']}) object representing a compound assignment statement.", 'ast.AugAssign')}
    , {'AST Grammar': aDocument("""The Python grammar restricts `ast.AugAssign.target` to three expression node types: `ast.Name`, `ast.Attribute`, and `ast.Subscript`. Any other expression node type in the `target` position is a grammar violation and raises `SyntaxError` at compile time.""")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Await"
    , aDocument(f"Make an `ast.Await` ({diminutive2etymology['Await']}) object for an `await` expression.")
    , aDocument("""The `ast.Await` object represents an `await` expression that suspends the enclosing coroutine until the awaited object completes. The `value` must be an awaitable object such as a coroutine call, `asyncio.Task`, or `asyncio.Future`.""")
    , {'value': aDocument("The awaitable expression to suspend on, such as a coroutine call or `asyncio.Future`.", 'ast.expr')}
    , {'awaitExpression': aDocument(f"An `ast.Await` ({diminutive2etymology['Await']}) object representing a suspension point in a coroutine.", 'ast.Await')}
    , {'Async Context': aDocument("""`ast.Await` nodes are valid only inside an `ast.AsyncFunctionDef` body. Placing an `ast.Await` node in a synchronous function body produces a `SyntaxError` at compile time.""")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.BinOp"
    , aDocument(f"Make an `ast.BinOp` ({diminutive2etymology['BinOp']}) object for a binary operation between two expressions.")
    , aDocument(f"""The `ast.BinOp` object represents a two-operand operation determined by `op` ({diminutive2etymology['op']}). The `left` ({diminutive2etymology['left']}) and `right` ({diminutive2etymology['right']}) parameters provide the two operands.""")
    , {'left': aDocument(f"({diminutive2etymology['left']}) Left operand expression.", 'ast.expr')
        , 'op': aDocument(f"({diminutive2etymology['op']}) Binary operator instance, such as `ast.Add()`, `ast.Sub()` ({diminutive2etymology['Sub']}), `ast.Mult()` ({diminutive2etymology['Mult']}), `ast.Div()` ({diminutive2etymology['Div']}), or any other `ast.operator` subclass.", 'ast.operator')
        , 'right': aDocument(f"({diminutive2etymology['right']}) Right operand expression.", 'ast.expr')}
    , {'binaryOperation': aDocument(f"An `ast.BinOp` ({diminutive2etymology['BinOp']}) object representing a two-operand arithmetic, bitwise, or other binary operation.", 'ast.BinOp')}
    , {'Operator Subclasses': aDocument("""The complete set of `ast.operator` subclasses usable as `op`: `ast.Add`, `ast.Sub`, `ast.Mult`, `ast.Div`, `ast.FloorDiv`, `ast.Mod`, `ast.Pow`, `ast.LShift`, `ast.RShift`, `ast.BitOr`, `ast.BitXor`, `ast.BitAnd`, `ast.MatMult`. Each subclass in `Make` also provides a `join()` classmethod that chains an iterable of expressions into a left-associative tree of `ast.BinOp` nodes.""")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.boolop"
    , aDocument(f"Make a base `ast.boolop` ({diminutive2etymology['boolop']}) object.")
    , aDocument("""The `ast.boolop` abstract class is the parent of `ast.And` and `ast.Or`. Use `Make.And()`, `Make.Or()`, or `Make.BoolOp()` for concrete boolean operations. `Make.boolop` creates the abstract base instance, which is useful only in antecedent-action patterns with visitor classes.""")
    , {}
    , {'baseBooleanOperator': aDocument(f"A base `ast.boolop` ({diminutive2etymology['boolop']}) object.", 'ast.boolop')}
    , {'Visitor Pattern': aDocument("""`Make.boolop()` is used in antecedent-action patterns where a visitor method must match any boolean operator node without specifying a concrete subclass. Concrete subclasses `ast.And` and `ast.Or` carry no fields; they are distinguished only by their type.""")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.BoolOp"
    , aDocument(f"Make an `ast.BoolOp` ({diminutive2etymology['BoolOp']}) object for a logical operation over multiple operands.")
    , aDocument("""The `ast.BoolOp` object represents `and` or `or` applied to two or more operands collected in `values`. A single `ast.BoolOp` with `op` = `ast.And()` and three `values` is equivalent to `a and b and c`; the Python grammar flattens chained boolean operators into one node rather than nesting multiple `ast.BoolOp` nodes.""")
    , {'op': aDocument(f"({diminutive2etymology['boolop']}) Boolean operator instance: either `ast.And()` or `ast.Or()`.", 'ast.boolop')
        , 'values': aDocument("Sequence of two or more operand expressions to combine with `op`.", 'Sequence[ast.expr]')}
    , {'booleanOperation': aDocument(f"An `ast.BoolOp` ({diminutive2etymology['BoolOp']}) object representing a logical operation over multiple operands.", 'ast.BoolOp')}
    , {'AST Structure': aDocument("""The Python grammar represents `a and b and c` as `ast.BoolOp(op=ast.And(), values=[a, b, c])`, not as nested `ast.BoolOp` nodes. `values` must contain at least two elements; a single-element `values` list is syntactically valid in the AST but does not correspond to any source-level boolean expression.""")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Break"
    , aDocument("Make an `ast.Break` object for a `break` statement.")
    , aDocument("""The `ast.Break` object represents a `break` statement that immediately terminates the nearest enclosing `for` or `while` loop. When a `break` is encountered, the optional `else` clause of the enclosing loop does not execute.""")
    , {}
    , {'breakStatement': aDocument("An `ast.Break` object representing a loop termination statement.", 'ast.Break')}
    , {'Loop Interaction': aDocument("""`ast.Break` suppresses the `orelse` body of the enclosing `ast.For`, `ast.AsyncFor`, or `ast.While` node. A `break` placed outside any loop body raises `SyntaxError` at compile time.""")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Call"
    , aDocument("Make an `ast.Call` object for a function or method invocation.")
    , aDocument("""The `ast.Call` object represents a call expression such as `func(a, b, key=val)`. `callee` holds the callable expression; `listParameters` holds positional arguments; `list_keyword` ({diminutive2etymology['list_keyword']}) holds keyword arguments as a list of `ast.keyword` objects, including `**unpacked` arguments where `ast.keyword.arg` is `None`.""")
    , {'callee': aDocument("Callable expression, such as an `ast.Name`, `ast.Attribute`, or any other expression that evaluates to a callable.", 'ast.expr')
        , 'listParameters': aDocument("Sequence of positional argument expressions, including `*unpacked` arguments represented as `ast.Starred` nodes.", 'Sequence[ast.expr] | None = None')
        , 'list_keyword': aDocument(f"({diminutive2etymology['list_keyword']}) Keyword argument objects. Pass `ast.keyword(None, expr)` to represent `**expr` unpacking.", 'list[ast.keyword] | None = None')}
    , {'functionCall': aDocument("An `ast.Call` object representing a call expression with positional and keyword arguments.", 'ast.Call')}
    , {'Field Mapping': aDocument("""`Make.Call` renames `ast.Call.func` to `callee` and `ast.Call.args` to `listParameters` to avoid shadowing the Python `func` and `args` identifiers. Internally these are passed as `func` and `args` keyword arguments to `ast.Call`.""")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.ClassDef"
    , aDocument(f"Make an `ast.ClassDef` ({diminutive2etymology['ClassDef']}) object for a `class` declaration.")
    , aDocument(f"""The `ast.ClassDef` object represents a `class` statement including base classes, keyword arguments (such as `metaclass=`), decorators, body statements, and optional type parameters. The `type_params` ({diminutive2etymology['type_params']}) parameter supports generic classes introduced in Python 3.12.""")
    , {'name': aDocument("Class name as a string identifier.", 'str')
        , 'bases': aDocument(f"({diminutive2etymology['bases']}) Sequence of base class expressions for inheritance. An empty sequence produces a class with no explicit bases.", 'Sequence[ast.expr] | None = None')
        , 'list_keyword': aDocument(f"({diminutive2etymology['list_keyword']}) Keyword arguments to the class definition such as `metaclass=ABCMeta`. This parameter corresponds to `ast.ClassDef.keywords`.", 'list[ast.keyword] | None = None')
        , 'body': aDocument("Sequence of statements forming the class body.", 'Sequence[ast.stmt] | None = None')
        , 'decorator_list': aDocument("Sequence of decorator expressions applied to the class, in declaration order.", 'Sequence[ast.expr] | None = None')
        , 'type_params': aDocument(f"({diminutive2etymology['type_params']}) Sequence of type parameters for generic classes. Requires Python 3.12 or later.", 'Sequence[ast.type_param] | None = None')}
    , {'classDefinition': aDocument(f"An `ast.ClassDef` ({diminutive2etymology['ClassDef']}) object representing a complete class declaration.", 'ast.ClassDef')}
    , {'Field Mapping': aDocument("""`Make.ClassDef` renames `ast.ClassDef.keywords` to `list_keyword` for consistency with other `Make` methods that accept keyword argument lists. Internally `list_keyword` is passed as the `keywords` field of `ast.ClassDef`.""")
        , 'Examples': aDocument("""```python
        # Creates AST equivalent to: class Vehicle: pass
        simpleClass = Make.ClassDef('Vehicle', body=[Make.Pass()])

        # Creates AST equivalent to: class Bicycle(Vehicle, metaclass=ABCMeta): pass
        inheritedClass = Make.ClassDef(
            'Bicycle',
            bases=[Make.Name('Vehicle')],
            list_keyword=[Make.keyword('metaclass', Make.Name('ABCMeta'))],
            body=[Make.Pass()]
        )
        ```
        """)}
))

listDocstring.append(Docstring(f"{identifierToolClass}.cmpop"
    , aDocument(f"Make a base `ast.cmpop` ({diminutive2etymology['cmpop']}) object.")
    , aDocument(f"""The `ast.cmpop` abstract class is the parent of all comparison operator classes used in `ast.Compare`. `Make.cmpop` creates the abstract base instance, which is useful only in antecedent-action patterns with visitor classes. Use a concrete subclass for actual comparison operations: `ast.Eq` ({diminutive2etymology['Eq']}), `ast.NotEq` ({diminutive2etymology['NotEq']}), `ast.Lt` ({diminutive2etymology['Lt']}), `ast.LtE` ({diminutive2etymology['LtE']}), `ast.Gt` ({diminutive2etymology['Gt']}), `ast.GtE` ({diminutive2etymology['GtE']}), `ast.Is`, `ast.IsNot`, `ast.In`, `ast.NotIn` ({diminutive2etymology['NotIn']}).""")
    , {}
    , {'comparisonOperator': aDocument(f"A base `ast.cmpop` ({diminutive2etymology['cmpop']}) object.", 'ast.cmpop')}
    , {'Visitor Pattern': aDocument("""`Make.cmpop()` is used in antecedent-action patterns where a visitor method must match any comparison operator node without specifying a concrete subclass. All `ast.cmpop` concrete subclasses carry no fields; they are distinguished only by their type.""")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Compare"
    , aDocument("Make an `ast.Compare` object for a comparison expression, including chained comparisons.")
    , aDocument(f"""The `ast.Compare` object represents a comparison expression such as `x == 0` or a chained comparison such as `0 <= x < 100`. The `left` ({diminutive2etymology['left']}) expression is compared to each element of `comparators` using the corresponding operator from `ops` ({diminutive2etymology['ops']}). `ops` and `comparators` must have the same length.""")
    , {'left': aDocument(f"({diminutive2etymology['left']}) Leftmost expression in the comparison.", 'ast.expr')
        , 'ops': aDocument(f"({diminutive2etymology['ops']}) Sequence of `ast.cmpop` ({diminutive2etymology['cmpop']}) instances, one per comparator. Valid operators: `ast.Eq` ({diminutive2etymology['Eq']}), `ast.NotEq` ({diminutive2etymology['NotEq']}), `ast.Lt` ({diminutive2etymology['Lt']}), `ast.LtE` ({diminutive2etymology['LtE']}), `ast.Gt` ({diminutive2etymology['Gt']}), `ast.GtE` ({diminutive2etymology['GtE']}), `ast.Is`, `ast.IsNot`, `ast.In`, `ast.NotIn` ({diminutive2etymology['NotIn']}).", 'Sequence[ast.cmpop]')
        , 'comparators': aDocument("Sequence of right-hand expressions, one per operator. The N-th comparator is compared to the (N−1)-th expression using `ops[N−1]`.", 'Sequence[ast.expr]')}
    , {'comparison': aDocument("An `ast.Compare` object representing a comparison or chained comparison expression.", 'ast.Compare')}
    , {'Chained Comparison Structure': aDocument("""Python represents `a < b <= c` as `ast.Compare(left=a, ops=[Lt(), LtE()], comparators=[b, c])`, not as nested `ast.BoolOp` or `ast.BinOp` nodes. The semantics of a chained comparison are: each consecutive pair is evaluated from left to right and the results are combined with short-circuit `and`. The `ops` and `comparators` sequences must have identical length; a mismatch is a grammar error.""")
        , 'Examples': aDocument("""```python
        # Creates AST equivalent to: `temperature == 72`
        temperatureCheck = Make.Compare(
            left=Make.Name('temperature'),
            ops=[Make.Eq()],
            comparators=[Make.Constant(72)]
        )

        # Creates AST equivalent to: `0 <= inventory < 100`
        inventoryRange = Make.Compare(
            left=Make.Constant(0),
            ops=[Make.LtE(), Make.Lt()],
            comparators=[Make.Name('inventory'), Make.Constant(100)]
        )
        ```
        """)}
))

listDocstring.append(Docstring(f"{identifierToolClass}.comprehension"
    , aDocument("Make an `ast.comprehension` object for one `for` clause in a comprehension or generator expression.")
    , aDocument(f"""The `ast.comprehension` object represents a single `for` clause within a list comprehension, set comprehension, dictionary comprehension, or generator expression. The `target` receives each item from `iter` ({diminutive2etymology['iter']}); the optional `ifs` ({diminutive2etymology['ifs']}) sequence filters items before the enclosing expression body is evaluated.""")
    , {'target': aDocument("Variable expression that receives each item yielded by `iter`. May be a name, tuple, or other valid assignment target.", 'ast.expr')
        , 'iter': aDocument(f"({diminutive2etymology['iter']}) Iterable expression whose items are bound to `target` on each step.", 'ast.expr')
        , 'ifs': aDocument(f"({diminutive2etymology['ifs']}) Sequence of filter expressions. An item proceeds to the body only when every expression in `ifs` evaluates to `True`. An empty sequence applies no filter.", 'Sequence[ast.expr]')
        , 'is_async': aDocument(f"({diminutive2etymology['is_async']}) Set to `1` to indicate an `async for` clause inside an `async def` body; `0` for a synchronous clause.", 'int = 0')}
    , {'comprehensionClause': aDocument("An `ast.comprehension` object representing one `for` clause with optional filters.", 'ast.comprehension')}
    , {'Multiple Clauses': aDocument("""A comprehension with multiple `for` clauses uses a list of `ast.comprehension` objects in the `generators` field of the enclosing `ast.ListComp`, `ast.SetComp`, `ast.DictComp`, or `ast.GeneratorExp`. The first `ast.comprehension` in `generators` is the outermost loop; subsequent objects are nested inner loops, equivalent to `for … for …` written left to right in source.""")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Constant"
    , aDocument("Make an `ast.Constant` object for a literal value in Python source.")
    , aDocument("""The `ast.Constant` object is the unified representation for all Python literal constants: integers, floats, complex numbers, strings, bytes, booleans, and `None`. `ast.Constant` replaced the deprecated node types `ast.Num`, `ast.Str`, `ast.Bytes`, `ast.NameConstant`, and `ast.Ellipsis` starting in Python 3.8.""")
    , {'value': aDocument("The literal constant value. May be any type accepted by `ast.Constant.value`: `int`, `float`, `complex`, `str`, `bytes`, `bool`, `None`, or `...` (Ellipsis).", 'ConstantValueType')
        , 'kind': aDocument('Optional string hint preserved for compatibility with `u`-prefixed string literals (`u"..."``). Pass `None` for all other constant types.', 'str | None = None')}
    , {'constantValue': aDocument("An `ast.Constant` object holding the specified literal value.", 'ast.Constant')}
    , {'Deprecated Predecessors': aDocument("""Before Python 3.8, separate node classes represented each constant category: `ast.Num` for numeric literals, `ast.Str` for string literals, `ast.Bytes` for bytes literals, `ast.NameConstant` for `True`, `False`, and `None`, and `ast.Ellipsis` for `...`. These classes were removed in Python 3.12. All literal constants are now uniformly represented by `ast.Constant`.""")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Continue"
    , aDocument("Make an `ast.Continue` object for a `continue` statement.")
    , aDocument("""The `ast.Continue` object represents a `continue` statement that skips the remaining statements in the current loop body and proceeds to the next iteration of the nearest enclosing `for` or `while` loop. The optional `else` clause of the enclosing loop is not affected by `continue`.""")
    , {}
    , {'continueStatement': aDocument("An `ast.Continue` object representing a loop continuation statement.", 'ast.Continue')}
    , {'Loop Interaction': aDocument("""`ast.Continue` does not suppress the `orelse` body of the enclosing loop—only `ast.Break` suppresses it. A `continue` placed outside any loop body raises `SyntaxError` at compile time.""")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Del"
    , aDocument("Make a delete context for removing expressions from memory.")
    , aDocument(f"""The `ast.Del` ({diminutive2etymology['Del']}) context indicates expressions are deletion targets in `del` statements. Note that `ast.Del` is the expression context, not the `del` keyword itself - `ast.Delete` represents the `del` statement.""")
    , {}
    , {'deleteContext': aDocument("AST context object indicating deletion operations on expressions.")}
    , {'Examples': aDocument("""Creates AST equivalent to deletion: del bicycle.wheel
        ```python
        wheelDeletion = Make.Attribute(Make.Name('bicycle'), 'wheel', Make.Del())
        ```
        """, 'ast.Del')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Delete"
    , aDocument("Create an `ast.Delete` node for deletion statements.")
    , aDocument("""The `Delete` node represents a `del` statement that removes references to objects. Can delete variables, attributes, subscripts, or slices.""")
    , {'targets': aDocument("List of expressions identifying what to delete.")}
    , {'nodeDelete': aDocument("The constructed deletion statement node.", 'ast.Delete')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Dict"
    , aDocument(f"Combine `keys` and `values` into an AST ({diminutive2etymology['AST']}) representation of the Python built-in `class` `dict` ({diminutive2etymology['dict']}).")
    , aDocument(f"""The `ast.Dict` ({diminutive2etymology['Dict']}) `object` represents dictionary literals using curly brace notation. It supports both regular key-value pairs and dictionary unpacking operations where keys can be None to indicate unpacking expressions.""")
    , {'keys': aDocument("Sequence of key expressions or None for unpacking operations.")
        , 'values': aDocument("Sequence of value expressions corresponding to the keys.")}
    , {'dictionaryLiteral': aDocument(f"({diminutive2etymology['Dict']}) AST `object` representing a dictionary literal with specified key-value pairs.", 'ast.Dict')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.DictComp"
    , aDocument("Make a dictionary comprehension AST `object` for dynamic dictionary construction.")
    , aDocument(f"""The `ast.DictComp` ({diminutive2etymology['DictComp']}) `object` represents dictionary comprehensions that make dictionaries using iterator expressions. It combines key-value generation with filtering and nested iteration capabilities.""")
    , {'key': aDocument("Expression that generates dictionary keys.")
        , 'value': aDocument("Expression that generates dictionary values.")
        , 'generators': aDocument("Sequence of `ast.comprehension` defining iteration and filtering.")}
    , {'dictionaryComprehension': aDocument(f"({diminutive2etymology['DictComp']}) AST `object` representing a dictionary comprehension expression.")}
    , {'Examples': aDocument("""```
        # Creates AST equivalent to: `{recipe: difficulty for recipe in cookbook}`
        recipeDifficulty = Make.DictComp(
            key=Make.Name('recipe'),
            value=Make.Name('difficulty'),
            generators=[Make.comprehension(
                target=Make.Name('recipe'),
                iter=Make.Name('cookbook'),
                ifs=[]
            )]
        )
        ```
        """, 'ast.DictComp')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Eq"
    , aDocument("'Eq', meaning 'is ***Eq***ual to', is the `object` representation of Python comparison operator '`==`'.")
    , aDocument("""`class` `ast.Eq` is a subclass of `ast.cmpop`, '***c***o***mp***arison ***op***erator', and only used in `class` `ast.Compare`, parameter '`ops`', ***op***erator***s***.""")
    , {}
    , {'equalityOperator': aDocument("AST `object` representing the '`==`' equality comparison operator for use in `ast.Compare`.", 'ast.Eq')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.excepthandler"
    , aDocument("Exception handler abstract base class for try-except constructs.")
    , aDocument(f"""The `ast.excepthandler` ({diminutive2etymology['excepthandler']}) abstract base class represents exception handling clauses in try-except statements. This is the foundation for `ast.ExceptHandler` which implements the actual exception catching logic.""")
    , {}
    , {'exceptionHandler': aDocument("Abstract AST object for exception handling clause classification.", 'ast.excepthandler')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.ExceptHandler"
    , aDocument("Exception handler clause for try-except statements.")
    , aDocument(f"""The `ast.ExceptHandler` ({diminutive2etymology['ExceptHandler']}) object represents individual `except` clauses that catch and handle specific exceptions. It defines the exception type to catch, optional variable binding, and statements to execute when matched.""")
    , {'type': aDocument("Exception type expression to catch; None catches all exceptions.")
        , 'name': aDocument("Variable name string to bind caught exception; None for no binding.")
        , 'body': aDocument("List of statements to execute when exception is caught.")}
    , {'exceptionHandler': aDocument("AST object representing an except clause in try-except statements.", 'ast.ExceptHandler')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.expr"
    , aDocument("Abstract ***expr***ession `object` for base expression operations.")
    , aDocument("""The `ast.expr` class serves as the abstract base class for all expression objects in Python's AST. Unlike `ast.stmt` which represents statements that perform actions, `ast.expr` represents expressions that evaluate to values and can be used within larger expressions or as parts of statements.

        Expressions vs Statements:
        - **expr**: Evaluates to a value and can be composed into larger expressions. Examples include literals (`42`, `"hello"`), operations (`x + y`), function calls (`len(data)`), and attribute access (`obj.method`).
        - **stmt**: Performs an action and does not evaluate to a usable value. Examples include assignments (`x = 5`), control flow (`if`, `for`, `while`), function definitions (`def`), and imports (`import`).""")
    , {}
    , {'expression': aDocument("Abstract expression `object` that serves as the base class for all Python expressions in AST structures.")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Expr"
    , aDocument("Create an `ast.Expr` node for expression statements.")
    , aDocument("""The `Expr` node represents a statement that consists of a single expression whose value is discarded. This is used for expressions evaluated for their side effects rather than their return value.""")
    , {'value': aDocument("Expression to evaluate as a statement.")}
    , {'nodeExpr': aDocument("The constructed expression statement node.", 'ast.Expr')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.expr_context"
    , aDocument("Expression context abstract base class for expression usage patterns.")
    , aDocument(f"""The `ast.expr_context` ({diminutive2etymology['expr_context']}) abstract base class represents how expressions are used in code: whether they load values, store values, or delete them. This is the foundation for `ast.Load`, `ast.Store`, and `ast.Del` contexts.""")
    , {}
    , {'expressionContext': aDocument("Abstract AST context object for expression usage classification.", 'ast.expr_context')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Expression"
    , aDocument("Create an `ast.Expression` node for expression-only modules.")
    , aDocument("""The `Expression` node represents a module that contains only a single expression. This is used in contexts where only an expression is expected, such as with `eval()` or interactive mode single expressions.""")
    , {'body': aDocument("The single expression that forms the module body")}
    , {'nodeExpression': aDocument("The constructed expression module node", 'ast.Expression')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.For"
    , aDocument("Make a for loop AST `object` for iterating over iterable expressions.")
    , aDocument("""The `ast.For` `object` represents traditional `for` loops that iterate over sequences, generators, or any iterable object. It supports optional else clauses that execute when the loop completes normally.""")
    , {'target': aDocument("The loop variable that receives each item from the iterable expression.")
        , 'iter': aDocument(f"({diminutive2etymology['iter']}) The iterable expression being iterated over, such as a list, range, or generator.")
        , 'body': aDocument("Sequence of statements executed for each iteration of the loop.")
        , 'orelse': aDocument(f"({diminutive2etymology['orElse']}) Optional statements executed when the loop completes normally without encountering a break statement.")}
    , {'forLoop': aDocument("AST `object` representing a for loop iteration construct.", 'ast.For')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.FormattedValue"
    , aDocument("Make a formatted value AST `object` for f-string interpolation components.")
    , aDocument("""The `ast.FormattedValue` `object` represents individual expressions within f-string literals, including format specifications and conversion options. It handles the interpolation mechanics of formatted string literals.""")
    , {'value': aDocument("The expression to be formatted and interpolated.")
        , 'conversion': aDocument("Conversion flag (0=no conversion, 115='s', 114='r', 97='a').")
        , 'format_spec': aDocument(f"({diminutive2etymology['format_spec']}) Optional format specification expression.")}
    , {'formattedValue': aDocument("AST `object` representing a formatted value within an f-string expression.", 'ast.FormattedValue')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.FunctionDef"
    , aDocument("Make a function definition AST object for standard `def` declarations with typing support.")
    , aDocument("""The `ast.FunctionDef` object represents standard function definitions including parameters, return annotations, decorators, and function body. Supports modern Python typing features and generic type parameters.""")
    , {'name': aDocument("Function name as string identifier.")
        , 'args': aDocument("Function parameter specification.")
        , 'body': aDocument("List of statements forming the function body.")
        , 'decorator_list': aDocument("List of decorator expressions applied to function.")
        , 'returns': aDocument(f"({diminutive2etymology['returns']}) Optional return type annotation expression.")
        , 'type_params': aDocument(f"({diminutive2etymology['type_params']}) List of type parameters for generic functions (Python 3.12+).")}
    , {'functionDefinition': aDocument("AST object representing a complete function definition with metadata.")}
    , {'Examples': aDocument("""```
        # Creates AST equivalent to: def cook(): pass
        simpleFunction = Make.FunctionDef('cook', body=[Make.Pass()])

        # Creates AST equivalent to: def bake(recipe: str, temperature: int = 350) -> bool: return True
        typedFunction = Make.FunctionDef(
            'bake',
            Make.arguments(
                args=[Make.arg('recipe', Make.Name('str')), Make.arg('temperature', Make.Name('int'))],
                defaults=[Make.Constant(350)]
            ),
            [Make.Return(Make.Constant(True))],
            returns=Make.Name('bool')
        )
        ```
        """)}
))

listDocstring.append(Docstring(f"{identifierToolClass}.FunctionType"
    , aDocument("Create an `ast.FunctionType` node for function type annotations.")
    , aDocument("""The `FunctionType` node represents function type annotations of the form `(arg_types) -> return_type`. This is used in type annotations and variable annotations for callable types.""")
    , {'argtypes': aDocument(f"({diminutive2etymology['argtypes']}) List of expressions representing argument types")
        , 'returns': aDocument(f"({diminutive2etymology['returns']}) Expression representing the return type")}
    , {'nodeFunctionType': aDocument("The constructed function type annotation node", 'ast.FunctionType')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.GeneratorExp"
    , aDocument("Make a generator expression object for memory-efficient iteration.")
    , aDocument(f"""The `ast.GeneratorExp` ({diminutive2etymology['GeneratorExp']}) object represents generator expressions that create iterator objects without constructing intermediate collections. It provides lazy evaluation and memory efficiency for large datasets.""")
    , {'element': aDocument("Expression that generates each element of the generator.")
        , 'generators': aDocument("Sequence of `ast.comprehension` objects defining iteration and filtering.")}
    , {'generatorExpression': aDocument("AST object representing a generator expression for lazy evaluation.", 'ast.GeneratorExp')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Global"
    , aDocument("Create an `ast.Global` node for global declarations.")
    , aDocument("""The `Global` node represents a `global` statement that declares variables as referring to global scope rather than local scope. This affects variable lookup and assignment within the current function.""")
    , {'names': aDocument("List of variable names to declare as global.")}
    , {'nodeGlobal': aDocument("The constructed global declaration node.", 'ast.Global')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Gt"
    , aDocument("'Gt', meaning 'Greater than', is the `object` representation of Python operator '`>`'.")
    , aDocument("""`class` `ast.Gt` is a subclass of `ast.cmpop`, '***c***o***mp***arison ***op***erator', and only used in `class` `ast.Compare`, parameter '`ops`', ***op***erator***s***.""")
    , {}
    , {'greaterThanOperator': aDocument("AST `object` representing the '`>`' greater-than comparison operator for use in `ast.Compare`.", 'ast.Gt')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.GtE"
    , aDocument("'GtE', meaning 'is Greater than or Equal to', is the `object` representation of Python comparison operator '`>=`'.")
    , aDocument("""`class` `ast.GtE` is a subclass of `ast.cmpop`, '***c***o***mp***arison ***op***erator', and only used in `class` `ast.Compare`, parameter '`ops`', ***op***erator***s***.""")
    , {}
    , {'greaterThanOrEqualOperator': aDocument("AST `object` representing the '`>=`' greater-than-or-equal comparison operator for use in `ast.Compare`.", 'ast.GtE')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.If"
    , aDocument("Make a conditional statement AST `object` for branching execution paths.")
    , aDocument("""The `ast.If` `object` represents `if` statements that conditionally execute code blocks based on boolean test expressions. It supports optional else clauses for alternative execution paths.""")
    , {'test': aDocument("The boolean expression that determines which branch to execute.")
        , 'body': aDocument("Sequence of statements executed when the test expression evaluates to True.")
        , 'orElse': aDocument(f"({diminutive2etymology['orElse']}) Optional statements executed when the test expression evaluates to False. This parameter corresponds with `ast.If.orelse` ({diminutive2etymology['orelse']}).")}
    , {'conditionalStatement': aDocument("AST `object` representing a conditional branching statement.")}
    , {'Examples': aDocument("""```python
        # Creates AST for: if userLoggedIn:
        #                     showDashboard()
        simpleIf = Make.If(
            Make.Name('userLoggedIn'),
            [Make.Expr(Make.Call(Make.Name('showDashboard')))]
        )

        # Creates AST for: if temperature > 100:
        #                     activateCooling()
        #                 else:
        #                     maintainTemperature()
        ifElse = Make.If(
            Make.Compare(Make.Name('temperature'), [Make.Gt()], [Make.Constant(100)]),
            [Make.Expr(Make.Call(Make.Name('activateCooling')))],
            [Make.Expr(Make.Call(Make.Name('maintainTemperature')))]
        )

        # Creates AST for nested if-elif-else chains
        ifElifElse = Make.If(
            Make.Compare(Make.Name('score'), [Make.GtE()], [Make.Constant(90)]),
            [Make.Assign([Make.Name('grade')], Make.Constant('A'))],
            [Make.If(
                Make.Compare(Make.Name('score'), [Make.GtE()], [Make.Constant(80)]),
                [Make.Assign([Make.Name('grade')], Make.Constant('B'))],
                [Make.Assign([Make.Name('grade')], Make.Constant('C'))]
            )]
        )
        ```
        """)}
))

listDocstring.append(Docstring(f"{identifierToolClass}.IfExp"
    , aDocument("Make a 'ChooseThis `if` ConditionIsTrue `else` ChooseThat' conditional expression.")
    , aDocument(f"""The `ast.IfExp` ({diminutive2etymology['IfExp']}) `object` represents inline conditional expressions using the ternary operator syntax `execute_if_true if condition else execute_if_false`.""")
    , {'test': aDocument("The `True`/`False` condition expression.")
        , 'body': aDocument("If `test` is `True`, the interpreter executes this singular expression.")
        , 'orElse': aDocument(f"({diminutive2etymology['orElse']}) If `test` is `False`, the interpreter executes this singular expression. This parameter corresponds with `ast.IfExp.orelse` ({diminutive2etymology['orelse']}).")}
    , {'conditionalExpression': aDocument(f"`ast.AST` ({diminutive2etymology['AST']}) `object` representing an inline conditional expression.")}
    , {'Examples': aDocument("""```python
        # To create the `ast.AST` representation of `maxVolume if amplified else defaultVolume`:
        Make.IfExp(
            test = Make.Name('amplified'),
            body = Make.Name('maxVolume'),
            orElse = Make.Name('defaultVolume')
        )

        # To create the `ast.AST` representation of `"sunny" if weather > 70 else "cloudy"`:
        Make.IfExp(
            test = Make.Compare(Make.Name('weather'), [ Make.Gt() ], [ Make.Constant(70) ]),
            body = Make.Constant("sunny"),
            orElse = Make.Constant("cloudy")
        )
        ```
        """)}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Import"
    , aDocument("Make an `ast.Import` `object` representing a single `import` statement.")
    , aDocument("""The `ast.Import` `object` represents one `import` statement with zero or more module names separated by commas. Each module name is an `ast.alias` `object`. The series of module names is stored in `ast.Import.names` as a `list` of `ast.alias`.

    Nevertheless, with `Make.Import`, you must create exactly one `ast.alias` `object` to be placed in `ast.Import.names`.""")
    , {'dotModule': aDocument(f"({diminutive2etymology['dotModule']}) The name of the module to import: the name may be in dot notation, also called attribute access; the name may be an absolute or relative import. This parameter corresponds with `ast.alias.name` in `ast.Import.names[0]`; or, written as one dot-notation statement, it corresponds with `ast.Import.names[0].name`.")
        , 'asName': aDocument(f"({diminutive2etymology['asName']}) The identifier of the module in the local scope: `asName` must be a valid identifier, so it cannot be in dot notation. This parameter corresponds with `ast.alias.asname` in `ast.Import.names[0]`; or, written as one dot-notation statement, it corresponds with `ast.Import.names[0].asname`.")}
    , {'importStatement': aDocument("An `ast.Import` `object` with one `ast.alias` `object` representing a single `import` statement with a single module name.")}
    , {'Examples': aDocument("""```python
        # To represent: `import os`
        Make.Import(dotModule = 'os')

        # To represent: `import re as regex`
        Make.Import(dotModule = 're', asName = 'regex')

        # To represent: `import collections.abc`
        Make.Import(dotModule = 'collections.abc')

        # To represent: `import scipy.signal.windows as SciPy`
        Make.Import(dotModule = 'scipy.signal.windows', asName = 'SciPy')
        ```
        """)}
))

listDocstring.append(Docstring(f"{identifierToolClass}.ImportFrom"
    , aDocument("Make a from-import statement AST `object` for selective module imports.")
    , aDocument("""The `ast.ImportFrom` `object` represents `from ... import` statements that selectively import specific names from modules. It supports relative imports and multiple import aliases.""")
    , {'module': aDocument("The source module name using dot notation, or None for relative imports that rely solely on the level parameter.")
        , 'names': aDocument("List of alias objects specifying which names to import and their optional aliases.")
        , 'level': aDocument(f"({diminutive2etymology['level']}) Import level controlling relative vs absolute imports. Zero indicates absolute import, positive values indicate relative import depth.")}
    , {'fromImportStatement': aDocument("AST `object` representing a selective module import statement.", 'ast.ImportFrom')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.In"
    , aDocument("'In', meaning 'is ***In***cluded in' or 'has membership In', is the `object` representation of Python keyword '`in`'.")
    , aDocument("""`class` `ast.In` is a subclass of `ast.cmpop`, '***c***o***mp***arison ***op***erator', and only used in `class` `ast.Compare`, parameter '`ops`', ***op***erator***s***. The Python interpreter declares *This* `object` 'is ***In***cluded in' *That* `iterable` if *This* `object` matches a part of *That* `iterable`.""")
    , {}
    , {'membershipOperator': aDocument("AST `object` representing the keyword '`in`' membership test operator for use in `ast.Compare`.", 'ast.In')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Interactive"
    , aDocument(f"Create an `ast.Interactive` ({diminutive2etymology['Interactive']}) node for interactive mode modules.")
    , aDocument("""The `Interactive` node represents a module intended for interactive execution, such as in the Python REPL. Unlike regular modules, interactive modules can contain multiple statements that are executed sequentially.""")
    , {'body': aDocument("List of statements forming the interactive module body")}
    , {'nodeInteractive': aDocument("The constructed interactive module node", 'ast.Interactive')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Interpolation"
    , aDocument("Make an interpolation AST `object` for template strings.")
    , aDocument("""The `ast.Interpolation` `object` represents a single interpolation within a template string. It captures the expression being interpolated, along with any conversion flags and format specifiers.""")
    , {'value': aDocument("The expression to be evaluated and interpolated.", 'ast.expr'),
		'string': aDocument("The original string representation of the interpolation. https://github.com/python/cpython/issues/143661", 'builtins.str'),
		'conversion': aDocument("The conversion flag (e.g., -1 for none, 115 for 's', 114 for 'r', 97 for 'a').", 'int'),
		'format_spec': aDocument("Optional format specifier expression.", 'ast.expr | None = None')
	}
    , {'nodeInterpolation': aDocument("AST `object` representing an interpolation component of a template string.", 'ast.Interpolation')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Invert"
    , aDocument("Make a bitwise complement operator representing Python '`~`' operator.")
    , aDocument("""Class `ast.Invert` is a subclass of `ast.unaryop` and represents the bitwise complement or inversion operator '`~`' in Python source code. This operator performs bitwise NOT operation, flipping all bits of its operand. Used within `ast.UnaryOp` as the `op` parameter.""")
    , {}
    , {'bitwiseComplementOperator': aDocument("AST `object` representing the '`~`' bitwise complement operator for use in `ast.UnaryOp`.", 'ast.Invert')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Is"
    , aDocument("'Is', meaning 'Is identical to', is the `object` representation of Python keyword '`is`'.", AIgenerated=False)
    , aDocument("""`class` `ast.Is` is a subclass of `ast.cmpop`, '***c***o***mp***arison ***op***erator', and only used in `class` `ast.Compare`, parameter '`ops`', ***op***erator***s***.

        The Python interpreter declares *This* logical `object` 'Is identical to' *That* logical `object` if they use the same physical memory location. Therefore, modifying one `object` will necessarily modify the other `object`.

        What's the difference between equality and identity? - The work of Jane Austen 'is Equal to' the work of Franz Kafka. - The work of Mark Twain 'is Equal to' the work of Samuel Clemens. - And Mark Twain 'Is identical to' Samuel Clemens: because they are the same person.""", AIgenerated=False)
    , {}
    , {'identityOperator': aDocument("AST `object` representing the '`is`' identity comparison operator for use in `ast.Compare`.", AIgenerated=False)}
    , {'Examples': aDocument("""```python
        # Logically equivalent to: `... valueAttributes is None ...` comparisonNode =
        Make.Compare(
            left=Make.Name('valueAttributes'), ops=[Make.Is()], comparators=[Make.Constant(None)]
        )
        ```

        In the first example, the two statements are logically equal but they cannot be identical.""", AIgenerated=False)}
))

listDocstring.append(Docstring(f"{identifierToolClass}.IsNot"
    , aDocument("'IsNot', meaning 'Is Not identical to', is the `object` representation of Python keywords '`is not`'.")
    , aDocument("""`class` `ast.IsNot` is a subclass of `ast.cmpop`, '***c***o***mp***arison ***op***erator',
        and only used in `class` `ast.Compare`, parameter '`ops`', ***op***erator***s***.

        The Python interpreter declares *This* logical `object` 'Is Not identical to' *That* logical
        `object` if they do not use the same physical memory location.

        What's the difference between equality and identity? - The work of Jane Austen 'is Equal to'
        the work of Franz Kafka. - The work of Mark Twain 'is Equal to' the work of Samuel Clemens.
        - And Mark Twain 'Is identical to' Samuel Clemens: because they are the same person.

        Python programmers frequently use '`is not None`' because keyword `None` does not have a
        physical memory location, so `if chicken is not None`, `chicken` must have a physical memory
        location (and be in the current scope and blah blah blah...).""")
    , {}
    , {'identityNegationOperator': aDocument("AST `object` representing the '`is not`' identity comparison operator for use in `ast.Compare`.")}
    , {'Examples': aDocument("""```python
        # Logically equivalent to: `... chicken is not None ...` comparisonNode =
        Make.Compare(
            left=Make.Name('chicken'), ops=[Make.IsNot()], comparators=[Make.Constant(None)]
        )
        ```

        In the first example, the two statements are logically equal but they cannot be identical.""")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.JoinedStr"
    , aDocument("Make a joined string AST `object` for f-string literal construction.")
    , aDocument(f"""The `ast.JoinedStr` ({diminutive2etymology['JoinedStr']}) `object` represents f-string literals that combine constant text with interpolated expressions. It coordinates multiple string components and formatted values into a single string literal.""")
    , {'values': aDocument("Sequence of string components, including `ast.Constant` and `ast.FormattedValue` objects.")}
    , {'joinedString': aDocument("AST `object` representing an f-string literal with interpolated values.", 'ast.JoinedStr')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.keyword"
    , aDocument("Make a keyword argument AST object for named parameters in function calls.")
    , aDocument("""The `ast.keyword` object represents keyword arguments passed to function calls or class constructors. Contains the parameter name and corresponding value expression, including support for **keywordArguments unpacking.""")
    , {'Buffalo_buffalo_Buffalo_buffalo_buffalo_buffalo_Buffalo_buffalo': aDocument("Parameter name string; None for **keywordArguments unpacking. This corresponds to `ast.keyword.arg`.")
        , 'value': aDocument("Expression providing the argument value.")}
    , {'keywordArgument': aDocument("AST object representing a named argument in function calls.")}
    , {'Examples': aDocument("""Creates AST equivalent to: temperature=350
        ```python
        namedArgument = Make.keyword('temperature', Make.Constant(350))
        ```

        Creates AST equivalent to: **settings (keyword arguments unpacking)
        ```python
        unpackedArguments = Make.keyword(None, Make.Name('settings'))
        ```
        """)}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Lambda"
    , aDocument("Make a lambda function AST `object` for anonymous function expressions.")
    , aDocument(f"""The `ast.Lambda` ({diminutive2etymology['Lambda']}) `object` represents lambda expressions that define anonymous functions with a single expression body. Lambda functions are limited to expressions and cannot contain statements or multiple lines.""")
    , {'argumentSpecification': aDocument("The function arguments specification as `ast.arguments`.")
        , 'body': aDocument("Single expression that forms the lambda function body.")}
    , {'lambdaFunction': aDocument("AST `object` representing an anonymous lambda function expression.", 'ast.Lambda')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.List"
    , aDocument("Make a list literal AST `object` with ordered element collection.")
    , aDocument("""The `ast.List` `object` represents list literals using square bracket notation. It creates ordered, mutable collections and supports various contexts like loading values, storing to variables, or deletion operations.""")
    , {'listElements': aDocument("Sequence of expressions that become list elements.")
        , 'context': aDocument("Expression context for how the list is used.")}
    , {'listLiteral': aDocument("AST `object` representing a list literal with specified elements.", 'ast.List')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.ListComp"
    , aDocument("Make a list comprehension AST `object` for dynamic list construction.")
    , aDocument(f"""The `ast.ListComp` ({diminutive2etymology['ListComp']}) `object` represents list comprehensions that create lists using iterator expressions. It provides concise syntax for filtering and transforming collections into new lists.""")
    , {'element': aDocument(f"({diminutive2etymology['elt']}) Expression that generates each element of the resulting list.")
        , 'generators': aDocument("Sequence of `ast.comprehension` objects defining iterator and filtering.")}
    , {'listComprehension': aDocument("AST `object` representing a list comprehension expression.", 'ast.ListComp')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Load"
    , aDocument("Make a load context for reading expression values.")
    , aDocument("""The `ast.Load` context indicates expressions are being read or evaluated to retrieve their values. This is the default context for most expressions like `bicycle.wheel` when accessing the wheel attribute value.""")
    , {}
    , {'loadContext': aDocument("AST context object indicating value retrieval operations.", 'ast.Load')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Lt"
    , aDocument("'Lt', meaning 'is Less than', is the `object` representation of Python comparison operator '`<`'.")
    , aDocument("""`class` `ast.Lt` is a subclass of `ast.cmpop`, '***c***o***mp***arison ***op***erator', and only used in `class` `ast.Compare`, parameter '`ops`', ***op***erator***s***.""")
    , {}
    , {'lessThanOperator': aDocument("AST `object` representing the '`<`' less-than comparison operator for use in `ast.Compare`.", 'ast.Lt')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.LtE"
    , aDocument("'LtE', meaning 'is Less than or Equal to', is the `object` representation of Python comparison operator '`<=`'.")
    , aDocument("""`class` `ast.LtE` is a subclass of `ast.cmpop`, '***c***o***mp***arison ***op***erator', and only used in `class` `ast.Compare`, parameter '`ops`', ***op***erator***s***.""")
    , {}
    , {'lessThanOrEqualOperator': aDocument("AST `object` representing the '`<=`' less-than-or-equal comparison operator for use in `ast.Compare`.", 'ast.LtE')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Match"
    , aDocument("Make a match statement AST object for pattern matching with multiple cases.")
    , aDocument(f"""The `ast.Match` ({diminutive2etymology['Match']}) object represents match statements that perform pattern matching against a subject expression. Contains the value being matched and a list of case clauses with their patterns and corresponding actions.""")
    , {'subject': aDocument("Expression being matched against the case patterns.")
        , 'cases': aDocument(f"({diminutive2etymology['match_case']}) List of match_case objects defining pattern-action pairs.")}
    , {'matchStatement': aDocument("AST object representing a complete pattern matching statement.", 'ast.Match')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.match_case"
    , aDocument("Make a match case clause AST object for individual cases in `match` statements.")
    , aDocument(f"""The `ast.match_case` ({diminutive2etymology['match_case']}) object represents individual case clauses within match statements. Contains the pattern to match, optional guard condition, and statements to execute when the pattern matches successfully.""")
    , {'pattern': aDocument("Pattern expression defining what values match this case.")
        , 'guard': aDocument("Optional conditional expression for additional filtering.")
        , 'body': aDocument("List of statements to execute when pattern matches.")}
    , {'matchCase': aDocument("AST object representing a single case clause in match statements.", 'ast.match_case')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.MatchAs"
    , aDocument("Create an `ast.MatchAs` node representing a capture pattern or wildcard.")
    , aDocument(f"""The `ast.MatchAs` ({diminutive2etymology['MatchAs']}) node represents match patterns that capture values or serve as wildcards. This includes bare name patterns like `bicycle` that capture the matched value, "as" patterns like `Point(x, y) as location` that match a pattern and capture the result, and the wildcard pattern `_`.""")
    , {'pattern': aDocument("Optional pattern to match against. When `None`, creates a capture pattern (bare name) if `name` is provided, or wildcard if both are `None`.")
        , 'name': aDocument("Optional identifier to bind the matched value. When `None` and pattern is also `None`, creates the wildcard pattern.")}
    , {'matchAsNode': aDocument("An `ast.MatchAs` node with the specified pattern and name.", 'ast.MatchAs')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.MatchClass"
    , aDocument("Create an `ast.MatchClass` node for matching class instances.")
    , aDocument(f"""The `ast.MatchClass` ({diminutive2etymology['MatchClass']}) node represents patterns that match instances of a specific class, checking both the class type and extracting values from the instance's attributes. This enables structural pattern matching against objects.""")
    , {'cls': aDocument(f"({diminutive2etymology['cls']}) Expression identifying the class to match against.")
        , 'patterns': aDocument("Sequence of pattern nodes for positional matching against class-defined attributes.")
        , 'kwd_attrs': aDocument(f"({diminutive2etymology['kwd_attrs']}) List of attribute names for keyword-style matching.")
        , 'kwd_patterns': aDocument(f"({diminutive2etymology['kwd_patterns']}) Sequence of pattern nodes corresponding to the keyword attributes.")}
    , {'matchClassNode': aDocument("An `ast.MatchClass` node configured for the specified class and patterns.", 'ast.MatchClass')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.MatchMapping"
    , aDocument("Create an `ast.MatchMapping` node for matching dictionary-like objects.")
    , aDocument(f"""The `ast.MatchMapping` ({diminutive2etymology['MatchMapping']}) node represents patterns that match mapping objects like dictionaries, checking for specific keys and extracting their values. The pattern can also capture remaining unmapped keys.""")
    , {'keys': aDocument("Sequence of expression nodes representing the keys to match.")
        , 'patterns': aDocument("Sequence of pattern nodes corresponding to the values associated with each key.")
        , 'rest': aDocument(f"({diminutive2etymology['rest']}) Optional identifier to capture remaining mapping elements not otherwise matched.")}
    , {'matchMappingNode': aDocument("An `ast.MatchMapping` node for the specified key-value patterns and optional rest capture.", 'ast.MatchMapping')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.MatchOr"
    , aDocument("Create an `ast.MatchOr` node for alternative pattern matching.")
    , aDocument(f"""The `ast.MatchOr` ({diminutive2etymology['MatchOr']}) node represents or-patterns that match if any of the alternative subpatterns succeed. The pattern tries each alternative in sequence until one matches or all fail.""")
    , {'patterns': aDocument("Sequence of alternative pattern nodes. The match succeeds if any subpattern matches the subject.")}
    , {'matchOrNode': aDocument("An `ast.MatchOr` node containing the alternative patterns.", 'ast.MatchOr')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.MatchSequence"
    , aDocument("Create an `ast.MatchSequence` node for matching sequences.")
    , aDocument(f"""The `ast.MatchSequence` ({diminutive2etymology['MatchSequence']}) node represents patterns that match sequence objects like lists and tuples, checking both length and element patterns. Supports both fixed-length and variable-length sequence matching.""")
    , {'patterns': aDocument("Sequence of pattern nodes to match against sequence elements. If any pattern is `MatchStar`, enables variable-length matching; otherwise requires exact length match.")}
    , {'matchSequenceNode': aDocument("An `ast.MatchSequence` node for the specified element patterns.", 'ast.MatchSequence')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.MatchSingleton"
    , aDocument("Create an `ast.MatchSingleton` node for matching singleton values.")
    , aDocument(f"""The `ast.MatchSingleton` ({diminutive2etymology['MatchSingleton']}) node represents patterns that match singleton constants by identity rather than equality. This pattern succeeds only if the match subject is the exact same object as the specified constant.""")
    , {'value': aDocument("The singleton constant to match against. Must be `None`, `True`, or `False`. Matching uses identity comparison (`is`) rather than equality comparison (`==`).")}
    , {'matchSingletonNode': aDocument("An `ast.MatchSingleton` node for the specified singleton value.", 'ast.MatchSingleton')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.MatchStar"
    , aDocument("Create an `ast.MatchStar` node for capturing sequence remainder.")
    , aDocument(f"""The `ast.MatchStar` ({diminutive2etymology['MatchStar']}) node represents star patterns that capture remaining elements in variable-length sequence patterns. This enables flexible sequence matching where some elements are specifically matched and others are collected.""")
    , {'name': aDocument("Optional identifier to bind the remaining sequence elements. When `None`, the remaining elements are matched but not captured.")}
    , {'matchStarNode': aDocument("An `ast.MatchStar` node with the specified capture name.", 'ast.MatchStar')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.MatchValue"
    , aDocument("Create an `ast.MatchValue` node for matching literal values.")
    , aDocument(f"""The `ast.MatchValue` ({diminutive2etymology['MatchValue']}) node represents patterns that match by equality comparison against a literal value or expression. The pattern succeeds if the match subject equals the evaluated value expression.""")
    , {'value': aDocument("Expression node representing the value to match against. Typically a constant, name, or attribute access. The expression is evaluated and compared using equality (`==`).")}
    , {'matchValueNode': aDocument("An `ast.MatchValue` node for the specified value expression.", 'ast.MatchValue')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.mod", aDocument(f"Create an abstract `ast.mod` ({diminutive2etymology['mod']}) `object`.", AIgenerated=False)))

listDocstring.append(Docstring(f"{identifierToolClass}.Module"
    , aDocument("Make a module AST object representing complete Python modules with statements and type ignores.")
    , aDocument("""The `ast.Module` object represents entire Python modules as parsed from source files. Contains all top-level statements and tracks type ignore comments for static analysis tools and type checkers.""")
    , {'body': aDocument("List of statements forming the module content.")
        , 'type_ignores': aDocument(f"({diminutive2etymology['type_ignores']}) List of TypeIgnore objects for `# type: ignore` comments.")}
    , {'moduleDefinition': aDocument("AST object representing a complete Python module structure.")}
    , {'Examples': aDocument("""Creates AST equivalent to: x = 42
        ```python
        simpleModule = Make.Module([Make.Assign([Make.Name('x')], Make.Constant(42))])
        ```

        Creates AST equivalent to module with function and assignment
        ```python
        moduleWithFunction = Make.Module([
            Make.FunctionDef('calculate', body=[Make.Return(Make.Constant(100))]),
            Make.Assign([Make.Name('result')], Make.Call(Make.Name('calculate'), []))
        ])
        ```
        """)}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Name"
    , aDocument("Make a name AST `object` for variable and identifier references.")
    , aDocument("""The `ast.Name` `object` represents identifiers like variable names, function names, and class names in Python code. The context parameter determines whether the name is being loaded, stored to, or deleted.""")
    , {'id': aDocument(f"({diminutive2etymology['id']}) The identifier string representing the name.")
    , 'context': aDocument("Expression context specifying how the name is used.")}
    , {'nameReference': aDocument("AST `object` representing an identifier reference with specified context.", 'ast.Name')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.NamedExpr"
    , aDocument("Make a named expression AST `object` for assignment expressions (walrus operator).")
    , aDocument(f"""The `ast.NamedExpr` ({diminutive2etymology['NamedExpr']}) `object` represents assignment expressions using the walrus operator `:=` introduced in Python 3.8. It allows assignment within expressions and is commonly used in comprehensions and conditional statements.""")
    , {'target': aDocument("The `ast.Name` `object` representing the variable being assigned to.")
        , 'value': aDocument("The expression whose value is assigned to the target.")}
    , {'namedExpression': aDocument("AST `object` representing an assignment expression with the walrus operator.")}
    , {'Examples': aDocument("""```python
        # Creates AST equivalent to: `(inventory := len(warehouse)) > 10`
        inventoryCheck = Make.Compare(
            left=Make.NamedExpr(
                target=Make.Name('inventory', ast.Store()),
                value=Make.Call(Make.Name('len'), [Make.Name('warehouse')])
            ),
            ops=[Make.Gt()],
            comparators=[Make.Constant(10)]
        )
        ```
        """, 'ast.NamedExpr')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Nonlocal"
    , aDocument("Create an `ast.Nonlocal` node for nonlocal declarations.")
    , aDocument("""The `Nonlocal` node represents a `nonlocal` statement that declares variables as referring to the nearest enclosing scope that is not global. This is used in nested functions to modify variables from outer scopes.""")
    , {'names': aDocument("List of variable names to declare as nonlocal.")}
    , {'nodeNonlocal': aDocument("The constructed nonlocal declaration node.", 'ast.Nonlocal')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Not"
    , aDocument("Make a logical negation operator representing Python keyword '`not`'.")
    , aDocument("""Class `ast.Not` is a subclass of `ast.unaryop` and represents the logical negation operator keyword '`not`' in Python source code. This operator returns the boolean inverse of its operand's truthiness. Used within `ast.UnaryOp` as the `op` parameter.""")
    , {}
    , {'logicalNegationOperator': aDocument("AST `object` representing the keyword '`not`' logical negation operator for use in `ast.UnaryOp`.", 'ast.Not')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.NotEq"
    , aDocument("'NotEq' meaning 'is ***Not*** ***Eq***ual to', is the `object` representation of Python comparison operator '`!=`'.")
    , aDocument("""`class` `ast.NotEq` is a subclass of `ast.cmpop`, '***c***o***mp***arison ***op***erator', and only used in `class` `ast.Compare`, parameter '`ops`', ***op***erator***s***.""")
    , {}
    , {'inequalityOperator': aDocument("AST `object` representing the '`!=`' inequality comparison operator for use in `ast.Compare`.", 'ast.NotEq')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.NotIn"
    , aDocument("'NotIn', meaning 'is Not ***In***cluded in' or 'does Not have membership In', is the `object` representation of Python keywords '`not in`'.")
    , aDocument("""`class` `ast.NotIn` is a subclass of `ast.cmpop`, '***c***o***mp***arison ***op***erator', and only used in `class` `ast.Compare`, parameter '`ops`', ***op***erator***s***. The Python interpreter declares *This* `object` 'is Not ***In***cluded in' *That* `iterable` if *This* `object` does not match a part of *That* `iterable`.""")
    , {}
    , {'negativeMembershipOperator': aDocument("AST `object` representing the keywords '`not in`' negative membership test operator for use in `ast.Compare`.", 'ast.NotIn')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.operator"
    , aDocument("Create an `ast.operator` node for arithmetic and bitwise operations.")
    , aDocument("""The `operator` method creates operator nodes used in binary operations, unary operations, and comparison operations. These represent the specific operation to be performed.""")
    , {}
    , {'nodeOperator': aDocument("The constructed operator node", 'ast.operator')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.ParamSpec"
    , aDocument("Make a parameter specification type parameter for generic callable types.")
    , aDocument(f"""The `ast.ParamSpec` ({diminutive2etymology['ParamSpec']}) object represents parameter specification type parameters used in generic callable types. Captures both positional and keyword argument signatures for type-safe function composition and higher-order functions.""")
    , {'name': aDocument("Type parameter name as string identifier.")
        , 'default_value': aDocument("Optional default type expression (Python 3.13+).")}
    , {'parameterSpecification': aDocument("AST object representing a parameter specification type parameter.", 'ast.ParamSpec')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Pass"
    , aDocument("Create an `ast.Pass` node for pass statements.")
    , aDocument("""The `Pass` node represents a `pass` statement, which is a null operation that does nothing when executed. It serves as syntactic placeholder where a statement is required but no action is needed.""")
    , {}
    , {'nodePass': aDocument("The constructed pass statement node.", 'ast.Pass')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.pattern"
    , aDocument("Create a base `ast.pattern` node.")
    , aDocument("""Creates a generic `ast.pattern` node that serves as the abstract base for all pattern types in match statements. This method is typically used for creating pattern node instances programmatically when the specific pattern type is determined at runtime.""")
    , {}
    , {'patternNode': aDocument("A base `ast.pattern` node with the specified attributes.", 'ast.pattern')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Raise"
    , aDocument("Create an `ast.Raise` node for raise statements.")
    , aDocument("""The `Raise` node represents a `raise` statement that raises an exception. Can re-raise the current exception, raise a new exception, or raise with an explicit cause chain.""")
    , {'exc': aDocument(f"({diminutive2etymology['exc']}) Optional expression for the exception to raise.")
        , 'cause': aDocument("Optional expression for the exception cause.")}
    , {'nodeRaise': aDocument("The constructed raise statement node.", 'ast.Raise')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Return"
    , aDocument("Make a return statement AST object for function value returns and early exits.")
    , aDocument("""The `ast.Return` object represents return statements that exit functions and optionally provide return values. Used for both value-returning functions and procedures that return None implicitly or explicitly.""")
    , {'value': aDocument("Optional expression providing the return value; None for empty return.")}
    , {'returnStatement': aDocument("AST object representing a function return with optional value.", 'ast.Return')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Set"
    , aDocument("Make a set literal AST `object` for unordered unique element collections.")
    , aDocument("""The `ast.Set` `object` represents set literals using curly brace notation. It creates unordered collections of unique elements with efficient membership testing and set operations.""")
    , {'listElements': aDocument("Sequence of expressions that become set elements.")}
    , {'setLiteral': aDocument("AST `object` representing a set literal with specified unique elements.", 'ast.Set')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.SetComp"
    , aDocument("Make a set comprehension AST `object` for dynamic set construction.")
    , aDocument(f"""The `ast.SetComp` ({diminutive2etymology['SetComp']}) `object` represents set comprehensions that create sets using iterator expressions. It automatically handles uniqueness while providing concise syntax for filtering and transforming collections.""")
    , {'element': aDocument("Expression that generates each element of the resulting set.")
        , 'generators': aDocument("Sequence of `ast.comprehension` objects defining iteration and filtering.")}
    , {'setComprehension': aDocument("AST `object` representing a set comprehension expression.", 'ast.SetComp')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Slice"
    , aDocument("Make a slice AST `object` for sequence slicing operations.")
    , aDocument("""The `ast.Slice` `object` represents slice expressions used with subscription operations to extract subsequences from collections. It supports the full Python slicing syntax with optional start, stop, and step parameters.""")
    , {'lower': aDocument(f"({diminutive2etymology['lower']}) Optional expression for slice start position.")
        , 'upper': aDocument(f"({diminutive2etymology['upper']}) Optional expression for slice end position.")
        , 'step': aDocument("Optional expression for slice step size.")}
    , {'sliceExpression': aDocument("AST `object` representing a slice operation for sequence subscripting.", 'ast.Slice')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Starred"
    , aDocument("Make a starred expression AST `object` for unpacking operations.")
    , aDocument("""The `ast.Starred` `object` represents starred expressions using the `*` operator for unpacking iterables in various contexts like function calls, assignments, and collection literals.""")
    , {'value': aDocument("The expression to be unpacked with the star operator.")
        , 'context': aDocument("Expression context determining how the starred expression is used.")}
    , {'starredExpression': aDocument("AST `object` representing a starred expression for unpacking operations.")}
    , {'Examples': aDocument("""```python
        # Creates AST equivalent to: `*ingredients` in function call
        unpackIngredients = Make.Starred(Make.Name('ingredients'))

        # Creates AST equivalent to: `*remaining` in assignment like `first, *remaining = groceries`
        unpackRemaining = Make.Starred(Make.Name('remaining'), ast.Store())
        ```
        """)}
))

listDocstring.append(Docstring(f"{identifierToolClass}.stmt"
    , aDocument(f"`class` `ast.stmt` ({diminutive2etymology['stmt']}) is the base class for all statement nodes.")
    , Parameters={'**keywordArguments': aDocument("Positional attributes.")}
    , Returns={'nodeStmt': aDocument("The constructed statement node.", 'ast.stmt')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Store"
    , aDocument("Make a store context for assigning values to expressions.")
    , aDocument("""The `ast.Store` context indicates expressions are assignment targets receiving new values. Used in assignments, loop targets, and function parameters where expressions store rather than load values.""")
    , {}
    , {'storeContext': aDocument("AST context object indicating value assignment operations.")}
    , {'Examples': aDocument("""Creates AST equivalent to assignment: bicycle.wheel = newWheel
        ```python
        wheelAssignment = Make.Attribute(Make.Name('bicycle'), 'wheel', Make.Store())
        ```
        """, 'ast.Store')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Subscript"
    , aDocument("Make a subscript AST `object` for indexing and slicing operations.")
    , aDocument("""The `ast.Subscript` `object` represents subscription operations using square brackets for indexing, slicing, and key access in dictionaries and other subscriptable objects.""")
    , {'value': aDocument("The expression being subscripted (e.g., list, dict, string).")
        , 'slice': aDocument("The subscript expression, which can be an index, slice, or key.")
        , 'context': aDocument("Expression context for how the subscript is used.")}
    , {'subscriptExpression': aDocument("AST `object` representing a subscription operation with brackets.", 'ast.Subscript')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.TemplateStr"
    , aDocument("Make a template string AST `object`.")
    , aDocument("""The `ast.TemplateStr` `object` represents a template string. It consists of a sequence of components which can be constant strings or interpolations.""")
    , {'values': aDocument("A sequence of nodes (typically `ast.Constant` or `ast.Interpolation`) forming the template string.", 'Sequence[ast.expr]')}
    , {'templateString': aDocument("AST `object` representing a template string.", 'ast.TemplateStr')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Try"
    , aDocument("Make a try-except statement AST `object` for exception handling and resource cleanup.")
    , aDocument("""The `ast.Try` `object` represents `try-except` statements that handle exceptions and provide cleanup mechanisms. It supports multiple exception handlers, optional else clauses, and finally blocks for guaranteed cleanup.""")
    , {'body': aDocument("Sequence of statements in the try block that may raise exceptions.")
        , 'handlers': aDocument("List of exception handler objects that catch and process specific exception types or patterns.")
        , 'orelse': aDocument(f"({diminutive2etymology['orElse']}) Optional statements executed when the try block completes without raising exceptions.")
        , 'finalbody': aDocument(f"({diminutive2etymology['finalbody']}) Optional statements always executed for cleanup, regardless of whether exceptions occurred.")}
    , {'tryStatement': aDocument("AST `object` representing an exception handling statement with optional cleanup.", 'ast.Try')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.TryStar"
    , aDocument("Make a try-except* statement AST `object` for exception group handling.")
    , aDocument(f"""The `ast.TryStar` ({diminutive2etymology['TryStar']}) `object` represents `try-except*` statements introduced in Python 3.11 for handling exception groups. It enables catching and processing multiple related exceptions that occur simultaneously.""")
    , {'body': aDocument("Sequence of statements in the try block that may raise exception groups.")
        , 'handlers': aDocument("List of exception handler objects that catch and process specific exception types within exception groups.")
        , 'orelse': aDocument(f"({diminutive2etymology['orElse']}) Optional statements executed when the try block completes without raising exceptions.")
        , 'finalbody': aDocument(f"({diminutive2etymology['finalbody']}) Optional statements always executed for cleanup, regardless of whether exception groups occurred.")}
    , {'tryStarStatement': aDocument("AST `object` representing an exception group handling statement with optional cleanup.", 'ast.TryStar')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Tuple"
    , aDocument("Make a tuple literal AST `object` for ordered immutable collections.")
    , aDocument("""The `ast.Tuple` `object` represents tuple literals using parentheses or comma separation. Tuples are immutable, ordered collections often used for multiple assignments and function return values.""")
    , {'listElements': aDocument("Sequence of expressions that become tuple elements.")
        , 'context': aDocument("Expression context for how the tuple is used.")}
    , {'tupleLiteral': aDocument("AST `object` representing a tuple literal with specified elements.", 'ast.Tuple')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.type_ignore"
    , aDocument(f"`class` `ast.type_ignore` ({diminutive2etymology['type_ignore']}) is the base class for `ast.TypeIgnore`.")
))

listDocstring.append(Docstring(f"{identifierToolClass}.type_param"
    , aDocument("Abstract type parameter base for generic type constructs.")
    , aDocument(f"""The `ast.type_param` ({diminutive2etymology['type_param']}) object serves as the abstract base for type parameters including TypeVar, ParamSpec, and TypeVarTuple. Provides common functionality for generic type definitions in classes, functions, and type aliases.""")
    , {}
    , {'typeParameter': aDocument("Abstract AST object representing the base of type parameter hierarchy.", 'ast.type_param')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.TypeAlias"
    , aDocument("Make a type alias definition AST object for `type` statement declarations.")
    , aDocument(f"""The `ast.TypeAlias` ({diminutive2etymology['TypeAlias']}) object represents type alias definitions using the `type` statement syntax. Associates a name with a type expression, supporting generic type parameters for flexible type definitions.""")
    , {'name': aDocument("Name expression (typically ast.Name) for the alias identifier."),
        'type_params': aDocument(f"({diminutive2etymology['type_params']}) List of type parameters for generic aliases."),
        'value': aDocument("Type expression defining what the alias represents.")}
    , {'typeAliasDefinition': aDocument("AST object representing a complete type alias declaration.", 'ast.TypeAlias')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.TypeIgnore"
    , aDocument("Make a type ignore comment AST object for `# type: ignore` directives.")
    , aDocument(f"""The `ast.TypeIgnore` ({diminutive2etymology['TypeIgnore']}) object represents `# type: ignore` comments that instruct static type checkers to skip type analysis for specific lines. Includes optional tags for categorizing different types of ignores.""")
    , {'lineno': aDocument(f"({diminutive2etymology['lineno']}) Line number where the ignore comment appears."),
        'tag': aDocument("Optional string tag for categorizing the ignore (e.g., '[assignment]').")}
    , {'typeIgnoreDirective': aDocument("AST object representing a type checker ignore comment.")}
    , {'Examples': aDocument("""Creates AST equivalent to: # type: ignore (on line 42)
        ```python
        simpleIgnore = Make.TypeIgnore(42, '')
        ```

        Creates AST equivalent to: # type: ignore[assignment] (on line 15)
        ```python
        taggedIgnore = Make.TypeIgnore(15, '[assignment]')
        ```
        """)}
))

listDocstring.append(Docstring(f"{identifierToolClass}.TypeVar"
    , aDocument("Make a type variable parameter for generic types with optional bounds and defaults.")
    , aDocument(f"""The `ast.TypeVar` ({diminutive2etymology['TypeVar']}) object represents type variable parameters used in generic classes, functions, and type aliases. Supports type bounds, constraints, and default values for flexible generic programming.""")
    , {'name': aDocument("Type variable name as string identifier."),
        'bound': aDocument("Optional type expression constraining allowed types."),
        'default_value': aDocument("Optional default type expression (Python 3.13+).")}
    , {'typeVariable': aDocument("AST object representing a type variable with optional constraints.", 'ast.TypeVar')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.TypeVarTuple"
    , aDocument("Make a type variable tuple for variadic generic types.")
    , aDocument(f"""The `ast.TypeVarTuple` ({diminutive2etymology['TypeVarTuple']}) object represents type variable tuples used for variadic generic types that accept variable numbers of type arguments. Enables generic types that work with arbitrary-length type sequences.""")
    , {'name': aDocument("Type variable tuple name as string identifier."),
        'default_value': aDocument("Optional default type tuple expression (Python 3.13+).")}
    , {'typeVariableTuple': aDocument("AST object representing a variadic type variable.", 'ast.TypeVarTuple')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.UAdd"
    , aDocument("Unary addition operator representing Python '`+`' operator.")
    , aDocument(f"""Class `ast.UAdd` ({diminutive2etymology['UAdd']}) is a subclass of `ast.unaryop` and represents the unary positive operator '`+`' in Python source code. This operator explicitly indicates a positive numeric value. Used within `ast.UnaryOp` as the `op` parameter.""")
    , {}
    , {'unaryPositiveOperator': aDocument("AST `object` representing the '`+`' unary positive operator for use in `ast.UnaryOp`.", 'ast.UAdd')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.unaryop"
    , aDocument("Abstract unary operator `object` for use in AST construction.")
    , aDocument(f"""Class `ast.unaryop` ({diminutive2etymology['unaryop']}) is the base for all unary operators in Python's AST. It serves as the abstract parent for specific unary operators: `ast.Invert`, `ast.Not`, `ast.UAdd`, `ast.USub`. This factory method makes a generic unary operator `object` that can be used in the antecedent-action pattern with visitor classes.

        Unlike `ast.cmpop` which handles binary comparison operations between two operands, `ast.unaryop` represents operators that act on a single operand. Both serve as abstract base classes but for different categories of operations: `ast.cmpop` for comparisons and `ast.unaryop` for unary transformations.""")
    , {}
    , {'unaryOperator': aDocument("Abstract unary operator `object` that serves as the base `class` for all Python unary operators in AST structures.")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.UnaryOp"
    , aDocument("Unary operation AST `object` for single-operand operations.")
    , aDocument(f"""The `ast.UnaryOp` ({diminutive2etymology['UnaryOp']}) `object` represents unary operations that take a single operand, such as negation, logical not, bitwise inversion, and positive sign operations.""")
    , {'op': aDocument(f"({diminutive2etymology['op']}) The unary operator like `ast.UAdd()`, `ast.USub()`, `ast.Not()`, `ast.Invert()`."),
        'operand': aDocument("The expression that the unary operator is applied to.")}
    , {'unaryOperation': aDocument(f"({diminutive2etymology['UnaryOp']}) AST `object` representing a unary operation on a single expression.", 'ast.UnaryOp')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.USub"
    , aDocument("Unary subtraction operator representing Python '`-`' operator.")
    , aDocument(f"""Class `ast.USub` ({diminutive2etymology['USub']}) is a subclass of `ast.unaryop` and represents the unary negation operator '`-`' in Python source code. This operator makes the arithmetic negative of its operand. Used within `ast.UnaryOp` as the `op` parameter.""")
    , {}
    , {'unaryNegativeOperator': aDocument("AST `object` representing the '`-`' unary negation operator for use in `ast.UnaryOp`.", 'ast.USub')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.While"
    , aDocument("Make a while loop AST `object` for condition-based iteration.")
    , aDocument("""The `ast.While` `object` represents `while` loops that repeatedly execute a block of statements as long as a test condition remains True. It supports optional else clauses that execute when the loop exits normally.""")
    , {'test': aDocument("The boolean expression evaluated before each iteration to determine whether the loop should continue executing."),
        'body': aDocument("Sequence of statements executed repeatedly while the test condition is True."),
        'orelse': aDocument(f"({diminutive2etymology['orElse']}) Optional statements executed when the loop exits normally without encountering a break statement.")}
    , {'whileLoop': aDocument("AST `object` representing a condition-based iteration statement.", 'ast.While')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.With"
    , aDocument("Make a context manager statement AST `object` for resource management and cleanup.")
    , aDocument("""The `ast.With` `object` represents `with` statements that manage resources using context managers. These ensure proper setup and cleanup of resources like files, database connections, or locks.""")
    , {'items': aDocument("Sequence of context manager items, each specifying a context manager expression and optional variable binding for the managed resource."),
        'body': aDocument("Sequence of statements executed within the context manager scope.")}
    , {'withStatement': aDocument("AST `object` representing a context manager statement for resource management.", 'ast.With')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.withitem"
    , aDocument("Make a context manager item AST object for individual items in `with` statements.")
    , aDocument(f"""The `ast.withitem` ({diminutive2etymology['withitem']}) object represents individual context manager specifications within `with` statements. Contains the context expression and optional variable binding for the context manager's return value.""")
    , {'context_expr': aDocument(f"({diminutive2etymology['context_expr']}) Expression providing the context manager object."),
        'optional_vars': aDocument(f"({diminutive2etymology['optional_vars']}) Optional variable expression for `as` binding.")}
    , {'contextItem': aDocument("AST object representing a single context manager in with statements.", 'ast.withitem')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Yield"
    , aDocument("Make a yield expression AST `object` for generator function values.")
    , aDocument(f"""The `ast.Yield` ({diminutive2etymology['Yield']}) `object` represents yield expressions that produce values in generator functions. It suspends function execution and yields a value to the caller, allowing resumption from the same point.""")
    , {'value': aDocument("Optional expression to yield; None yields None value.")}
    , {'yieldExpression': aDocument(f"({diminutive2etymology['Yield']}) AST `object` representing a yield expression for generator functions.", 'ast.Yield')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.YieldFrom"
    , aDocument("Make a yield from expression AST `object` for delegating to sub-generators.")
    , aDocument(f"""The `ast.YieldFrom` ({diminutive2etymology['YieldFrom']}) `object` represents `yield from` expressions that delegate generator execution to another iterable or generator. It provides efficient sub-generator delegation introduced in Python 3.3.""")
    , {'value': aDocument("The iterable or generator expression to delegate to.")}
    , {'yieldFromExpression': aDocument(f"({diminutive2etymology['YieldFrom']}) AST `object` representing a yield from expression for generator delegation.", 'ast.YieldFrom')}
))

for subclass in ast.boolop.__subclasses__():
    listDocstring.append(Docstring(f"{identifierToolClass}.{subclass.__name__}"  # noqa: PERF401
        , aDocument(f"Identical to the `ast` ({diminutive2etymology['ast']}) class but with a method, `join()`, that 'joins' expressions using the `ast.BoolOp` ({diminutive2etymology['BoolOp']}) class.", AIgenerated=False)))

for subclass in ast.operator.__subclasses__():
    listDocstring.append(Docstring(f"{identifierToolClass}.{subclass.__name__}"  # noqa: PERF401
        , aDocument(f"Identical to the `ast` ({diminutive2etymology['ast']}) class but with a method, `join()`, that 'joins' expressions using the `ast.BinOp` ({diminutive2etymology['BinOp']}) class.", AIgenerated=False)))

for data in listDocstring:
    docstrings[identifierToolClass][data.identifier.removeprefix(f"{identifierToolClass}.")] = Make.Expr(Make.Constant(make1docstring(data, firstIndent=2)))
del listDocstring

data = Docstring(identifierToolClass
    , aDocument("Create a `class` `ast.AST` `object` or an `ast.AST` subclass `object`.", AIgenerated=False)
    , aDocument(f"I describe `keywordArguments` of `{identifierToolClass}` methods here.", AIgenerated=False)
    , {'col_offset': aDocument(f"({diminutive2etymology['col_offset']}) Position information specifying the column where an AST object begins.", 'int', AIgenerated=False)
    , 'end_col_offset': aDocument(f"({diminutive2etymology['end_col_offset']}) Position information specifying the column where an AST object ends.", '(int | None) | int', AIgenerated=False)
    , 'end_lineno': aDocument(f"({diminutive2etymology['end_lineno']}) Position information specifying the line number where an AST object ends.", '(int | None) | int', AIgenerated=False)
    , 'level': aDocument(f"({diminutive2etymology['level']}) An absolute import is 'level' 0. A relative import is `level` deep.", 'int = 0', AIgenerated=False)
    , 'lineno': aDocument(f"({diminutive2etymology['lineno']}) Position information manually specifying the line number where an AST object begins.", 'int', AIgenerated=False)
    , 'type_comment': aDocument(f"({diminutive2etymology['type_comment']}) Optional string with the type annotation as a comment or `# type: ignore`.", 'str', AIgenerated=False)}
    , categories={'Notes': aDocument(f"""Every non-deprecated subclass of `ast.AST` ({diminutive2etymology['AST']}), has a corresponding method in `Make`, and for each `class`, you can set the value of each attribute. But, what is an "attribute"? In the `ast` universe, one word may have many different meanings, and if you want to avoid confusion, you should pay close attention to capitalization, leading underscores, and context. In Python, an "attribute" is a property of an `object`. In `class` `Make`, when you create an `ast.AST` subclass `object`, you can set the value of any attribute of that `object`. The `ast` universe divides attributes into two categories, `_attributes` and `_fields` (or `_field*`).

    The attributes in category `_attributes` are `lineno` ({diminutive2etymology['lineno']}), `col_offset` ({diminutive2etymology['col_offset']}), `end_lineno` ({diminutive2etymology['end_lineno']}), and `end_col_offset` ({diminutive2etymology['end_col_offset']}). These attributes of an `ast` `object` represent the physical location of the text when rendered as Python code. With abstract syntax trees, as opposed to concrete syntax trees for example, you rarely need to work directly with physical locations, therefore `_attributes` are almost always relegated to `**keywordArguments` in `Make` methods. For a counter example, see `Make.TypeIgnore` ({diminutive2etymology['TypeIgnore']}), for which `lineno` is a named parameter.

    In an attempt to distinguish the attributes of `ast.AST` subclasses that are not in the category `_attributes` from the four attributes in the category `_attributes`, all other attributes of `ast.AST` subclasses are in category `_fields` (or sometimes, category `_field*`, such as `_field_types`).

    You probably want to try to avoid confusing these concepts and categories with similarly named things, including `ast.Attribute`, `ast.Attribute.attr` ({diminutive2etymology['attr']}), `getattr`, `setattr`, `ast.MatchClass.kwd_attrs` ({diminutive2etymology['kwd_attrs']}), and `_Attributes` (no, really, it's a thing)."""
, AIgenerated=False)}
)
docstrings[settingsManufacturing.identifiers[identifierToolClass]][settingsManufacturing.identifiers[identifierToolClass]] = Make.Expr(Make.Constant(make1docstring(data, firstIndent=1)))
del data

data = Docstring(settingsManufacturing.identifiers['boolopJoinMethod']
    , aDocument("'Join' expressions with a boolean operator.")
    , aDocument("This private method provides the core logic for boolean operator joining used by `And.join()` and `Or.join()` methods. "
        "It handles edge cases like empty sequences and single expressions while creating properly nested `ast.BoolOp` structures for multiple expressions. "
        "If you are looking for public join functionality, use the specific boolean operator classes (`Make.And.join()`, `Make.Or.join()`) instead of this internal method.")
    , {'ast_operator': aDocument("The boolean operator type (`ast.And` or `ast.Or`) to use for joining.", 'type[ast.boolop]')
        , 'expressions': aDocument("Sequence of expressions to join with the boolean operator.", 'Sequence[ast.expr]')}
    , {'joinedExpression': aDocument("Single expression representing the joined boolean operation, or the original expression if only one provided.", 'ast.expr')}
)
docstrings[settingsManufacturing.identifiers[identifierToolClass]][settingsManufacturing.identifiers['boolopJoinMethod']] = Make.Expr(Make.Constant(make1docstring(data, firstIndent=2)))
del data

data = Docstring('join_boolop'
    , aDocument(f"Make a single `ast.expr` ({diminutive2etymology['expr']}) from a `Sequence` of `ast.expr` by creating an `ast.BoolOp` ({diminutive2etymology['BoolOp']}) `object` that logically 'joins' the `Sequence`.", AIgenerated=False)
    , aDocument(f"Like str.join() ({diminutive2etymology['str']}) but for AST ({diminutive2etymology['AST']}) expressions.", AIgenerated=False)
    , {'expressions': aDocument("Collection of expressions to join.", 'Sequence[ast.expr]', AIgenerated=False)
        , '**keywordArguments': aDocument("", 'ast_attributes', AIgenerated=False)}
    , {'joinedExpression': aDocument("Single expression representing the joined expressions.", 'ast.expr', AIgenerated=False)}
    , {'Examples': aDocument("""```python
            # Instead of manually constructing ast.BoolOp structures:
            ast.BoolOp(
                op=ast.And(),
                values=[ast.Name('Lions'), ast.Name('tigers'), ast.Name('bears')]
            )

            # Simply use:
            astToolkit.And.join([ast.Name('Lions'), ast.Name('tigers'), ast.Name('bears')])

            # Both produce the same AST structure but the join() method eliminates the manual construction.
            ```
        """, AIgenerated=False)}
)
docstrings[settingsManufacturing.identifiers[identifierToolClass]]['join_boolop'] = Make.Expr(Make.Constant(make1docstring(data, firstIndent=3)))
del data

data = Docstring('_operatorJoinMethod'
    , aDocument("'Join' expressions with a binary operator.")
    , aDocument("This private method provides the core logic for binary operator joining used by operator classes like `Add.join()`, `BitOr.join()`, etc. "
        "It creates left-associative nested `ast.BinOp` structures by chaining expressions from left to right. "
        "If you are looking for public join functionality, use the specific operator classes (`Make.Add.join()`, `Make.BitOr.join()`, etc.) instead of this internal method.")
    , {'ast_operator': aDocument("The binary operator type (like `ast.Add`, `ast.BitOr`) to use for joining.", 'type[ast.operator]')
        , 'expressions': aDocument("Collection of expressions to join with the binary operator.", 'Iterable[ast.expr]')}
    , {'joinedExpression': aDocument("Single expression representing the left-associative chained binary operations, or empty string constant if no expressions provided.", 'ast.expr')}
)
docstrings[settingsManufacturing.identifiers[identifierToolClass]]['_operatorJoinMethod'] = Make.Expr(Make.Constant(make1docstring(data, firstIndent=2)))
del data

data = Docstring('join_operator'
    , aDocument(f"Make a single `ast.expr` ({diminutive2etymology['expr']}) from a `Sequence` of `ast.expr` by creating nested `ast.BinOp` ({diminutive2etymology['BinOp']}) `object` that are logically 'joined' by the `ast.operator` subclass.", AIgenerated=False)
    , aDocument(f"Like str.join() ({diminutive2etymology['str']}) but for AST ({diminutive2etymology['AST']}) expressions.", AIgenerated=False)
    , {'expressions': aDocument("Collection of expressions to join.", 'Iterable[ast.expr]', AIgenerated=False)
        , '**keywordArguments': aDocument("", 'ast_attributes', AIgenerated=False)}
    , {'joinedExpression': aDocument("Single expression representing the joined expressions.", 'ast.expr', AIgenerated=False)}
    , {'Examples': aDocument("""```python
            # Instead of manually constructing nested ast.BinOp structures:
            ast.BinOp(
                left=ast.BinOp(
                    left=ast.Name('Crosby')
                    , op=ast.BitOr()
                    , right=ast.Name('Stills'))
                , op=ast.BitOr()
                , right=ast.Name('Nash')
            )

            # Simply use:
            astToolkit.BitOr().join([ast.Name('Crosby'), ast.Name('Stills'), ast.Name('Nash')])

            # Both produce the same AST structure but the join() method eliminates the manual nesting.
            ```
        """, AIgenerated=False)}
)
docstrings[settingsManufacturing.identifiers[identifierToolClass]]['join_operator'] = Make.Expr(Make.Constant(make1docstring(data, firstIndent=3)))
del data
