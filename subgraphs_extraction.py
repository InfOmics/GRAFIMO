"""

@author: Manuel Tognon

@email: manu.tognon@gmail.com
@email: manuel.tognon@studenti.univr.it

Script that performs the extraction of the subgraphs from the graph genome and 
takes the sequences to score from them

"""

import subprocess
import warnings
import handle_exception as he
import sys
import os

def get_data(genome_loc, bedfile, TFBS_len, vg_creation_pipeline):
    """
        returns the data necessary for the following steps of the analysis 
        pipeline
        ----
        Parameters:
            genome_loc (str) : path to the genome 
            bedfile (str) : path to the bedfile
            TFBS_len (int) : width of the motif 
            vg_creation_pipeline (bool) : defines which pipeline to follow
        ----
        Returns:
            fileloc (str) : path to the data obtained
    """
    
    cwd=os.getcwd()
    os.chdir(genome_loc)
    
    for i in range(20):
        print('#', end='')
    print() #newline
    print("Extracting subgraphs from regions defined in ", bedfile)
    print()
    for i in range(20):
        print('#', end='')
    print()
    
    if vg_creation_pipeline:
        vgc_sge(bedfile, TFBS_len)
        
    elif not vg_creation_pipeline:
        no_vgc_sge(genome_loc, bedfile, TFBS_len)
        
    else:
        pass ## TO DO: handle these situations
    
        
    fileloc=os.getcwd() # the tsv files are store in the cwd 
    
    os.chdir(cwd) # get back to the original directory
        
    return fileloc

def vgc_sge(bedfile, TFBS_len):
    """
        Extract the subgraphs from the genome graph and the sequences to score
        from them (step to follow in the pipeline with the vg creation)
        ----
        Parameters:
            bedfile (str) : path to the bedfile
            TFBS_len (int) : motif width
        ----
        Returns:
            None
    """
    
    bedfile='../'+bedfile
    
    peak_no=1
    
    try:
        bedf=open(bedfile, mode='r') # open the bedfile in read only mode
        
        CHR_LIST=list(range(1,23))+['X', 'Y']
        CHR_LIST=['chr'+str(c) for c in CHR_LIST]
        
        for line in bedf:
            print('Peak ', peak_no)
            chrom, start, end = line.split('\t')[0:3]
            print('Extracting region:', chrom, '['+start+'-'+end+']')
            #chromid=chrom.replace('chr', '')
            
            if chrom in CHR_LIST: # chromosome name is valid
                region_index=chrom+':'+start+'-'+end
            
                path_id=chrom+'_'+start+'-'+end
                subgraph_path=correct_path('./', path_id, '.vg')
            
                vg=chrom+'.xg' # for extraction xg is required
                
                code=extract_region(vg, region_index, subgraph_path)
            
                if code != 0:
                    warn="Region "+chrom+':'+'['+start+'-'+end+']'+" extraction failed!\n"
                    warnings.warn(warn, Warning)  # although we have an exception we don't stop the execution
                    
                else:
                    # write on the stderr
                    msg="Region"+chrom+'['+start+'-'+end+']'+"extracted\n"
                    sys.stderr.write(msg) 
                
                kmer_path=correct_path('./', path_id, '.tsv')
                
                # vg kmer works with vg not xg graphs
                code=retrieve_kmers(TFBS_len, subgraph_path, kmer_path)
            
                if code != 0:
                    warn="Kmers extraction from region "+chrom+':'+'['+start+'-'+end+']'+" failed!\n"
                    warnings.warn(warn, Warning) # although we have an exception we don't stop the execution
                    
                else:
                    # write on the stderr
                    msg="Kmers extraction for region"+chrom+'['+start+'-'+end+']'+"finished\n"
                    sys.stderr.write(msg)
                
                cmd='rm {0}'.format(subgraph_path)
                code=subprocess.call(cmd, shell=True)
            
                if code != 0:
                    cderr=he.throw_subprocess_error()
                    sys.exit(cderr)
                    
            else:
                warnings.warn('chromosome name not valid. Line skipped\n', Warning)
                # although we have an exception we don't stop the execution
                          
            peak_no += 1
            
    except:
        code=he.throw_bedfile_reading_error() # something went wrong while reading the bedfile
        sys.exit(code)
        
    else:
        bedf.close() # close the bedfile
        

