import maya.cmds as cmds
import maya.mel as mel

def unfoldBandUVs(object, divisions=1, history=True):
	'''
	This Definition Unfold Object Band UVs.
	
	@param object: Object. ( String )
	@param divisions: Extrusion Divisions. ( Integer )
	@param history: Keep Construction History. ( Boolean )
	'''

	edgesCount = cmds.polyEvaluate(object, edge=True)
	edges = cmds.ls(object +".e[0:" + str(edgesCount-1) + "]", fl=True, l=True)

	cmds.select(object)
	cmds.polySelectConstraint(m=3, t=0x8000, w=1)
	cmds.polySelectConstraint(m=0)
	for i in range(divisions):
		mel.eval("GrowPolygonSelectionRegion();")
	bandEdges = cmds.ls(sl=True, fl=True, l=True)
	bandFaces = cmds.ls(cmds.polyListComponentConversion(bandEdges, fe=True, tf=True), fl=True)
	cmds.select(bandFaces)
	cmds.polyForceUV(unitize=True)
	cmds.polySelectConstraint(m=3, t=0x8000, sm=1)
	seamsEdges = cmds.ls(sl=True, fl=True, l=True)
	weldEdges = list(set(bandEdges).difference(set(seamsEdges)))
	cmds.polyMapSewMove(weldEdges)
	cmds.polyLayoutUV(bandFaces, scale=1, rotateForBestFit=0, layout=1)
	uvs = cmds.polyListComponentConversion(bandFaces, toUV=1)
	cmds.polyEditUV(uvs, u=1, v=0)

	not history and cmds.delete(object, ch=True)

def unfoldBand_Button_OnClicked(state):
	'''
	This Definition Is Triggered By The unfoldBand Button When Clicked.
	
	@param state: Button State. ( Boolean )
	'''

	for object in cmds.ls(sl=True, l=True, o=True):
		unfoldBandUVs(object, divisions=cmds.intSliderGrp("divisions_IntSliderGrp", q=True, v=True), history=cmds.checkBox("keepConstructionHistory_CheckBox", q=True, v=True))
	
def unfoldBand_Window():
	'''
	This Definition Creates The Solidify Main Window.
	'''
	
	cmds.windowPref(enableAll=False)

	if (cmds.window("unfoldBand_Window", exists=True)):
		cmds.deleteUI("unfoldBand_Window")

	cmds.window("unfoldBand_Window",
		title="Unfold Band",
		width=384)

	spacing=5

	cmds.columnLayout(adjustableColumn=True, rowSpacing=spacing)

	cmds.separator(height=10, style="singleDash")

	cmds.intSliderGrp("divisions_IntSliderGrp", label="Divisions", field=True, minValue=0, maxValue=10, fieldMinValue=0, fieldMaxValue=65535, value=2)
	
	cmds.separator(style="single")
	
	cmds.columnLayout(columnOffset=("left", 140) )
	cmds.checkBox("keepConstructionHistory_CheckBox", label="Keep Construction History",  v=True)
	cmds.setParent(topLevel=True)

	cmds.separator(height=10, style="singleDash")
	
	cmds.button("unfoldBand_Button", label="Unfold Band!", command=unfoldBand_Button_OnClicked)

	cmds.showWindow("unfoldBand_Window")

	cmds.windowPref(enableAll=True)
	
def unfoldBand():
	'''
	This Definition Launches The Unfold Band Main Window.
	'''

	unfoldBand_Window()

def IUnfoldBand():
	'''
	This Definition Is The unfoldBand Method Interface.
	'''
	
	unfoldBand()	