from setuptools import setup

APP = ['snst.py']
OPTIONS = {'argv_emulation': False}

setup(app=APP, options={'py2app':OPTIONS},setup_requires=['py2app'])
