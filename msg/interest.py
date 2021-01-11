# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 11:25:47 2016

@author: kyithar
"""

class Interest:
    def __init__(self,name,chunk_num,usr_name,start_t):
        self.name = name
        self.chunk_num = chunk_num
        self.usr_name = usr_name
        self.type='i'
        self.hash_value=hash(name+chunk_num)
        self.start_t =start_t

    