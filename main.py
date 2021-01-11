# -*- coding: utf-8 -*-
"""
Created on Tue May 31 20:11:44 2016

@author: kyithar
"""
import matplotlib.pyplot as plt
import itertools
import random
import simpy
import zipf
#import numpy as np
from base_station import Base_station
from mvno import MVNO
from user import User
from stats import Stats



catalog_size=10000#number of content
tot_chunk_num =5 #chunk number of each content
alpha=[0.5,0.6,0.7,0.8,0.9,1]
numSamples=100000
RANDOM_SEED = 42
T_INTER = [5, 10]        # Create a usr every [min, max] seconds
SIM_TIME = 100000      # Simulation time in seconds
#=====Variables related with Base Station ===============#
bs_list ={}
num_bs=3
bs_cache_size=100
back_haul_delay = 1
nCar = 600
bs_power = 40 #watt
transmit_power = 18.22 #dBm
bs_height = 30 #metre
bandwidth = 15e3 #kHz
bs_gain = 12 #dBi
bs_radius = 1e3 #metre
backhaul = 100 #Mbps
#=====Variables related with MVNO ===============#
mvno_cache_size =10
cache_increment=30
#=====Variables related with MVNO cache decision ===============#
cDecision =['vicwn','cache_all'] #'pre_filter_th','cache_all','vicwn'
threshold = 10
#=====Variables related with statistics =================#
stats = {}
stats_test = {}
tot_hit = {}
tot_miss = {}
tot_req ={}
total_received ={}
tot_delay={}
tot_server_hit = {}
monitor_phit_tes = {}
p_hit_th = []
phit_all = []
i_hit_th = []
i_hit_all = []
delay_hit_th = []
delay_hit_all = []
usr_test_list = {}
content_list_test = {}
tot_profit = {}
tot_bh = {}
profit_th = []
profit_all =[]
bh_th =[]
bh_all =[]

def gen_content(alpha_temp):
    content_list_test[0] = zipf.randZipf(catalog_size, alpha_temp, numSamples)

  
def setup_bs_mv(cDecision_temp):

 #=======Create Base Station =================#     
    bs1=Base_station('b1',bs_cache_size)   
    bs2=Base_station('b2',bs_cache_size)
    bs3=Base_station('b3',bs_cache_size)
    
 #============Create MVNO ==================#  
    mv1=MVNO(env,'b1','mvno1',mvno_cache_size,back_haul_delay,cDecision_temp,threshold)
    bs1.create_mv(mv1)
    bs_list[0]=bs1
    
    mv1=MVNO(env,'b2','mvno1',mvno_cache_size,back_haul_delay,cDecision_temp,threshold) 
    bs2.create_mv(mv1)  
    bs_list[1]=bs2
    
    mv1=MVNO(env,'b3','mvno1',mvno_cache_size,back_haul_delay,cDecision_temp,threshold) 
#    yield env.timeout(print('test'))
    bs3.create_mv(mv1)   
    bs_list[2]=bs3



def usr_allocation():
    cl=content_list_test[0]
    for i in range(numSamples):
        bs_num=random.randint(0,num_bs-1)
        req_content=cl[i % numSamples]
        usr=User(i,req_content,tot_chunk_num,bs_num,'mvno1')
        usr_test_list[i] = usr
        
def run_test():   
    env.process(usr(env,bs_list))
#    env.process(cache_ext_des(env))
 
#def cache_ext_des(env): 
#    while True:
#        yield env.timeout(10)
#        for n in range(len(bs_list)):
#            mv=bs_list[n].mv_list['mvno1']
#            mv.update_phit(env)
#            if mv.cache_is_full()==True:
#                if mv.phit < 0.5: 
#                    #print(probhit)             
#                    req_cache_capacity = bs_list[n].bscache_size-cache_increment  
#                    if req_cache_capacity >= 0:
##                    print('extend')
#                        bs_list[n].update_cachesize(cache_increment)
#                        mv.update_cache_size(cache_increment)
 
 #========Create Users 
def usr(env,bs):    
    for v in itertools.count():
        yield env.timeout(random.randint(*T_INTER))
        usr=usr_test_list[v]
        bs=bs_list[usr.bs]
        bs.count +=1
        mv=bs.mv_list[usr.mv]
        mv.attach_usr(usr) 
        usr_name=usr.name
        mv.usr_req_generator(usr_name)
        

        tot_hit[mv.name,mv.bs_name]=mv.hit
        tot_miss[mv.name,mv.bs_name]=mv.miss 
        tot_server_hit[mv.name,mv.bs_name]=mv.server_hit
        tot_req[mv.name,mv.bs_name]=mv.num_req
        total_received[mv.name,mv.bs_name]=mv.usr_rec
        tot_delay[mv.bs_name] = mv.delay_list
        tot_profit[mv.name,mv.bs_name]=mv.net_profit
        tot_bh[mv.name,mv.bs_name]=mv.bh_cost
        monitor_phit_tes [0] = mv.monitor_phit
        
        


