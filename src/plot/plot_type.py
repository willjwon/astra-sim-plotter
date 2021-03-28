"""
This source code is licensed under the MIT license found in the
LICENSE file in the root directory of this source tree.
"""

from enum import Enum


class PlotType(Enum):
    """
    Available plots are listed here.
    """
    CommsTime_CommScale = 1
    CommsTime_Topology = 2
    CommsTime_Cost = 3

