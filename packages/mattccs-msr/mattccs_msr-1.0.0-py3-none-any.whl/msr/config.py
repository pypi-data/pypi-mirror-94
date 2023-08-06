"""
Project configuration information.
"""

import os
import pathlib


VERSION = '1.0.0'


DEFAULT_CONFIG_HOME_VAR = 'XDG_CONFIG_HOME'
DEFAULT_CONFIG_HOME_PATH = pathlib.Path.home() / '.config'
CONFIG_HOME_PATH = os.environ.get(DEFAULT_CONFIG_HOME_VAR,
                                  pathlib.Path.home() / DEFAULT_CONFIG_HOME_PATH)

CONFIG_HOME_NAME = 'mattccs-msr'
CONFIG_HOME = pathlib.Path(CONFIG_HOME_PATH) / CONFIG_HOME_NAME

STORAGE_NAME = 'urls.txt'
STORAGE_PATH = CONFIG_HOME / STORAGE_NAME
