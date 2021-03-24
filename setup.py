from setuptools import setup

APP = ['AppleMusicRPC.py']
DATA_FILES = [('Resources', ['./Resources/config.ini', './Resources/getTrack.scpt', './Resources/icon.png'])]
PACKAGES = ['app', 'music', 'rpc']
OPTIONS = {
    'includes': ['pypresence', 'rumps'],
    'iconfile': './Resources/AppIcon.icns'
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
