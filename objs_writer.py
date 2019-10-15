"""

@author: Manuel Tognon

@email: manu.tognon@gmail.com
@email: manuel.tognon@studenti.univr.it

Scripts that writes the results to a user defined (or the default defined) 
directory.

"""

import sys
import os
import subprocess
import pandas as pd
import handle_exception as he

def writeresults(objs, dest):
    
    if not isinstance(objs, list):
        code=he.throw_not_list_err()
        sys.exit(code)
        
    if len(objs) <= 0:
        code=he.throw_objs_list_length()
        sys.exit(code)
        
    cwd=os.getcwd()
    
    if not os.path.isdir(dest): # tthe directory not exist
    
        cmd='mkdir {0}'.format(dest) # create the out directory
        code=subprocess.call(cmd, shell=True)
    
        if code!=0:
            cderr=he.throw_subprocess_error()
            sys.exit(cderr)
            
    else:
        os.chdir(dest) # for some reason it exists
        code=subprocess.call('rm *') # clear the directory
        
        if code != 0:
            cderr=he.throw_subprocess_error()
            sys.exit(cderr)
    
    # write objects in dest
    
    for obj in objs:
        
        if isinstance(obj, pd.DataFrame):
            df=obj
            df.to_csv('grafimo_out.csv', sep=',', encoding='utf-8')
            #print(df.to_html())
            
            
        
        ### if matplotlib istance ###
        ## write plots in dest ##
        
    
    os.chdir(cwd)
    
    
        
    
        

