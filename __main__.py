"""

GRAFIMO version {version}

Copyright (C) 2019 Manuel Tognon <manu.tognon@gmail.com> <manuel.tognon@studenti.univr.it>

GRAFIMO scores sequences likely to be transcription binding sites in ChIP-seq peaks

Usage:
    grafimo --cores [NCORES] --linear_genome [LINEAR_GENOME.fa] --vcf [VCF.vcf.gz] --bedfile [BEDFILE.bed] --motif [MOTIF.jaspar] [options]
    
    grafimo --cores [NCORES] --graph_genome [GRAPH_GENOME.xg] --bedfile [BEDFILE.bed] --motif [MOTIF.jaspar] [options]
    
The tool takes in input both a linear genome (in .fa format) and a vcf file 
(must be compressed, e.g. vcffile.vcf.gz) or a graph_genome (better if in .xg).
The results will be written to a .csv file in the directory specified by the user
(--o option or defalut value 'grafimo_out').

The tool is also error tollearnt in the subgrapahs extraction, since it doesn't 
stop its execution although we have some exceptions.

Citation:
    
    xxxx. Xxxx, xxxx
    
    
Run 'grafimo --help'to see all command-line options.
See https://xxxx for the full documentation.

Visit http://xxxx to run the web-based version.

"""

from argparse import ArgumentParser, SUPPRESS, HelpFormatter
from grafimo import __version__, with_vg_pipeline, without_vg_pipeline
import handle_exception as he
import time
import sys
import glob
import multiprocessing as mp
import subprocess
import vgCreation as vgc


class GRAFIMOArgumentParser(ArgumentParser):
    """
    
        This redefinition of the arguments parser:
            - The usage message is not prefixed by 'usage'
            - A brief message is printed instead of the full usage message
    
    """
    
    class GRAFIMOHelpFormatter(HelpFormatter):
        
        def add_usage(self, usage, actions, groups, prefix='None'):
            
            if usage is not SUPPRESS:
                args=usage, actions, groups, ''
                self._add_item(self._format_usage, args)
                
    def __init__(self, *args, **kwargs):
        kwargs['formatter_class']=self.GRAFIMOHelpFormatter
        kwargs['usage']=kwargs['usage'].replace("{version}", __version__)
        super().__init__(*args, **kwargs)
        
    def error(self, msg):
        sys.stderr.write("Run 'grafimo --help' to see the usage\n")
        self.exit(2, "\n{0}: ERROR: {1}\n".format(self.prog, msg))
        
class CmdError(Exception):
    pass

def get_AP():
    """
        Return the parser containing the input arguments
        ----
        Parameters:
            None
        ----
        Returns:
            parser(GRAFIMOArgumentParser)
    
    """
    
    parser=GRAFIMOArgumentParser(usage=__doc__, add_help=False)
   
    group=parser.add_argument_group("Options")
    group.add_argument("-h", "--help", action="help", help="Show the help message and exit")
    group.add_argument("--version", action="version", help="Show the version and exit", version=__version__)
    group.add_argument("--cores", type=int, default=0, metavar='NCORES', nargs='?', const=0, 
                           help="Number of cores to use. The defalut value is 0 (auto-detection)")
    
    # the three following arguments depend on the user approach
    group.add_argument("--linear_genome", type=str, help='path to the linear genome (fasta format required)',
                           nargs='?', default='', metavar='LINEAR-GENOME.fa')
    group.add_argument("--vcf", type=str, help='path to your .vcf file', nargs='?', default='', metavar='VCF.vcf')
    group.add_argument("--graph_genome", type=str, nargs= '?', metavar='PATH-TO-GRAPH-GENOME.xg',
                           help='path to the VG graph genome file (vg or xg format required)',
                           default='')
    
    group.add_argument("--bedfile", type=str, help='path to the BED file that defines the regions to score',
                           metavar='BEDFILE.bed')
    group.add_argument("--motif", type=str, metavar='MOTIF.jaspar',
                           help='path to the motif file to use for the scoring of the sequences (JASPAR format required)')
    
    # optional arguments
    group.add_argument("--bgfile", type=str, help='path to a file which defines the background distribution [optional]', nargs='?',
                          const='', default='', metavar='BGFILE')
    group.add_argument("--pseudo", type=float, help='pseudocount to add to the motif counts [optional]', nargs='?', const='0.1',
                       default='0.1', metavar='PSEUDOCOUNT')
    group.add_argument("--pvalueT", type=float, nargs='?', const='1e-3', metavar='PVALUE-THRESHOLD',
                           help='defines a threshold on the p-value obtained form the scoring of each sequence (1e-3 by default) [optional]',
                           default=1e-3)
    group.add_argument("--no_reverse", type=bool, nargs='?', const=False, default=False, metavar='TRUE | FALSE',
                           help='flag parameter to express if the user want to score only data from the forward or also from the reverse strand')
    group.add_argument("--o", type=str, help='name of the directory where the results will be stored [optional]',
                           nargs='?', const='grafimo_out', default='grafimo_out', metavar='OUTDIR')
    
    return parser

