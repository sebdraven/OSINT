'''
Created on Dec 20, 2012

@author: slarinier
'''
from pymongo.connection import Connection
import pymongo
import tldextract
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
        for domain in list_domains:
            tldex=tldextract.extract(domain,False)
            tld=tldex.tld
            subdomains=tldex.subdomain
            domain_value=tldex.domain
            print (tld+','+domain_value+','+','.join(subdomains[::-1]).replace('www','')).replace(',,',',')
            
        