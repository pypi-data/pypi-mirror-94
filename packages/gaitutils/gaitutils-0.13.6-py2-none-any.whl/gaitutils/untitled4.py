# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 10:47:20 2019

@author: vicon123
"""

import logging

from gaitutils import autoprocess


logging.basicConfig(level=logging.DEBUG)

autoprocess._do_autoproc(
    u"D:\\ViconData\\Clinical\\D0050_LR\\2019_9_5_postOp2v_itsenäinen_LR\\2019_9_5_postOp2v_itsenäinen_LR04.Trial.enf"
)
