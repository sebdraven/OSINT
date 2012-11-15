#!/usr/bin/python
from pymongo import Connection
import pymongo


class Create_Result():
	
	def __init__(self,dbname,critere):
		self.dbname=dbname
		self.critere=critere
		
	def process(self,collection):
		print "######### Print Result database ##########"
		connection=Connection('localhost',27017)
		db=connection[self.dbname]
		domaines=db[collection].find()
		if self.critere.find(','):
			critere=self.critere.split(',')
		else:
			if len(self.critere) > 0:
				critere=[critere]

		with open(self.dbname+'.log','w') as fw:
			for domaine in domaines:
				try:
					fw.write(','.join(domaine[key] for key in critere))
					fw.write('\n')
				except KeyError:
					print 'domaine: '+str(domaine)
				except pymongo.errors.OperationFailure:
					print 'error mongo '+ str(domaine)

	def processScanners(self, collection):
		connection = Connection('localhost', 27017)
		db = connection[self.dbname]
		domaines = db[collection].find()		
		if self.critere.find(','):
			critere = self.critere.split(',')
		else:
			if len(self.critere) > 0:
				critere = [critere]
									
		with open(self.dbname + '.log', 'w') as fw:
			for domaine in domaines:
				try:
					towrite=''
					for key in critere:
						infos = domaine[key]
						if len(infos)>0:
							if isinstance(infos, list):
								infos=','.join(infos)
							towrite=towrite+','+infos
							fw.write(towrite+'\n')
				except KeyError:
					print 'domaine: ' + str(domaine)
				except pymongo.errors.OperationFailure:
					print 'error mongo ' + str(domaine)