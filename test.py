#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 23:50:12 2019

@author: manuel
"""


import time
import glob
import pandas as pd
from multiprocessing import Process
import multiprocessing as mp
import numpy as np
import os
from collections import ChainMap



def get_dict(files, proc_no, res_dict):
    
    my_dict={}
    
    for file in files:
        name=file.split('.')[0]
        df=pd.read_csv(file, sep='\t', header=None)
        my_dict.update({name:df.loc[:,0].to_list()})
        
    res_dict[proc_no]=my_dict
        
    #q.put(my_dict)
    
if __name__=='__main__':
    
    N_CORES=4
    start=time.time()
    os.chdir("/Users/manuel/Desktop/LM-MedicalBioinformatics/Thesis/2019-08-16/data/peaks/")

    #dict_lst=[dict()]*N_CORES
        
    manager=mp.Manager()
    res_dict=manager.dict()

    files=glob.glob('*.tsv')
    files_splt=np.array_split(files, N_CORES)
    jobs=[]
    #pipe_lst=[]

    for i in range(N_CORES):
        #recv_end, send_end=mp.Pipe(False)
        #q=mp.Queue()
        p=Process(target=get_dict, args=(files_splt[i], i, res_dict))
        jobs.append(p)
        #pipe_lst.append(recv_end)
        p.start()
    
    
    for job in jobs:
        #dict_lst.append(q.get())
        job.join()

    
    #res=dict(ChainMap())
    
    
    end=time.time()

    print(res_dict)

    print('\n\n', end-start)




