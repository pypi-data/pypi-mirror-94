#! -*- coding: utf-8 -*-
from .quantize import mmcq
from .palette import get_palette, get_dominant_color


__version__ = (0, 1, 0)
__all__ = '__version__', 'get_dominant_color', 'get_palette', 'mmcq'
version = '{}.{}.{}'.format(*__version__)
