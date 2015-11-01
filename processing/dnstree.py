'''
Created on Dec 20, 2012

@author: slarinier
'''
from pymongo import MongoClient
import pymongo
from pyfaup.faup import Faup


class DNSTree(object):
    '''
    classdocs
    '''

    def __init__(self, db_value):
        '''
        Constructor
        '''
        connection = MongoClient(host='localhost', port=27017,db=db_value)
        self.db = connection[db_value]

    def process(self):
        list_domains = self.db['new_domaines'].distinct('domaine')
        fex = Faup()
        for domain in list_domains:
            url = 'http://' + str(domain)
            fex.decode(url, False)
            print (
            fex.get_tld() + ',' + fex.get_domain() + ',' + ','.join(fex.get_subdomain().split('.')[::-1]).replace('www',
                                                                                                                  '')).replace(
                ',,', ',')
