"""A warehouse for docstrings added to manufactured ast tools.

NOTE Use special indentation in this file.
    1. The generated files use spaces, not tabs, so use spaces here.
    2. As of this writing, I only know how to _manually_ align the indentation of the docstrings with the associated code. So,
        indent one or two levels as appropriate.
"""
from astToolFactory import settingsManufacturing
from astToolFactory.documentation import aDocument, diminutive2etymology, Docstring, docstrings, make1docstring
from astToolkit import Make
import ast

# NOTE "ClassDefIdentifier": {'attribute': "'attributeType' = 'defaultValue'"}

listDocstring: list[Docstring] = []

identifierToolClass: str = settingsManufacturing.identifiers['Make']

listDocstring.append(Docstring(f"{identifierToolClass}.alias"
    , aDocument("Import alias AST `object` representing name mapping in import statements.")
    , aDocument("""The `ast.alias` `object` represents name mappings used in `import` and `from ... import` statements. It handles both direct imports (`import math`) and aliased imports (`import re as regex`).""")
    , {'name' : aDocument("The actual module, class, or function name being imported.")
        , 'asName' : aDocument(f"Optional {diminutive2etymology['asName']} to use instead of the original name. This corresponds to `ast.alias.asname`.")}
    , {'importAlias' : aDocument("AST `object` representing an import name mapping with optional aliasing.", 'ast.alias')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.AnnAssign"
    , aDocument("Annotated assignment AST `object` for type-annotated variable assignments.")
    , aDocument(f"""The `ast.AnnAssign` ({diminutive2etymology['AnnAssign']}) `object` represents variable assignments with type annotations, such as `name: int = 42` or `config: dict[str, Any]`. This is the preferred form for annotated assignments in modern Python code.""")
    , {'target': aDocument("The assignment target, which must be a simple name, attribute access, or subscript operation that can receive the annotated assignment.")
        , 'annotation': aDocument("The type annotation expression specifying the variable's expected type.")
        , 'value': aDocument("Optional initial value expression for the annotated variable.")}
    , {'annotatedAssignment': aDocument("AST `object` representing a type-annotated variable assignment.", 'ast.AnnAssign')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.arg"
    , aDocument("Make an `ast.arg` object representing individual arguments in function signatures.")
    , aDocument(f"""The `ast.arg` ({diminutive2etymology['ast']}) object represents a single parameter in function definitions, including positional, keyword-only, and special parameters like `*arguments` and `**keywordArguments`. Contains the parameter name and optional type annotation.""")
    , {'Buffalo_buffalo_Buffalo_buffalo_buffalo_buffalo_Buffalo_buffalo': aDocument("Parameter name as string. This corresponds to `ast.arg.arg`; and in an `ast.FunctionDef` ({diminutive2etymology['FunctionDef']}) `object`, it corresponds to `ast.FunctionDef.args.args[n].arg.arg`, which has the same semantic value as `Buffalo_buffalo_Buffalo_buffalo_buffalo_buffalo_Buffalo_buffalo`.")
        , 'annotation': aDocument("Optional type annotation expression for the parameter.")}
    , {'argumentDefinition': aDocument("AST object representing a single function parameter with optional typing.", 'ast.arg')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.arguments"
    , aDocument("Make a function signature AST object containing all parameter specifications.")
    , aDocument("""The `ast.arguments` object represents the complete parameter specification for function definitions, organizing different parameter types including positional-only, regular, keyword-only, variadic, and default values.""")
    , {'posonlyargs': aDocument(f"({diminutive2etymology['posonlyargs']}) List of positional-only parameters (before /).")
        , 'list_arg': aDocument(f"({diminutive2etymology['list_arg']}) List of positional parameters. This corresponds to `ast.arguments.args`.")
        , 'vararg': aDocument(f"({diminutive2etymology['vararg']}) Single parameter for *arguments variadic arguments.")
        , 'kwonlyargs': aDocument(f"({diminutive2etymology['kwonlyargs']}) List of keyword-only parameters (after * or *arguments).")
        , 'kw_defaults': aDocument(f"({diminutive2etymology['kw_defaults']}) Default values for keyword-only parameters; None indicates required.")
        , 'kwarg': aDocument(f"({diminutive2etymology['kwarg']}) Single parameter for '**keywordArguments' keyword arguments.")
        , 'defaults': aDocument("Default values for regular positional parameters.")}
    , {'functionSignature': aDocument("AST object representing complete function parameter specification.", 'ast.arguments')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Assert"
    , aDocument("Create an `ast.Assert` node for assertion statements.")
    , aDocument("""The `Assert` node represents an `assert` statement that evaluates a test expression and optionally raises `AssertionError` with a message if the test fails. This is primarily used for debugging and testing purposes.""")
    , {'test': aDocument("Expression to evaluate for truthiness.")
        , 'msg': aDocument(f"({diminutive2etymology['msg']}) Optional expression for the assertion error message.")}
    , {'nodeAssert': aDocument("The constructed assertion node.", 'ast.Assert')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.AST"
    , aDocument("Make a base AST node object representing the abstract syntax tree foundation.")
    , aDocument("""The `ast.AST` object serves as the base class for all AST node types in Python's abstract syntax tree. This method creates a minimal AST instance, though in practice you will typically use specific node type factories like `Make.Name()`, `Make.Call()`, etc. Most users seeking AST node creation should use the specific factory methods for concrete node types rather than this base AST constructor.""")
    , {}
    , {'baseNode': aDocument("The fundamental AST object from which all other nodes inherit.", 'ast.AST')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Assign"
    , aDocument("Make an assignment AST `object` for variable assignments without type annotations.")
    , aDocument("""The `ast.Assign` `object` represents traditional variable assignments like `x = 5`, `a = b = c`, or `items[0] = newValue`. It supports multiple assignment targets and complex assignment patterns.""")
    , {'targets': aDocument("Sequence of assignment targets that will receive the value. Multiple targets enable chained assignments like `a = b = value`.")
        , 'value': aDocument("The expression whose result will be assigned to all targets.")}
    , {'assignment': aDocument("AST `object` representing a variable assignment operation.", 'ast.Assign')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.AsyncFor"
    , aDocument("Asynchronous for loop AST `object` for iterating over async iterables.")
    , aDocument(f"""The `ast.AsyncFor` ({diminutive2etymology['AsyncFor']}) `object` represents `async for` loops that iterate over asynchronous iterators and async generators. These loops can only exist within async functions and automatically handle await operations.""")
    , {'target': aDocument("The loop variable that receives each item from the async iterable.")
        , 'iter': aDocument(f"({diminutive2etymology['iter']}) The asynchronous iterable expression being iterated over.")
        , 'body': aDocument("Sequence of statements executed for each iteration of the async loop.")
        , 'orelse': aDocument(f"({diminutive2etymology['orElse']}) Optional statements executed when the loop completes normally without encountering a break statement.")}
    , {'asyncForLoop': aDocument("AST `object` representing an asynchronous for loop construct.", 'ast.AsyncFor')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.AsyncFunctionDef"
    , aDocument("Asynchronous function definition AST object for `async def` declarations.")
    , aDocument(f"""The `ast.AsyncFunctionDef` ({diminutive2etymology['AsyncFunctionDef']}) object represents asynchronous function definitions using the `async def` syntax. Supports coroutines, async generators, and other asynchronous operations with await expressions.""")
    , {'name': aDocument("Function name as string identifier.")
        , 'args': aDocument("Function parameter specification.")
        , 'body': aDocument("List of statements forming the function body.")
        , 'decorator_list': aDocument("List of decorator expressions applied to function.")
        , 'returns': aDocument(f"({diminutive2etymology['returns']}) Optional return type annotation expression.")
        , 'type_params': aDocument(f"({diminutive2etymology['type_params']}) List of type parameters for generic functions (Python 3.12+).")}
    , {'asyncFunction': aDocument("AST object representing an asynchronous function definition.", 'ast.AsyncFunctionDef')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.AsyncWith"
    , aDocument("Asynchronous context manager AST `object` for async resource management.")
    , aDocument(f"""The `ast.AsyncWith` ({diminutive2etymology['AsyncWith']}) `object` represents `async with` statements that manage asynchronous context managers. These ensure proper setup and cleanup of async resources like database connections or file handles.""")
    , {'items': aDocument("Sequence of context manager items, each specifying an async context manager and optional variable binding for the managed resource.")
        , 'body': aDocument("Sequence of statements executed within the async context manager scope.")}
    , {'asyncWithStatement': aDocument("AST `object` representing an asynchronous context manager statement.", 'ast.AsyncWith')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Attribute"
    , aDocument("Attribute access AST `object` representing dot notation in Python code.")
    , aDocument("""The `ast.Attribute` `object` represents attribute access using dot notation, such as `object.attribute` or chained access like `module.class.method`. This method supports chaining multiple attributes by passing additional attribute names.""")
    , {'value': aDocument("The base expression before the first dot.")
        , 'attribute': aDocument("One or more attribute names to chain together with dot notation.")
        , 'context': aDocument("Are you loading from, storing to, or deleting the `ast.Attribute`? Values may be `ast.Load()`, `ast.Store()`, or `ast.Del()`, meaning 'Delete' the `ast.Attribute`. `context` corresponds to `ast.Attribute.ctx`.")}
    , {'attributeAccess': aDocument("AST `object` representing attribute access with potential chaining.", 'ast.Attribute')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.AugAssign"
    , aDocument("Augmented assignment AST `object` for compound assignment operations.")
    , aDocument(f"""The `ast.AugAssign` ({diminutive2etymology['AugAssign']}) `object` represents augmented assignment operators like `+=`, `-=`, `*=`, `/=`, and others that combine an operation with assignment. These provide concise syntax for modifying variables in-place.""")
    , {'target': aDocument("The assignment target being modified, which must be a name, attribute access, or subscript that supports in-place modification.")
        , 'op': aDocument(f"({diminutive2etymology['op']}) The binary operator defining the augmentation operation, such as `ast.Add()` for `+=` or `ast.Mult()` ({diminutive2etymology['Mult']}) for `*=`.")
        , 'value': aDocument("The expression whose result will be combined with the target using the specified operator.")}
    , {'augmentedAssignment': aDocument("AST `object` representing a compound assignment operation.", 'ast.AugAssign')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Await"
    , aDocument("Await expression AST `object` for asynchronous operations.")
    , aDocument(f"""The `ast.Await` ({diminutive2etymology['Await']}) `object` represents the keyword `await` used with asynchronous expressions in Python. It can only be used within async functions and suspends execution until the awaited coroutine completes.""")
    , {'value': aDocument("The expression to await, typically a coroutine or awaitable `object`.")}
    , {'awaitExpression': aDocument("AST `object` representing an await expression for asynchronous code.", 'ast.Await')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.BinOp"
    , aDocument("Make a binary operation AST `object` representing operators between two expressions.")
    , aDocument(f"""The `ast.BinOp` ({diminutive2etymology['BinOp']}) `object` represents binary operations like addition, subtraction, multiplication, and other two-operand operations. The operation type is determined by the `op` parameter using specific operator classes.""")
    , {'left': aDocument("The left-hand operand expression.")
        , 'op': aDocument("The binary operator, such as `ast.Add()`, `ast.Sub()`, `ast.Mult()`, etc.")
        , 'right': aDocument("The right-hand operand expression.")}
    , {'binaryOperation': aDocument("AST `object` representing a binary operation between two expressions.", 'ast.BinOp')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.boolop"
    , aDocument("Make a base boolean operator abstract class for logical operations.")
    , aDocument(f"""The `ast.boolop` ({diminutive2etymology['boolop']}) class serves as the abstract base for boolean operators like `ast.And` and `ast.Or`. This method creates a minimal boolop instance, though in practice you will typically use specific boolean operator factories like `Make.And()`, `Make.Or()`, or their join methods.

        Most users seeking boolean operation creation should use the specific operator classes or `Make.BoolOp()` rather than this abstract base constructor.""")
    , {}
    , {'baseBooleanOperator': aDocument(f"({diminutive2etymology['boolop']}) AST `object` representing a base boolean operator.")}
))

listDocstring.append(Docstring(f"{identifierToolClass}.BoolOp"
    , aDocument("Make a boolean operation AST `object` for logical operations with multiple operands.")
    , aDocument(f"""The `ast.BoolOp` ({diminutive2etymology['BoolOp']}) `object` represents boolean operations like keywords `and` and `or` that can operate on multiple expressions. Unlike binary operators, boolean operations can chain multiple values together efficiently.""")
    , {'op': aDocument(f"({diminutive2etymology['boolop']}) The boolean operator, either `ast.And()` or `ast.Or()`.")
        , 'values': aDocument("Sequence of expressions to combine with the boolean operator.")}
    , {'booleanOperation': aDocument(f"({diminutive2etymology['BoolOp']}) AST `object` representing a boolean operation with multiple operands.", 'ast.BoolOp')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Break"
    , aDocument("Create an `ast.Break` node for break statements.")
    , aDocument("""The `Break` node represents a `break` statement that terminates the nearest enclosing loop. Can only be used within loop constructs.""")
    , {}
    , {'nodeBreak': aDocument("The constructed break statement node.", 'ast.Break')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Call"
    , aDocument("Make a function call AST `object` representing function invocation with arguments.")
    , aDocument("""The `ast.Call` `object` represents function calls, method calls, and constructor invocations. It supports both positional and keyword arguments and handles various calling conventions including unpacking operators.""")
    , {'callee': aDocument("The callable expression, typically a function name or method access.")
        , 'listParameters': aDocument("Sequence of positional argument expressions.")
        , 'list_keyword': aDocument("Sequence of keyword arguments as `ast.keyword`.")}
    , {'functionCall': aDocument("AST `object` representing a function call with specified arguments.", 'ast.Call')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.ClassDef"
    , aDocument("Make a class definition AST object for `class` declarations with inheritance and metadata.")
    , aDocument("""The `ast.ClassDef` object represents class definitions including base classes, metaclass specifications, decorators, and the class body. Supports both traditional and modern Python class features.""")
    , {'name': aDocument("Class name as string identifier.")
        , 'bases': aDocument("List of base class expressions for inheritance.")
        , 'keywords': aDocument(f"({diminutive2etymology['list_keyword']}) including metaclass specifications.")
        , 'body': aDocument("List of statements forming the class body.")
        , 'decorator_list': aDocument("List of decorator expressions applied to class.")
        , 'type_params': aDocument(f"({diminutive2etymology['type_params']}) List of type parameters for generic classes (Python 3.12+).")}
    , {'classDefinition': aDocument("AST object representing a complete class definition with metadata.")}
    , {'Examples': aDocument("""```
        # Creates AST equivalent to: class Vehicle: pass
        simpleClass = Make.ClassDef('Vehicle', body=[Make.Pass()])

        # Creates AST equivalent to: class Bicycle(Vehicle, metaclass=ABCMeta): pass
        inheritedClass = Make.ClassDef(
            'Bicycle',
            bases=[Make.Name('Vehicle')],
            keywords=[Make.keyword('metaclass', Make.Name('ABCMeta'))],
            body=[Make.Pass()]
        )
        ```
        """)}
))

listDocstring.append(Docstring(f"{identifierToolClass}.cmpop"
    , aDocument(f"`class` `ast.cmpop`, {diminutive2etymology['cmpop']}, is the parent (or 'base') class of all comparison operator classes used in `ast.Compare`.")
    , aDocument("""It is the abstract parent for: `ast.Eq`, `ast.NotEq`, `ast.Lt`, `ast.LtE`, `ast.Gt`, `ast.GtE`, `ast.Is`, `ast.IsNot`, `ast.In`, `ast.NotIn`. This factory method makes a generic comparison operator `object` that can be used in the antecedent-action pattern with visitor classes.""")
    , {}
    , {'comparisonOperator': aDocument("Abstract comparison operator `object` that serves as the base `class` for all Python comparison operators in AST structures.", 'ast.cmpop')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Compare"
    , aDocument("Make a comparison AST `object` for chained comparison operations.")
    , aDocument(f"""The `ast.Compare` `object` represents comparison operations including equality, inequality, and ordering comparisons. It supports chained comparisons like `a < b <= c` through sequences of operators and comparators.

        All comparison operators: `ast.Eq` ({diminutive2etymology['Eq']}), `ast.NotEq` ({diminutive2etymology['NotEq']}), `ast.Lt` ({diminutive2etymology['Lt']}), `ast.LtE` ({diminutive2etymology['LtE']}), `ast.Gt` ({diminutive2etymology['Gt']}), `ast.GtE` ({diminutive2etymology['GtE']}), `ast.Is`, `ast.IsNot`, `ast.In`, `ast.NotIn` ({diminutive2etymology['NotIn']}).""")
    , {'left': aDocument(f"({diminutive2etymology['left']}) The leftmost expression in the comparison chain.")
        , 'ops': aDocument(f"({diminutive2etymology['ops']}) Sequence of comparison operators from the complete list above.")
        , 'comparators': aDocument("Sequence of expressions to compare against, one for each operator.")}
    , {'comparison': aDocument("AST `object` representing a comparison operation with potential chaining.")}
    , {'Examples': aDocument("""```python
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
    , aDocument("Make a comprehension clause AST object for `for` clauses in list/set/dict comprehensions.")
    , aDocument("""The `ast.comprehension` object represents individual `for` clauses within comprehension expressions. Contains the iteration target, source, conditional filters, and async specification for generator expressions.""")
    , {'target': aDocument("Variable expression receiving each iteration value.")
        , 'iter': aDocument(f"({diminutive2etymology['iter']}) Iterable expression being traversed.")
        , 'ifs': aDocument(f"({diminutive2etymology['ifs']}) List of conditional expressions filtering iteration results.")
        , 'is_async': aDocument(f"({diminutive2etymology['is_async']}) Integer flag (0 or 1) indicating async comprehension.")}
    , {'comprehensionClause': aDocument("AST object representing a single for clause in comprehensions.", 'ast.comprehension')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Constant"
    , aDocument("Make a constant value AST `object` for literal values in Python code.")
    , aDocument("""The `ast.Constant` `object` represents literal constant values like numbers, strings, booleans, and None. It replaces the deprecated specific literal and provides a unified representation for all constant values.""")
    , {'value': aDocument("The constant value.")
        , 'kind': aDocument("Optional string hint for specialized constant handling.")}
    , {'constantValue': aDocument("AST `object` representing a literal constant value.", 'ast.Constant')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Continue"
    , aDocument("Create an `ast.Continue` node for continue statements.")
    , aDocument("""The `Continue` node represents a `continue` statement that skips the remainder of the current iteration and continues with the next iteration of the nearest enclosing loop.""")
    , {}
    , {'nodeContinue': aDocument("The constructed continue statement node.", 'ast.Continue')}
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
        # Creates AST equivalent to: `{{recipe: difficulty for recipe in cookbook}}`
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
    , {'conditionalExpression': aDocument("`ast.AST` ({diminutive2etymology['AST']}) `object` representing an inline conditional expression.")}
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
    , aDocument("Create an `ast.Interactive` ({diminutive2etymology['Interactive']}) node for interactive mode modules.")
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
    , {'identityNegationOperator' : aDocument("AST `object` representing the '`is not`' identity comparison operator for use in `ast.Compare`.")}
    , {'Examples' : aDocument("""```python
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
    , {'values' : aDocument("Sequence of string components, including `ast.Constant` and `ast.FormattedValue` objects.")}
    , {'joinedString' : aDocument("AST `object` representing an f-string literal with interpolated values.", 'ast.JoinedStr')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.keyword"
    , aDocument("Make a keyword argument AST object for named parameters in function calls.")
    , aDocument("""The `ast.keyword` object represents keyword arguments passed to function calls or class constructors. Contains the parameter name and corresponding value expression, including support for **keywordArguments unpacking.""")
    , {'Buffalo_buffalo_Buffalo_buffalo_buffalo_buffalo_Buffalo_buffalo' : aDocument("Parameter name string; None for **keywordArguments unpacking. This corresponds to `ast.keyword.arg`.")
        , 'value' : aDocument("Expression providing the argument value.")}
    , {'keywordArgument' : aDocument("AST object representing a named argument in function calls.")}
    , {'Examples' : aDocument("""Creates AST equivalent to: temperature=350
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
    , {'argumentSpecification' : aDocument("The function arguments specification as `ast.arguments`.")
        , 'body' : aDocument("Single expression that forms the lambda function body.")}
    , {'lambdaFunction' : aDocument("AST `object` representing an anonymous lambda function expression.", 'ast.Lambda')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.List"
    , aDocument("Make a list literal AST `object` with ordered element collection.")
    , aDocument("""The `ast.List` `object` represents list literals using square bracket notation. It creates ordered, mutable collections and supports various contexts like loading values, storing to variables, or deletion operations.""")
    , {'listElements' : aDocument("Sequence of expressions that become list elements.")
        , 'context' : aDocument("Expression context for how the list is used.")}
    , {'listLiteral' : aDocument("AST `object` representing a list literal with specified elements.", 'ast.List')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.ListComp"
    , aDocument("Make a list comprehension AST `object` for dynamic list construction.")
    , aDocument(f"""The `ast.ListComp` ({diminutive2etymology['ListComp']}) `object` represents list comprehensions that create lists using iterator expressions. It provides concise syntax for filtering and transforming collections into new lists.""")
    , {'element' : aDocument(f"({diminutive2etymology['elt']}) Expression that generates each element of the resulting list.")
        , 'generators' : aDocument("Sequence of `ast.comprehension` objects defining iterator and filtering.")}
    , {'listComprehension' : aDocument("AST `object` representing a list comprehension expression.", 'ast.ListComp')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Load"
    , aDocument("Make a load context for reading expression values.")
    , aDocument("""The `ast.Load` context indicates expressions are being read or evaluated to retrieve their values. This is the default context for most expressions like `bicycle.wheel` when accessing the wheel attribute value.""")
    , {}
    , {'loadContext' : aDocument("AST context object indicating value retrieval operations.", 'ast.Load')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Lt"
    , aDocument("'Lt', meaning 'is Less than', is the `object` representation of Python comparison operator '`<`'.")
    , aDocument("""`class` `ast.Lt` is a subclass of `ast.cmpop`, '***c***o***mp***arison ***op***erator', and only used in `class` `ast.Compare`, parameter '`ops`', ***op***erator***s***.""")
    , {}
    , {'lessThanOperator' : aDocument("AST `object` representing the '`<`' less-than comparison operator for use in `ast.Compare`.", 'ast.Lt')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.LtE"
    , aDocument("'LtE', meaning 'is Less than or Equal to', is the `object` representation of Python comparison operator '`<=`'.")
    , aDocument("""`class` `ast.LtE` is a subclass of `ast.cmpop`, '***c***o***mp***arison ***op***erator', and only used in `class` `ast.Compare`, parameter '`ops`', ***op***erator***s***.""")
    , {}
    , {'lessThanOrEqualOperator' : aDocument("AST `object` representing the '`<=`' less-than-or-equal comparison operator for use in `ast.Compare`.", 'ast.LtE')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.Match"
    , aDocument("Make a match statement AST object for pattern matching with multiple cases.")
    , aDocument(f"""The `ast.Match` ({diminutive2etymology['Match']}) object represents match statements that perform pattern matching against a subject expression. Contains the value being matched and a list of case clauses with their patterns and corresponding actions.""")
    , {'subject' : aDocument("Expression being matched against the case patterns.")
        , 'cases' : aDocument(f"({diminutive2etymology['match_case']}) List of match_case objects defining pattern-action pairs.")}
    , {'matchStatement' : aDocument("AST object representing a complete pattern matching statement.", 'ast.Match')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.match_case"
    , aDocument("Make a match case clause AST object for individual cases in `match` statements.")
    , aDocument(f"""The `ast.match_case` ({diminutive2etymology['match_case']}) object represents individual case clauses within match statements. Contains the pattern to match, optional guard condition, and statements to execute when the pattern matches successfully.""")
    , {'pattern' : aDocument("Pattern expression defining what values match this case.")
        , 'guard' : aDocument("Optional conditional expression for additional filtering.")
        , 'body' : aDocument("List of statements to execute when pattern matches.")}
    , {'matchCase' : aDocument("AST object representing a single case clause in match statements.", 'ast.match_case')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.MatchAs"
    , aDocument("Create an `ast.MatchAs` node representing a capture pattern or wildcard.")
    , aDocument(f"""The `ast.MatchAs` ({diminutive2etymology['MatchAs']}) node represents match patterns that capture values or serve as wildcards. This includes bare name patterns like `bicycle` that capture the matched value, "as" patterns like `Point(x, y) as location` that match a pattern and capture the result, and the wildcard pattern `_`.""")
    , {'pattern' : aDocument("Optional pattern to match against. When `None`, creates a capture pattern (bare name) if `name` is provided, or wildcard if both are `None`.")
        , 'name' : aDocument("Optional identifier to bind the matched value. When `None` and pattern is also `None`, creates the wildcard pattern.")}
    , {'matchAsNode' : aDocument("An `ast.MatchAs` node with the specified pattern and name.", 'ast.MatchAs')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.MatchClass"
    , aDocument("Create an `ast.MatchClass` node for matching class instances.")
    , aDocument(f"""The `ast.MatchClass` ({diminutive2etymology['MatchClass']}) node represents patterns that match instances of a specific class, checking both the class type and extracting values from the instance's attributes. This enables structural pattern matching against objects.""")
    , {'cls' : aDocument(f"({diminutive2etymology['cls']}) Expression identifying the class to match against.")
        , 'patterns' : aDocument("Sequence of pattern nodes for positional matching against class-defined attributes.")
        , 'kwd_attrs' : aDocument(f"({diminutive2etymology['kwd_attrs']}) List of attribute names for keyword-style matching.")
        , 'kwd_patterns' : aDocument(f"({diminutive2etymology['kwd_patterns']}) Sequence of pattern nodes corresponding to the keyword attributes.")}
    , {'matchClassNode' : aDocument("An `ast.MatchClass` node configured for the specified class and patterns.", 'ast.MatchClass')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.MatchMapping"
    , aDocument("Create an `ast.MatchMapping` node for matching dictionary-like objects.")
    , aDocument(f"""The `ast.MatchMapping` ({diminutive2etymology['MatchMapping']}) node represents patterns that match mapping objects like dictionaries, checking for specific keys and extracting their values. The pattern can also capture remaining unmapped keys.""")
    , {'keys' : aDocument("Sequence of expression nodes representing the keys to match.")
        , 'patterns' : aDocument("Sequence of pattern nodes corresponding to the values associated with each key.")
        , 'rest' : aDocument(f"({diminutive2etymology['rest']}) Optional identifier to capture remaining mapping elements not otherwise matched.")}
    , {'matchMappingNode' : aDocument("An `ast.MatchMapping` node for the specified key-value patterns and optional rest capture.", 'ast.MatchMapping')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.MatchOr"
    , aDocument("Create an `ast.MatchOr` node for alternative pattern matching.")
    , aDocument(f"""The `ast.MatchOr` ({diminutive2etymology['MatchOr']}) node represents or-patterns that match if any of the alternative subpatterns succeed. The pattern tries each alternative in sequence until one matches or all fail.""")
    , {'patterns' : aDocument("Sequence of alternative pattern nodes. The match succeeds if any subpattern matches the subject.")}
    , {'matchOrNode' : aDocument("An `ast.MatchOr` node containing the alternative patterns.", 'ast.MatchOr')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.MatchSequence"
    , aDocument("Create an `ast.MatchSequence` node for matching sequences.")
    , aDocument(f"""The `ast.MatchSequence` ({diminutive2etymology['MatchSequence']}) node represents patterns that match sequence objects like lists and tuples, checking both length and element patterns. Supports both fixed-length and variable-length sequence matching.""")
    , {'patterns' : aDocument("Sequence of pattern nodes to match against sequence elements. If any pattern is `MatchStar`, enables variable-length matching; otherwise requires exact length match.")}
    , {'matchSequenceNode' : aDocument("An `ast.MatchSequence` node for the specified element patterns.", 'ast.MatchSequence')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.MatchSingleton"
    , aDocument("Create an `ast.MatchSingleton` node for matching singleton values.")
    , aDocument(f"""The `ast.MatchSingleton` ({diminutive2etymology['MatchSingleton']}) node represents patterns that match singleton constants by identity rather than equality. This pattern succeeds only if the match subject is the exact same object as the specified constant.""")
    , {'value' : aDocument("The singleton constant to match against. Must be `None`, `True`, or `False`. Matching uses identity comparison (`is`) rather than equality comparison (`==`).")}
    , {'matchSingletonNode' : aDocument("An `ast.MatchSingleton` node for the specified singleton value.", 'ast.MatchSingleton')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.MatchStar"
    , aDocument("Create an `ast.MatchStar` node for capturing sequence remainder.")
    , aDocument(f"""The `ast.MatchStar` ({diminutive2etymology['MatchStar']}) node represents star patterns that capture remaining elements in variable-length sequence patterns. This enables flexible sequence matching where some elements are specifically matched and others are collected.""")
    , {'name' : aDocument("Optional identifier to bind the remaining sequence elements. When `None`, the remaining elements are matched but not captured.")}
    , {'matchStarNode' : aDocument("An `ast.MatchStar` node with the specified capture name.", 'ast.MatchStar')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.MatchValue"
    , aDocument("Create an `ast.MatchValue` node for matching literal values.")
    , aDocument(f"""The `ast.MatchValue` ({diminutive2etymology['MatchValue']}) node represents patterns that match by equality comparison against a literal value or expression. The pattern succeeds if the match subject equals the evaluated value expression.""")
    , {'value' : aDocument("Expression node representing the value to match against. Typically a constant, name, or attribute access. The expression is evaluated and compared using equality (`==`).")}
    , {'matchValueNode' : aDocument("An `ast.MatchValue` node for the specified value expression.", 'ast.MatchValue')}
))

listDocstring.append(Docstring(f"{identifierToolClass}.mod", aDocument(f"Create an abstract `ast.mod` ({diminutive2etymology['mod']}) `object`.", AIgenerated=False)))

listDocstring.append(Docstring(f"{identifierToolClass}.Module"
    , aDocument("Make a module AST object representing complete Python modules with statements and type ignores.")
    , aDocument("""The `ast.Module` object represents entire Python modules as parsed from source files. Contains all top-level statements and tracks type ignore comments for static analysis tools and type checkers.""")
    , {'body' : aDocument("List of statements forming the module content.")
        , 'type_ignores' : aDocument(f"({diminutive2etymology['type_ignores']}) List of TypeIgnore objects for `# type: ignore` comments.")}
    , {'moduleDefinition' : aDocument("AST object representing a complete Python module structure.")}
    , {'Examples' : aDocument("""Creates AST equivalent to: x = 42
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
    , {'values': aDocument( "A sequence of nodes (typically `ast.Constant` or `ast.Interpolation`) forming the template string.", 'Sequence[ast.expr]')}
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
    , {'col_offset': aDocument(f"({diminutive2etymology['col_offset']}) Position information specifying the column where an AST object begins." , 'int', AIgenerated=False)
    , 'end_col_offset': aDocument(f"({diminutive2etymology['end_col_offset']}) Position information specifying the column where an AST object ends." , '(int | None) | int', AIgenerated=False)
    , 'end_lineno': aDocument(f"({diminutive2etymology['end_lineno']}) Position information specifying the line number where an AST object ends." , '(int | None) | int', AIgenerated=False)
    , 'level': aDocument(f"({diminutive2etymology['level']}) An absolute import is 'level' 0. A relative import is `level` deep." , 'int = 0', AIgenerated=False)
    , 'lineno': aDocument(f"({diminutive2etymology['lineno']}) Position information manually specifying the line number where an AST object begins." , 'int', AIgenerated=False)
    , 'type_comment': aDocument(f"({diminutive2etymology['type_comment']}) Optional string with the type annotation as a comment or `# type: ignore`." , 'str', AIgenerated=False)}
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
