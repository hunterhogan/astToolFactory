"""A warehouse for docstrings added to manufactured ast tools.
NOTE Use special indentation in this file.
    1. The generated files use spaces, not tabs, so use spaces here.
    2. As of this writing, I only know how to _manually_ align the indentation of the docstrings with the associated code. So, indent one or two levels as appropriate."""
from astToolFactory import dictionaryIdentifiers
from astToolFactory.documentation import docstrings
from astToolkit import Make
import ast

identifierToolClass: str = 'Make'

ImaDocstring: str = """Identical to the `ast` class but with a method, `join()`, that "joins" expressions using the `ast.BoolOp` class."""
for subclass in ast.boolop.__subclasses__():
    docstrings[dictionaryIdentifiers[identifierToolClass]][subclass.__name__] = Make.Expr(Make.Constant(ImaDocstring))
del ImaDocstring

ImaDocstring: str = """Identical to the `ast` class but with a method, `join()`, that "joins" expressions using the `ast.BinOp` class."""
for subclass in ast.operator.__subclasses__():
    docstrings[dictionaryIdentifiers[identifierToolClass]][subclass.__name__] = Make.Expr(Make.Constant(ImaDocstring))
del ImaDocstring

        # context (ast.Load()): Are you loading from, storing to, or deleting the identifier? The `context` (also, `ctx`) value is `ast.Load()`, `ast.Store()`, or `ast.Del()`.
        # kind (None): str|None Used for type annotations in limited cases.

ImaDocstring: str = (
    """
    All parameters described here are only accessible through a method's `**keywordArguments` parameter.

    Parameters:
        col_offset (0): int Position information specifying the column where an AST node begins.
        end_col_offset (None): int|None Position information specifying the column where an AST node ends.
        end_lineno (None): int|None Position information specifying the line number where an AST node ends.
        level (0): int Module import depth level that controls relative vs absolute imports. Default 0 indicates absolute import.
        lineno: int Position information manually specifying the line number where an AST node begins.
        type_comment (None): str|None "type_comment is an optional string with the type annotation as a comment." or `# type: ignore`.
    """
)
docstrings[dictionaryIdentifiers[identifierToolClass]][dictionaryIdentifiers[identifierToolClass]] = Make.Expr(Make.Constant(ImaDocstring))
del ImaDocstring

ImaDocstring: str = (
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
docstrings[dictionaryIdentifiers[identifierToolClass]][dictionaryIdentifiers['operatorJoinMethod']] = Make.Expr(Make.Constant(ImaDocstring))
del ImaDocstring

ImaDocstring: str = (
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
docstrings[dictionaryIdentifiers[identifierToolClass]][dictionaryIdentifiers['boolopJoinMethod']] = Make.Expr(Make.Constant(ImaDocstring))
del ImaDocstring

ImaDocstring: str = (
        """
        If two identifiers are joined by a dot '`.`', they are _usually_ an `ast.Attribute`, but see, for example, `ast.ImportFrom`.

        Parameters:
            value: the part before the dot (e.g., `ast.Name`.)
            attribute: an identifier after a dot '`.`'; you can pass multiple `attribute` and they will be chained together.
        """
)
docstrings[dictionaryIdentifiers[identifierToolClass]]['Attribute'] = Make.Expr(Make.Constant(ImaDocstring))
del ImaDocstring


ImaDocstring: str = (
        """
        'Gt', meaning 'Greater than', is the `object` representation of Python '`>`'.

        `ast.Gt` is a subclass of `ast.cmpop`, '***c***o***mp***arison ***op***erator', and
        only used in class `ast.Compare`, parameter '`ops`'.
        """
)
docstrings[dictionaryIdentifiers[identifierToolClass]]['Gt'] = Make.Expr(Make.Constant(ImaDocstring))
del ImaDocstring

ImaDocstring: str = (
        """
        An `ast.IsNot` `object` represents Python keywords '`is not`', which compare `object` identities.

        Jane Austen and Franz Kafka are equally skilled writers, but Mark Twain and Samuel Clemens are
        identical because they are the same person. '`is not`' compares memory locations to determine identity.

        `ast.IsNot` is a subclass of `ast.cmpop`, '***c***o***mp***arison ***op***erator', and
        only used in class `ast.Compare`, parameter '`ops`'.

        Returns
        -------
        identityComparisonOperator: ast.IsNot
            AST node representing the '`is not`' comparison operator for use in `ast.Compare` nodes.

        Examples
        --------
        ```python
        # Creates AST equivalent to: `if chicken is not None`
        comparisonNode = Make.Compare(
            left=Make.Name('chicken'),
            ops=[Make.IsNot()],
            comparators=[Make.Constant(None)]
        )
        ```
        """
)
docstrings[dictionaryIdentifiers[identifierToolClass]]['IsNot'] = Make.Expr(Make.Constant(ImaDocstring))
del ImaDocstring