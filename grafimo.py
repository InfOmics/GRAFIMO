"""

@author: Manuel Tognon

@email: manu.tognon@gmail.com
@email: manuel.tognon@studenti.univr.it


Script where are defined the software version working and the two different
pipelines available:
    
    - with vg creation
    - only scoring (indexing of the vg if required [vg => xg])

"""

import subgraphs_extraction as sge
import motif as mtf
import paths_scoring as ps
import vgCreation as vgc
import objs_writer as ow

__version__='0.5'

def with_vg_pipeline(cores, linear_genome, vcf, bedfile, motif, bgfile, 
                         pseudo, pvalueT, no_reverse, dest, pipeline):

    printWelcomeMsg("WITH_VG_CREATION")

    vg_loc=vgc.create_vg(linear_genome, vcf) # create the vg
    m=mtf.get_motif_pwm(motif, bgfile, pseudo) # create the motif
    data=sge.get_data(vg_loc, bedfile, m.getWidth(), pipeline) # extract the region peaks
    df=ps.scoreGraphsPaths(data, m, pvalueT, cores, no_reverse) # scoring
    
    objs_towrite=[df] # initialize the list of objects to save
    ##TO DO: matplotlib or seaborn plots 
    ##TO DO: add plots objects to objs_toWrite() 
    ow.writeresults(objs_towrite, dest) # write results
    
def without_vg_pipeline(cores, graph_genome, bedfile, motif, bgfile,
                            pseudo, pvalueT, no_reverse, dest, pipeline, gplus=False):
    
    printWelcomeMsg("WITHOUT_VG_CREATION")
    
    m=mtf.get_motif_pwm(motif, bgfile, pseudo)
    data=sge.get_data(graph_genome, bedfile, m.getWidth(), pipeline, gplus)
    df=ps.scoreGraphsPaths(data, m, pvalueT, cores, no_reverse)
    
    objs_towrite=[df] # initialize the list of objects to save
    ##TO DO: matplotlib or seaborn plots 
    ##TO DO: add plots objects to objs_toWrite() 
    ow.writeresults(objs_towrite, dest)
    
def printWelcomeMsg(pipeline):
    
    for _ in range(35):
        print('*', end='')
    print()
    print("\tWELCOME TO GRAFIMO v", __version__, sep='')
    print()
    print("Beginning the "+ pipeline+" pipeline")
    print()
    
    for _ in range(35):
        print('*', end='')
    print('\n')
    
    
    

        
        
        
        
        
        
        
        
        
    
    

    
    
    