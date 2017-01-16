import csv, cv2, os
from pysettings import conf
from pyforms import BaseWidget
from PyQt4 import QtCore, QtGui
from pyforms.Controls import ControlButton
from pyforms.Controls import ControlCombo
from pyforms.Controls import ControlLabel
from pyforms.Controls import ControlText
from pythonvideoannotator_models.models.video.objects.object2d import Object2D
from pythonvideoannotator_models_gui.dialogs import Dialog
from pythonvideoannotator_models_gui.models.imodel_gui import IModelGUI
from pythonvideoannotator_models_gui.models.video.objects.object2d.datasets.path import Path
from pythonvideoannotator_models_gui.models.video.objects.object2d.datasets.contours import Contours
from pythonvideoannotator_models_gui.models.video.objects.object2d.datasets.value import Value

class Object2dGUI(IModelGUI, Object2D, BaseWidget):

	def __init__(self, video):
		IModelGUI.__init__(self)
		Object2D.__init__(self, video)
		BaseWidget.__init__(self, '2D Object', parent_win=video)
		
		self._addpath 		= ControlButton('Add path')
		self._addcontours	= ControlButton('Add contours')
		self._addvalues		= ControlButton('Add values')
		self._removeobj  	= ControlButton('Remove')


		self.formset = [
			'_name', 			
			('_addpath', '_addcontours'),
			'_addvalues',
			'_removeobj',
			' '
		]

		self._addpath.icon 	= conf.ANNOTATOR_ICON_ADD
		self._removeobj.icon 	= conf.ANNOTATOR_ICON_REMOVE		
		self._addcontours.icon 	= conf.ANNOTATOR_ICON_CONTOUR		
		self._addvalues.icon 	= conf.ANNOTATOR_ICON_CONTOUR

		self._addpath.value = self.create_path
		self._addcontours.value = self.create_contours
		self._addvalues.value = self.create_value
		self._removeobj.value = self.__remove_object

		self.create_tree_nodes()

	######################################################################
	### FUNCTIONS ########################################################
	######################################################################




	def __sub__(self, obj):
		super(Object2dGUI, self).__sub__(obj)
		if isinstance(obj, Path): self.treenode.removeChild(obj.treenode)
		if isinstance(obj, Contours): self.treenode.removeChild(obj.treenode)
		if isinstance(obj, Value): self.treenode.removeChild(obj.treenode)		
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
	def create_contours(self): return Contours(self)
	def create_value(self): return Value(self)

	######################################################################
	### EVENTS ###########################################################
	######################################################################

	def on_click(self, event, x, y):
		for dataset in self.datasets: dataset.on_click(event, x, y)

	def draw(self, frame, frame_index):
		for dataset in self.datasets: dataset.draw(frame, frame_index)
	

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
	def parent_treenode(self):  return self.video.treenode
