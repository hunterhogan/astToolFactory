"""A warehouse for docstrings added to manufactured ast tools.
NOTE Use special indentation in this file.
    1. The generated files use spaces, not tabs, so use spaces here.
    2. As of this writing, I only know how to _manually_ align the indentation of the docstrings with the associated code. So, indent one or two levels as appropriate."""
from astToolFactory import dictionaryIdentifiers
from astToolFactory.documentation import docstrings
from astToolkit import Make
import ast

identifierToolClass: str = 'Make'
# context (ast.Load()): Are you loading from, storing to, or deleting the identifier? The `context` (also, `ctx`) value is `ast.Load()`, `ast.Store()`, or `ast.Del()`.
# kind (None): str|None Used for type annotations in limited cases.

for subclass in ast.boolop.__subclasses__():
    docstrings[dictionaryIdentifiers[identifierToolClass]][subclass.__name__] = Make.Expr(Make.Constant("""Identical to the `ast` class but with a method, `join()`, that "joins" expressions using the `ast.BoolOp` class."""))

for subclass in ast.operator.__subclasses__():
    docstrings[dictionaryIdentifiers[identifierToolClass]][subclass.__name__] = Make.Expr(Make.Constant("""Identical to the `ast` class but with a method, `join()`, that "joins" expressions using the `ast.BinOp` class."""))

docstrings[dictionaryIdentifiers[identifierToolClass]][dictionaryIdentifiers[identifierToolClass]] = Make.Expr(Make.Constant(
    """
    All parameters described here are only accessible through a method's `**keywordArguments` parameter.

    Parameters:
        col_offset (0): int Position information specifying the column where an AST `object` begins.
        end_col_offset (None): int|None Position information specifying the column where an AST `object` ends.
        end_lineno (None): int|None Position information specifying the line number where an AST `object` ends.
        level (0): int Module import depth level that controls relative vs absolute imports. Default 0 indicates absolute import.
        lineno: int Position information manually specifying the line number where an AST `object` begins.
        type_comment (None): str|None "type_comment is an optional string with the type annotation as a comment." or `# type: ignore`.
    """
))

docstrings[dictionaryIdentifiers[identifierToolClass]][dictionaryIdentifiers['operatorJoinMethod']] = Make.Expr(Make.Constant(
        """
        Single `ast.expr` from a collection of `ast.expr` by forming nested `ast.BinOp` that are logically "joined" using the `ast.operator` subclass.

        Like str.join() but for AST expressions.

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
))

docstrings[dictionaryIdentifiers[identifierToolClass]][dictionaryIdentifiers['boolopJoinMethod']] = Make.Expr(Make.Constant(
        """
        Single `ast.expr` from a sequence of `ast.expr` by forming an `ast.BoolOp` that logically "joins" expressions using the `ast.BoolOp` subclass.

        Like str.join() but for AST expressions.

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
))

docstrings[dictionaryIdentifiers[identifierToolClass]]['Attribute'] = Make.Expr(Make.Constant(
        """
        If two identifiers are joined by a dot '`.`', they are _usually_ an `ast.Attribute`, but see, for example, `ast.ImportFrom`.

        Parameters:
            value: the part before the dot (e.g., `ast.Name`.)
            attribute: an identifier after a dot '`.`'; you can pass multiple `attribute` and they will be chained together.
        """
))

docstrings[dictionaryIdentifiers[identifierToolClass]]['cmpop'] = Make.Expr(Make.Constant(
        """
        Abstract ***c***o***mp***arison ***op***erator `object` for use in AST construction.
        (AI generated docstring)

        Class `ast.cmpop` is the base for all comparison operators in Python's AST.
        It serves as the abstract parent for specific comparison operators: `ast.Eq`, `ast.NotEq`,
        `ast.Lt`, `ast.LtE`, `ast.Gt`, `ast.GtE`, `ast.Is`, `ast.IsNot`, `ast.In`, `ast.NotIn`.
        This factory method makes a generic comparison operator `object` that can be used
        in the antecedent-action pattern with visitor classes.

        Returns
        -------
        comparisonOperator: ast.cmpop
            Abstract comparison operator `object` that serves as the base `class` for all
            Python comparison operators in AST structures.
        """
))

docstrings[dictionaryIdentifiers[identifierToolClass]]['Eq'] = Make.Expr(Make.Constant(
        """
        'Eq', meaning 'is ***Eq***ual to', is the `object` representation of Python comparison operator '`==`'.

        `class` `ast.Eq` is a subclass of `ast.cmpop`, '***c***o***mp***arison ***op***erator', and
        only used in `class` `ast.Compare`, parameter '`ops`', ***op***erator***s***.

        Returns
        -------
        equalityOperator:
            AST `object` representing the '`==`' equality comparison operator for use
            in `ast.Compare`.
        """
))

