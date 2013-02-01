'''
Created on Jan 18, 2013

@author: slarinier
'''

import datetime
import logging

class History(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        d=datetime.datetime.now()
        date_value=d.strftime("%Y-%m-%d")
        self.logger=logging.getLogger('history')
        hdlr = logging.FileHandler('history/'+date_value+'.log')
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        self.logger.addHandler(hdlr) 
        self.logger.setLevel(logging.INFO)
          
    def register(self,action):
        self.logger.info(action)
        
        