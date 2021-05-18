from setuptools import setup, find_packages

APP = ['main.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'AppIcon.icns',
    'plist': {
        'LSUIElement': True,
    },
    'packages': ['pypresence', 'rumps'],
    'resources': ['config.ini', 'getTrack.scpt', 'AppIcon.icns']
}

setup(
    app=APP,
    data_files=DATA_FILES,
    name='Apple Music RPC',
    options={'py2app': OPTIONS},
    packages=find_packages(),
    setup_requires=['py2app'],
)
