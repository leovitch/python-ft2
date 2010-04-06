# python-ft2
# Copyright (C) 2010 Ryan Coyner
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.

import ctypes
import logging


logger = logging.getLogger('ft2')
logger.setLevel(logging.INFO)
logger.propagate = False

if len(logger.handlers) == 0:
    logger.addHandler(logging.NullHandler())

try:
    logger.info('Loading libfreetype...')
    libfreetype = ctypes.cdll.LoadLibrary('libfreetype.so')
except OSError as e:
    logger.warning(e)


from ft2.system import *
from ft2.types import *
from ft2.image import *
from ft2.api import *
