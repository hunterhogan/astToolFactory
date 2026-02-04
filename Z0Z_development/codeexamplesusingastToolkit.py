from astToolkit import (
	Be, DOT, Grab, identifierDotAttribute, IfThis, IngredientsFunction, Make, NodeChanger, NodeTourist, Then)
from collections.abc import Callable, Sequence
from typing import cast, TypeIs
from Z0Z_tools import autoDecodingRLE, raiseIfNone
import ast

# code examples using astToolkit
ingredientsTarget= IngredientsFunction(Make.FunctionDef('targetCallableIdentifier'))
ingredientsCaller= IngredientsFunction(Make.FunctionDef('targetCallableIdentifier'))
ingredientsFunction= IngredientsFunction(Make.FunctionDef('targetCallableIdentifier'))
ingredientsCount= IngredientsFunction(Make.FunctionDef('targetCallableIdentifier'))
unRepackDataclass= IngredientsFunction(Make.FunctionDef('targetCallableIdentifier'))
ingredientsFunctionDispatcher= IngredientsFunction(Make.FunctionDef('targetCallableIdentifier'))
# --

# Find annoted assignment to identifer, get the annotation
findThis: Callable[[ast.AST], TypeIs[ast.AnnAssign] | bool] = Be.AnnAssign.targetIs(IfThis.isNameIdentifier(self.name))
doThat: Callable[[ast.AnnAssign], ast.Name] = Then.extractIt(DOT.annotation)
self.astAnnotation = raiseIfNone(NodeTourist[ast.AnnAssign, ast.Name](findThis, doThat).captureLastMatch(dataclassClassDef))

# Type "Overload[(node: hasDOTannotation_expr) -> expr, (node: hasDOTannotation_exprOrNone) -> (expr | None)]" is not assignable to declared type "(AnnAssign) -> Name"
#   No overloaded function matches type "(AnnAssign) -> Name"

#--

# change return
changeReturnCallable: NodeChanger[ast.Return, ast.Return] = NodeChanger(Be.Return, Then.replaceWith(Make.Return(shatteredDataclass.fragments4AssignmentOrParameters)))
changeReturnCallable.visit(ingredientsTarget.astFunctionDef)

#--

# Find Assign that calls a function, replace the assignment, insert statements before, insert statements after.
astCallTargetCallable: ast.Call = Make.Call(Make.Name(targetCallableIdentifier), shatteredDataclass.listName4Parameters)
replaceAssignTargetCallable: NodeChanger[ast.Assign, ast.Assign] = NodeChanger(Be.Assign.valueIs(IfThis.isCallIdentifier(targetCallableIdentifier)), Then.replaceWith(Make.Assign([shatteredDataclass.fragments4AssignmentOrParameters], value=astCallTargetCallable)))
unpack4targetCallable: NodeChanger[ast.Assign, Sequence[ast.AST]] = NodeChanger(Be.Assign.valueIs(IfThis.isCallIdentifier(targetCallableIdentifier)), Then.insertThisAbove(shatteredDataclass.listUnpack))
repack4targetCallable: NodeChanger[ast.Assign, Sequence[ast.AST]] = NodeChanger(Be.Assign.valueIs(IfThis.isCallIdentifier(targetCallableIdentifier)), Then.insertThisBelow([shatteredDataclass.repack]))
replaceAssignTargetCallable.visit(ingredientsCaller.astFunctionDef)
unpack4targetCallable.visit(ingredientsCaller.astFunctionDef)
repack4targetCallable.visit(ingredientsCaller.astFunctionDef)

#--

# get list of all ast.Name.id
listName: list[ast.Name] = []
NodeTourist(Be.Name, Then.appendTo(listName)).visit(ingredientsFunction.astFunctionDef)
listIdentifiers: list[str] = [astName.id for astName in listName]
listIdentifiersNotUsed: list[str] = list(set(list_arg_arg) - set(listIdentifiers))

#--

