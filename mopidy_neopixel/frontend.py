from __future__ import unicode_literals
import logging
import colorsys
import threading
from time import sleep

from mopidy import core
from mopidy.audio import PlaybackState

from colorthief import ColorThief
from urllib import request

import pykka
import board
import neopixel

logger = logging.getLogger(__name__)

class NeoPixelThread(threading.Thread):
    def __init__(self, core, pin, nb_leds):
        super().__init__()
        self.name = "NeoPixel Thread"
        self.core = core
        self.pin, self.nb_leds = pin, nb_leds
        
        self.current_track = None
        self.dominant_color = None
        self._stop = threading.Event()

        if self.nb_leds == 0:
            raise exceptions.FrontendError(f"NeoPixel startup failed: nb_leds must be at least 1")

        pins = {10: board.D10,
                12: board.D12,
                18: board.D18,
                21: board.D21 }
        try: 
            self.pixels = neopixel.NeoPixel(pins[self.pin], self.nb_leds)
            self.pixels.fill((255, 0, 0))
            sleep(1)
            self.pixels.fill((0, 255, 0))
            sleep(1)
            self.pixels.fill((0, 0, 255))
            sleep(1)
        except KeyError as exc:
            raise exceptions.FrontendError(f"NeoPixel startup failed: {exc}")

    def run(self):
        led = 0
        while not self._stop.isSet():
            if self.current_track and self.core.playback.get_state().get() == PlaybackState.PLAYING:
                if self.dominant_color:
                    self.pixels[led] = self.dominant_color
                else:
                    self.rainbow_wheel(led)
                led = (led + 1) % self.pixels.n 
            else:
                self.pixels.fill((0, 0, 0))
            sleep(1/50)

    def rainbow_wheel(self, led):
        length = self.current_track.length
        position = self.core.playback.get_time_position().get()
        
        if length and position:
            red, green, blue = colorsys.hsv_to_rgb(position/length, 1, 1)
            self.pixels[led] = tuple(map(int, (red * 255, green * 255, blue * 255)))

    def update_volume(self):
        self.pixels.brightness = self.core.mixer.get_volume().get()/100 if not self.core.mixer.get_mute().get() else 0    

    def update_track(self):
        logger.info("Updating...")
        self.dominant_color = None
        self.current_track = self.core.playback.get_current_track().get()
        if not self.current_track:
            logger.info("No current track")
            return

        images = self.core.library.get_images([self.current_track.uri]).get()
        if not images:
            logger.info("Image not found")
            return

        logger.info(images)
        image_uri = images[self.current_track.uri][0].uri
        if image_uri.startswith("http://") or image_uri.startswith("https://"):
            image = ColorThief(request.urlopen(image_uri)) 
        else:
            image = ColorThief(image_uri)
        
        self.dominant_color = image.get_color(quality=1)

        logger.info("Updated: %s", self.dominant_color)
    
    def stop(self):
        self.pixels.fill((0, 0, 0))
        self._stop.set()


class NeoPixelFrontend(pykka.ThreadingActor, core.CoreListener):
    def __init__(self, config, core):
        super().__init__()
        self.config = config['neopixel']
        self.core = core

    def on_start(self):
        logger.info("Starting Mopidy NeoPixel")
        self.neopixelthread = NeoPixelThread(self.core, self.config['pin'], self.config['nb_leds'] )
        self.neopixelthread.start()

    def on_stop(self):
        logger.info("Stoping Mopidy NeoPixel")
        self.neopixelthread.stop()

    def on_event(self, event, **kwargs):
        if event in ["track_playback_started", "track_playback_ended"]:
            self.neopixelthread.update_track()
        elif event in ["volume_changed", "mute_changed"]:
            self.neopixelthread.update_volume()
