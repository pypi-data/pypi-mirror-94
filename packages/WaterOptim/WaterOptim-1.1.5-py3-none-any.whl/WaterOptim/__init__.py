# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 08:46:03 2020

@author: HEDI
"""

PY = 3.14
from .__version__ import __version__
#from .wpinch_mono import __pinch__
from .uiwpinch import pinch
__all__ = ['__version__',"pinch"]