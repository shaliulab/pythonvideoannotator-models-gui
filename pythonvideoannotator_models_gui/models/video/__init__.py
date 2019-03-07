from pythonvideoannotator_models_gui.models.video.video_gui import VideoGUI
from confapp import conf

Video = type(
	'Video',
	tuple(conf.MODULES.find_class('models.video.Video') + [VideoGUI]),
	{}
)
