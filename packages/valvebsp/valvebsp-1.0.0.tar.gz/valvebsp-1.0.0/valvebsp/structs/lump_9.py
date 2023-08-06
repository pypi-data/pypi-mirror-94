"""
Lump 9 - Occlusion
==================

This lump contains a single :any:`doccluder_t`, regrouping multiple :any:`doccluderdata_t` and :any:`doccluderpolydata_t`
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from future import standard_library
standard_library.install_aliases()

from construct import *  # NOQA: #402
from valvebsp.constants import *  # NOQA: #402
from valvebsp.exceptions import *  # NOQA: #402
from valvebsp.structs.common import *  # NOQA: #402

doccluderdata_t = Struct(
    'flags' / Int32sl,
    'firstPoly' / Int32sl,
    'polyCount' / Int32sl,
    'mins' / Vector,
    'maxs' / Vector,
    'area' / Int32sl,
)

doccluderpolydata_t = Struct(
    'firstVertexIndex' / Int32sl,
    'vertexCount' / Int32sl,
    'planeNum' / Int32sl,
)

doccluder_t = Struct(
    'count' / Int32sl,
    'data' / doccluderdata_t[this.count],
    'polyDataCount' / Int32sl,
    'polyData' / doccluderpolydata_t[this.polyDataCount],
    'vertexIndexCount' / Int32sl,
    'vertexIndices' / Int32sl[this.vertexIndexCount],
)


def lump_9(header, profile=None):
    if header.version == 2:
        return lump_struct(LUMP_OCCLUSION, doccluder_t, header)
    else:
        raise LumpVersionUnsupportedError(header.version)
