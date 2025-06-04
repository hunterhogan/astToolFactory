"""A warehouse for docstrings added to manufactured ast tools.
NOTE Use special indentation in this file.
    1. The generated files use spaces, not tabs, so use spaces here.
    2. As of this writing, I only know how to _manually_ align the indentation of the docstrings with the associated code. So, indent one or two levels as appropriate."""
import ast

docstring: str = """This file is generated automatically, so changes to this file will be lost."""
docstringWarning = ast.Expr(ast.Constant(docstring))
del docstring

docstring: str = """Identical to the `ast` class but with a method, `join()`, that "joins" expressions using the `ast.BoolOp` class."""
ClassDefDocstring_ast_boolop = ast.Expr(ast.Constant(docstring))
del docstring

docstring: str = """Identical to the `ast` class but with a method, `join()`, that "joins" expressions using the `ast.BinOp` class."""
ClassDefDocstring_ast_operator = ast.Expr(ast.Constant(docstring))
del docstring

docstring: str = (
    """Type guard functions for safe AST node identification and type narrowing.
    (AI generated docstring)

    Provides static methods that perform runtime type checking for all AST node types
    while enabling compile-time type narrowing through `TypeIs` annotations. Forms
    the foundation of type-safe AST analysis and transformation throughout the toolkit.

    Each method takes an `ast.AST` node and returns a `TypeIs` that confirms both
    runtime type safety and enables static type checkers to narrow the node type in
    conditional contexts. This eliminates the need for unsafe casting while providing
    comprehensive coverage of Python's AST node hierarchy.

    Methods correspond directly to Python AST node types, following the naming convention
    of the AST classes themselves. Coverage includes expression nodes (`Add`, `Call`,
    `Name`), statement nodes (`Assign`, `FunctionDef`, `Return`), operator nodes
    (`And`, `Or`, `Not`), and structural nodes (`Module`, `arguments`, `keyword`).

    The class serves as the primary type-checking component in the antecedent-action
    pattern, where predicates identify target nodes and actions specify operations.
    Type guards from this class are commonly used as building blocks in `IfThis`
    predicates and directly as `findThis` parameters in visitor classes.

    Parameters:

        node: AST node to test for specific type membership

    Returns:

        typeIs: `TypeIs` enabling both runtime validation and static type narrowing

    Examples:

        Type-safe node processing with automatic type narrowing:

            if Be.FunctionDef(node):
                functionName = node.name  # Type-safe access to name attribute
                parameterCount = len(node.args.args)

        Building complex predicates for visitor patterns:

            NodeTourist(Be.Return, Then.extractIt(DOT.value)).visit(functionNode)

        Combining type guards in conditional logic:

            if Be.Call(node) and Be.Name(node.func):
                callableName = node.func.id  # Type-safe access to function name
    """
)

ClassDefDocstringBe = ast.Expr(ast.Constant(docstring))
del docstring

docstring: str = (
    """
    Access attributes and sub-nodes of AST elements via consistent accessor methods.

    The DOT class provides static methods to access specific attributes of different types of AST nodes in a consistent
    way. This simplifies attribute access across various node types and improves code readability by abstracting the
    underlying AST structure details.

    DOT is designed for safe, read-only access to node properties, unlike the grab class which is designed for modifying
    node attributes.
    """
)
ClassDefDocstringDOT = ast.Expr(ast.Constant(docstring))
del docstring

docstring: str = (
    """
    Create functions that verify AST nodes by type and attribute conditions.

    The ClassIsAndAttribute class provides static methods that generate conditional functions for determining if an AST
    node is of a specific type AND its attribute meets a specified condition. These functions return TypeIs-enabled
    callables that can be used in conditional statements to narrow node types during code traversal and transformation.

    Each generated function performs two checks:
    1. Verifies that the node is of the specified AST type
    2. Tests if the specified attribute of the node meets a custom condition

    This enables complex filtering and targeting of AST nodes based on both their type and attribute contents.
    """
)
ClassDefDocstringClassIsAndAttribute = ast.Expr(ast.Constant(docstring))
del docstring

