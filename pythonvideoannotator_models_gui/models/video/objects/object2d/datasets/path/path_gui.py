import math
from pysettings import conf
from pyforms import BaseWidget
from PyQt4 import QtCore, QtGui
from pyforms.Controls import ControlButton
from pyforms.Controls import ControlCombo
from pyforms.Controls import ControlLabel
from pyforms.Controls import ControlText
from pythonvideoannotator_models_gui.dialogs.paths_selector import PathsSelectorDialog
from pythonvideoannotator_models.models.video.objects.object2d.datasets.path import Path


class PathGUI(Path, BaseWidget):

	def __init__(self, object2d=None):
		BaseWidget.__init__(self, '2D Object', parent_win=object2d)
		
		self._name = ControlText('Name')
		
		Path.__init__(self, object2d)

		

		self.__create_tree_nodes()
		self._name.changed_event 				 = self.__name_changed_event



		
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
		self._name.changed_event 				 = self.__name_changed_event
		self._sel_pto_btn.value			 = self.__sel_pto_btn_event
		self._remove_btn.value			 = self.__remove_path_dataset
		

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
		

		self.treenode_pos = self.tree.create_child('position', icon=conf.ANNOTATOR_ICON_POSITION, parent=self.treenode )
		x_treenode = self.tree.create_child('x', icon=conf.ANNOTATOR_ICON_X, parent=self.treenode_pos )
		y_treenode = self.tree.create_child('y', icon=conf.ANNOTATOR_ICON_Y, parent=self.treenode_pos )
		self.tree.add_popup_menu_option(label='View on the timeline', function_action=self.__send_pos_x_to_timeline_event, item=x_treenode, icon=conf.ANNOTATOR_ICON_TIMELINE)
		self.tree.add_popup_menu_option(label='View on the timeline', function_action=self.__send_pos_y_to_timeline_event, item=y_treenode, icon=conf.ANNOTATOR_ICON_TIMELINE)
		
		self.treenode_vel = self.tree.create_child('velocity', icon=conf.ANNOTATOR_ICON_VELOCITY, parent=self.treenode )
		vx_treenode = self.tree.create_child('x', icon=conf.ANNOTATOR_ICON_X, parent=self.treenode_vel )
		vy_treenode = self.tree.create_child('y', icon=conf.ANNOTATOR_ICON_Y, parent=self.treenode_vel )
		absv_treenode = self.tree.create_child('absolute', icon=conf.ANNOTATOR_ICON_INFO, parent=self.treenode_vel )
		self.tree.add_popup_menu_option(label='View on the timeline', function_action=self.__send_vel_x_to_timeline_event, item=vx_treenode, icon=conf.ANNOTATOR_ICON_TIMELINE)
		self.tree.add_popup_menu_option(label='View on the timeline', function_action=self.__send_vel_y_to_timeline_event, item=vy_treenode, icon=conf.ANNOTATOR_ICON_TIMELINE)
		self.tree.add_popup_menu_option(label='View on the timeline', function_action=self.__send_absvel_to_timeline_event, item=absv_treenode, icon=conf.ANNOTATOR_ICON_TIMELINE)
		
		self.treenode_acc = self.tree.create_child('acceleration', icon=conf.ANNOTATOR_ICON_ACCELERATION, parent=self.treenode )
		ax_treenode = self.tree.create_child('x', icon=conf.ANNOTATOR_ICON_X, parent=self.treenode_acc )
		ay_treenode = self.tree.create_child('y', icon=conf.ANNOTATOR_ICON_Y, parent=self.treenode_acc )
		absa_treenode = self.tree.create_child('absolute', icon=conf.ANNOTATOR_ICON_INFO, parent=self.treenode_acc )
		self.tree.add_popup_menu_option(label='View on the timeline', function_action=self.__send_acc_x_to_timeline_event, item=ax_treenode, icon=conf.ANNOTATOR_ICON_TIMELINE)
		self.tree.add_popup_menu_option(label='View on the timeline', function_action=self.__send_acc_y_to_timeline_event, item=ay_treenode, icon=conf.ANNOTATOR_ICON_TIMELINE)
		self.tree.add_popup_menu_option(label='View on the timeline', function_action=self.__send_absacc_to_timeline_event, item=absa_treenode, icon=conf.ANNOTATOR_ICON_TIMELINE)
		

		y_treenode.win = x_treenode.win = self.treenode_pos.win = \
		absv_treenode.win = vy_treenode.win = vx_treenode.win = self.treenode_vel.win = \
		absa_treenode.win = ay_treenode.win = ax_treenode.win = self.treenode_acc.win = \
		self.treenode.win = self

		y_treenode.object2d = x_treenode.object2d = self.treenode_pos.object2d = \
		absv_treenode.object2d = vy_treenode.object2d = vx_treenode.object2d = self.treenode_vel.object2d = \
		absa_treenode.object2d = ay_treenode.object2d = ax_treenode.object2d = self.treenode_acc.object2d = \
		self.treenode.object2d = self.object2d
		

	

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

	def __name_changed_event(self):
		self._name_changed_activated = True
		self.name = self._name.value
		del self._name_changed_activated

	def __remove_path_dataset(self):
		item = self.tree.selected_item
		if item is not None: self.object2d -= item.win


	def __send_pos_x_to_timeline_event(self):
		data = [(i,self.get_position(i)[0]) for i in range(len(self)) if self.get_position(i) is not None]
		self.mainwindow.add_graph('{0} x position'.format(self.name), data)

	def __send_pos_y_to_timeline_event(self):
		data = [(i,self.get_position(i)[1]) for i in range(len(self)) if self.get_position(i) is not None]
		self.mainwindow.add_graph('{0} y position'.format(self.name), data)

	####################################################################

	def __send_vel_x_to_timeline_event(self):
		data = [(i,self.get_velocity(i)[0]) for i in range(len(self)) if self.get_velocity(i) is not None]
		self.mainwindow.add_graph('{0} x position'.format(self.name), data)

	def __send_vel_y_to_timeline_event(self):
		data = [(i,self.get_velocity(i)[1]) for i in range(len(self)) if self.get_velocity(i) is not None]
		self.mainwindow.add_graph('{0} y position'.format(self.name), data)

	def __send_absvel_to_timeline_event(self):
		data = []
		for i in range(len(self)):
			vel = self.get_velocity(i)
			if vel is not None:
				data.append([i, math.sqrt(vel[1]**2+vel[0]**2)])
		self.mainwindow.add_graph('{0} absolute velocity'.format(self.name), data)


	####################################################################

	def __send_acc_x_to_timeline_event(self):
		data = [(i,self.get_acceleration(i)[0]) for i in range(len(self)) if self.get_acceleration(i) is not None]
		self.mainwindow.add_graph('{0} x position'.format(self.name), data)

	def __send_acc_y_to_timeline_event(self):
		data = [(i,self.get_acceleration(i)[1]) for i in range(len(self)) if self.get_acceleration(i) is not None]
		self.mainwindow.add_graph('{0} y position'.format(self.name), data)

	def __send_absacc_to_timeline_event(self):
		data = []
		for i in range(len(self)):
			vel = self.get_acceleration(i)
			if vel is not None:
				data.append([i,math.sqrt(vel[1]**2+vel[0]**2)])
		self.mainwindow.add_graph('{0} absolute acceleration'.format(self.name), data)


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


	def name_updated(self, newname): pass
	
	
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


	@property
	def name(self): return self._name.value
	@name.setter
	def name(self, value):
		if not hasattr(self, '_name_changed_activated'): self._name.value = value
		if hasattr(self, 'treenode'): self.treenode.setText(0,value)
		
		for dialog in PathsSelectorDialog.instantiated_dialogs: dialog.refresh()