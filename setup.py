import re
from setuptools import setup, find_packages


def get_version(filename):
    content = open(filename).read()
    metadata = dict(re.findall("__([a-z]+)__ = '([^']+)'", content))
    return metadata['version']


setup(
    name='Mopidy-NeoPixel',
    version=get_version('mopidy_neopixel/__init__.py'),
    url='https://github.com/fmatray/mopidy-neopixel',
    license='Apache License, Version 2.0',
    author='Frédéric Matray-Marin',
    author_email='frederic.matray@me.com',
    description='You can always add leds to a mopidy player :-)',
    long_description=open('README.rst').read(),
    packages=find_packages(exclude=['tests', 'tests.*']),
    zip_safe=False,
    include_package_data=True,
    download_url='https://github.com/fmatray/mopidy-neopixel/archive/0.1.0.zip',
    keywords=['Mopidy', 'Mopidy-frontend', 'Neopixels'],
    install_requires=[
        'setuptools',
        'Mopidy >= 0.14',
        'Pykka >= 1.1',
        'rpi_ws281x',
        'adafruit-circuitpython-neopixel',
        'colorthief'
    ],
    entry_points={
        'mopidy.ext': [
            'neopixel = mopidy_neopixel:Extension',
        ],
    },
    classifiers=[
        'Environment :: No Input/Output (Daemon)',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Multimedia :: Sound/Audio :: Players',
    ],
)
