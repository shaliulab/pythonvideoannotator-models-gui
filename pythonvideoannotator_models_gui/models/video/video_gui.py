#! /usr/bin/python2
# -*- coding: utf-8 -*-
import os, cv2
from pysettings import conf
from pyforms import BaseWidget
from pyforms.Controls import ControlFile
from pyforms.Controls import ControlButton
from pythonvideoannotator_models_gui.models.video.objects.object2d import Object2D
from pythonvideoannotator_models_gui.dialogs.paths_selector import PathsSelectorDialog
from pythonvideoannotator_models.models.video import Video

class VideoGUI(Video, BaseWidget):

	def __init__(self, project):
		BaseWidget.__init__(self, 'Video window', parent_win=project)
		Video.__init__(self, project)

		self._file 			= ControlFile('Video')
		self._addobj 		= ControlButton('Add object')
		self._removevideo  	= ControlButton('Remove video')


		self.formset = [
			'_file', 			
			('_addobj', '_removevideo'),
			' '
		]

		self._addobj.icon 	 = conf.ANNOTATOR_ICON_ADD


		self._addobj.value   = self.create_object
		self._file.changed_event = self.__filename_changed_evt

		self._removevideo.value = self.__removevideo_changed_evt

		self.create_tree_nodes()


	
	

	#####################################################################################
	########### FUNCTIONS ###############################################################
	#####################################################################################


	def create_tree_nodes(self):
		self.treenode = self.tree.create_child('Video', icon=conf.ANNOTATOR_ICON_VIDEO)
		self.treenode.win = self
		self.tree.selected_item = self.treenode

	def choose_file(self): self._file.click()
		

	def create_object(self): return Object2D(self)

	#####################################################################################
	########### EVENTS ##################################################################
	#####################################################################################

	def __removevideo_changed_evt(self): 
		project = self.project
		project -= self

	def __filename_changed_evt(self):
		self._updating_filename = True
		self.filepath = self._file.value
		del self._updating_filename

	#####################################################################################
	########### PROPERTIES ##############################################################
	#####################################################################################

	
	@property
	def mainwindow(self): 	return self.project.mainwindow

	@property
	def tree(self): return self._project.tree

	@property
	def filepath(self): return self._file.value
	@filepath.setter 
	def filepath(self, value):
		Video.filepath.fset(self, value)
		
		self.treenode.setText(0, self.name)
		self.mainwindow.video = self.video_capture

		for dialog in PathsSelectorDialog.instantiated_dialogs:
			dialog.refresh_videos_list()

		if hasattr(self, '_updating_filename'): return
		
		self._file.value = value
			

		
			