# Find a very specific statement and replace with another complicated statement and change the return statement.
findThis: Callable[[ast.AST], TypeIs[ast.AugAssign] | bool] = Be.AugAssign.targetIs(IfThis.isNameIdentifier(job.shatteredDataclass.countingVariableName.id))
doThat: Callable[[ast.AugAssign], ast.Expr] = Then.replaceWith(Make.Expr(Make.Call(Make.Attribute(Make.Name(spices.numbaProgressBarIdentifier),'update'),[Make.Constant(1)])))
countWithProgressBar: NodeChanger[ast.AugAssign, ast.Expr] = NodeChanger(findThis, doThat)
countWithProgressBar.visit(ingredientsFunction.astFunctionDef)

removeReturnStatement: NodeChanger[ast.Return, None] = NodeChanger(Be.Return, Then.removeIt)
removeReturnStatement.visit(ingredientsFunction.astFunctionDef)
ingredientsFunction.astFunctionDef.returns = Make.Constant(value=None)

#--

def move_arg2FunctionDefDOTbodyAndAssignInitialValues(ingredientsFunction: IngredientsFunction, job: RecipeJobTheorem2Numba) -> IngredientsFunction:
	ingredientsFunction.imports.update(job.shatteredDataclass.imports)

	list_argCuzMyBrainRefusesToThink: list[ast.arg] = ingredientsFunction.astFunctionDef.args.args + ingredientsFunction.astFunctionDef.args.posonlyargs + ingredientsFunction.astFunctionDef.args.kwonlyargs
	list_arg_arg: list[str] = [ast_arg.arg for ast_arg in list_argCuzMyBrainRefusesToThink]
	listName: list[ast.Name] = []
	NodeTourist(Be.Name, Then.appendTo(listName)).visit(ingredientsFunction.astFunctionDef)
	listIdentifiers: list[str] = [astName.id for astName in listName]
	listIdentifiersNotUsed: list[str] = list(set(list_arg_arg) - set(listIdentifiers))

	for ast_arg in list_argCuzMyBrainRefusesToThink:
		if ast_arg.arg in job.shatteredDataclass.field2AnnAssign:
			if ast_arg.arg in listIdentifiersNotUsed:
				pass
			else:
				ImaAnnAssign, elementConstructor = job.shatteredDataclass.Z0Z_field2AnnAssign[ast_arg.arg]
				match elementConstructor:
					case 'scalar':
						cast(ast.Constant, cast(ast.Call, ImaAnnAssign.value).args[0]).value = int(job.state.__dict__[ast_arg.arg])
					case 'array':
						dataAsStrRLE: str = autoDecodingRLE(job.state.__dict__[ast_arg.arg], True)
						dataAs_astExpr: ast.expr = cast(ast.Expr, ast.parse(dataAsStrRLE).body[0]).value
						cast(ast.Call, ImaAnnAssign.value).args = [dataAs_astExpr]
					case _:
						list_exprDOTannotation: list[ast.expr] = []
						list_exprDOTvalue: list[ast.expr] = []
						for dimension in job.state.mapShape:
							list_exprDOTannotation.append(Make.Name(elementConstructor))
							list_exprDOTvalue.append(Make.Call(Make.Name(elementConstructor), [Make.Constant(dimension)]))
						cast(ast.Tuple, cast(ast.Subscript, cast(ast.AnnAssign, ImaAnnAssign).annotation).slice).elts = list_exprDOTannotation
						cast(ast.Tuple, ImaAnnAssign.value).elts = list_exprDOTvalue

				ingredientsFunction.astFunctionDef.body.insert(0, ImaAnnAssign)

			findThis: Callable[[ast.AST], TypeIs[ast.arg] | bool] = IfThis.is_argIdentifier(ast_arg.arg)
			remove_arg: NodeChanger[ast.arg, None] = NodeChanger(findThis, Then.removeIt)
			remove_arg.visit(ingredientsFunction.astFunctionDef)

	ast.fix_missing_locations(ingredientsFunction.astFunctionDef)
	return ingredientsFunction

#--

