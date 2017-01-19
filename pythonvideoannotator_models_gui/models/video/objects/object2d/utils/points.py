import math, numpy as np

def points_angle(p1, p2): 
	x1, y1 = p1
	x2, y2 = p2
	rads = math.atan2(-(y2-y1),x2-x1)
	rads %= 2*math.pi
	return rads

def lin_dist(p1, p2): return np.linalg.norm( (p1[0]-p2[0], p1[1]-p2[1]) )