def main(cmdLineargs=None):
    """
    
        Main function of the tool
        ----
        Parameters:
            cmdLineArgs (str) : the arguments given in command line
            
        ----
        Returns:
            None
    
    """
    
    start=time.time()
    
    WITH_VG_CREATION=False
    
    parser=get_AP()
    if cmdLineargs is None:
        cmdLineargs=sys.argv[1:] # take input args
        
    args=parser.parse_args(args=cmdLineargs)
    
    if not args.linear_genome and not args.graph_genome:
        parser.error("Needed at least one between '--linear_genome --vcf [other args]' and '--graph_genome [other args]'")
        
    if args.linear_genome and args.graph_genome:
        parser.error("Only one between --linear_genome --vcf [other args]' and '--graph_genome [other args]' is allowed")
        
    if args.graph_genome and args.vcf:
        parser.error("Only one between --linear_genome --vcf [other args]' and '--graph_genome [other args]' is allowed")
    
    if args.cores<0:
        parser.error('The number of cores cannot be negative')
        
    if args.cores==0:
        cores=mp.cpu_count()
        
    else:
        cores=args.cores
        
    if args.linear_genome:
        if args.linear_genome.split('.')[-1]!='fa' and \
            args.linear_genome.split('.')[-1]!='fasta':
            parser.error('The linear genome must be in fasta format (.fasta and .fa allowed)')
            
        else:
            linear_genome=args.linear_genome
            
    if args.vcf:
        if args.vcf.split('.')[-1]!='gz' or \
            args.vcf.split('.')[-2]!='vcf': # allow also the compressed vcf files
                                            # like something.vcf.gz
            parser.error('Incorrect vcf file given')
        else:
            vcf=args.vcf
            WITH_VG_CREATION=True
            
            
    if args.graph_genome:
        graph_genome=args.graph_genome
        WITH_VG_CREATION=False
        
    if args.bedfile.split('.')[-1]!='bed':
        parser.error('Incorrect bedfile given')
    
    else:
        bedfile=args.bedfile
        
    if args.motif.split('.')[-1]!='jaspar':
        parser.error('Incorrect motif file given, JASPAR format allowed (visit http://jaspar.genereg.net)')
        
    else:
        motif=args.motif
        
    if args.bgfile:
        bgfile=args.bgfile
    else:
        bgfile=args.bgfile
        
    if args.pseudo <= 0:
        parser.error('The pseudocount cannot be less than or equal 0')
    
    else:
        pseudocount=args.pseudo
        
    if args.pvalueT < 0 or args.pvalueT > 1:
        parser.error('The pvalue threshold must be between 0 and 1')
    
    else:
        pvalueT=args.pvalueT
        
    if not isinstance(args.no_reverse, bool):
        parser.error('The no_reverse parameter accepts only as values True or False')
        
    else:
        no_reverse=args.no_reverse
        
    if args.o:
        dest=args.o
        
    if WITH_VG_CREATION:
            
        dest+='/'
        
        with_vg_pipeline(cores, linear_genome, vcf, bedfile, motif, bgfile,
                             pseudocount, pvalueT, no_reverse, dest, WITH_VG_CREATION)
        
        
    elif not WITH_VG_CREATION:
        
        if graph_genome.split('.')[-1]!='xg' and \
            graph_genome.split('.')[-1]!='vg':
                code=he.throw_no_xg_and_vg_err()
                sys.exit(code)
        
        elif graph_genome.split('.')[-1]=='vg': # we are given a vg genome
            vg=graph_genome
            xg=vgc.indexVG(vg)
            
        else: # we are given an xg genome
            xg=graph_genome
        
        without_vg_pipeline(cores, xg, bedfile, motif, bgfile,
                                pseudocount, pvalueT, no_reverse, dest, WITH_VG_CREATION)
        
    
    else:
        code=he.throw_wrong_input_err()
        sys.exit(code)
        
    end=time.time()
    
    print('elapsed time', end-start)
    
    
### run main  point ###

if __name__=='__main__':
    main()
    
    
    