def statistics(alpha_temp,cDecision_temp):
    
    total_hit=sum(tot_hit.values())   
    total_miss=sum(tot_miss.values())
    total_server_hit=sum(tot_server_hit.values())
    total_profit = sum(tot_profit.values())
    total_bh = sum(tot_bh.values())
    t_receive=sum(total_received.values())
    total_request=sum(tot_req.values())
    prob_hit=total_hit/(total_hit+total_miss)
    inner_hit=(t_receive-total_server_hit)/t_receive
    b1_delay=tot_delay['b1']
    b2_delay=tot_delay['b2']
    b3_delay=tot_delay['b3']
    b1_avg_delay=sum(b1_delay.values())/len(b1_delay)
    b2_avg_delay=sum(b2_delay.values())/len(b2_delay)
    b3_avg_delay=sum(b3_delay.values())/len(b3_delay)
    total_avg_delay=(b1_avg_delay+b2_avg_delay+b3_avg_delay)/num_bs
    
    stats.setdefault(float(alpha_temp),[]).append(Stats(cDecision_temp,prob_hit,inner_hit,total_avg_delay,total_profit,total_bh,total_request))

    
    print('Prob of cache hit %s'%prob_hit)
    print('Inner cache hit %s'%inner_hit)
    print('Avg delay %s'%total_avg_delay)
    print('Total received packets %d'%t_receive)
    print('Total server hit %d'%total_server_hit)
    print('Total cache miss %d'%total_miss)
    print('Total req %d'%total_request)
    print('Total bh %s'%(total_bh/total_request))
    print('Net profit %s'%(total_profit))
    print('--------------------------')



# Setup and start the simulation
for x in range(len(alpha)):
    gen_content(alpha[x])
    usr_allocation()
    for y in range (len(cDecision)): 
        print('Setup and start the simulation with zipf value %s' %alpha[x])
        print('Cache Decision algorithm is %s' %cDecision[y])
            
        random.seed(RANDOM_SEED)
        # Create environment and start processes
        env = simpy.Environment()
        setup_bs_mv(cDecision[y])
        run_test()
        # Execute!
        env.run(until=SIM_TIME)
#=================Updating Statistics=====================================#
        statistics(alpha[x],cDecision[y])
    
    if x+1 == len(alpha):
        for k in range(len(alpha)):
            stat_test_temp=stats[alpha[k]]

            for i in range(len(cDecision)):
                if i == 0:
                    p_hit_th.append(stat_test_temp[i].p_hit)
                    i_hit_th.append(stat_test_temp[i].i_hit)
                    delay_hit_th.append(stat_test_temp[i].avg_delay)
                    profit_th.append(stat_test_temp[i].profit)
                    bh_th.append(stat_test_temp[i].bh/stat_test_temp[i].req)
                else:
                    phit_all.append(stat_test_temp[i].p_hit) 
                    i_hit_all.append(stat_test_temp[i].i_hit)
                    delay_hit_all.append(stat_test_temp[i].avg_delay)
                    profit_all.append(stat_test_temp[i].profit)
                    bh_all.append(stat_test_temp[i].bh/stat_test_temp[i].req)
                    
#combine stat collection and plot generating                     

#=================Generating_Plot=====================================#
        plt.xticks(range(len(alpha)), alpha)
        plt.grid(True)
        line_up,=plt.plot(p_hit_th,'ro-',label=cDecision[0])
        line_down,=plt.plot(phit_all,'g^-',label=cDecision[1])
        plt.legend(handles=[line_up, line_down])
        plt.ylabel('P-Hit')
        plt.xlabel('zipf(alpha)')
        plt.show()
        
        plt.xticks(range(len(alpha)), alpha)
        plt.grid(True)
        line_up,=plt.plot(i_hit_th,'ro-',label=cDecision[0])
        line_down,=plt.plot(i_hit_all,'g^-',label=cDecision[1])
        plt.legend(handles=[line_up, line_down])
        plt.ylabel('i-Hit')
        plt.xlabel('zipf(alpha)')
        plt.show()
        
        plt.xticks(range(len(alpha)), alpha)
        plt.grid(True)
        line_up,=plt.plot(delay_hit_th,'ro-',label=cDecision[0])
        line_down,=plt.plot(delay_hit_all,'g^-',label=cDecision[1])
        plt.legend(handles=[line_up, line_down])
        plt.ylabel('avg_delay')
        plt.xlabel('zipf(alpha)')
        plt.show()
        
        plt.xticks(range(len(alpha)), alpha)
        plt.grid(True)
        line_up,=plt.plot(profit_th,'ro-',label=cDecision[0])
        line_down,=plt.plot(profit_all,'g^-',label=cDecision[1])
        plt.legend(handles=[line_up, line_down])
        plt.ylabel('net profit')
        plt.xlabel('zipf(alpha)')
        plt.show()
        
        plt.xticks(range(len(alpha)), alpha)
        plt.grid(True)
        line_up,=plt.plot(bh_th,'ro-',label=cDecision[0])
        line_down,=plt.plot(bh_all,'g^-',label=cDecision[1])
        plt.legend(handles=[line_up, line_down])
        plt.ylabel('backhaul_usage (2 units pre chunk)')
        plt.xlabel('zipf(alpha)')
        plt.show()

        
        
    


