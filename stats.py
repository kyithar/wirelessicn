# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 17:08:37 2016

@author: kyithar
"""

class Stats:
    def __init__(self,cDecision,p_hit,i_hit,avg_delay,profit,bh,req):
        self.cDecision =cDecision
#        self.alpha = alpha
        self.p_hit = p_hit
        self.i_hit = i_hit
        self.avg_delay = avg_delay
        self.profit = profit
        self.bh =bh
        self.req = req