from __future__ import unicode_literals
import logging
import colorsys
import threading
from time import sleep

from mopidy import core
from mopidy.audio import PlaybackState
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

    def stop(self):
        self.pixels.fill((0, 0, 0))
        self._stop.set()

    def rainbow_wheel(self, current_track, led):
        length = current_track.length
        position = self.core.playback.get_time_position().get()
        brightness = self.core.mixer.get_volume().get()/100 if not self.core.mixer.get_mute().get() else 0   

        red, green, blue = colorsys.hsv_to_rgb(position/length, 1, brightness)
        self.pixels[led] = tuple(map(int, (red * 255, green * 255, blue * 255)))

    def run(self):
        led = 0
        while not self._stop.isSet():
            current_track = self.core.playback.get_current_track().get()
            if current_track and self.core.playback.get_state().get() == PlaybackState.PLAYING:
                self.rainbow_wheel(current_track, led)
                led = (led + 1) % self.pixels.n 
            else:
                self.pixels.fill((0, 0, 0))
            sleep(1/50)

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
