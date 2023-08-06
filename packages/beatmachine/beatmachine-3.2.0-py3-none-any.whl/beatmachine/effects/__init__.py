"""
The `effects` module provides a base effect class as well as some common effects to play with.
"""

from . import base, periodic, temporal

load_from_dict = base.EffectRegistry.load_effect_from_dict
load_effect = base.EffectRegistry.load_effect

from .periodic import *
from .temporal import *
