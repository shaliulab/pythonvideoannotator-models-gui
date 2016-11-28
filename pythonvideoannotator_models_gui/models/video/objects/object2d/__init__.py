from pysettings import conf
from pythonvideoannotator_models_gui.models.video.objects.object2d.object2d_gui import Object2dGUI

Object2D = type(
	'Object2D',
	tuple(conf.MODULES.find_class('models.video.objects.object2d.Object2d') + [Object2dGUI]),
	{}
)
