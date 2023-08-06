#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='pydream-led-3',
      version='0.3.1',
      description='PyDream3 - driver for Dream Cheeky 21x7 LED display (VendorId: 0x1d34 DeviceId: 0x001)',
      author='Benjamin Pryor',
      author_email='programmer2514@gmail.com',
      url='https://github.com/programmer2514/pydream-led-3',
      packages=['pydream3'],
      install_requires=[
          'pyusb',
      ],
     )
