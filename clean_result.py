import sys
import glob
import os
from mongodb import mongodb

pathdirectory=glob.glob(sys.argv[1])
db=sys.argv[2]
mdb=mongodb.mongodb('localhost',27017,db)
with open(db+'_cleaned.log','w') as fw:
	for name_file in pathdirectory:
		fileName, fileExtension =os.path.splitext(name_file)
		tokens=fileName.split('/')
		domaine=tokens[len(tokens)-1]
		results=mdb.selectbycreteria('domaine',domaine,'new_domaines')
	
		for result in results:
			 fw.write(result['ip']+';'+result['domaine']+'\n')
fw.close()
