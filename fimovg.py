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

__version__='0.2'

def with_vg_pipeline(cores, linear_genome, vcf, bedfile, motif, bgfile, 
                         pseudo, pvalueT, no_reverse, dest, pipeline):

    vg_loc=vgc.create_vg(linear_genome, vcf) # create the vg
    m=mtf.get_motif_pwm(motif, bgfile, pseudo, no_reverse) # create the motif
    data=sge.get_data(vg_loc, bedfile, m.getWidth(), pipeline) # extract the region peaks
    df=ps.scoreGraphsPaths(data, m, pvalueT, cores) # scoring
    
    objs_towrite=[df] # initialize the list of objects to save
    ##TO DO: matplotlib or seaborn plots 
    ##TO DO: add plots objects to objs_toWrite() 
    ow.writeresults(objs_towrite, dest) # write results
    
def without_vg_pipeline(cores, graph_genome, bedfile, motif, bgfile,
                            pseudo, pvalueT, no_reverse, dest, pipeline):
    
    m=mtf.get_motif_pwm(motif, bgfile, pseudo, no_reverse)
    data=sge.get_data(graph_genome, bedfile, m.getWidth(), pipeline)
    df=ps.scoreGraphsPaths(data, m, pvalueT, cores)
    
    objs_towrite=[df] # initialize the list of objects to save
    ##TO DO: matplotlib or seaborn plots 
    ##TO DO: add plots objects to objs_toWrite() 
    ow.writeresults(objs_towrite, dest)
    

        
        
        
        
        
        
        
        
        
    
    

    
    
    