from pymongo.connection import Connection
import glob
import os
import sys

class Cleandb(object):

	def __init__(self,db_value,directory,filters):
		connection=Connection('localhost',27017)
		self.db=connection[db_value]
		self.filters=filters
		self.directory=directory
	def clean(self):
		list_domains=[]
		list_files=glob.glob(self.directory+'/*.png')
		for name_file in list_files:
			fileName, fileExtension=os.path.splitext(name_file)
			tokens=fileName.split('/')
			domain=tokens[len(tokens)-1]
			list_domains.append(domain)
		list_domains_db_unicode=self.db.new_domaines.distinct('domaine')
		list_domains_db=[str(domain) for domain in list_domains_db_unicode ]
		list_to_remove=list(set(list_domains_db)-set(list_domains))
		for domain in list_to_remove:
			if self._filters(domain):
				self.db.new_domaines.remove({'domaine':domain})
	def _filters(self,domain):
		for filter in self.filters:
			if filter.find(domain)!=-1:
				return False
			return True 