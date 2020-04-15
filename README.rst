****************************
Mopidy-NeoPixel
****************************

.. image:: https://img.shields.io/pypi/v/Mopidy-NeoPixel
    :target: https://pypi.org/project/Mopidy-NeoPixel/
    :alt: Latest PyPI version

.. image:: https://img.shields.io/circleci/build/gh/fmatray/mopidy-neopixel
    :target: https://circleci.com/gh/fmatray/mopidy-neopixel
    :alt: CircleCI build status

.. image:: https://img.shields.io/codecov/c/gh/fmatray/mopidy-neopixel
    :target: https://codecov.io/gh/fmatray/mopidy-neopixel
    :alt: Test coverage

We always can add leds to mopidy players.


Installation
============

Install by running::

    python3 -m pip install Mopidy-NeoPixel

See https://mopidy.com/ext/neopixel/ for alternative installation methods.


Configuration
=============

Before starting Mopidy, you must add configuration for
Mopidy-NeoPixel to your Mopidy configuration file::

   [neopixel]
   enabled = true
   #Led Pin. You can only use pins 10, 12, 18 or 21
   pin = 12
   # Number of leds
   nb_leds = 7

Limitations
===========

Mopidy MUST run as root to have access to /dev/mem. 
As long as you don't use this plugin to rule a sattelite or a WMD, it should be ok :-)
Keep this for a small personnal project.

Project resources
=================

- `Source code <https://github.com/fmatray/mopidy-neopixel>`_
- `Issue tracker <https://github.com/fmatray/mopidy-neopixel/issues>`_
- `Changelog <https://github.com/fmatray/mopidy-neopixel/blob/master/CHANGELOG.rst>`_


Credits
=======

- Original author: `Frédéric Matray-Marin <https://github.com/fmatray>`__
- Current maintainer: `Frédéric Matray-Marin <https://github.com/fmatray>`__
- `Contributors <https://github.com/fmatray/mopidy-neopixel/graphs/contributors>`_
