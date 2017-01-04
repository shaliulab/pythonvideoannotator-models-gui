import pyforms
from pyforms import BaseWidget
from pyforms.Controls import ControlCheckBoxList
from pythonvideoannotator_models.models.video import Video

class VideosSelectorDialog(BaseWidget):

	instantiated_dialogs = []

	def __init__(self, parent_win=None):
		BaseWidget.__init__(self, 'Videos selector', parent_win=parent_win)
		self.instantiated_dialogs.append(self)

		self._project = None

		self._videos  = ControlCheckBoxList('Videos filter')

		self.formset = ['_videos']

		self._videos.selection_changed_event 	= self.__selection_changed_event	
		
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
	def refresh(self): self._videos.refresh()
	
	def __add__(self, other):
		if isinstance(other, Video): self._videos += (other, False)
		return self

	def __sub__(self, other):
		if isinstance(other, Video): self._videos -= other
		return self
	
	
	

	#####################################################################
	### PROPERTIES ######################################################
	#####################################################################

	@property
	def selected_data(self): return self._videos.value
		
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
	
if __name__ == "__main__":	 pyforms.startApp( VideosSelectorDialog )