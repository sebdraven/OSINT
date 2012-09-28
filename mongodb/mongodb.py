from pymongo import Connection
import bson
import pymongo
class mongodb(object):
	def __init__(self,host,port,db):
		self.host=host
		self.port=port
		self.connection=Connection(host,port)
		self.db=self.connection[db]
	def insert(self,collection,key,value):				
		col=self.db[collection]
		value_db={'domaine':value}
		#col.create_index([('domaine', pymongo.DESCENDING)])		
		col.save(value_db)
	def update(self,item,collection):
		col=self.db[collection]
		try:
			col.save(item)
		except bson.errors.InvalidStringData:
			print 'InvalidString '+ str(item)
	def selectbyDict(self,request,col):
		self.col=self.db[col]
		return self.col.find(request)

	def selectbycreteria(self,key,criteria,col):
		request={key:criteria}
		self.col=self.db[col]
		return self.col.find(request)
	
	def selectall(self,collection):
		col=self.db[collection]
		return col.find()
		
	def insertMultiCriteria(self,collection,items):
		print "insert "+str(items)
		col=self.db[collection]
		try:
			col.save(items)
		except ValueError:
			print 'Erreur encoding: ' + items
