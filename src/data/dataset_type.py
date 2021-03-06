"""
This source code is licensed under the MIT license found in the
LICENSE file in the root directory of this source tree.
"""

from enum import Enum


class DatasetType(Enum):
    """
    Available dataset types are defined here
    """
    BackendEndToEnd = 1
    BackendLayerWise = 2