docstrings[dictionaryIdentifiers[identifierToolClass]]['Is'] = Make.Expr(Make.Constant(
        """
        'Is', meaning 'Is identical to', is the `object` representation of Python keyword '`is`'.

        `class` `ast.Is` is a subclass of `ast.cmpop`, '***c***o***mp***arison ***op***erator', and
        only used in `class` `ast.Compare`, parameter '`ops`', ***op***erator***s***.

        The Python interpreter declares *This* logical `object` 'Is identical to' *That* logical `object` if they use the same physical memory location. Therefore, modifying one `object` will necessarily modify the other `object`.

        What's the difference between equality and identity?
        - The work of Jane Austen 'is Equal to' the work of Franz Kafka.
        - The work of Mark Twain 'is Equal to' the work of Samuel Clemens.
        - And Mark Twain 'Is identical to' Samuel Clemens: because they are the same person.

        Returns
        -------
        identityOperator:
            AST `object` representing the '`is`' identity comparison operator for use in `ast.Compare`.

        Examples
        --------
        ```python
        # Logically equivalent to: `... valueAttributes is None ...`
        comparisonNode = Make.Compare(
            left=Make.Name('valueAttributes'),
            ops=[Make.Is()],
            comparators=[Make.Constant(None)]
        )
        ```

            In the first example, the two statements are logically equal but they cannot be identical.
        """
))

docstrings[dictionaryIdentifiers[identifierToolClass]]['IsNot'] = Make.Expr(Make.Constant(
        """
        'IsNot', meaning 'Is Not identical to', is the `object` representation of Python keywords '`is not`'.

        `class` `ast.IsNot` is a subclass of `ast.cmpop`, '***c***o***mp***arison ***op***erator', and
        only used in `class` `ast.Compare`, parameter '`ops`', ***op***erator***s***.

        The Python interpreter declares *This* logical `object` 'Is Not identical to' *That* logical `object` if they do not use the same physical memory location.

        What's the difference between equality and identity?
        - The work of Jane Austen 'is Equal to' the work of Franz Kafka.
        - The work of Mark Twain 'is Equal to' the work of Samuel Clemens.
        - And Mark Twain 'Is identical to' Samuel Clemens: because they are the same person.

        Python programmers frequently use '`is not None`' because keyword `None` does not have a physical memory location, so `if chicken is not None`, `chicken` must have a physical memory location (and be in the current scope and blah blah blah...).

        Returns
        -------
        identityNegationOperator:
            AST `object` representing the '`is not`' identity comparison operator for use in `ast.Compare`.

        Examples
        --------
        ```python
        # Logically equivalent to: `... chicken is not None ...`
        comparisonNode = Make.Compare(
            left=Make.Name('chicken'),
            ops=[Make.IsNot()],
            comparators=[Make.Constant(None)]
        )
        ```

            In the first example, the two statements are logically equal but they cannot be identical.
        """
))

docstrings[dictionaryIdentifiers[identifierToolClass]]['NotEq'] = Make.Expr(Make.Constant(
        """
        'NotEq' meaning 'is ***Not*** ***Eq***ual to', is the `object` representation of Python comparison operator '`!=`'.

        `class` `ast.NotEq` is a subclass of `ast.cmpop`, '***c***o***mp***arison ***op***erator', and
        only used in `class` `ast.Compare`, parameter '`ops`', ***op***erator***s***.

        Returns
        -------
        inequalityOperator:
            AST `object` representing the '`!=`' inequality comparison operator for use
            in `ast.Compare`.
        """
))

docstrings[dictionaryIdentifiers[identifierToolClass]]['Lt'] = Make.Expr(Make.Constant(
        """
        'Lt', meaning 'is Less than', is the `object` representation of Python comparison operator '`<`'.

        `class` `ast.Lt` is a subclass of `ast.cmpop`, '***c***o***mp***arison ***op***erator', and
        only used in `class` `ast.Compare`, parameter '`ops`', ***op***erator***s***.

        Returns
        -------
        lessThanOperator:
            AST `object` representing the '`<`' less-than comparison operator for use
            in `ast.Compare`.
        """
))

docstrings[dictionaryIdentifiers[identifierToolClass]]['LtE'] = Make.Expr(Make.Constant(
        """
        'LtE', meaning 'is Less than or Equal to', is the `object` representation of Python comparison operator '`<=`'.

        `class` `ast.LtE` is a subclass of `ast.cmpop`, '***c***o***mp***arison ***op***erator', and
        only used in `class` `ast.Compare`, parameter '`ops`', ***op***erator***s***.

        Returns
        -------
        lessThanOrEqualOperator:
            AST `object` representing the '`<=`' less-than-or-equal comparison operator
            for use in `ast.Compare`.
        """
))

