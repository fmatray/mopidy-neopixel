import logging
import pathlib

import pkg_resources

from mopidy import config, ext

#__version__ = pkg_resources.get_distribution("Mopidy-NeoPixel").version
__version__ = '0.1.0'
logger = logging.getLogger(__name__)


class Extension(ext.Extension):

    dist_name = "Mopidy-NeoPixel"
    ext_name = "neopixel"
    version = __version__

    def get_default_config(self):
        return config.read(pathlib.Path(__file__).parent / "ext.conf")

    def get_config_schema(self):
        schema = super().get_config_schema()
        schema["pin"] = config.Integer()
        schema["nb_leds"] = config.Integer()
        return schema

    def setup(self, registry):
        from .frontend import NeoPixelFrontend
        registry.add("frontend", NeoPixelFrontend)

