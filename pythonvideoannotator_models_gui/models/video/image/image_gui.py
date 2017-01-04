import csv, cv2, os
from pysettings import conf
from pyforms import BaseWidget
from PyQt4 import QtCore, QtGui
from pyforms.Controls import ControlButton
from pyforms.Controls import ControlCombo
from pyforms.Controls import ControlLabel
from pyforms.Controls import ControlText
from pythonvideoannotator_models.models.video.image import Image
from pythonvideoannotator_models_gui.dialogs.paths_selector import PathsSelectorDialog
from pythonvideoannotator_models_gui.models.video.objects.object2d.datasets.path import Path

class ImageGUI(Image, BaseWidget):

	def __init__(self, video):
		BaseWidget.__init__(self, 'Image', parent_win=video)
		
		self._name 			= ControlText('Name' )
		self._removeimg  	= ControlButton('Remove')

		Image.__init__(self, video)


		self.formset = [
			'_name', 			
			'_removeimg',
			' '
		]

		self._name.changed_event = self.__name_changed_event
		self._removeimg.value = self.__remove_image_event

		self.create_tree_nodes()


	######################################################################
	### EVENTS ###########################################################
	######################################################################

	def on_click(self, event, x, y):
		pass

	def __name_changed_event(self):
		self._name_changed_activated = True
		self.name = self._name.value
		del self._name_changed_activated

	def __remove_image_event(self):
		self.video -= self

	######################################################################
	### OBJECT FUNCTIONS #################################################
	######################################################################

	def draw(self, frame, frame_index): pass
		
	######################################################################
	### CLASS FUNCTIONS ##################################################
	######################################################################

	def create_tree_nodes(self):
		self.treenode = self.tree.create_child(self.name, icon=conf.ANNOTATOR_ICON_PICTURE, parent=self.video.treenode)
		self.treenode.win = self


	######################################################################
	### EVENTS ###########################################################
	######################################################################
	
	def double_clicked_event(self):
		#cv2.imshow(self.name, self.image)
		self.mainwindow.player.frame = self.image


	######################################################################
	### PROPERTIES #######################################################
	######################################################################
	
	@property
	def mainwindow(self): 	return self.video.mainwindow
	@property
	def tree(self): 		return self.video.tree
	

	@property
	def name(self): return self._name.value
	@name.setter
	def name(self, value):
		if not hasattr(self, '_name_changed_activated'): self._name.value = value
		if hasattr(self, 'treenode'): self.treenode.setText(0,value)


	@property 
	def parent_treenode(self):  return self.video.treenode

	