docstrings[dictionaryIdentifiers[identifierToolClass]]['Gt'] = Make.Expr(Make.Constant(
        """
        'Gt', meaning 'Greater than', is the `object` representation of Python operator '`>`'.

        `class` `ast.Gt` is a subclass of `ast.cmpop`, '***c***o***mp***arison ***op***erator', and
        only used in `class` `ast.Compare`, parameter '`ops`', ***op***erator***s***.

        Returns
        -------
        greaterThanOperator:
            AST `object` representing the '`>`' greater-than comparison operator for use
            in `ast.Compare`.
        """
))

docstrings[dictionaryIdentifiers[identifierToolClass]]['GtE'] = Make.Expr(Make.Constant(
        """
        'GtE', meaning 'is Greater than or Equal to', is the `object` representation of Python comparison operator '`>=`'.

        `class` `ast.GtE` is a subclass of `ast.cmpop`, '***c***o***mp***arison ***op***erator', and
        only used in `class` `ast.Compare`, parameter '`ops`', ***op***erator***s***.

        Returns
        -------
        greaterThanOrEqualOperator:
            AST `object` representing the '`>=`' greater-than-or-equal comparison operator
            for use in `ast.Compare`.
        """
))

docstrings[dictionaryIdentifiers[identifierToolClass]]['In'] = Make.Expr(Make.Constant(
        """
        'In', meaning 'is ***In***cluded in' or 'has membership In', is the `object` representation of Python keyword '`in`'.

        `class` `ast.In` is a subclass of `ast.cmpop`, '***c***o***mp***arison ***op***erator', and
        only used in `class` `ast.Compare`, parameter '`ops`', ***op***erator***s***. The Python interpreter
        declares *This* `object` 'is ***In***cluded in' *That* `iterable` if *This* `object` matches a part of *That* `iterable`.

        Returns
        -------
        membershipOperator:
            AST `object` representing the keyword '`in`' membership test operator for use
            in `ast.Compare`.
        """
))

docstrings[dictionaryIdentifiers[identifierToolClass]]['NotIn'] = Make.Expr(Make.Constant(
        """
        'NotIn', meaning 'is Not ***In***cluded in' or 'does Not have membership In', is the `object` representation of Python keywords '`not in`'.

        `class` `ast.NotIn` is a subclass of `ast.cmpop`, '***c***o***mp***arison ***op***erator', and
        only used in `class` `ast.Compare`, parameter '`ops`', ***op***erator***s***. The Python interpreter
        declares *This* `object` 'is Not ***In***cluded in' *That* `iterable` if *This* `object` does not match a part of *That* `iterable`.

        Returns
        -------
        negativeMembershipOperator:
            AST `object` representing the keywords '`not in`' negative membership test operator
            for use in `ast.Compare`.
        """
))

docstrings[dictionaryIdentifiers[identifierToolClass]]['unaryop'] = Make.Expr(Make.Constant(
        """
        Abstract ***un***ary ***op***erator `object` for use in AST construction.
        (AI generated docstring)

        Class `ast.unaryop` is the base for all unary operators in Python's AST.
        It serves as the abstract parent for specific unary operators: `ast.Invert`,
        `ast.Not`, `ast.UAdd`, `ast.USub`. This factory method makes a generic
        unary operator `object` that can be used in the antecedent-action pattern with visitor classes.

        Unlike `ast.cmpop` which handles binary comparison operations between two operands,
        `ast.unaryop` represents operators that act on a single operand. Both serve as abstract
        base classes but for different categories of operations: `ast.cmpop` for comparisons
        and `ast.unaryop` for unary transformations.

        Returns
        -------
        unaryOperator: ast.unaryop
            Abstract unary operator `object` that serves as the base `class` for all
            Python unary operators in AST structures.
        """
))

docstrings[dictionaryIdentifiers[identifierToolClass]]['Invert'] = Make.Expr(Make.Constant(
        """
        Bitwise complement operator representing Python '`~`' operator.
        (AI generated docstring)

        Class `ast.Invert` is a subclass of `ast.unaryop` and represents the bitwise complement
        or inversion operator '`~`' in Python source code. This operator performs bitwise
        NOT operation, flipping all bits of its operand. Used within `ast.UnaryOp`
        as the `op` parameter.

        Returns
        -------
        bitwiseComplementOperator: ast.Invert
            AST `object` representing the '`~`' bitwise complement operator for use
            in `ast.UnaryOp`.
        """
))

docstrings[dictionaryIdentifiers[identifierToolClass]]['Not'] = Make.Expr(Make.Constant(
        """
        Logical negation operator representing Python keyword '`not`'.
        (AI generated docstring)

        Class `ast.Not` is a subclass of `ast.unaryop` and represents the logical negation
        operator keyword '`not`' in Python source code. This operator returns the boolean
        inverse of its operand's truthiness. Used within `ast.UnaryOp` as the
        `op` parameter.

        Returns
        -------
        logicalNegationOperator: ast.Not
            AST `object` representing the keyword '`not`' logical negation operator for use
            in `ast.UnaryOp`.
        """
))

