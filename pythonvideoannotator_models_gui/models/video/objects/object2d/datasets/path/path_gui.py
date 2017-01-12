import math, cv2
from pysettings import conf
from pyforms import BaseWidget
from PyQt4 import QtCore, QtGui
from pyforms.Controls import ControlButton
from pyforms.Controls import ControlCombo
from pyforms.Controls import ControlLabel
from pyforms.Controls import ControlText
from pythonvideoannotator.utils import tools

from pythonvideoannotator_models.models.video.objects.object2d.datasets.path import Path
from pythonvideoannotator_models_gui.models.video.objects.object2d.datasets.dataset_gui import DatasetGUI


class PathGUI(DatasetGUI, Path, BaseWidget):

	def __init__(self, object2d=None):
		DatasetGUI.__init__(self)
		Path.__init__(self, object2d)
		BaseWidget.__init__(self, '2D Object', parent_win=object2d)

		self.__create_tree_nodes()
 		

		
		self._mark_pto_btn 	  	  = ControlButton('Mark point', checkable=True)
		self._sel_pto_btn 	  	  = ControlButton('Select point')
		self._del_path_btn 	  	  = ControlButton('Delete path')
		self._interpolation_title = ControlLabel('Interpolation')
		self._interpolation_mode  = ControlCombo('Mode')
		self._interpolate_btn 	  = ControlButton('Apply')
		self._remove_btn 	  	  = ControlButton('Remove')

		self._formset = [ 
			'_name',
			('_mark_pto_btn','_sel_pto_btn'),
			'_del_path_btn',
			'_interpolation_title',
			('_interpolation_mode','_interpolate_btn'),
			'_remove_btn',
			' '
		]


		#### set controls ##############################################
		self._interpolation_title.value = 'INTERPOLATION'
		self._interpolation_mode.add_item("Auto")
		self._interpolation_mode.add_item("Linear", 'slinear')
		self._interpolation_mode.add_item("Quadratic", 'quadratic')
		self._interpolation_mode.add_item("Cubic", 'cubic')

		self._del_path_btn.hide()
		self._interpolate_btn.hide()
		self._interpolation_mode.hide()
		self._interpolation_title.hide()

		self._del_path_btn.icon = conf.ANNOTATOR_ICON_DELETEPATH
		self._interpolate_btn.icon = conf.ANNOTATOR_ICON_INTERPOLATE
		self._mark_pto_btn.icon = conf.ANNOTATOR_ICON_MARKPLACE
		self._sel_pto_btn.icon = conf.ANNOTATOR_ICON_SELECTPOINT
		self._remove_btn.icon = conf.ANNOTATOR_ICON_REMOVE

		#### set events #################################################
		self._del_path_btn.value 		 = self.__del_path_btn_event
		self._interpolation_mode.changed_event = self.__interpolation_mode_changed_event
		self._interpolate_btn.value 	 = self.__interpolate_btn_event
		self._sel_pto_btn.value			 = self.__sel_pto_btn_event
		self._remove_btn.value			 = self.__remove_path_dataset


	######################################################################
	### FUNCTIONS ########################################################
	######################################################################

	def get_velocity(self, index):
		p1 = self.get_position(index)
		p2 = self.get_position(index-1)
		if p1 is None or p2 is None: return None
		return p2[0]-p1[0], p2[1]-p1[1]
		

	def get_acceleration(self, index):
		v1 = self.get_velocity(index)
		v2 = self.get_velocity(index-1)
		if v1 is None or v2 is None: return None
		return v2[0]-v1[0], v2[1]-v1[1]



	def get_position_x_value(self, index):
		v = self.get_position(index)
		return v[0] if v is not None else None

	def get_position_y_value(self, index):
		v = self.get_position(index)
		return v[1] if v is not None else None


	def get_velocity_x_value(self, index):
		v = self.get_velocity(index)
		return v[0] if v is not None else None

	def get_velocity_y_value(self, index):
		v = self.get_velocity(index)
		return v[1] if v is not None else None

	def get_velocity_absolute_value(self, index):
		v = self.get_velocity(index)
		return math.sqrt(v[1]**2+v[0]**2) if v is not None else None


	def get_acceleration_x_value(self, index):
		v = self.get_acceleration(index)
		return v[0] if v is not None else None

	def get_acceleration_y_value(self, index):
		v = self.get_acceleration(index)
		return v[1] if v is not None else None

	def get_acceleration_absolute_value(self, index):
		v = self.get_acceleration(index)
		return math.sqrt(v[1]**2+v[0]**2) if v is not None else None
		

	######################################################################
	### AUX FUNCTIONS ####################################################
	######################################################################

	def __create_tree_nodes(self):

		self.treenode = self.tree.create_child(self.name, icon=conf.ANNOTATOR_ICON_PATH, parent=self.parent_treenode )
		self.tree.add_popup_menu_option(
			label='Remove', 
			function_action=self.__remove_path_dataset, 
			item=self.treenode, icon=conf.ANNOTATOR_ICON_DELETE
		)
		self.treenode.win = self

		self.create_group_node('position', 		icon=conf.ANNOTATOR_ICON_POSITION)
		self.create_data_node('position > x', 	icon=conf.ANNOTATOR_ICON_X)
		self.create_data_node('position > y', 	icon=conf.ANNOTATOR_ICON_Y)

		self.create_group_node('velocity', 			icon=conf.ANNOTATOR_ICON_VELOCITY)
		self.create_data_node('velocity > x', 		icon=conf.ANNOTATOR_ICON_X)
		self.create_data_node('velocity > y', 		icon=conf.ANNOTATOR_ICON_Y)
		self.create_data_node('velocity > absolute', icon=conf.ANNOTATOR_ICON_INFO)

		self.create_group_node('acceleration', 			icon=conf.ANNOTATOR_ICON_ACCELERATION)
		self.create_data_node('acceleration > x', 		icon=conf.ANNOTATOR_ICON_X)
		self.create_data_node('acceleration > y', 		icon=conf.ANNOTATOR_ICON_Y)
		self.create_data_node('acceleration > absolute', icon=conf.ANNOTATOR_ICON_INFO)



	
		

	
	

	######################################################################
	### GUI EVENTS #######################################################
	######################################################################



	def __sel_pto_btn_event(self):
		if self.mainwindow._player.video_index<0:return 
		self._sel_pts.append( self.mainwindow._player.video_index)
		#store a temporary path for interpolation visualization
		if len(self._sel_pts) == 2: 
			#########################################################
			#In case 2 frames are selected, draw the temporary path##
			#########################################################
			self.calculate_tmp_interpolation()
			self._interpolate_btn.show()
			self._interpolation_mode.show()
			self._interpolation_title.show()
			self._del_path_btn.show()
			#########################################################
		else:
			self._interpolate_btn.hide()
			self._interpolation_mode.hide()
			self._interpolation_title.hide()
			self._del_path_btn.hide()
			self._tmp_path = []
		self.mainwindow._player.refresh()


	def __remove_path_dataset(self):
		item = self.tree.selected_item
		if item is not None: self.object2d -= item.win



	####################################################################

	def __interpolate_btn_event(self): 
		#store a temporary path for interpolation visualization
		if len(self._sel_pts) == 2:
			mode = None if self._interpolation_mode.value=='Auto' else self._interpolation_mode.value		 #store a temporary path for interpolation visualization
			self.interpolate_range( self._sel_pts[0], self._sel_pts[1], interpolation_mode=mode)
			self.mainwindow._player.refresh()
		else:
			QtGui.QMessageBox.about(self, "Error", "You need to select 2 frames.")

	def __interpolation_mode_changed_event(self): 
		#store a temporary path for interpolation visualization
		if len(self._sel_pts) == 2:

			self.calculate_tmp_interpolation()
			self.mainwindow._player.refresh()

	def __del_path_btn_event(self): #store a temporary path for interpolation visualization
		if len(self._sel_pts) == 2:
			reply = QtGui.QMessageBox.question(self, 'Confirmation',
											   "Are you sure you want to delete this path?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
			if reply == QtGui.QMessageBox.Yes: #store a temporary path for interpolation visualization
				start, end = self._sel_pts[0], self._sel_pts[1]
				self.delete_range(start+1, end)
				self.calculate_tmp_interpolation()
				self.mainwindow._player.refresh()
		else:
			QtGui.QMessageBox.about(self, "Error", "You need to select 2 frames.")


	######################################################################
	### VIDEO EVENTS #####################################################
	######################################################################

	def on_click(self, event, x, y):

		if event.button() == 1:
			frame_index = self.mainwindow._player.video_index


			if self._mark_pto_btn.checked:
				self.set_position(frame_index if frame_index>=0 else 0, x, y)
				self._mark_pto_btn.checked = False
			else:
				position = self.get_position(frame_index)
				if position is not None:
					modifier = int(event.modifiers())

					# If the control button is pressed will add the blob to the previous selections
					if modifier == QtCore.Qt.ControlModifier:
						if frame_index not in self._sel_pts: #store a temporary path for interpolation visualization
							self._sel_pts.append(frame_index)
							
						else:
							# Remove the blob in case it was selected before #store a temporary path for interpolation visualization
							self._sel_pts.remove(frame_index)
					else:
						# The control key was not pressed so will select only one #store a temporary path for interpolation visualization
						self._sel_pts =[frame_index]
				else: #store a temporary path for interpolation visualization
					self._sel_pts =[]  # No object selected: remove previous selections #store a temporary path for interpolation visualization
				self._sel_pts =sorted(self._sel_pts)

 			#store a temporary path for interpolation visualization
			if len(self._sel_pts) == 2: 
				#########################################################
				#In case 2 frames are selected, draw the temporary path##
				#########################################################
				self.calculate_tmp_interpolation()
				self._interpolate_btn.show()
				self._interpolation_mode.show()
				self._interpolation_title.show()
				self._del_path_btn.show()
				#########################################################
			else:
				self._interpolate_btn.hide()
				self._interpolation_mode.hide()
				self._interpolation_title.hide()
				self._del_path_btn.hide()
				self._tmp_path = []
				
			
			self.mainwindow._player.refresh()

	def draw(self, frame, frame_index):
		pos = self.get_position(frame_index)
		if pos is None: return
		
		cv2.circle(frame, pos, 8, (255,255,255), -1)
		cv2.circle(frame, pos, 6, (100,0,100), 	 -1)
		


	######################################################################
	### PROPERTIES #######################################################
	######################################################################

	@property
	def mainwindow(self): 	 return self._object2d.mainwindow
	@property 
	def tree(self):  		 return self._object2d.tree
	@property 
	def video_capture(self): return self._object2d.video_capture

	@property 
	def parent_treenode(self):  return self._object2d.treenode


