#!/usr/bin/python
from mongodb import mongodb
import sys
import filters
db=sys.argv[1]
mdb=mongodb.mongodb('localhost',27017,db)

i=0

with open(db+'_domaine.txt','w') as fw:
	fw.write('**** *domaine\n')
	for domaine in mdb.selectall('metadatas'):
		fw.write(domaine['domaine'])		
		fw.write('\n')		
with open(db+'_metadatas.txt','w') as fw:
	fw.write('**** *metadata\n')
	for domaine in mdb.selectall('metadatas'):		
		meta=domaine['meta']
		for filt in filters.filters_metadata:
			meta=meta.replace(filt,'')
			meta=meta.replace(filt.swapcase(),'')
		fw.write(meta.encode('ascii','ignore'))		
		fw.write('\n')
		
	
		
fw.close()
	
		
