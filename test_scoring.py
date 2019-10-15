#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 15:48:33 2019

@author: manuel
"""

import sys
import motif as mtf
import paths_scoring as ps
import objs_writer as ow
import os
import time


if __name__=='__main__':
    
    sgs=sys.argv[1]
    motif=sys.argv[2]
    pval=sys.argv[3]
    bgs=sys.argv[4]
    dest=sys.argv[5]
    
    try:
        start=time.time()
        cwd=os.getcwd()
        m=mtf.get_motif_pwm(motif, bgs, 0.1, False)
        df=ps.scoreGraphsPaths(sgs, m, 1e-3, 0)
        #os.chdir(cwd)
        print(df)
        objtw=[df]
        ow.writeresults(objtw, dest)
        end=time.time()
        
    except:
        sys.stderr.write('test not passed\n')
        
    else:
        print(end-start)
        sys.stderr.write('test passed\n')
        
        
        