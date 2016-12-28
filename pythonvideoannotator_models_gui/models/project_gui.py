#! /usr/bin/python2
# -*- coding: utf-8 -*-
import os
from pysettings import conf
from pyforms import BaseWidget
from PyQt4 import QtGui, QtCore
from pyforms.Controls import ControlButton
from pyforms.Controls import ControlTree
from pyforms.Controls import ControlList
from pyforms.Controls import ControlEmptyWidget
from pyforms.dialogs  import CsvParserDialog


from pythonvideoannotator_models.models import Project
from pythonvideoannotator_models_gui.models.video import Video





class ProjectGUI(Project, BaseWidget):
	"""Application form"""

	def __init__(self, parent=None):
		self._parent = parent
		Project.__init__(self)
		BaseWidget.__init__(self, 'Project window', parent_win=parent)
		

		self._tree 			= ControlTree('')
		self._addvideo 		= ControlButton('Add video')
		self._removevideo 	= ControlButton('Remove video')
		self.formset 		= [
			'_tree', 
			'_addvideo',
		]
		
		## set controls ##########################################################
		self._tree.show_header  = False
		self._addvideo.value 	= self.__create_video_event

		self._addvideo.icon 	= conf.ANNOTATOR_ICON_ADD

		self.tree.item_selection_changed_event = self.tree_item_selection_changed_event
		

	######################################################################################
	#### FUNCTIONS #######################################################################
	######################################################################################

	def create_video(self): return Video(self)

	######################################################################################
	#### GUI EVENTS ######################################################################
	######################################################################################

	def tree_item_selection_changed_event(self):
		if self.tree.selected_item is not None and hasattr(self.tree.selected_item,'win'):
			self.mainwindow.details = self.tree.selected_item.win
			self.mainwindow.details.show()
	

	def __create_video_event(self):
		video = self.create_video()
		video.choose_file()

	def __remove_video_event(self):
		 item = self.tree.selected_item
		 if item: self -= item.win

	######################################################################################
	#### PUBLIC FUNCTIONS ################################################################
	######################################################################################

	def __add__(self, obj):
		super(ProjectGUI, self).__add__(obj)
		if isinstance(obj, Video) and hasattr(self.mainwindow, 'added_video_event'): 
			self.mainwindow.added_video_event(obj)
		return self

	def __sub__(self, obj):
		super(ProjectGUI, self).__sub__(obj)
		if isinstance(obj, Video): self._tree -= obj.treenode
		if hasattr(self.mainwindow, 'removed_video_event'): self.mainwindow.removed_video_event(obj)
		return self
		
	def player_on_click(self, event, x, y):
		if self._tree.selected_row_index is not None:
			obj = self._tree.selected_item.win
			obj.on_click(event, x, y)

	def draw(self, frame, frame_index):
		if self._tree.selected_row_index is not None:
			obj = self._tree.selected_item.win
			obj.draw(frame, frame_index)

	def save(self, data, project_path=None):
		data = super(ProjectGUI, self).save(data, project_path)
		timeline_path = os.path.join(project_path, 'timeline.csv')
		self.mainwindow.timeline.export_csv_file(timeline_path)
		return data

	def load(self, data, project_path=None):
		super(ProjectGUI, self).load(data, project_path)
		timeline_path = os.path.join(project_path, 'timeline.csv')
		self.mainwindow.timeline.import_csv_file(timeline_path)
		return data
		
	######################################################################################
	#### PROPERTIES ######################################################################
	######################################################################################

	@property
	def mainwindow(self): 	return self._parent

	@property
	def tree(self): 	return self._tree

	@property
	def objects(self):  	return [item.win for item in self._tree.value]
