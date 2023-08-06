""" xaview also known as glorot
it is more easy for me because tensorflow uses glorot
"""

from torch.nn.init import (xavier_uniform_,
                          xavier_normal_)

#simple aliasing
glorot_normal = xavier_uniform_
glorot_unified = xavier_normal_
