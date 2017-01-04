from pysettings import conf
from pythonvideoannotator_models_gui.models.video.image.image_gui import ImageGUI

Image = type(
	'Image',
	tuple(conf.MODULES.find_class('models.video.image.Image') + [ImageGUI]),
	{}
)
