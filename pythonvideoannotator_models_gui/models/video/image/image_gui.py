import csv, cv2, os
from pysettings import conf
from pyforms import BaseWidget
from PyQt4 import QtCore, QtGui
from pyforms.Controls import ControlButton
from pyforms.Controls import ControlCombo
from pyforms.Controls import ControlLabel
from pyforms.Controls import ControlText
from pythonvideoannotator_models.models.video.image import Image
from pythonvideoannotator_models_gui.dialogs import DatasetsDialog
from pythonvideoannotator_models_gui.models.imodel_gui import IModelGUI
from pythonvideoannotator_models_gui.models.video.objects.object2d.datasets.path import Path

class ImageGUI(IModelGUI, Image, BaseWidget):

	def __init__(self, video):
		IModelGUI.__init__(self)
		Image.__init__(self, video)
		BaseWidget.__init__(self, 'Image', parent_win=video)
		
		self._removeimg  	= ControlButton('Remove')

		
		self.formset = [
			'_name', 			
			'_removeimg',
			' '
		]

		self._removeimg.value = self.__remove_image_event

		self.create_tree_nodes()


	######################################################################
	### EVENTS ###########################################################
	######################################################################

	def on_click(self, event, x, y):
		pass



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
	def parent_treenode(self):  return self.video.treenode

	