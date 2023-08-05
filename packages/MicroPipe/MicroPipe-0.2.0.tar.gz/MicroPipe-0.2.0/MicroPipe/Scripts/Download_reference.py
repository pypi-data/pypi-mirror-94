#!/usr/bin/env python
#coding:utf-8

import os,sys

sys.path.append(os.path.split(__file__)[0]+'/../Lib/')
from Dependcy import *
from urllib2 import urlopen
from optparse import OptionParser
import ssl
usage = "python2.7 %prog [options]"
parser = OptionParser(usage =usage )
parser.add_option("-i", "--ID", action="store",
                  dest="ID",

                  help="GBK_ID")
parser.add_option("-o", "--Output", action="store",
                  dest="output",

                  help="OutputPath")
if __name__ == '__main__':
	(options, args) = parser.parse_args()
	ID = options.ID
	OUTPUT = options.output
	Get_Path(OUTPUT)
	base_url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nucleotide"
	fasta_url = base_url+"&id=%s&rettype=fasta&retmode=text"%(ID)
	gbk_url = base_url+ "&id=%s&rettype=gbwithparts&retmode=text"%(ID)
	ssl._create_default_https_context = ssl._create_unverified_context
	print(fasta_url  )
	print( OUTPUT+'/'+ID+'.fasta' )
	if not os.path.exists(OUTPUT+'/'+ID+'.fasta'):
		os.system( """wget "%s" -O %s"""%(fasta_url,OUTPUT+'/'+ID+'.fasta' )  )
		#fasta_record = urlopen(fasta_url).read()
		#FASTA = open(OUTPUT+'/'+ID+'.fasta','w')
		#FASTA.write(fasta_record)
		#FASTA.close()
		
	if not os.path.exists(OUTPUT+'/'+ID+'.gbk'):
		os.system( """wget "%s" -O %s"""%(gbk_url,OUTPUT+'/'+ID+'.gbk' )  )
		#GBK = open(OUTPUT+'/'+ID+'.gbk','w')
		#gbk_record = urlopen(gbk_url).read()
		#GBK.write(gbk_record)
	
		#GBK.close()