docstrings[dictionaryIdentifiers[identifierToolClass]]['UAdd'] = Make.Expr(Make.Constant(
        """
        'UAdd', meaning 'Unary Addition', operator representing Python '`+`' operator.
        (AI generated docstring)

        Class `ast.UAdd` is a subclass of `ast.unaryop` and represents the unary positive
        operator '`+`' in Python source code. This operator explicitly indicates
        a positive numeric value. Used within `ast.UnaryOp` as the `op` parameter.

        Returns
        -------
        unaryPositiveOperator: ast.UAdd
            AST `object` representing the '`+`' unary positive operator for use
            in `ast.UnaryOp`.
        """
))

docstrings[dictionaryIdentifiers[identifierToolClass]]['USub'] = Make.Expr(Make.Constant(
        """
        'USub', meaning 'Unary Subtraction', operator representing Python '`-`' operator.
        (AI generated docstring)

        Class `ast.USub` is a subclass of `ast.unaryop` and represents the unary negation
        operator '`-`' in Python source code. This operator makes the arithmetic
        negative of its operand. Used within `ast.UnaryOp` as the `op` parameter.

        Returns
        -------
        unaryNegativeOperator: ast.USub
            AST `object` representing the '`-`' unary negation operator for use
            in `ast.UnaryOp`.
        """
))

docstrings[dictionaryIdentifiers[identifierToolClass]]['Attribute'] = Make.Expr(Make.Constant(
        """
        Attribute access AST `object` representing dot notation in Python code.
        (AI generated docstring)

        The `ast.Attribute` `object` represents attribute access using dot notation, such as
        `object.attribute` or chained access like `module.class.method`. This method
        supports chaining multiple attributes by passing additional attribute names.

        Parameters:
            value: The base expression before the first dot, typically an `ast.Name` or another expression.
            attribute: One or more attribute names to chain together with dot notation.
            context (ast.Load()): The expression context determining how the attribute is used.

        Returns
        -------
        attributeAccess: ast.Attribute
            AST `object` representing attribute access with potential chaining.

        Examples
        --------
        ```python
        # Makes AST equivalent to: `module.function`
        simpleAttribute = Make.Attribute(Make.Name('module'), 'function')

        # Makes AST equivalent to: `self.config.database.host`
        chainedAttribute = Make.Attribute(Make.Name('self'), 'config', 'database', 'host')
        ```
        """
))

docstrings[dictionaryIdentifiers[identifierToolClass]]['Await'] = Make.Expr(Make.Constant(
        """
        Await expression AST `object` for asynchronous operations.
        (AI generated docstring)

        The `ast.Await` `object` represents the keyword `await` used with asynchronous
        expressions in Python. It can only be used within async functions and
        suspends execution until the awaited coroutine completes.

        Parameters:
            value: The expression to await, typically a coroutine or awaitable `object`.

        Returns
        -------
        awaitExpression: ast.Await
            AST `object` representing an await expression for asynchronous code.
        """
))

docstrings[dictionaryIdentifiers[identifierToolClass]]['BinOp'] = Make.Expr(Make.Constant(
        """
        Binary operation AST `object` representing operators between two expressions.
        (AI generated docstring)

        The `ast.BinOp` `object` represents binary operations like addition, subtraction,
        multiplication, and other two-operand operations. The operation type is
        determined by the `op` parameter using specific operator classes.

        Parameters:
            left: The left-hand operand expression.
            op: The binary operator, such as `ast.Add()`, `ast.Sub()`, `ast.Mult()`, etc.
            right: The right-hand operand expression.

        Returns
        -------
        binaryOperation: ast.BinOp
            AST `object` representing a binary operation between two expressions.
        """
))

docstrings[dictionaryIdentifiers[identifierToolClass]]['BoolOp'] = Make.Expr(Make.Constant(
        """
        Boolean operation AST `object` for logical operations with multiple operands.
        (AI generated docstring)

        The `ast.BoolOp` `object` represents boolean operations like keywords `and` and `or` that
        can operate on multiple expressions. Unlike binary operators, boolean operations
        can chain multiple values together efficiently.

        Parameters:
            op: The boolean operator, either `ast.And()` or `ast.Or()`.
            values: Sequence of expressions to combine with the boolean operator.

        Returns
        -------
        booleanOperation: ast.BoolOp
            AST `object` representing a boolean operation with multiple operands.
        """
))

docstrings[dictionaryIdentifiers[identifierToolClass]]['Call'] = Make.Expr(Make.Constant(
        """
        Function call AST `object` representing function invocation with arguments.
        (AI generated docstring)

        The `ast.Call` `object` represents function calls, method calls, and constructor
        invocations. It supports both positional and keyword arguments and handles
        various calling conventions including unpacking operators.

        Parameters:
            callee: The callable expression, typically a function name or method access.
            listParameters ([]): Sequence of positional argument expressions.
            list_keyword ([]): Sequence of keyword arguments as `ast.keyword`.

        Returns
        -------
        functionCall: ast.Call
            AST `object` representing a function call with specified arguments.
        """
))

