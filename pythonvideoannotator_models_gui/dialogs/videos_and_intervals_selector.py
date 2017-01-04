import pyforms
from pyforms import BaseWidget
from pyforms.Controls import ControlBoundingSlider
from pyforms.Controls import ControlEmptyWidget
from pythonvideoannotator_models_gui.dialogs.videos_selector import VideosSelectorDialog

class VideosAndIntervalsSelectorDialog(BaseWidget):

	instantiated_dialogs = []

	def __init__(self, parent_win=None):
		BaseWidget.__init__(self, 'Videos and intervals selector', parent_win=parent_win)

		self.instantiated_dialogs.append(self)

		self._panel  	= ControlEmptyWidget(default=VideosSelectorDialog(parent_win=self))
		self._interval 	= ControlBoundingSlider('Interval', horizontal=True)
		
		self.formset = [
			'_panel', 
			'_interval'
		]

		self._intervals = {}

		self._panel.value.video_selection_changed_event = self.__video_selection_changed_event
		self._interval.changed_event = self.__update_intervals_event

	#####################################################################
	### PRIVATE FUNCTIONS ###############################################
	#####################################################################

	def __update_intervals_event(self):
		self._intervals[self.current_video] = self._interval.value

	def __video_selection_changed_event(self):
		video = self.current_video
		
		if video is not None and video.video_capture is not None:
			self._interval.max 	 = self.current_video_capture.get(7)
			if video not in self._intervals.keys(): 
				self._intervals[video] = 0, self._interval.max
			
			self._interval.value = self._intervals[video]
		self.video_selection_changed_event()

	#####################################################################
	### EVENTS ##########################################################
	#####################################################################

	def video_selection_changed_event(self):  pass
	

	#####################################################################
	### FUNCTIONS #######################################################
	#####################################################################

	def refresh(self):  self._panel.value.refresh()

	#####################################################################
	### PROPERTIES ######################################################
	#####################################################################

	@property
	def current_video(self): 		return self._panel.value.current_video
	@property
	def current_video_capture(self):return self._panel.value.current_video_capture
	@property
	def project(self): 				return self._panel.value.project
	@project.setter
	def project(self, value): 		self._panel.value.project = value

	@property
	def selected_data(self):
		for video in self._panel.value.selected_data:
			begin, end =  self._intervals.get(video, (0, video.total_frames)  )
			yield video, (begin, end )

	


if __name__ == "__main__":	 pyforms.startApp( PathsAndIntervalsSelectorDialog )