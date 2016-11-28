import pyforms
from pyforms import BaseWidget
from pyforms.Controls import ControlCheckBoxList

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

		self._videos.changed_event  			= self.__videos_changed_event
		self._videos.selection_changed_event 	= self.__selection_changed_event
		self._objects.changed_event 			= self.__objects_changed_event

	#####################################################################
	### PRIVATE FUNCTIONS ###############################################
	#####################################################################

	def __selection_changed_event(self): self.video_selection_changed_event()
	def __videos_changed_event(self): 	 self.update_objects()
	def __objects_changed_event(self): 	 self.update_paths()

	#####################################################################
	### EVENTS ##########################################################
	#####################################################################

	def video_selection_changed_event(self): pass

	#####################################################################
	### FUNCTIONS #######################################################
	#####################################################################

	# used to update automaticly the name of the videos, objects and paths
	def refresh_videos_list(self): 	self._videos.refresh()
	def refresh_objects_list(self): self._objects.refresh()
	def refresh_paths_list(self): 	self._paths.refresh()
	
	# update the model visualization
	def update_videos(self):
		videos = [elem for elem, checked in self._videos.items]
		for video in self.project.videos:
			if video not in videos: self._videos += (video, False)

		items = self._videos.items
		self._videos.clear()
		self._videos.value = items
		self.update_objects()

	def update_objects(self):
		objects = [elem for elem, checked in self._objects.items]

		for video, checked in self._videos.items:
			for obj in video.objects:
				if not checked and obj in objects:
					self._objects -= obj
				elif checked and obj not in objects:
					self._objects += (obj, False)

		self.update_paths()

	def update_paths(self):
		paths = [elem for elem, checked in self._paths.items]

		for obj, checked in self._objects.items:
			for path in obj.datasets:
				if not checked and path in paths:
					self._paths -= path
				elif checked and path not in paths:
					self._paths += (path, False)

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