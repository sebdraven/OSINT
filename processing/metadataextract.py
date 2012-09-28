import os
import subprocess
from subprocess import Popen, PIPE
import threading
import pymongo
from pymongo import Connection
import simplejson
import HTMLParser
class metadataextract(threading.Thread):
	def __init__(self,scriptjs,db,domaine,url):
		threading.Thread.__init__(self)
		self.result=[]
		self.domaine=domaine
		self.scriptjs=scriptjs
		self.url=url
		self.connection=Connection('localhost',27017)
		self.db=self.connection[db]

	def run(self):
		result=subprocess.Popen(['casperjs',self.scriptjs,self.url],stdout=PIPE)
		meta=''
		contents=[]
		
		for ligne in result.stdout:
			meta=meta+ligne
			
		try:
			data = simplejson.loads(meta)
			#print data
			print len(data)
			if len(data) > 0:
				print data
				for content in data:
					contents.append(content['content'])
					
				meta=' '.join(contents)
				print meta
				if len(meta) >0:
					h = HTMLParser.HTMLParser()
					print h.unescape(meta)
					value_db={'domaine':self.domaine,'meta':h.unescape(meta)}
					self.db.metadatas.save(value_db)
		except ValueError:
			print 'Erreur encoding: '+ meta
