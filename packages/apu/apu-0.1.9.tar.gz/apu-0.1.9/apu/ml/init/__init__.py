""" apu.ml.init: anton python utils machine learning initializers """

__version__ = (0, 0, 1)
__email__ = "anton.feldmann@gmail.com"
__author__ = "anton feldmann"


from apu.ml.init.glorot import (glorot_normal, glorot_unified)
from apu.ml.init.he import (he_normal,
                            he_uniform)

__all__=['glorot_normal',
         "glorot_unified",
         "he_normal",
         "he_uniform"]
