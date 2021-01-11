# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 14:31:21 2016

@author: kyithar
"""
import operator

class CDecision:
    def decision(cDecision,content,req_counter,th,req_obj):
        if cDecision is 'no_cache':
            return CDecision.no_cache(content)
            
        if cDecision is 'cache_all':
            return CDecision.cache_all(content)
            
        if cDecision is 'pre_filter_th':
            return CDecision.pre_filter_th(content,req_counter,th)
            
        if cDecision is 'vicwn':
            return CDecision.vicwn(content, req_obj,th)
        
    def no_cache(content):
        return False
        
    def cache_all(content):
        return True
    
    def pre_filter_th(content,req_counter,th):
        if req_counter >th:
            return True
        else:
            return False
            
    def vicwn(content,req_obj,th):
        cache_objc = []
        temp_req_obj = sorted(req_obj.items(), key=operator.itemgetter(1),reverse=True) 
        if len(temp_req_obj) < th:
            for k in range(len(temp_req_obj)):
                cache_objc.append(temp_req_obj[k][0])
                
            return cache_objc
        else:
            for k in range(th):
                cache_objc.append(temp_req_obj[k][0])
               
            return cache_objc
        
        