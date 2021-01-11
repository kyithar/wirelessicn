# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 16:54:27 2016

@author: kyithar
"""

from cache import pylru
from delay import Cable
from cache.cache_decision import CDecision

class MVNO:
    def __init__(self,env,bs_name,name,cache_size,bh_delay,cDecision,threshold):
        self.env = env
        self.cache_monitor = env.process(self.hit_monitor(env))
        self.pop_cdecision = env.process(self.pop_cdecision(env))
        self.PIT = {}
        self.usr_list = {}
        self.delay_list = {}
        self.delay = 0.0
        self.bs_name=bs_name
        self.name = name
        self.cache_size=cache_size
        self.hit  = 0
        self.miss = 0
        self.phit = 0.0
        self.max_phit = 0.0
        self.server_hit=0
        self.ContentStore = pylru.lrucache(self.cache_size)
        self.num_req=0
        self.usr_rec=0
        self.cable = Cable(env,bh_delay)
        self.req_counter={}
        self.cDecision = cDecision
        self.th = threshold
        self.monitor_phit =[]
        self.bh_cost = 0
        self.radio_cost = 0
        self.cache_space_cost = 0
        self.net_profit = 0
        self.total_req= 0
        
    def cache_is_full(self):
        if self.ContentStore.__len__()==self.cache_size:
            return True
    
#    def update_phit(self):
##        yield env.timeout(1)
#        if self.hit > 0:
#            self.phit=self.hit/(self.hit+self.miss)
#            print(self.phit)
    
    def update_cache_size(self,cache_size):
        self.cache_size +=cache_size
        self.ContentStore.size(self.cache_size)
        
    def attach_usr(self,usr):
        self.usr_list[usr.name]=usr
        
    def usr_req_generator(self,usr_name):   
        req_content=self.usr_list[usr_name].create_int(0)#create interest pkg
        if req_content.chunk_num > 5:
            print(req_content.chunk_num)
        self.num_req +=1
        self.req_arrival(req_content)#send to base station
    
    def req_arrival(self,req_content):#request arrival at the bs
        counter = 0
        self.total_req +=1;
        self.radio_cost +=1
        if req_content.hash_value in self.req_counter:
            counter = self.req_counter[req_content.hash_value]
            self.req_counter[req_content.hash_value] = counter+1
        else:
            self.req_counter[req_content.hash_value] =1
        self.cs_check(req_content)
        
        

    def cs_check(self,req_content):
        if req_content.hash_value in self.ContentStore:          
            self.ContentStore[req_content.hash_value]
            self.hit +=1
            self.usr_receive(req_content,req_content.usr_name)
        else:
            self.miss +=1
            if self.forwarding_decision(req_content) == True:
                req_content.start_t = self.env.now
                self.cable.put(req_content)
                self.env.process(self.server(self.env, self.cable)) 
    
    def pop_cdecision(self,env):
        if self.cDecision is 'vicwn':
            dec =True
        else:
            dec = False
        while dec:
            yield self.env.timeout(10)
            temp_cache_obj=CDecision.decision(self.cDecision,0,0,self.ContentStore.size(), self.req_counter)
            self.ContentStore.clear()
            for key in range(len(temp_cache_obj)):
                self.ContentStore[key] = 1  
         
            
    def hit_monitor(self,env):
       if self.cDecision is 'vicwn':
            dec =True
       else:
            dec =True
       while dec:
            
            yield self.env.timeout(600)
            revenue = self.total_req*2
            invest = self.bh_cost+self.radio_cost+self.cache_space_cost
            self.net_profit =(revenue-invest)/(revenue+invest)

            if self.cache_is_full()==True:           
                self.phit=self.hit/(self.hit+self.miss)
                self.monitor_phit.append(self.phit)
                if self.phit>self.max_phit:
                    self.max_phit=self.phit
#                    if self.bs_name=='b1':
##                    print(self.phit)
#                        print(self.max_phit-self.phit)
#                        print('-----')
                else:
                    if self.cDecision is 'vicwn':
                        if self.max_phit<0.5:
##                        if self.bs_name=='b1':
##                            print('need cache extension')
                            if self.cache_size < 100:
                                self.update_cache_size(10)
                                self.cache_space_cost = (self.cache_size/10)*1
                            
##                        print('-----')
                    

                           
    def forwarding_decision(self,Int_msg):

        if Int_msg.hash_value in self.PIT:  
#            print('int_msg hashvalue %s'%Int_msg.hash_value)
#            print(Int_msg.hash_value)
            self.PIT.setdefault(int(Int_msg.hash_value),[]).append(Int_msg.usr_name)
            return False
        else:
            self.bh_cost +=1;
#            print('int_msg hashvalue %s'%Int_msg.hash_value)
            self.PIT.setdefault(int(Int_msg.hash_value),[]).append(Int_msg.usr_name)
            return True      

    def server(self,env,cable): 
                  
            Int_msg = yield cable.get()
            self.server_hit +=1 
            cable.put(Int_msg)
            self.env.process(self.data_handler(env,cable))  

   
    def data_handler(self,env,cable): 
        req_content = yield self.cable.get()
        req_content.start_t=env.now-req_content.start_t     
        if self.cDecision != 'vicwn':
            if CDecision.decision(self.cDecision,req_content,self.req_counter[req_content.hash_value],self.th, self.req_counter) is True: 
                self.cs_store(req_content) 
#            if self.cache_is_full()==True:
#                self.env.process(self.hit_monitor())
#                self.env.run(until=100000)
        temp_usr_list=self.PIT[req_content.hash_value]
#        print('before sending to user module')
        for z in range(len(temp_usr_list)):
            self.usr_receive(req_content,temp_usr_list[z])
            if z+1 == len(temp_usr_list):
                del self.PIT[req_content.hash_value]

         
    def cs_store(self,req_content):
            self.ContentStore[req_content.hash_value] = 1     

        
    
    def usr_receive(self,int_msg,usr_name):
#        self.net_profit = (self.total_req*2)-(self.bh_cost+self.radio_cost+self.cache_space_cost)
        self.usr_rec +=1 #counter at mvno       
        self.usr_list[usr_name].tot_delay +=int_msg.start_t
#        print(self.usr_list[int_msg.usr_name].tot_delay)
        
        if self.usr_list[usr_name].chunk_count == self.usr_list[usr_name].tot_chunk:
            self.usr_list[usr_name].avg_delay=self.usr_list[usr_name].tot_delay/self.usr_list[usr_name].tot_chunk
            self.delay_list[usr_name]=self.usr_list[usr_name].avg_delay
            del self.usr_list[usr_name]
#            print('user%d received complet pkg of content '%usr_name)
        else:
            self.usr_list[usr_name].chunk_count +=1
#            print('request next chunk %d' %self.usr_list[usr_name].chunk_count)
#              print('------')
            self.usr_req_generator(usr_name)
        
       

 