docstrings[dictionaryIdentifiers[identifierToolClass]]['Compare'] = Make.Expr(Make.Constant(
        """
        Comparison AST `object` for chained comparison operations.
        (AI generated docstring)

        The `ast.Compare` `object` represents comparison operations including equality,
        inequality, and ordering comparisons. It supports chained comparisons like
        `a < b <= c` through sequences of operators and comparators.

        All comparison operators: `ast.Eq`, `ast.NotEq`, `ast.Lt`, `ast.LtE`,
        `ast.Gt`, `ast.GtE`, `ast.Is`, `ast.IsNot`, `ast.In`, `ast.NotIn`.

        Parameters:
            left: The leftmost expression in the comparison chain.
            ops: Sequence of comparison operators from the complete list above.
            comparators: Sequence of expressions to compare against, one for each operator.

        Returns
        -------
        comparison: ast.Compare
            AST `object` representing a comparison operation with potential chaining.

        Examples
        --------
        ```python
        # Makes AST equivalent to: `x == 42`
        equality = Make.Compare(
            left=Make.Name('x'),
            ops=[Make.Eq()],
            comparators=[Make.Constant(42)]
        )

        # Makes AST equivalent to: `0 <= value < 100`
        rangeCheck = Make.Compare(
            left=Make.Constant(0),
            ops=[Make.LtE(), Make.Lt()],
            comparators=[Make.Name('value'), Make.Constant(100)]
        )
        ```
        """
))

docstrings[dictionaryIdentifiers[identifierToolClass]]['Constant'] = Make.Expr(Make.Constant(
        """
        Constant value AST `object` for literal values in Python code.
        (AI generated docstring)

        The `ast.Constant` `object` represents literal constant values like numbers,
        strings, booleans, and None. It replaces the deprecated specific literal
        and provides a unified representation for all constant values.

        Parameters:
            value: The constant value (int, float, str, bool, None, bytes, etc.).
            kind (None): Optional string hint for specialized constant handling.

        Returns
        -------
        constantValue: ast.Constant
            AST `object` representing a literal constant value.
        """
))

docstrings[dictionaryIdentifiers[identifierToolClass]]['Dict'] = Make.Expr(Make.Constant(
        """
        Dictionary literal AST `object` with key-value pairs.
        (AI generated docstring)

        The `ast.Dict` `object` represents dictionary literals using curly brace notation.
        It supports both regular key-value pairs and dictionary unpacking operations
        where keys can be None to indicate unpacking expressions.

        Parameters:
            keys ([None]): Sequence of key expressions or None for unpacking operations.
            values ([]): Sequence of value expressions corresponding to the keys.

        Returns
        -------
        dictionaryLiteral: ast.Dict
            AST `object` representing a dictionary literal with specified key-value pairs.
        """
))

docstrings[dictionaryIdentifiers[identifierToolClass]]['DictComp'] = Make.Expr(Make.Constant(
        """
        Dictionary comprehension AST `object` for dynamic dictionary construction.
        (AI generated docstring)

        The `ast.DictComp` `object` represents dictionary comprehensions that make
        dictionaries using iterator expressions. It combines key-value generation
        with filtering and nested iteration capabilities.

        Parameters:
            key: Expression that generates dictionary keys.
            value: Expression that generates dictionary values.
            generators: Sequence of `ast.comprehension` defining iteration and filtering.

        Returns
        -------
        dictionaryComprehension: ast.DictComp
            AST `object` representing a dictionary comprehension expression.

        Examples
        --------
        ```python
        # Makes AST equivalent to: `{x: x**2 for x in range(10)}`
        squares = Make.DictComp(
            key=Make.Name('x'),
            value=Make.BinOp(Make.Name('x'), Make.Pow(), Make.Constant(2)),
            generators=[Make.comprehension(
                target=Make.Name('x'),
                iter=Make.Call(Make.Name('range'), [Make.Constant(10)]),
                ifs=[]
            )]
        )
        ```
        """
))

docstrings[dictionaryIdentifiers[identifierToolClass]]['FormattedValue'] = Make.Expr(Make.Constant(
        """
        Formatted value AST `object` for f-string interpolation components.
        (AI generated docstring)

        The `ast.FormattedValue` `object` represents individual expressions within
        f-string literals, including format specifications and conversion options.
        It handles the interpolation mechanics of formatted string literals.

        Parameters:
            value: The expression to be formatted and interpolated.
            conversion: Conversion flag (0=no conversion, 115='s', 114='r', 97='a').
            format_spec (None): Optional format specification expression.

        Returns
        -------
        formattedValue: ast.FormattedValue
            AST `object` representing a formatted value within an f-string expression.

        Examples
        --------
        ```python
        # Makes component for f-string: f"Value: {variable}"
        simpleFormatted = Make.FormattedValue(
            value=Make.Name('variable'),
            conversion=0
        )

        # Makes component for f-string: f"Debug: {obj!r:.2f}"
        complexFormatted = Make.FormattedValue(
            value=Make.Name('obj'),
            conversion=114,  # 'r' for repr()
            format_spec=Make.Constant('.2f')
        )
        ```
        """
))