# Remove one identifier from 10-20 Assign targets
findThis = Be.Assign.targetsIs(lambda list_expr: any([IfThis.isSubscriptIdentifier('foldGroups')(node) for node in list_expr ]))
remove_foldGroups: NodeChanger[ast.Name, None] = NodeChanger(findThis, Then.removeIt)
remove_foldGroups.visit(ingredientsCount.astFunctionDef)

#---

# Replace variable identifiers with their dynamically determined values
listIdentifiersStaticValues: list[str] = listIdentifiersStaticValuesHARDCODED
for identifier in listIdentifiersStaticValues:
    findThis: Callable[[ast.AST], TypeIs[ast.Name] | bool] = IfThis.isNameIdentifier(identifier)
    doThat: Callable[[ast.Name], ast.Constant] = Then.replaceWith(Make.Constant(int(job.state.__dict__[identifier])))
    NodeChanger(findThis, doThat).visit(ingredientsCount.astFunctionDef)

#--

changeReturnParallelCallable: NodeChanger[ast.Return, ast.Return] = NodeChanger(Be.Return, Then.replaceWith(Make.Return(job.shatteredDataclass.countingVariableName)))
changeReturnParallelCallable.visit(ingredientsCount.astFunctionDef)

#--
# get identifier from function's only argument, then update while test in the body, using a custom function added to `IfThis`
dataclassInstanceIdentifier: identifierDotAttribute = raiseIfNone(NodeTourist(Be.arg, Then.extractIt(DOT.arg)).captureLastMatch(ingredientsFunction.astFunctionDef))
theCountingIdentifier: identifierDotAttribute = theCountingIdentifierDEFAULT

findThisZ = IfThis.isWhileAttributeNamespaceIdentifierGreaterThan0(dataclassInstanceIdentifier, 'leaf1ndex')
doThatZ: Callable[[ast.While], ast.While] = Grab.testAttribute(Grab.andDoAllOf([Grab.opsAttribute(Then.replaceWith([ast.Eq()])), Grab.leftAttribute(Grab.attrAttribute(Then.replaceWith(theCountingIdentifier)))]))
NodeChanger(findThis, doThat).visit(ingredientsFunction.astFunctionDef.body[0])

#--

astTuple: ast.Tuple = raiseIfNone(NodeTourist[ast.Return, ast.Tuple | None](Be.Return, Then.extractIt(DOT.value)).captureLastMatch(ingredientsFunction.astFunctionDef))
astTuple.ctx = ast.Store()

findThis: Callable[[ast.AST], TypeIs[ast.Assign] | bool] = Be.Assign.valueIs(IfThis.isCallIdentifier(targetCallableIdentifier))
doThat = Then.replaceWith(Make.Assign([astTuple], value=Make.Call(Make.Name(targetCallableIdentifier), astTuple.elts)))
changeAssignCallToTarget = NodeChanger(findThis, doThat)
changeAssignCallToTarget.visit(ingredientsFunctionDispatcher.astFunctionDef)

# Argument of type "Overload[(node: hasDOTvalue_boolOrNone) -> (bool | None), (node: hasDOTvalue_ConstantValueType) -> ConstantValueType, (node: hasDOTvalue_expr) -> expr, (node: hasDOTvalue_exprOrNone) -> (expr | None)]" cannot be assigned to parameter "doThat" of type "(Return) -> (Tuple | None)" in function "__init__"
#   No overloaded function matches type "(Return) -> (Tuple | None)"

#--
findThis = Be.While.testIs(Be.Compare.leftIs(IfThis.isNameIdentifier('leafConnectee')))
captureCountGapsCodeBlock: NodeTourist[ast.While, Sequence[ast.stmt]] = NodeTourist(findThis, doThat = Then.extractIt(DOT.body))
countGapsCodeBlock: Sequence[ast.stmt] = raiseIfNone(captureCountGapsCodeBlock.captureLastMatch(ingredientsFunction.astFunctionDef))

