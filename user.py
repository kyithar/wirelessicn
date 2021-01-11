# -*- coding: utf-8 -*-
"""
Created on Tue Jun 14 20:49:35 2016

@author: kyithar
"""

from msg.interest import Interest

class User:
     def __init__(self,name,req_content,tot_chunk,bs,mv):
        self.name = name
        self.req_content = req_content
        self.tot_chunk = tot_chunk
        self.chunk_count = 1
        self.tot_delay = 0.0
        self.avg_delay = 0.0
        self.bs=bs
        self.mv=mv
        
    
     def create_int(self,start_t):
         return Interest(self.req_content,self.chunk_count,self.name,start_t)
                  
     def receive(self,int_msg):
         self.chunk_count = int_msg.chunk_num+1



