import sys
from harvesting import white_list
import mongodb

db=sys.argv[1]
mdb=mongodb.mongodb('localhost',27017,db)

for domaine in mdb.selectall('new_domaines'):
    dm=domaine['domaine']
    