docstrings[dictionaryIdentifiers[identifierToolClass]]['GeneratorExp'] = Make.Expr(Make.Constant(
        """
        Generator ***expr***ession object for memory-efficient iteration.
        (AI generated docstring)

        The `ast.GeneratorExp` object represents generator expressions that create
        iterator objects without constructing intermediate collections. It provides
        lazy evaluation and memory efficiency for large datasets.

        Parameters:
            element: Expression that generates each element of the generator.
            generators: Sequence of `ast.comprehension` objects defining iteration and filtering.

        Returns
        -------
        generatorExpression: ast.GeneratorExp
            AST object representing a generator expression for lazy evaluation.

        Examples
        --------
        ```python
        # Creates AST equivalent to: `(x*2 for x in numbers if x > 0)`
        doubledPositive = Make.GeneratorExp(
            element=Make.BinOp(Make.Name('x'), Make.Mult(), Make.Constant(2)),
            generators=[Make.comprehension(
                target=Make.Name('x'),
                iter=Make.Name('numbers'),
                ifs=[Make.Compare(Make.Name('x'), [Make.Gt()], [Make.Constant(0)])]
            )]
        )
        ```
        """
))

docstrings[dictionaryIdentifiers[identifierToolClass]]['IfExp'] = Make.Expr(Make.Constant(
        """
        Conditional ***expr***ession `object` for inline if-else operations.
        (AI generated docstring)

        The `ast.IfExp` `object` represents conditional expressions using the ternary
        operator syntax `value_if_true if condition else value_if_false`. It
        provides inline conditional logic without full if-statement structures.

        Parameters:
            test: The condition expression to evaluate for truthiness.
            body: Expression to return when the condition is true.
            orElse: Expression to return when the condition is false.

        Returns:
            conditionalExpression: ast.IfExp
                AST `object` representing an inline conditional expression.

        Examples:
            ```python
            # Creates AST equivalent to: `"positive" if x > 0 else "non-positive"`
            signDescription = Make.IfExp(
                test=Make.Compare(Make.Name('x'), [Make.Gt()], [Make.Constant(0)]),
                body=Make.Constant("positive"),
                orElse=Make.Constant("non-positive")
            )

            # Creates AST equivalent to: `max_value if enabled else default_value`
            conditionalValue = Make.IfExp(
                test=Make.Name('enabled'),
                body=Make.Name('max_value'),
                orElse=Make.Name('default_value')
            )
            ```
        """
))

docstrings[dictionaryIdentifiers[identifierToolClass]]['JoinedStr'] = Make.Expr(Make.Constant(
        """
        Joined string `object` for f-string literal construction.
        (AI generated docstring)

        The `ast.JoinedStr` `object` represents f-string literals that combine constant
        text with interpolated expressions. It coordinates multiple string components
        and formatted values into a single string literal.

        Parameters:
            values: Sequence of string components, including `ast.Constant` and `ast.FormattedValue` objects.

        Returns
        -------
        joinedString: ast.JoinedStr
            AST `object` representing an f-string literal with interpolated values.

        Examples
        --------
        ```python
        # Creates AST equivalent to: f"Hello, {name}!"
        greeting = Make.JoinedStr([
            Make.Constant("Hello, "),
            Make.FormattedValue(Make.Name('name'), 0),
            Make.Constant("!")
        ])

        # Creates AST equivalent to: f"Result: {value:.2f} ({status})"
        report = Make.JoinedStr([
            Make.Constant("Result: "),
            Make.FormattedValue(Make.Name('value'), 0, Make.Constant('.2f')),
            Make.Constant(" ("),
            Make.FormattedValue(Make.Name('status'), 0),
            Make.Constant(")")
        ])
        ```
        """
))

docstrings[dictionaryIdentifiers[identifierToolClass]]['Lambda'] = Make.Expr(Make.Constant(
        """
        Lambda function `object` for anonymous function expressions.
        (AI generated docstring)

        The `ast.Lambda` `object` represents lambda expressions that define anonymous
        functions with a single expression body. Lambda functions are limited to
        expressions and cannot contain statements or multiple lines.

        Parameters:
            argumentSpecification: The function arguments specification as `ast.arguments`.
            body: Single expression that forms the lambda function body.

        Returns:
            lambdaFunction: ast.Lambda
                AST `object` representing an anonymous lambda function expression.
        """
))

