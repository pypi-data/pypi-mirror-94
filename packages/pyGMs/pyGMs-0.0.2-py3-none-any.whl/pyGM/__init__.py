"""
pyGM: Python Graphical Model code

A simple graphical model class for learning about, testing, and developing algorithms
for graphical models.

Version 0.0.1 (2015-09-28)
Version 0.0.2 (2021-02-09)

(c) 2015- Alexander Ihler under the FreeBSD license; see license.txt for details.
"""

import numpy as np;
from sortedcontainers import SortedSet as sset;

from .factor import *
#from .factorSparse import *
from .graphmodel import *
from .filetypes import *
from .misc import *
from .draw import *


__title__ = 'pyGM'
__version__ = '0.0.2'
__author__ = 'Alexander Ihler'
__license__ = 'FreeBSD'
__copyright__ = '2015-2021, Alexander Ihler'


