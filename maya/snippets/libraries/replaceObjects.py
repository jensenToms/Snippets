import random
import maya.cmds as cmds

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2010 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["stacksHandler",
			"replaceTargetsObjectsWithSources",
			"pickSources_button_OnClicked",
			"pickTargets_button_OnClicked",
			"replaceObjects_button_OnClicked",
			"replaceObjects_window",
			"replaceObjects",
			"IReplaceObjects"]

def stacksHandler(object):
	"""
	Handles Maya stacks.

	:param object: Python object.
	:type object: object
	:return: Python function.
	:rtype: object
	"""

	def stacksHandlerCall(*args, **kwargs):
		"""
		Handles Maya stacks.

		:return: Python object.
		:rtype: object
		"""

		cmds.undoInfo(openChunk=True)
		value = object(*args, **kwargs)
		cmds.undoInfo(closeChunk=True)
		# Maya produces a weird command error if not wrapped here.
		try:
			cmds.repeatLast(addCommand="python(\"import %s; %s.%s()\")" % (__name__, __name__, object.__name__), addCommandLabel=object.__name__)
		except:
			pass
		return value

	return stacksHandlerCall

def replaceTargetsObjectsWithSources(sources, targets, inPlace=False, usePivot=False, asInstance=False, deleteTargets=True):
	"""
	Replaces the targets with sources.

	:param sources: Sources.
	:type sources: list
	:param targets: Targets.
	:type targets: list
	:param inPlace: In place replacement.
	:type inPlace: bool
	:param usePivot: Use target pivot.
	:type usePivot: bool
	:param asInstance: Duplicate as instances.
	:type asInstance: bool
	:param deleteTargets: Delete targets.
	:type deleteTargets: bool
	"""

	duplicatedObjects = []
	for target in targets:
		if not asInstance:
			duplicatedObject = cmds.duplicate(sources[random.randrange(0, len(sources))], rr=True)[0]
		else:
			duplicatedObject = cmds.instance(sources[random.randrange(0, len(sources))])[0]

		duplicatedObjects.append(duplicatedObject)
		if not inPlace:
			if usePivot:
				components = ("rx", "ry", "rz", "sx", "sy", "sz")
				pivot = cmds.xform(target, query=True, worldSpace=True, rotatePivot=True)
				for i, component  in enumerate(("tx", "ty", "tz")):
					cmds.setAttr(duplicatedObject + "." + component, pivot[i])
			else:
				components = ("tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz")

			for component in components:
				cmds.setAttr(duplicatedObject + "." + component, cmds.getAttr(target + "." + component))
		if deleteTargets:
			cmds.delete(target)

	if duplicatedObjects:
		if not inPlace:
			duplicationGrp = cmds.group(em=True)
			for duplicatedObject in duplicatedObjects:
				cmds.parent(duplicatedObject, duplicationGrp)
			cmds.rename(duplicationGrp, "duplication_grp")

@stacksHandler
def pickSources_button_OnClicked(state=None):
	"""
	Defines the slot triggered by **pickSources_button** button when clicked.

	:param state: Button state.
	:type state: bool
	"""

	cmds.textField("sources_textField", edit=True, text=", ".join(cmds.ls(sl=True, l=True)))

@stacksHandler
def pickTargets_button_OnClicked(state=None):
	"""
	Defines the slot triggered by **pickTargets_button** button when clicked.

	:param state: Button state.
	:type state: bool
	"""

	cmds.textField("targets_textField", edit=True, text=", ".join(cmds.ls(sl=True, l=True)))

@stacksHandler
def replaceObjects_button_OnClicked(state=None):
	"""
	Defines the slot triggered by **replaceObjects_button** button when clicked.

	:param state: Button state.
	:type state: bool
	"""

	sources = [source for source in cmds.textField("sources_textField", query=True, text=True).split(", ") if cmds.objExists(source)]
	targets = [target for target in cmds.textField("targets_textField", query=True, text=True).split(", ")	if cmds.objExists(target)]

	replaceTargetsObjectsWithSources(sources, targets, cmds.checkBox("duplicateInPlace_checkBox", q=True, v=True), cmds.checkBox("useTargetsPivots_checkBox", q=True, v=True), 	cmds.checkBox("duplicateAsInstances_checkBox", q=True, v=True))

def replaceObjects_window():
	"""
	Creates the 'Replace Objects' main window.
	"""

	cmds.windowPref(enableAll=False)

	if (cmds.window("replaceObjects_window", exists=True)):
		cmds.deleteUI("replaceObjects_window")

	cmds.window("replaceObjects_window",
		title="Replace Objects",
		width=320)

	spacing = 5

	cmds.columnLayout(adjustableColumn=True, rowSpacing=spacing)

	cmds.rowLayout(numberOfColumns=3, columnWidth3=(125, 150, 130), adjustableColumn=2, columnAlign=(2, "left"), columnAttach=[(1, "both", spacing), (2, "both", spacing), (3, "both", spacing)])
	cmds.text(label="Sources:")
	sources_textField = cmds.textField("sources_textField")
	cmds.button("pickSources_button", label="Pick Sources!", command=pickSources_button_OnClicked)
	cmds.setParent(topLevel=True)

	cmds.rowLayout(numberOfColumns=3, columnWidth3=(125, 150, 130), adjustableColumn=2, columnAlign=(2, "left"), columnAttach=[(1, "both", spacing), (2, "both", spacing), (3, "both", spacing)])
	cmds.text(label="Targets:")
	targets_textField = cmds.textField("targets_textField")
	cmds.button("pickTargets_button", label="Pick Targets!", command=pickTargets_button_OnClicked)
	cmds.setParent(topLevel=True)

	cmds.separator(style="single")

	cmds.columnLayout(columnOffset=("left", 40))
	cmds.checkBox("duplicateInPlace_checkBox", label="Duplicate In Place")
	cmds.checkBox("useTargetsPivots_checkBox", label="Use Targets Pivots", v=True)
	cmds.checkBox("duplicateAsInstances_checkBox", label="Duplicate As Instances")
	cmds.checkBox("deleteTargets_checkBox", label="Delete Targets", 	 v=True)
	cmds.setParent(topLevel=True)

	cmds.separator(style="single")

	cmds.button("replaceObjects_button", label="Replace Objects!", command=replaceObjects_button_OnClicked)

	cmds.showWindow("replaceObjects_window")

	cmds.windowPref(enableAll=True)

def replaceObjects():
	"""
	Launches the 'Replace Objects' main window.
	"""

	replaceObjects_window()

@stacksHandler
def IReplaceObjects():
	"""
	Defines the replaceObjects definition Interface.
	"""

	replaceObjects()
