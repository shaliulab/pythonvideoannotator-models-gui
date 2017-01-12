#! /usr/bin/python2
# -*- coding: utf-8 -*-
import os, cv2
from pysettings import conf
from pyforms import BaseWidget
from pyforms.Controls import ControlText
from pyforms.Controls import ControlFile
from pyforms.Controls import ControlButton
from pythonvideoannotator_models_gui.models.video.image import Image
from pythonvideoannotator_models_gui.models.video.objects.object2d import Object2D
from pythonvideoannotator_models_gui.dialogs import Dialog
from pythonvideoannotator_models.models.video import Video
from pythonvideoannotator_models_gui.models.imodel_gui import IModelGUI

class VideoGUI(IModelGUI, Video, BaseWidget):

	def __init__(self, project):
		IModelGUI.__init__(self)
		Video.__init__(self, project)
		BaseWidget.__init__(self, 'Video window', parent_win=project)
		
		self._file 			= ControlFile('Video')
		self._addobj 		= ControlButton('Add object')
		self._addimg 		= ControlButton('Add Image')
		self._removevideo  	= ControlButton('Remove')

		

		self.formset = [
			'_name',
			'_file', 			
			('_addobj', '_addimg'),
			'_removevideo',
			' '
		]

		self._name.enabled = False

		self._addobj.icon 	 	= conf.ANNOTATOR_ICON_ADD
		self._addimg.icon 	 	= conf.ANNOTATOR_ICON_ADD
		self._removevideo.icon 	= conf.ANNOTATOR_ICON_REMOVE

		self._addobj.value   	 = self.create_object
		self._addimg.value   	 = self.create_image
		

		self._removevideo.value  = self.__remove_video_changed_event
		self._file.changed_event = self.__file_changed_event

		self.create_tree_nodes()

		# fix bug: video windows open ditached from the main window when a project is opened
		if len(project.videos)>1: self.hide()


	
	

	#####################################################################################
	########### FUNCTIONS ###############################################################
	#####################################################################################

	def draw(self, frame, frame_index):
		for obj in self.objects: obj.draw(frame, frame_index)


	def create_tree_nodes(self):
		self.treenode = self.tree.create_child('Video', icon=conf.ANNOTATOR_ICON_VIDEO)
		self.treenode.win = self
		self.tree.selected_item = self.treenode

		self.tree.add_popup_menu_option(
			label='Remove', 
			function_action=self.__remove_video_changed_event, 
			item=self.treenode, icon=conf.ANNOTATOR_ICON_DELETE
		)

	def choose_file(self): self._file.click()
		

	def create_object(self): return Object2D(self)
	def create_image(self): return Image(self)


	#####################################################################################
	########### EVENTS ##################################################################
	#####################################################################################

	def __remove_video_changed_event(self): 
		project = self.project
		project -= self
		if len(project.videos)==0: self.close()

	def __file_changed_event(self):
		self.filepath = self._file.value
	
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
		self.mainwindow.video 	= self.video_capture
		self._file.value 		= value
		
	def show(self):
		if hasattr(self, '_right_docker'): self._right_docker.value = self
		super(VideoGUI, self).show()
		
			


