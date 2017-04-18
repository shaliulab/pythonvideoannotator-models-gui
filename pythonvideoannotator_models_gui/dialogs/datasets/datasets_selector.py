import pyforms
from pyforms import BaseWidget
from pyforms.Controls import ControlCheckBoxList
from pythonvideoannotator_models.models.video import Video
from pythonvideoannotator_models.models.video.objects.object2d import Object2D
from pythonvideoannotator_models.models.video.objects.object2d.datasets.dataset import Dataset
from pythonvideoannotator_models_gui.dialogs.dialog import Dialog

class DatasetsSelectorDialog(Dialog, BaseWidget):

	def __init__(self, parent_win=None):
		BaseWidget.__init__(self, 'Datasets selector', parent_win=parent_win)
		
		self._videos   = ControlCheckBoxList('Videos filter')
		self._objects  = ControlCheckBoxList('Objects filter')
		self._datasets = ControlCheckBoxList('Datasets filter')

		Dialog.__init__(self)
		
		self._videos.add_popup_menu_option('Select video', self.__selection_changed_event)

		self.formset = [('_videos','||','_objects','||','_datasets')]

		self._videos.selection_changed_event 	= self.__selection_changed_event
		self._videos.changed_event  			= self.__update_objects
		self._objects.changed_event 			= self.__update_objects
		self._datasets.changed_event 			= self.__datasets_changed_event

		#for video in conf.PROJECT.videos: self += video


	#####################################################################
	### PRIVATE FUNCTIONS ###############################################
	#####################################################################

	def __selection_changed_event(self): self.video_selection_changed_event()

	def __datasets_changed_event(self): self.datasets_changed_event()

	#####################################################################
	### EVENTS ##########################################################
	#####################################################################

	def video_selection_changed_event(self): pass

	def datasets_changed_event(self): pass

	#####################################################################
	### FUNCTIONS #######################################################
	#####################################################################

	# used to update automaticly the name of the videos, objects and paths
	def refresh(self):
		self._videos.refresh()
		self._objects.refresh()
		self._datasets.refresh()

	def clear(self):
		self._videos.clear()
		self._objects.clear()
		self._datasets.clear()
	
	def __add__(self, other):
		if isinstance(other, Video): 	self._videos += (other, False)
		if isinstance(other, Object2D): self.__update_objects()
		if isinstance(other, Dataset): 	self.__update_datasets()
		return self
		

	def __sub__(self, other):
		if isinstance(other, Video): 	
			self._videos -= other
			self.__update_objects()
		if isinstance(other, Object2D): self.__update_objects()
		if isinstance(other, Dataset): 	self.__update_datasets()
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

		self.__update_datasets()



	def __update_datasets(self):
		"""
		Update the paths in the list
		"""
		datasets = [elem for elem, checked in self._datasets.items]

		datasets_list = []
		for obj, checked in self._objects.items:
			if not isinstance(obj,Object2D): continue

			for dataset in obj.datasets:
				if hasattr(self, '_datasets_filter') and not self._datasets_filter(dataset): continue
				
				if dataset not in datasets_list: datasets_list.append(dataset)

				if not checked and dataset in datasets:
					self._datasets -= dataset
				elif checked and dataset not in datasets:
					self._datasets += (dataset, False)

		for dataset in datasets:
			if dataset not in datasets_list: self._datasets -= dataset

		

	

	#####################################################################
	### PROPERTIES ######################################################
	#####################################################################

	@property
	def videos(self): return self._videos.value


	@property
	def datasets(self): return self._datasets.value

	@property
	def selected_data(self):
		videos 	= self._videos.value
		datasets= self._datasets.value
		res 	= []
		for video in videos:
			datasets_list = []
			for obj in video.objects2D:
				for dataset in obj.datasets:
					if dataset in datasets:
						datasets_list.append(dataset)
			res.append( (video, datasets_list) )
		return res
		
	@property
	def selected_video(self): 
		###########################################
		# current mouse selected video
		###########################################
		index = self._videos.selected_row_index
		if index<0: return None

		video, selected = self._videos.items[index]
		return video


	@property
	def datasets_filter(self): return self._datasets_filter
	@datasets_filter.setter
	def datasets_filter(self, value): self._datasets_filter = value

	
	
	
if __name__ == "__main__":	 pyforms.startApp( DatasetsSelectorDialog )