thisIsMyTaskIndexCodeBlock = ast.If(ast.BoolOp(ast.Or()
    , values=[ast.Compare(ast.Name('leaf1ndex'), ops=[ast.NotEq()], comparators=[ast.Name('taskDivisions')])
            , ast.Compare(Make.Mod.join([ast.Name('leafConnectee'), ast.Name('taskDivisions')]), ops=[ast.Eq()], comparators=[ast.Name('taskIndex')])])
, body=list(countGapsCodeBlock[0:-1]))

countGapsCodeBlockNew: list[ast.stmt] = [thisIsMyTaskIndexCodeBlock, countGapsCodeBlock[-1]]
NodeChanger[ast.While, Sequence[ast.stmt]](findThis, doThat = Grab.bodyAttribute(Then.replaceWith(countGapsCodeBlockNew))).visit(ingredientsFunction.astFunctionDef)

# Argument of type "(hasDOTbody) -> hasDOTbody" cannot be assigned to parameter "doThat" of type "(While) -> Sequence[stmt]" in function "__init__"
#   Type "(hasDOTbody) -> hasDOTbody" is not assignable to type "(While) -> Sequence[stmt]"
#     Function return type "hasDOTbody" is incompatible with type "Sequence[stmt]"
#       Type "hasDOTbody" is not assignable to type "Sequence[stmt]"
#         "AsyncFor" is not assignable to "Sequence[stmt]"

#--

NodeChanger(
			findThis = Be.arg.annotationIs(IfThis.isNameIdentifier(dataclassIdentifier))
			, doThat = Grab.annotationAttribute(Grab.idAttribute(Then.replaceWith(dataclassIdentifierParallel)))
		).visit(unRepackDataclass.astFunctionDef)
unRepackDataclass.astFunctionDef.returns = Make.Name(dataclassIdentifierParallel)

# Argument of type "(AST) -> (TypeIs[Name] | bool)" cannot be assigned to parameter "attributeCondition" of type "(expr | None) -> bool" in function "annotationIs"
#   Type "(AST) -> (TypeIs[Name] | bool)" is not assignable to type "(expr | None) -> bool"
#     Parameter 1: type "expr | None" is incompatible with type "AST"
#       Type "expr | None" is not assignable to type "AST"
#         "None" is not assignable to "AST"

#--

astTuple: ast.expr = raiseIfNone(NodeTourist(Be.Return, Then.extractIt(DOT.value)).captureLastMatch(ingredientsFunction.astFunctionDef))
astTuple.ctx = ast.Store()
findThis: Callable[[ast.AST], TypeIs[ast.Assign] | bool] = Be.Assign.valueIs(IfThis.isCallIdentifier(targetCallableIdentifier))
doThat: Callable[[ast.Assign], ast.Assign] = Then.replaceWith(Make.Assign([astTuple], value=Make.Call(Make.Name(targetCallableIdentifier), astTuple.elts)))
changeAssignCallToTarget: NodeChanger[ast.Assign, ast.Assign] = NodeChanger(findThis, doThat)
changeAssignCallToTarget.visit(unRepackDataclass.astFunctionDef)
# Cannot assign to attribute "ctx" for class "expr"
#   Attribute "ctx" is unknown
# Type of "elts" is unknown
# Argument type is unknown
#   Argument corresponds to parameter "listParameters" in function "Call"
# Cannot access attribute "elts" for class "expr"
#   Attribute "elts" is unknown

#--

dataclassInstanceIdentifier: identifierDotAttribute = raiseIfNone(NodeTourist(Be.arg, Then.extractIt(DOT.arg)).captureLastMatch(ingredientsFunction.astFunctionDef))

findThis = IfThis.isWhileAttributeNamespaceIdentifierGreaterThan0(dataclassInstanceIdentifier, 'leaf1ndex')
doThat = Grab.testAttribute(Grab.comparatorsAttribute(Then.replaceWith([Make.Constant(4)])))
NodeChanger(findThis, doThat).visit(ingredientsFunction.astFunctionDef)