docstrings[dictionaryIdentifiers[identifierToolClass]]['List'] = Make.Expr(Make.Constant(
        """
        List literal `object` with ordered element collection.
        (AI generated docstring)

        The `ast.List` `object` represents list literals using square bracket notation.
        It creates ordered, mutable collections and supports various contexts like
        loading values, storing to variables, or deletion operations.

        Parameters:
            listElements ([]): Sequence of expressions that become list elements.
            context (ast.Load()): Expression context for how the list is used.

        Returns:
            listLiteral: ast.List
            AST `object` representing a list literal with specified elements.
        """
))

docstrings[dictionaryIdentifiers[identifierToolClass]]['ListComp'] = Make.Expr(Make.Constant(
        """
        List ***c***o***mp***rehension `object` for dynamic list construction.
        (AI generated docstring)

        The `ast.ListComp` `object` represents list comprehensions that create lists
        using iterator expressions. It provides concise syntax for filtering and
        transforming collections into new lists.

        Parameters:
            element: Expression that generates each element of the resulting list.
            generators: Sequence of `ast.comprehension` objects defining iteration and filtering.

        Returns:
            listComprehension: ast.ListComp
            AST `object` representing a list comprehension expression.
        """
))

docstrings[dictionaryIdentifiers[identifierToolClass]]['Name'] = Make.Expr(Make.Constant(
        """
        Name `object` for variable and identifier references.
        (AI generated docstring)

        The `ast.Name` `object` represents identifiers like variable names, function names,
        and class names in Python code. The context parameter determines whether the
        name is being loaded, stored to, or deleted.

        Parameters:
            id: The identifier string representing the name.
            context (ast.Load()): Expression context specifying how the name is used.

        Returns:
            nameReference: ast.Name
            AST `object` representing an identifier reference with specified context.
        """
))

docstrings[dictionaryIdentifiers[identifierToolClass]]['NamedExpr'] = Make.Expr(Make.Constant(
        """
        Named ***expr***ession `object` for assignment expressions (walrus operator).
        (AI generated docstring)

        The `ast.NamedExpr` `object` represents assignment expressions using the walrus
        operator `:=` introduced in Python 3.8. It allows assignment within expressions
        and is commonly used in comprehensions and conditional statements.

        Parameters:
            target: The `ast.Name` `object` representing the variable being assigned to.
            value: The expression whose value is assigned to the target.

        Returns:
            namedExpression: ast.NamedExpr
            AST `object` representing an assignment expression with the walrus operator.

        Examples:
            ```python
            # Creates AST equivalent to: `(length := len(data)) > 10`
            lengthCheck = Make.Compare(
                left=Make.NamedExpr(
                    target=Make.Name('length', ast.Store()),
                    value=Make.Call(Make.Name('len'), [Make.Name('data')])
                ),
                ops=[Make.Gt()],
                comparators=[Make.Constant(10)]
            )
            ```
        """
))

docstrings[dictionaryIdentifiers[identifierToolClass]]['Set'] = Make.Expr(Make.Constant(
        """
        Set literal `object` for unordered unique element collections.
        (AI generated docstring)

        The `ast.Set` `object` represents set literals using curly brace notation.
        It creates unordered collections of unique elements with efficient
        membership testing and set operations.

        Parameters:
            listElements ([]): Sequence of expressions that become set elements.

        Returns:
            setLiteral: ast.Set
            AST `object` representing a set literal with specified unique elements.
        """
))

docstrings[dictionaryIdentifiers[identifierToolClass]]['SetComp'] = Make.Expr(Make.Constant(
        """
        Set ***c***o***mp***rehension `object` for dynamic set construction.
        (AI generated docstring)

        The `ast.SetComp` `object` represents set comprehensions that create sets
        using iterator expressions. It automatically handles uniqueness while
        providing concise syntax for filtering and transforming collections.

        Parameters:
            element: Expression that generates each element of the resulting set.
            generators: Sequence of `ast.comprehension` objects defining iteration and filtering.

        Returns:
            setComprehension: ast.SetComp
            AST `object` representing a set comprehension expression.
        """
))

docstrings[dictionaryIdentifiers[identifierToolClass]]['Slice'] = Make.Expr(Make.Constant(
        """
        Slice `object` for sequence slicing operations.
        (AI generated docstring)

        The `ast.Slice` `object` represents slice expressions used with subscription
        operations to extract subsequences from collections. It supports the full
        Python slicing syntax with optional start, stop, and step parameters.

        Parameters:
            lower (None): Optional expression for slice start position.
            upper (None): Optional expression for slice end position.
            step (None): Optional expression for slice step size.

        Returns:
            sliceExpression: ast.Slice
            AST `object` representing a slice operation for sequence subscripting.
        """
))

