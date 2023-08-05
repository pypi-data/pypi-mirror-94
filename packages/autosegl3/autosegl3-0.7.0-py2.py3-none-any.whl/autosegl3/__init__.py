"""Top-level package for L3 Auto-segmentation Tool."""

__author__ = """Ralph Brecheisen"""
__email__ = 'ralph.brecheisen@gmail.com'
__version__ = '0.7.0'

from .cnn import AutoSegL3CNN
from .autosegl3 import AutoSegL3
from . import models
from . import utils
