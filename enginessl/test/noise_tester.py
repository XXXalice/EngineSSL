import inspect
import os
import sys
REL_HIERARCHY = 2
BASE_PATH = os.path.join(''.join(inspect.stack()[0][1].split('/')[:-REL_HIERARCHY]))
EFFECT_MODULE = os.path.join(BASE_PATH, 'ml')
sys.path.append(EFFECT_MODULE)
from data_handling import effect_func