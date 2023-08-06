"""
Lump 50 - Water Overlays
========================

This lump contains an array of dwateroverlay_t, identical to :any:`doverlay_t`. (:ref:`as seen in lump_45<lump_45>`).
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from future import standard_library
standard_library.install_aliases()

from construct import *  # NOQA: #402
from valvebsp.constants import *  # NOQA: #402
from valvebsp.exceptions import *  # NOQA: #402
from valvebsp.structs.common import *  # NOQA #402
from valvebsp.structs.lump_45 import doverlay_t as dwateroverlay_t  # NOQA #402


def lump_50(header, profile=None):
    if header.version != 0:
        raise LumpVersionUnsupportedError(header.version)
    return lump_array(LUMP_WATEROVERLAYS, dwateroverlay_t, header)
