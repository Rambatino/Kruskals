"""
This module provides helper functions for the rest of the testing module
"""

from collections import Iterable
import os
import sys

ROOT_FOLDER = os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + '/../')

sys.path.append(ROOT_FOLDER)

from Kruskals import *
