#!/usr/bin/env python

# --- LICENSE.txt -----------------------------------------------------------------
#
#    Copyright 2013 Matthew Walker
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

__author__ = "Matthew Walker & The Elemental of Creation"
__version__ = "0.29.1"

from msglite import constants
from msglite.attachment import Attachment
from msglite.message import Message
from msglite.prop import create_prop
from msglite.properties import Properties
from msglite.recipient import Recipient
from msglite.utils import parse_type, properHex
