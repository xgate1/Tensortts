import tensorflow as tf

import yaml
import numpy as np
import matplotlib.pyplot as plt

import IPython.display as ipd

import os
import sys
l=os.getcwd()
l2=os.path.join(l,'Tensor_ver\TensorflowTTS-master')
sys.path.append(l2)

l3=os.path.join(l2,'tensorflow_tts')
sys.path.append(l3)

# from tensorflow_tts.processor import LJSpeechProcessor
from tensorflow_tts.text import symbols, _symbol_to_id
from tensorflow_tts.text import text_to_sequence