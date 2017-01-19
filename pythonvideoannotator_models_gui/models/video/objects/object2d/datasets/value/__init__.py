from pythonvideoannotator_models_gui.models.video.objects.object2d.datasets.value.value_gui import ValueGUI
from pysettings import conf


Value = type(
	'Value',
	tuple(conf.MODULES.find_class('models.video.objects.object2d.datasets.value.Value') + [ValueGUI]),
	{}
)
