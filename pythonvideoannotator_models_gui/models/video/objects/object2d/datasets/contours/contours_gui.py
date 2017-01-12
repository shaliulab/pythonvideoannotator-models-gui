import math, cv2, numpy as np
from pysettings import conf
from pyforms import BaseWidget
from PyQt4 import QtCore, QtGui
from pyforms.Controls import ControlButton
from pyforms.Controls import ControlCombo
from pyforms.Controls import ControlLabel
from pyforms.Controls import ControlText
from pythonvideoannotator.utils import tools
from pythonvideoannotator_models_gui.models.video.objects.object2d.utils import points as pts_utils
from pythonvideoannotator_models.models.video.objects.object2d.datasets.contours import Contours

from pythonvideoannotator_models_gui.models.video.objects.object2d.datasets.dataset_gui import DatasetGUI


class ContoursGUI(DatasetGUI, Contours, BaseWidget):

	def __init__(self, object2d=None):
		DatasetGUI.__init__(self)
		Contours.__init__(self, object2d)
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
		self._remove_btn.value			 = self.remove_dataset

		self.create_tree_nodes()

	######################################################################
	### FUNCTIONS ########################################################
	######################################################################

	def create_tree_nodes(self):

		self.treenode = self.tree.create_child(self.name, icon=conf.ANNOTATOR_ICON_CONTOUR, parent=self.parent_treenode )
		self.tree.add_popup_menu_option(
			label='Remove', 
			function_action=self.remove_dataset, 
			item=self.treenode, icon=conf.ANNOTATOR_ICON_DELETE
		)
		self.treenode.win = self

		self.create_group_node('position', icon=conf.ANNOTATOR_ICON_POSITION)
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

		self.create_tracking_tree_nodes()



	######################################################################
	### FUNCTIONS ########################################################
	######################################################################

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








	################# BOUNDING RECT ###################################################
		
	def create_tracking_boundingrect_tree_nodes(self):
		self.create_group_node('bounding rect', icon=conf.ANNOTATOR_ICON_AREA)
		self.create_data_node('bounding rect > left x', icon=conf.ANNOTATOR_ICON_X)
		self.create_data_node('bounding rect > left y', icon=conf.ANNOTATOR_ICON_Y)
		self.create_data_node('bounding rect > width',  icon=conf.ANNOTATOR_ICON_WIDTH)
		self.create_data_node('bounding rect > height', icon=conf.ANNOTATOR_ICON_HEIGHT)
		self.create_data_node('bounding rect > aspect ratio', icon=conf.ANNOTATOR_ICON_ASPECT_RATIO)
		self.create_data_node('bounding rect > area',   icon=conf.ANNOTATOR_ICON_AREA)
		self.create_data_node('bounding rect > extend', icon=conf.ANNOTATOR_ICON_INFO)

	def get_boundingrect_leftx_value(self, index):
		v = self.get_bounding_box(index)
		return v[0] if v is not None else None

	def get_boundingrect_lefty_value(self, index):
		v = self.get_bounding_box(index)
		return v[1] if v is not None else None

	def get_boundingrect_width_value(self, index):
		v = self.get_bounding_box(index)
		return v[2] if v is not None else None

	def get_boundingrect_height_value(self, index):
		v = self.get_bounding_box(index)
		return v[3] if v is not None else None

	def get_boundingrect_aspectratio_value(self, index):
		cnt = self.get_contour(index)
		if cnt is None: return None
		x,y,w,h = cv2.boundingRect(cnt)
		return float(w)/float(h)

	def get_boundingrect_area_value(self, index):
		v = self.get_bounding_box(index)
		return v[0]*v[1] if v is not None else None
		
	def get_boundingrect_extend_value(self, index):
		cnt = self.get_contour(index)
		if cnt is None: return None
		area = cv2.contourArea(cnt)
		x,y,w,h = cv2.boundingRect(cnt)
		rect_area = w*h
		return float(area)/float(rect_area)

	################# BOUNDING RECT ###################################################



	def create_tracking_minenclosingcircle_tree_nodes(self):
		self.create_group_node('minimum enclosing circle', 		icon=conf.ANNOTATOR_ICON_CIRCLE)
		self.create_group_node('minimum enclosing circle > x', 	icon=conf.ANNOTATOR_ICON_X)
		self.create_group_node('minimum enclosing circle > y', 	icon=conf.ANNOTATOR_ICON_Y)
		self.create_group_node('minimum enclosing circle > radius', icon=conf.ANNOTATOR_ICON_WIDTH)


	################# EXTREME POINTS ####################################################
		
	def create_tracking_extremepoints_tree_nodes(self):
		self.create_group_node('extreme points', 			icon=conf.ANNOTATOR_ICON_POINT)
		
		self.create_group_node('extreme points > p1', 	icon=conf.ANNOTATOR_ICON_POINT)
		self.create_data_node('extreme points > p1 > x', 	icon=conf.ANNOTATOR_ICON_X)
		self.create_data_node('extreme points > p1 > y', 	icon=conf.ANNOTATOR_ICON_Y)
		
		self.create_group_node('extreme points > p2', 	icon=conf.ANNOTATOR_ICON_POINT)
		self.create_data_node('extreme points > p2 > x', 	icon=conf.ANNOTATOR_ICON_X)
		self.create_data_node('extreme points > p2 > y', 	icon=conf.ANNOTATOR_ICON_Y)
		
		self.create_data_node('extreme points > angle', 	icon=conf.ANNOTATOR_ICON_ANGLE)		
		
	def get_extremepoints_p1_x_value(self, index):
		v = self.get_extreme_points(index)
		return v[0][0] if v is not None else None

	def get_extremepoints_p1_y_value(self, index):
		v = self.get_extreme_points(index)
		return v[0][1] if v is not None else None

	def get_extremepoints_p2_x_value(self, index):
		v = self.get_extreme_points(index)
		return v[1][0] if v is not None else None

	def get_extremepoints_p2_y_value(self, index):
		v = self.get_extreme_points(index)
		return v[1][1] if v is not None else None

	def get_extremepoints_angle_value(self, index):
		v = self.get_extreme_points(index)
		return math.degrees(pts_utils.points_angle(v[0], v[1])) if v is not None else None

	################# FIT ELLISPSE ####################################################











	################# FIT ELLIPSE ####################################################
		
	def create_tracking_fitellipse_tree_nodes(self):
		self.create_group_node('fit ellipse', 				 icon=conf.ANNOTATOR_ICON_ELLIPSE)
		self.create_data_node('fit ellipse > center x', 		 icon=conf.ANNOTATOR_ICON_X)
		self.create_data_node('fit ellipse > center y', 		 icon=conf.ANNOTATOR_ICON_Y)
		self.create_data_node('fit ellipse > major axis size', icon=conf.ANNOTATOR_ICON_HEIGHT)
		self.create_data_node('fit ellipse > minor axis size', icon=conf.ANNOTATOR_ICON_WIDTH)
		self.create_data_node('fit ellipse > angle', 			 icon=conf.ANNOTATOR_ICON_ANGLE)

		
		
	def get_fitellipse_centerx_value(self, index):
		v = self.get_fit_ellipse(index)
		return v[0][0] if v is not None else None

	def get_fitellipse_centery_value(self, index):
		v = self.get_fit_ellipse(index)
		return v[0][1] if v is not None else None

	def get_fitellipse_majoraxissize_value(self, index):
		v = self.get_fit_ellipse(index)
		return v[1][0] if v is not None else None

	def get_fitellipse_minoraxissize_value(self, index):
		v = self.get_fit_ellipse(index)
		return v[1][1] if v is not None else None

	def get_fitellipse_angle_value(self, index):
		v = self.get_fit_ellipse(index)
		return v[2] if v is not None else None


	################# FIT ELLIPSE ####################################################









	################# CONVEX HULL ####################################################
		
	def create_tracking_convexhull_tree_nodes(self):
		self.create_group_node('convex hull', 		  icon=conf.ANNOTATOR_ICON_HULL)
		self.create_data_node('convex hull > solidity', icon=conf.ANNOTATOR_ICON_BLACK_CIRCLE)
		
	def get_convexhull_solidity_value(self, index):
		cnt = self.get_contour(index)
		if cnt is None: return None
		area = cv2.contourArea(cnt)
		hull = cv2.convexHull(cnt)
		hull_area = cv2.contourArea(hull)
		return float(area)/float(hull_area)

	################# CONVEX HULL ####################################################




	################# ROTATED RECTANGLE ####################################################

	def create_tracking_rotatedrectangle_tree_nodes(self):
		self.create_group_node('rotated rectangle', 		  	icon=conf.ANNOTATOR_ICON_AREA)
		self.create_data_node('rotated rectangle > center x', 	icon=conf.ANNOTATOR_ICON_X)
		self.create_data_node('rotated rectangle > center y', 	icon=conf.ANNOTATOR_ICON_Y)
		self.create_data_node('rotated rectangle > width', 		icon=conf.ANNOTATOR_ICON_HEIGHT)
		self.create_data_node('rotated rectangle > height', 	icon=conf.ANNOTATOR_ICON_WIDTH)
		self.create_data_node('rotated rectangle > angle', 		icon=conf.ANNOTATOR_ICON_ANGLE)

	def get_rotatedrectangle(self, index):
		contour = self.get_contour(index)
		if contour is None: return None
		return cv2.minAreaRect(contour)

	def get_rotatedrectangle_centerx_value(self, index):
		v = self.get_rotatedrectangle(index)
		return v[0][0] if v is not None else None

	def get_rotatedrectangle_centery_value(self, index):
		v = self.get_rotatedrectangle(index)
		return v[0][1] if v is not None else None

	def get_rotatedrectangle_width_value(self, index):
		v = self.get_rotatedrectangle(index)
		return v[1][0] if v is not None else None

	def get_rotatedrectangle_height_value(self, index):
		v = self.get_rotatedrectangle(index)
		return v[1][1] if v is not None else None

	def get_rotatedrectangle_angle_value(self, index):
		v = self.get_rotatedrectangle(index)
		return v[2] if v is not None else None

	

	################# ROTATED RECTANGLE ####################################################






	################# MOMENTS ####################################################

	def create_tracking_moments_tree_nodes(self):
		self.create_group_node('moments', 		  	icon=conf.ANNOTATOR_ICON_HULL)
		self.create_data_node('moments > m00', 	icon=conf.ANNOTATOR_ICON_X)
		self.create_data_node('moments > m10', 	icon=conf.ANNOTATOR_ICON_X)
		self.create_data_node('moments > m01', 	icon=conf.ANNOTATOR_ICON_X)
		self.create_data_node('moments > m20', 	icon=conf.ANNOTATOR_ICON_X)
		self.create_data_node('moments > m11', 	icon=conf.ANNOTATOR_ICON_X)
		self.create_data_node('moments > m02', 	icon=conf.ANNOTATOR_ICON_X)
		self.create_data_node('moments > m30', 	icon=conf.ANNOTATOR_ICON_X)
		self.create_data_node('moments > m21', 	icon=conf.ANNOTATOR_ICON_X)
		self.create_data_node('moments > m12', 	icon=conf.ANNOTATOR_ICON_X)
		self.create_data_node('moments > m03', 	icon=conf.ANNOTATOR_ICON_X)
		self.create_data_node('moments > mu20', 	icon=conf.ANNOTATOR_ICON_X)
		self.create_data_node('moments > mu11', 	icon=conf.ANNOTATOR_ICON_X)
		self.create_data_node('moments > mu02', 	icon=conf.ANNOTATOR_ICON_X)
		self.create_data_node('moments > mu30', 	icon=conf.ANNOTATOR_ICON_X)
		self.create_data_node('moments > mu21', 	icon=conf.ANNOTATOR_ICON_X)
		self.create_data_node('moments > mu12', 	icon=conf.ANNOTATOR_ICON_X)
		self.create_data_node('moments > mu03', 	icon=conf.ANNOTATOR_ICON_X)
		self.create_data_node('moments > nu20', 	icon=conf.ANNOTATOR_ICON_X)
		self.create_data_node('moments > nu11', 	icon=conf.ANNOTATOR_ICON_X)
		self.create_data_node('moments > nu02', 	icon=conf.ANNOTATOR_ICON_X)
		self.create_data_node('moments > nu30', 	icon=conf.ANNOTATOR_ICON_X)
		self.create_data_node('moments > nu21', 	icon=conf.ANNOTATOR_ICON_X)
		self.create_data_node('moments > nu12', 	icon=conf.ANNOTATOR_ICON_X)
		self.create_data_node('moments > nu03', 	icon=conf.ANNOTATOR_ICON_X)

	################# MOMENTS ####################################################

	def get_moments(self, index):
		contour = self.get_contour(index)
		if contour is None: return None
		return cv2.moments(contour)

	def get_moment(self, index, key):
		m = self.get_moments(index)
		return None if m is None else m[key]

	def get_moments_m00_value(self, index): return self.get_moment(index, 'm00')
	def get_moments_m10_value(self, index): return self.get_moment(index, 'm10')
	def get_moments_m01_value(self, index): return self.get_moment(index, 'm01')
	def get_moments_m20_value(self, index): return self.get_moment(index, 'm20')
	def get_moments_m11_value(self, index): return self.get_moment(index, 'm11')
	def get_moments_m02_value(self, index): return self.get_moment(index, 'm02')
	def get_moments_m30_value(self, index): return self.get_moment(index, 'm30')
	def get_moments_m21_value(self, index): return self.get_moment(index, 'm21')
	def get_moments_m12_value(self, index): return self.get_moment(index, 'm12')
	def get_moments_m03_value(self, index): return self.get_moment(index, 'm03')
	def get_moments_mu20_value(self, index): return self.get_moment(index, 'mu20')
	def get_moments_mu11_value(self, index): return self.get_moment(index, 'mu11')
	def get_moments_mu02_value(self, index): return self.get_moment(index, 'mu02')
	def get_moments_mu30_value(self, index): return self.get_moment(index, 'mu30')
	def get_moments_mu21_value(self, index): return self.get_moment(index, 'mu21')
	def get_moments_mu12_value(self, index): return self.get_moment(index, 'mu12')
	def get_moments_mu03_value(self, index): return self.get_moment(index, 'mu03')
	def get_moments_nu20_value(self, index): return self.get_moment(index, 'nu20')
	def get_moments_nu11_value(self, index): return self.get_moment(index, 'nu11')	
	def get_moments_nu30_value(self, index): return self.get_moment(index, 'nu02')
	def get_moments_nu02_value(self, index): return self.get_moment(index, 'nu30')
	def get_moments_nu21_value(self, index): return self.get_moment(index, 'nu21')
	def get_moments_nu12_value(self, index): return self.get_moment(index, 'nu12')
	def get_moments_nu03_value(self, index): return self.get_moment(index, 'nu03')



	################# HU MOMENTS ####################################################

	def create_tracking_humoments_tree_nodes(self):
		self.create_group_node('hu moments', 		icon=conf.ANNOTATOR_ICON_HULL)
		self.create_data_node('hu moments > hu0', 	icon=conf.ANNOTATOR_ICON_X)
		self.create_data_node('hu moments > hu1', 	icon=conf.ANNOTATOR_ICON_X)
		self.create_data_node('hu moments > hu2', 	icon=conf.ANNOTATOR_ICON_X)
		self.create_data_node('hu moments > hu3', 	icon=conf.ANNOTATOR_ICON_X)
		self.create_data_node('hu moments > hu4', 	icon=conf.ANNOTATOR_ICON_X)
		self.create_data_node('hu moments > hu5', 	icon=conf.ANNOTATOR_ICON_X)
		self.create_data_node('hu moments > hu6', 	icon=conf.ANNOTATOR_ICON_X)


	def get_humoments(self, index):
		moments = self.get_moments(index)
		if moments is None: return None
		return cv2.HuMoments(moments)

	def get_humoment(self, index, key):
		m = self.get_humoments(index)
		return None if m is None else m[key]

	def get_humoments_hu0_value(self, index): return self.get_humoment(index, 0)
	def get_humoments_hu1_value(self, index): return self.get_humoment(index, 1)
	def get_humoments_hu2_value(self, index): return self.get_humoment(index, 2)
	def get_humoments_hu3_value(self, index): return self.get_humoment(index, 3)
	def get_humoments_hu4_value(self, index): return self.get_humoment(index, 4)
	def get_humoments_hu5_value(self, index): return self.get_humoment(index, 5)
	def get_humoments_hu6_value(self, index): return self.get_humoment(index, 6)
	


	################# HU MOMENTS ####################################################










	def create_tracking_tree_nodes(self):
		################# CONTOUR #########################################################
		self.create_data_node('area', icon=conf.ANNOTATOR_ICON_AREA)
		self.create_data_node('perimeter', icon=conf.ANNOTATOR_ICON_AREA)
		
		self.create_data_node('equivalent diameter', icon=conf.ANNOTATOR_ICON_CIRCLE)

		self.create_tracking_boundingrect_tree_nodes()		
		self.create_tracking_fitellipse_tree_nodes()
		self.create_tracking_extremepoints_tree_nodes()
		self.create_tracking_convexhull_tree_nodes()
		self.create_tracking_rotatedrectangle_tree_nodes()
		self.create_tracking_minenclosingcircle_tree_nodes()
		self.create_tracking_moments_tree_nodes()
		self.create_tracking_humoments_tree_nodes()
				
	######################################################################
	### FUNCTIONS ########################################################
	######################################################################


	def draw(self, frame, frame_index):
		cnt = self.get_contour(frame_index)
		if cnt is not None: cv2.polylines(frame, np.array( [cnt] ), True, (0,255,0), 2)

		head, tail = self.get_extreme_points(frame_index)
		if head is not None:
			cv2.circle(frame, head, 5, (255,255,255), -1)
			cv2.circle(frame, head, 3, (100,0,100), -1)
		if tail is not None:
			cv2.circle(frame, tail, 5, (255,255,255), -1)
			cv2.circle(frame, tail, 3, (100,100,0), -1)


	################# CONTOUR #########################################################

	def get_area_value(self, index):
		cnt = self.get_contour(index)
		if cnt is None: return None
		return cv2.contourArea(cnt)

	def get_perimeter_value(self, index):
		cnt = self.get_contour(index)
		if cnt is None: return None
		return cv2.arcLength(cnt, True)

	def get_equivalentdiameter_value(self, index):
		cnt = self.get_contour(index)
		if cnt is None: return None
		area = cv2.contourArea(cnt)
		return np.sqrt(4*area/np.pi)


	

	@property
	def mainwindow(self): 	 return self.object2d.mainwindow
	@property 
	def tree(self): return self.object2d.tree
	@property 
	def video_capture(self): return self._object2d.video_capture

	@property 
	def parent_treenode(self):  return self.object2d.treenode
