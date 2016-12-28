import csv, cv2, os
from pysettings import conf
from pyforms import BaseWidget
from PyQt4 import QtCore, QtGui
from pyforms.Controls import ControlButton
from pyforms.Controls import ControlCombo
from pyforms.Controls import ControlLabel
from pyforms.Controls import ControlText
from pythonvideoannotator_models.models.video.objects.object2d import Object2D
from pythonvideoannotator_models_gui.dialogs.paths_selector import PathsSelectorDialog
from pythonvideoannotator_models_gui.models.video.objects.object2d.datasets.path import Path

class Object2dGUI(Object2D, BaseWidget):

	def __init__(self, video):
		BaseWidget.__init__(self, '2D Object', parent_win=video)
		
		self._name 			= ControlText('Name' )
		self._addpath 		= ControlButton('Add path')
		self._removeobj  	= ControlButton('Remove')

		Object2D.__init__(self, video)

		self.formset = [
			'_name', 			
			('_addpath', '_removeobj'),
			' '
		]

		self._addpath.icon 	= conf.ANNOTATOR_ICON_ADD
		self._removeobj.icon 	= conf.ANNOTATOR_ICON_REMOVE

		self._name.changed_event = self.__name_changed_event
		self._addpath.value = self.create_path
		self._removeobj.value = self.__remove_object

		self.create_tree_nodes()

	######################################################################
	### FUNCTIONS ########################################################
	######################################################################


	def __add__(self, obj):
		super(Object2dGUI, self).__add__(obj)
		if isinstance(obj, Path): self.mainwindow.added_dataset_event(obj)
		return self

	def __sub__(self, obj):
		super(Object2dGUI, self).__sub__(obj)
		if isinstance(obj, Path): 
			self.treenode.removeChild(obj.treenode)
			self.mainwindow.removed_dataset_event(obj)
		return self

			

	def create_tree_nodes(self):
		self.treenode = self.tree.create_child(self.name, icon=conf.ANNOTATOR_ICON_OBJECT, parent=self.video.treenode)
		self.treenode.win = self

		self.tree.add_popup_menu_option(
			label='Remove', 
			function_action=self.__remove_object, 
			item=self.treenode, icon=conf.ANNOTATOR_ICON_DELETE
		)
		
	def __remove_object(self):
		item = self.tree.selected_item
		if item is not None: self.video -= item.win

	def create_path(self): return Path(self)


	######################################################################
	### EVENTS ###########################################################
	######################################################################

	def on_click(self, event, x, y):
		pass

	def __name_changed_event(self):
		self._name_changed_activated = True
		self.name = self._name.value
		del self._name_changed_activated

	def name_updated(self, newname): pass

	######################################################################
	### PROPERTIES #######################################################
	######################################################################

	@property
	def mainwindow(self): 	return self.video.mainwindow
	@property
	def tree(self): 		return self.video.tree
	@property
	def video_capture(self):return self.video.video_capture

	@property
	def name(self): return self._name.value
	@name.setter
	def name(self, value):
		if not hasattr(self, '_name_changed_activated'): self._name.value = value
		if hasattr(self, 'treenode'): self.treenode.setText(0,value)

		for dialog in PathsSelectorDialog.instantiated_dialogs: dialog.refresh()


	@property 
	def parent_treenode(self):  return self.video.treenode
