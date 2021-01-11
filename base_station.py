# -*- coding: utf-8 -*-
"""
Created on Tue Jun 14 19:00:51 2016

@author: kyithar
"""

class Base_station:    
    #def __init__(self,name,cache_size,bs_power,transmit_power,bs_height,bandwidth,bs_gain,bs_radius,backhaul):
    def __init__(self,name,cache_size):
        self.mv_list = {} 
        self.name = name
        self.bscache_size=cache_size
        self.count=0
        
    def create_mv(self,mv):
        self.mv_list[mv.name]=mv
        self.update_cachesize(mv.cache_size)
        
    def update_cachesize(self,cache_size):
        self.bscache_size=self.bscache_size-cache_size
        
    def cache_ext_permission(self,req_size):
        if self.bscache_size-req_size >=0:
            return True
        else:
            return False
            
    def cs_check(self,req_content): 
#        print('usr_cs_check')
        if hash(req_content.name+req_content.chunk_num) in self.ContentStore:
#            print('content found')
            
            self.ContentStore[req_content.hash_value]
            self.hit +=1
            self.usr_receive(req_content)
        else:
            self.miss +=1
#            print('content not found')
            if self.forwarding_decision(req_content) == True:
                self.server(req_content)
                
    

        
        
        

        

      
        



#    global actual,revenue,hit,miss
#    if req_content in cachelru1:
#        actual +=radio_r
#        revenue +=slic_r 
#        hit += 1
#        hit1 = hit
#    else:
#        actual +=radio_r+backhaul_r
#        revenue +=slic_r 
#        miss += 1
#        cachelru1[req_content] = 1
        #if len(cache)<current_c_space:
            #cachelru[req_content] = 1
            #cache.append(req_content)
