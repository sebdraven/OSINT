#!/usr/bin/python
import pymongo
from pymongo import Connection
import sys

def usage():
    print "#Create result: ./create_result.py base 'critere1,critere2'"
    print len(sys.argv)
    sys.exit(1)
if len(sys.argv) != 3:
    usage()

client=sys.argv[1]
critere=sys.argv[2]

if critere.find(','):
    critere=critere.split(',')
else:
    usage()


print "######### Print Result database ##########"
connection=Connection('localhost',27017)
db=connection[client]
domaines=db.new_domaines.find()

with open(client+'.log','w') as fw:
    for domaine in domaines:
        try:
            fw.write(','.join(domaine[key] for key in critere))
            fw.write('\n')
        except KeyError:
            print 'domaine: '+str(domaine)
        except pymongo.errors.OperationFailure:
            print 'error mongo '+ str(domaine)