docstring: str = (
    """
    Modify specific attributes of AST nodes while preserving the node structure.

    The Grab class provides static methods that create transformation functions to modify specific attributes of AST
    nodes. Unlike DOT which provides read-only access, Grab allows for targeted modifications of node attributes without
    replacing the entire node.

    Each method returns a function that takes a node, applies a transformation to a specific attribute of that node, and
    returns the modified node. This enables fine-grained control when transforming AST structures.
    """
)
ClassDefDocstringGrab = ast.Expr(ast.Constant(docstring))
del docstring

docstring: str = (
    """
    Almost all parameters described here are only accessible through a method's `**keywordArguments` parameter.

    Parameters:
        context (ast.Load()): Are you loading from, storing to, or deleting the identifier? The `context` (also, `ctx`) value is `ast.Load()`, `ast.Store()`, or `ast.Del()`.
        col_offset (0): int Position information specifying the column where an AST node begins.
        end_col_offset (None): int|None Position information specifying the column where an AST node ends.
        end_lineno (None): int|None Position information specifying the line number where an AST node ends.
        level (0): int Module import depth level that controls relative vs absolute imports. Default 0 indicates absolute import.
        lineno: int Position information manually specifying the line number where an AST node begins.
        kind (None): str|None Used for type annotations in limited cases.
        type_comment (None): str|None "type_comment is an optional string with the type annotation as a comment." or `# type: ignore`.
        type_params: list[ast.type_param] Type parameters for generic type definitions.

    The `ast._Attributes`, lineno, col_offset, end_lineno, and end_col_offset, hold position information; however, they are, importantly, _not_ `ast._fields`.
    """
)
ClassDefDocstringMake = ast.Expr(ast.Constant(docstring))
del docstring

docstring: str = (
        """
        Create a single `ast.expr` from a collection of `ast.expr` by forming nested `ast.BinOp`
        that are logically "joined" using the `ast.operator` subclass. Like str.join() but for AST expressions.

        Parameters
        ----------
        expressions : Iterable[ast.expr]
            Collection of expressions to join.
        **keywordArguments : ast._attributes

        Returns
        -------
        joinedExpression : ast.expr
            Single expression representing the joined expressions.

        Examples
        --------
        Instead of manually constructing nested ast.BinOp structures:
        ```
        ast.BinOp(
            left=ast.BinOp(
                left=ast.Name('Crosby')
                , op=ast.BitOr()
                , right=ast.Name('Stills'))
            , op=ast.BitOr()
            , right=ast.Name('Nash')
        )
        ```

        Simply use:
        ```
        astToolkit.BitOr().join([ast.Name('Crosby'), ast.Name('Stills'), ast.Name('Nash')])
        ```

        Both produce the same AST structure but the join() method eliminates the manual nesting.
        Handles single expressions and empty iterables gracefully.
        """
)
FunctionDefDocstring_join_operator = ast.Expr(ast.Constant(docstring))
del docstring

docstring: str = (
        """
        Create a single `ast.expr` from a sequence of `ast.expr` by forming an `ast.BoolOp`
        that logically "joins" expressions using the `ast.BoolOp` subclass. Like str.join() but for AST expressions.

        Parameters
        ----------
        expressions : Sequence[ast.expr]
            Collection of expressions to join.
        **keywordArguments : ast._attributes

        Returns
        -------
        joinedExpression : ast.expr
            Single expression representing the joined expressions.

        Examples
        --------
        Instead of manually constructing ast.BoolOp structures:
        ```
        ast.BoolOp(
            op=ast.And(),
            values=[ast.Name('Lions'), ast.Name('tigers'), ast.Name('bears')]
        )
        ```

        Simply use:
        ```
        astToolkit.And.join([ast.Name('Lions'), ast.Name('tigers'), ast.Name('bears')])
        ```

        Both produce the same AST structure but the join() method eliminates the manual construction.
        Handles single expressions and empty sequences gracefully.
        """
)
FunctionDefDocstring_join_boolop = ast.Expr(ast.Constant(docstring))
del docstring

docstring: str = (
        """
        If two identifiers are joined by a dot '`.`', they are _usually_ an `ast.Attribute`, but see, for example, `ast.ImportFrom`.

        Parameters:
            value: the part before the dot (e.g., `ast.Name`.)
            attribute: an identifier after a dot '`.`'; you can pass multiple `attribute` and they will be chained together.
        """
)
FunctionDefMake_AttributeDocstring = ast.Expr(ast.Constant(docstring))
del docstring

