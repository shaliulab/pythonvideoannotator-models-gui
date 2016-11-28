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
		Object2D.__init__(self, video)

		self._name 			= ControlText('Name', 'object-{0}'.format(len(self.video.objects)) )
		self._addpath 		= ControlButton('Add path')
		self._removepath  	= ControlButton('Remove path')

		self.formset = [
			'_name', 			
			('_addpath', '_removepath'),
			' '
		]

		self._addpath.icon 	= conf.ANNOTATOR_ICON_ADD
		self._removepath.icon 	= conf.ANNOTATOR_ICON_REMOVE

		self._name.changed_event = self.__name_changed_evt
		self._addpath.value = self.create_path

		self.create_tree_nodes()

	######################################################################
	### FUNCTIONS ########################################################
	######################################################################

	def create_tree_nodes(self):
		self.treenode = self.tree.create_child(self.name, icon=conf.ANNOTATOR_ICON_OBJECT, parent=self.video.treenode)
		self.treenode.win = self

	def create_path(self): return Path(self)


	######################################################################
	### EVENTS ###########################################################
	######################################################################

	def on_click(self, event, x, y):
		pass

	def __name_changed_evt(self):
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

		for dialog in PathsSelectorDialog.instantiated_dialogs:
			dialog.refresh_objects_list()
