import math
from pysettings import conf
from pyforms import BaseWidget
from pyforms.Controls import ControlButton
from pyforms.Controls import ControlCombo
from pyforms.Controls import ControlLabel
from pyforms.Controls import ControlText
from pythonvideoannotator.utils import tools

from pythonvideoannotator_models.models.video.objects.object2d.datasets.value import Value
from pythonvideoannotator_models_gui.models.video.objects.object2d.datasets.dataset_gui import DatasetGUI


if conf.PYFORMS_USE_QT5:
	from PyQt5 import QtGui

else:	
	from PyQt4 import QtGui



class ValueGUI(DatasetGUI, Value, BaseWidget):

	def __init__(self, object2d=None):
		DatasetGUI.__init__(self)
		Value.__init__(self, object2d)
		BaseWidget.__init__(self, '2D Object', parent_win=object2d)

		self._remove_btn = ControlButton('Remove')

		self._formset = [ 
			'_name',
			'_remove_btn',
			' '
		]
		#### set controls ##############################################
		self._remove_btn.icon = conf.ANNOTATOR_ICON_REMOVE

		#### set events #################################################
		self._remove_btn.value = self.remove_dataset

		self.create_tree_nodes()

	######################################################################
	### FUNCTIONS ########################################################
	######################################################################

	def __derivate_data(self):
		for i in range(1, len(self)):
			a = self[i-1]
			b = self[i]
			if a is not None and b is not None:
				self._values[i-1] = b-a
			else:
				self._values[i-1] = 0
		QtGui.QMessageBox.about(self, "Info", "Operation complete.")

	def create_popupmenu_actions(self):

		fullname = self.name
		action = tools.make_lambda_func(self.send_2_timeline_event, graph_name=fullname, data_func=self.get_value )
		self.tree.add_popup_menu_option(
			label='View on the timeline', 
			function_action=action ,
			item=self.treenode,
			icon=conf.ANNOTATOR_ICON_TIMELINE
		)
		action = tools.make_lambda_func(self.export_2_csvfile_event, data_func=self.get_value )
		self.tree.add_popup_menu_option(
			label='Export to file',
			function_action=action ,
			item=self.treenode,
			icon=conf.PYFORMS_ICON_EVENTTIMELINE_EXPORT
		)
		
		self.tree.add_popup_menu_option(
			label='Derivate',
			function_action=self.__derivate_data ,
			item=self.treenode,
			icon=conf.ANNOTATOR_ICON_PATH
		)
		
		self.tree.add_popup_menu_option("-", item=self.treenode)
		self.tree.add_popup_menu_option(
			label='Remove', 
			function_action=self.remove_dataset, 
			item=self.treenode, icon=conf.ANNOTATOR_ICON_DELETE
		)

		

	def create_tree_nodes(self):
		self.treenode = self.tree.create_child(self.name, icon=conf.ANNOTATOR_ICON_INFO, parent=self.parent_treenode )
		self.treenode.win = self
		self.create_popupmenu_actions()

		

	

	@property
	def mainwindow(self): 	 return self.object2d.mainwindow
	@property 
	def tree(self): return self.object2d.tree
	@property 
	def video_capture(self): return self._object2d.video_capture
	@property 
	def parent_treenode(self):  return self.object2d.treenode
