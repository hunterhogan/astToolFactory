from astToolkit import Be, ClassIsAndAttribute, DOT, Grab, IfThis, Make, NodeTourist, parseLogicalPath2astModule, Then
import ast

dictionaryClass2Delimiters = {}

astModule = parseLogicalPath2astModule('ast')

# Find the _Unparser class
unparserClass = NodeTourist(
    IfThis.isClassDefIdentifier('_Unparser'),
    Then.extractIt
).captureLastMatch(astModule)

def startsWithVisit(methodName):
    if isinstance(methodName, str):
        return methodName.startswith('visit_')
    return False

print(f"Found _Unparser class: {unparserClass is not None}")

if unparserClass:
    # Find all visit methods that contain delimit calls
    visitMethods = []
    NodeTourist(
        ClassIsAndAttribute.nameIs(ast.FunctionDef, startsWithVisit),
        Then.appendTo(visitMethods)
    ).visit(unparserClass)

    print(f"Found {len(visitMethods)} visit methods")

    # For each visit method, find delimit calls and extract delimiters
    for visitMethod in visitMethods:
        # Extract the AST class name from method name (visit_DictComp -> DictComp)
        astClassName = DOT.name(visitMethod)[6:]  # Remove 'visit_' prefix

        # Find calls to 'delimit' in this method
        delimitCalls = []
        NodeTourist(
            ClassIsAndAttribute.funcIs(ast.Call, IfThis.isNameIdentifier('delimit')),
            Then.appendTo(delimitCalls)
        ).visit(visitMethod)

        if delimitCalls:
            print(f"Found delimit calls in {DOT.name(visitMethod)}")

        # Extract delimiters from the first delimit call found
        if delimitCalls:
            delimitCall = delimitCalls[0]
            callArgs = DOT.args(delimitCall)
            if len(callArgs) >= 2:
                # Extract string values from the first two arguments
                startDelim = None
                endDelim = None

                if Be.Constant(callArgs[0]):
                    startDelim = DOT.value(callArgs[0])
                if Be.Constant(callArgs[1]):
                    endDelim = DOT.value(callArgs[1])

                if startDelim is not None and endDelim is not None:
                    dictionaryClass2Delimiters[astClassName] = (startDelim, endDelim)
                    print(f"Added {astClassName}: {(startDelim, endDelim)}")

print(f"Final dictionary has {len(dictionaryClass2Delimiters)} entries")