findThis = IfThis.isIfAttributeNamespaceIdentifierGreaterThan0(dataclassInstanceIdentifier, 'leaf1ndex')
doThat = Then.extractIt(DOT.body)
insertLeaf = NodeTourist(findThis, doThat).captureLastMatch(ingredientsFunction.astFunctionDef)
findThis = IfThis.isIfAttributeNamespaceIdentifierGreaterThan0(dataclassInstanceIdentifier, 'leaf1ndex')
doThat = Then.replaceWith(insertLeaf)
NodeChanger(findThis, doThat).visit(ingredientsFunction.astFunctionDef)

findThis = IfThis.isAttributeNamespaceIdentifierGreaterThan0(dataclassInstanceIdentifier, 'leaf1ndex')
doThat = Then.removeIt
NodeChanger(findThis, doThat).visit(ingredientsFunction.astFunctionDef)

findThis = IfThis.isAttributeNamespaceIdentifierLessThanOrEqual0(dataclassInstanceIdentifier, 'leaf1ndex')
doThat = Then.removeIt
NodeChanger(findThis, doThat).visit(ingredientsFunction.astFunctionDef)

theCountingIdentifier: identifierDotAttribute = theCountingIdentifierDEFAULT
doubleTheCount: ast.AugAssign = Make.AugAssign(Make.Attribute(ast.Name(dataclassInstanceIdentifier), theCountingIdentifier), ast.Mult(), Make.Constant(2))
findThis = Be.Return
doThat = Then.insertThisAbove([doubleTheCount])
NodeChanger(findThis, doThat).visit(ingredientsFunction.astFunctionDef)

#--

dataclassInstanceIdentifier: identifierDotAttribute = raiseIfNone(NodeTourist(Be.arg, Then.extractIt(DOT.arg)).captureLastMatch(ingredientsFunction.astFunctionDef))

findThis = IfThis.isIfUnaryNotAttributeNamespaceIdentifier(dataclassInstanceIdentifier, 'dimensionsUnconstrained')
doThat = Then.removeIt
NodeChanger(findThis, doThat).visit(ingredientsFunction.astFunctionDef)

#--

def findDataclass(ingredientsFunction: IngredientsFunction) -> tuple[str, str, str]:

	dataclassName: ast.expr = raiseIfNone(NodeTourist(Be.arg, Then.extractIt(DOT.annotation)).captureLastMatch(ingredientsFunction.astFunctionDef))
	dataclassIdentifier: str = raiseIfNone(NodeTourist(Be.Name, Then.extractIt(DOT.id)).captureLastMatch(dataclassName))
	dataclassLogicalPathModule = None
	for moduleWithLogicalPath, listNameTuples in ingredientsFunction.imports._dictionaryImportFrom.items():
		for nameTuple in listNameTuples:
			if nameTuple[0] == dataclassIdentifier:
				dataclassLogicalPathModule = moduleWithLogicalPath
				break
		if dataclassLogicalPathModule:
			break
	dataclassInstanceIdentifier: identifierDotAttribute = raiseIfNone(NodeTourist(Be.arg, Then.extractIt(DOT.arg)).captureLastMatch(ingredientsFunction.astFunctionDef))
	return raiseIfNone(dataclassLogicalPathModule), dataclassIdentifier, dataclassInstanceIdentifier

#--

dataclassName: ast.expr = raiseIfNone(NodeTourist(Be.arg, Then.extractIt(DOT.annotation)).captureLastMatch(ingredientsFunction.astFunctionDef))
dataclassIdentifier: str = raiseIfNone(NodeTourist(Be.Name, Then.extractIt(DOT.id)).captureLastMatch(dataclassName))

dataclassLogicalPathModule = None
for moduleWithLogicalPath, listNameTuples in ingredientsFunction.imports._dictionaryImportFrom.items():
    for nameTuple in listNameTuples:
        if nameTuple[0] == dataclassIdentifier:
            dataclassLogicalPathModule = moduleWithLogicalPath
            break
    if dataclassLogicalPathModule:
        break
if dataclassLogicalPathModule is None:
    raise Exception
dataclassInstanceIdentifier: identifierDotAttribute = raiseIfNone(NodeTourist(Be.arg, Then.extractIt(DOT.arg)).captureLastMatch(ingredientsFunction.astFunctionDef))