docstrings[dictionaryIdentifiers[identifierToolClass]]['Starred'] = Make.Expr(Make.Constant(
        """
        Starred ***expr***ession `object` for unpacking operations.
        (AI generated docstring)

        The `ast.Starred` `object` represents starred expressions using the `*` operator
        for unpacking iterables in various contexts like function calls, assignments,
        and collection literals.

        Parameters:
            value: The expression to be unpacked with the star operator.
            context (ast.Load()): Expression context determining how the starred expression is used.

        Returns:
            starredExpression: ast.Starred
            AST `object` representing a starred expression for unpacking operations.

        Examples:
            ```python
            # Creates AST equivalent to: `*args` in function call
            unpackArgs = Make.Starred(Make.Name('args'))

            # Creates AST equivalent to: `*rest` in assignment like `first, *rest = items`
            unpackRest = Make.Starred(Make.Name('rest'), ast.Store())
            ```
        """
))

docstrings[dictionaryIdentifiers[identifierToolClass]]['Subscript'] = Make.Expr(Make.Constant(
        """
        Subscript `object` for indexing and slicing operations.
        (AI generated docstring)

        The `ast.Subscript` `object` represents subscription operations using square
        brackets for indexing, slicing, and key access in dictionaries and other
        subscriptable objects.

        Parameters:
            value: The expression being subscripted (e.g., list, dict, string).
            slice: The subscript expression, which can be an index, slice, or key.
            context (ast.Load()): Expression context for how the subscript is used.

        Returns:
            subscriptExpression: ast.Subscript
            AST `object` representing a subscription operation with brackets.
        """
))

docstrings[dictionaryIdentifiers[identifierToolClass]]['Tuple'] = Make.Expr(Make.Constant(
        """
        Tuple literal `object` for ordered immutable collections.
        (AI generated docstring)

        The `ast.Tuple` `object` represents tuple literals using parentheses or comma
        separation. Tuples are immutable, ordered collections often used for
        multiple assignments and function return values.

        Parameters:
            listElements ([]): Sequence of expressions that become tuple elements.
            context (ast.Load()): Expression context for how the tuple is used.

        Returns:
            tupleLiteral: ast.Tuple
            AST `object` representing a tuple literal with specified elements.
        """
))

docstrings[dictionaryIdentifiers[identifierToolClass]]['UnaryOp'] = Make.Expr(Make.Constant(
        """
        Unary ***op***eration `object` for single-operand operations.
        (AI generated docstring)

        The `ast.UnaryOp` `object` represents unary operations that take a single operand,
        such as negation, logical not, bitwise inversion, and positive sign operations.

        Parameters:
            op: The unary operator like `ast.UAdd()`, `ast.USub()`, `ast.Not()`, `ast.Invert()`.
            operand: The expression that the unary operator is applied to.

        Returns:
            unaryOperation: ast.UnaryOp
            AST `object` representing a unary operation on a single expression.
        """
))

docstrings[dictionaryIdentifiers[identifierToolClass]]['Yield'] = Make.Expr(Make.Constant(
        """
        Yield ***expr***ession `object` for generator function values.
        (AI generated docstring)

        The `ast.Yield` `object` represents yield expressions that produce values in
        generator functions. It suspends function execution and yields a value
        to the caller, allowing resumption from the same point.

        Parameters:
            value (None): Optional expression to yield; None yields None value.

        Returns:
            yieldExpression: ast.Yield
            AST `object` representing a yield expression for generator functions.
        """
))

docstrings[dictionaryIdentifiers[identifierToolClass]]['YieldFrom'] = Make.Expr(Make.Constant(
        """
        Yield from ***expr***ession `object` for delegating to sub-generators.
        (AI generated docstring)

        The `ast.YieldFrom` `object` represents `yield from` expressions that delegate
        generator execution to another iterable or generator. It provides efficient
        sub-generator delegation introduced in Python 3.3.

        Parameters:
            value: The iterable or generator expression to delegate to.

        Returns:
            yieldFromExpression: ast.YieldFrom
            AST `object` representing a yield from expression for generator delegation.
        """
))

docstrings[dictionaryIdentifiers[identifierToolClass]]['expr'] = Make.Expr(Make.Constant(
        """
        Abstract ***expr***ession `object` for base expression operations.
        (AI generated docstring)

        The `ast.expr` class serves as the abstract base class for all expression
        objects in Python's AST. Unlike `ast.stmt` which represents statements that
        perform actions, `ast.expr` represents expressions that evaluate to values
        and can be used within larger expressions or as parts of statements.

        Expressions vs Statements:
        - **expr**: Evaluates to a value and can be composed into larger expressions.
          Examples include literals (`42`, `"hello"`), operations (`x + y`),
          function calls (`len(data)`), and attribute access (`obj.method`).
        - **stmt**: Performs an action and does not evaluate to a usable value.
          Examples include assignments (`x = 5`), control flow (`if`, `for`, `while`),
          function definitions (`def`), and imports (`import`).

        Returns
        -------
        expression: ast.expr
            Abstract expression `object` that serves as the base class for all
            Python expressions in AST structures.
        """
))
