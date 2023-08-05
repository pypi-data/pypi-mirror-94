#!/usr/bin/python
# coding:utf-8
# Author:   --<>
# Purpose: 
# Created: 2014/4/2
import os , tempfile , sys

sys.path.append(os.path.split(__file__)[0] + '/../Lib/')
from lpp import *
from optparse import OptionParser

if __name__ == '__main__':
    usage = "python2.7 %prog [options]"
    parser = OptionParser(usage = usage)
    
    parser.add_option("-s" , "--Sequence" , action = "store" ,
                      dest = "Sequence" ,
                      help = "Sequence")
    

    
    parser.add_option("-o" , "--Out" , action = "store" ,
                      dest = "Output" ,
    
                      help = "output")

    parser.add_option("-r" , "--Ref" , action = "store" ,
                      dest = "Ref" ,

                      help = "reference sequence")
    (options , args) = parser.parse_args()
    RAW = fasta_check(  open(options.Sequence,'rU') )
    END = open(options.Output,'w')
    for t,s in RAW:
        END.write(t+s)
