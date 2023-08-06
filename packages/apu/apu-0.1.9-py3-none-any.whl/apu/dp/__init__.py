""" apu.dp: anton python utils design pattern module """

__version__ = (0, 0, 2)
__email__ = "anton.feldmann@gmail.com"
__author__ = "anton feldmann"

from apu.dp.null import Null
from apu.dp.blackboard import Blackboard, MetaInfo
from apu.dp.iterator import (AlphabeticalOrderIterator,
                            AlphabeticalOrderCollection)
from apu.dp.singleton import (singleton, Singleton)

__all__ = ['Null',
           "Blackboard",
           "MetaInfo",
           "AlphabeticalOrderIterator",
           "AlphabeticalOrderCollection",
           "singleton",
           "Singleton"]
