#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 12:07:48 2019

@author: manuel
"""

import motif as mtf
import sys

if __name__=='__main__':
    
    try:
        motif_file=sys.argv[1]
        bg=sys.argv[2]
        pseudo=float(sys.argv[3])
    
        m=mtf.build_motif_pwm_jaspar(motif_file, bg, pseudo)
    
        m.setHas_reverse(True)
        m=mtf.get_pwm_reverse(m)
   
    
        sm=mtf.scale_pwm(m.getMotif_matrix())
        m.setMotif_matrix_scaled(sm)
        

        
        smr=mtf.scale_pwm(m.getMotif_matrix_reverse())
        m.setMotif_matrix_scaled_reverse(smr)
        
        m=mtf.comp_pval_mat(m)
        
        print(m.getMotif_matrix())
        print(m.getMotif_matrix_reverse())
        print(m.getMotif_matrix_scaled())
        print(m.getMotif_matrix_scaled_reverse())
        print(m.getMotif_pval_mat(), len(m.getMotif_pval_mat()), sum(m.getMotif_pval_mat()))
        
    except:
        
        sys.stderr.write('motif.py: test not passed\n')
        
    else:
        
        sys.stderr.write('motif.py: test passed\n')
    
    
    