def no_vgc_sge(xg, bedfile, TFBS_len):
    """
        Extract the subgraphs from the genome graph and the sequences to score
        from them (step to follow in the pipeline without the vg creation)
        ----
        Parameters:
            bedfile (str) : path to the bedfile
            TFBS_len (int) : motif width
        ----
        Returns:
            None
    """
    
    peak_no=1
    
    try:
        bedf=open(bedfile, mode='r') # open the bedfile in read only mode
        
        CHR_LIST=list(range(1,23))+['X', 'Y']
        CHR_LIST=['chr'+str(c) for c in CHR_LIST]
        
        for line in bedf:
            print('Peak ', peak_no)
            chrom, start, end = line.split('\t')[0:3]
            print('Extracting region:', chrom, '['+start+'-'+end+']')
            #chromid=chrom.replace('chr', '')
            
            if chrom in CHR_LIST: # chromosome name is valid
                region_index=chrom+':'+start+'-'+end
            
                path_id=chrom+'_'+start+'-'+end
                subgraph_path=correct_path('./', path_id, '.vg')
                
                code=extract_region(xg, region_index, subgraph_path)
            
                if code != 0:
                    warn="Region "+chrom+':'+'['+start+'-'+end+']'+" extraction failed!\n"
                    warnings.warn(warn, Warning)  # although we have an exception we don't stop the execution
                    
                else:
                    # write on the stderr
                    msg="Region"+chrom+'['+start+'-'+end+']'+"extracted\n"
                    sys.stderr.write(msg) 
                
                kmer_path=correct_path('./', path_id, '.tsv')
                
                # vg kmer works with vg not xg graphs
                code=retrieve_kmers(TFBS_len, subgraph_path, kmer_path)
            
                if code != 0:
                    warn="Kmers extraction from region "+chrom+':'+'['+start+'-'+end+']'+" failed!\n"
                    warnings.warn(warn, Warning) # although we have an exception we don't stop the execution
                    
                else:
                    # write on the stderr
                    msg="Kmers extraction for region"+chrom+'['+start+'-'+end+']'+"finished\n"
                    sys.stderr.write(msg)
                
                cmd='rm {0}'.format(subgraph_path)
                code=subprocess.call(cmd, shell=True)
            
                if code != 0:
                    cderr=he.throw_subprocess_error()
                    sys.exit(cderr)
                    
            else:
                warnings.warn('chromosome name not valid. Line skipped\n', Warning)
                # although we have an exception we don't stop the execution
                          
            peak_no += 1
            
    except:
        code=he.throw_bedfile_reading_error() # something went wrong while reading the bedfile
        sys.exit(code)
        
    finally:
        bedf.close() # close the bedfile
        
    
def correct_path(path, path_id='', file_format=''):
    
    if path[-1:]=='/':
        new_path=path+path_id+file_format
    else:
        new_path=path+'/'+path_id+file_format
        
    return new_path

def retrieve_kmers(TFBS_len, subgraphs_path, kmers_path):
    """
        Obtain the sequences from the subgraphs
        ----
        Prameters:
            TFBS_len (int) : motif width
            subgraphs_path (str) : path to the subgraphs
            kmers_path (str) : path to which the sequences will be stored
        ----
        Returns:
            code (int) : success or not of subprocess.call()
    """    
    vg_km_cmd='vg kmers -k {0} -p {1} > {2}'.format(str(TFBS_len), subgraphs_path, kmers_path)
    code=subprocess.call(vg_km_cmd, shell=True)
    
    return code

def extract_region(genome, region_index, subgraphs_path):
    """
        Extract the subgraphs
        ----
        Parameters:
            genome (str) : path to the genome
            region_index (str) : region to extract
            subgraphs_path (str) : path to which the subgraphs will be stored
        ----
        Returns:
            code (int) : success or not of subprocess.call()
    """
    
    vg_sg_cmd='vg find -x {0} -p {1} > {2}'.format(genome, region_index, subgraphs_path)
    code=subprocess.call(vg_sg_cmd, shell=True)
    
    return code

def isGraph_genome_xg(graph_genome):
    """
        Check if the given genome graph is in xg format
        ----
        Parameters:
            graph_genome (str) : path to the genome graph
        ----
        Returns:
            (bool)
    """
    
    if not isinstance(graph_genome, str):
        code=he.throw_not_str_error()
        sys.exit(code)
        
    else:
        if graph_genome.split()[-1] == 'xg':
            return True
        else:
            return False
    
