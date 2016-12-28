import pyforms
from pyforms import BaseWidget
from pyforms.Controls import ControlCheckBoxList
from pythonvideoannotator_models.models.video import Video
from pythonvideoannotator_models.models.video.objects.object2d import Object2D
from pythonvideoannotator_models.models.video.objects.object2d.datasets.path import Path

class PathsSelectorDialog(BaseWidget):

	instantiated_dialogs = []

	def __init__(self, parent_win=None):
		BaseWidget.__init__(self, 'Paths selector', parent_win=parent_win)

		self.instantiated_dialogs.append(self)

		self._project = None

		self._videos  = ControlCheckBoxList('Videos filter')
		self._objects = ControlCheckBoxList('Objects filter')
		self._paths   = ControlCheckBoxList('Paths filter')

		self.formset = [('_videos','||','_objects','||','_paths')]

		self._videos.selection_changed_event 	= self.__selection_changed_event
		self._videos.changed_event  			= self.__update_objects
		self._objects.changed_event 			= self.__update_objects

	#####################################################################
	### PRIVATE FUNCTIONS ###############################################
	#####################################################################

	def __selection_changed_event(self): self.video_selection_changed_event()

	#####################################################################
	### EVENTS ##########################################################
	#####################################################################

	def video_selection_changed_event(self): pass

	#####################################################################
	### FUNCTIONS #######################################################
	#####################################################################

	# used to update automaticly the name of the videos, objects and paths
	def refresh(self):
		self._videos.refresh()
		self._objects.refresh()
		self._paths.refresh()
	
	def __add__(self, other):
		if isinstance(other, Video): 	self._videos += (other, False)
		if isinstance(other, Object2D): self.__update_objects()
		if isinstance(other, Path): 	self.__update_paths()
		return self

	def __sub__(self, other):
		if isinstance(other, Video): 	
			self._videos -= other
			self.__update_objects()
		if isinstance(other, Object2D): self.__update_objects()
		if isinstance(other, Path): 	self.__update_paths()
		return self
	
	
	def __update_objects(self):
		"""
		Update the objects in the list
		"""
		objects = [elem for elem, checked in self._objects.items]

		objects_list = []
		for video, checked in self._videos.items:
			for obj in video.objects:
				objects_list.append(obj)
				if not checked and obj in objects:
					self._objects -= obj
				elif checked and obj not in objects:
					self._objects += (obj, False)
				
		for obj in objects:
			if obj not in objects_list: self._objects -= obj


		self.__update_paths()

	def __update_paths(self):
		"""
		Update the paths in the list
		"""
		paths = [elem for elem, checked in self._paths.items]

		paths_list = []
		for obj, checked in self._objects.items:
			for path in obj.datasets:
				paths_list.append(path)
				if not checked and path in paths:
					self._paths -= path
				elif checked and path not in paths:
					self._paths += (path, False)

		for path in paths:
			if path not in paths_list: self._paths -= path

		

	

	#####################################################################
	### PROPERTIES ######################################################
	#####################################################################

	@property
	def paths(self): return self._paths.value

	@property
	def selected_data(self):
		videos 	= self._videos.value
		paths 	= self._paths.value
		res 	= []
		for video in videos:
			paths_list = []
			for obj in video.objects:
				for path in obj.paths:
					if path in paths: paths_list.append(path)
			res.append( (video, paths_list) )
		return res
		
	@property
	def current_video(self): 
		###########################################
		# current mouse selected video
		###########################################
		index = self._videos.selected_row_index
		if index<0: return None

		video, selected = self._videos.items[index]
		return video

	@property
	def current_video_capture(self): 
		video = self.current_video
		return video.video_capture if video is not None else None
	
	@property
	def project(self): return self._project
	@project.setter
	def project(self, value): self._project = value
	
if __name__ == "__main__":	 pyforms.startApp( PathsSelectorDialog )