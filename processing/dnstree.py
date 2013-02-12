'''
Created on Dec 20, 2012

@author: slarinier
'''
from pymongo.connection import Connection
import pymongo
from pyfaup.faup import Faup
class DNSTree(object):
    '''
    classdocs
    '''


    def __init__(self,db_value):
        '''
        Constructor
        '''
        connection=Connection('localhost',27017)
        self.db=connection[db_value]
    def process(self):
        list_domains=self.db['new_domaines'].distinct('domaine')
        fex=Faup()
        for domain in list_domains:
            url='http://'+str(domain)
            fex.decode(url, False)
            print (fex.get_tld()+','+fex.get_domain()+','+','.join(fex.get_subdomain().split('.')[::-1]).replace('www','')).replace(',,',',')
            
        