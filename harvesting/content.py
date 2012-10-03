'''
Created on Oct 1, 2012

@author: slarinier
'''
import re
from content_search import Content_search

class Content(object):
    '''
    classdocs
    '''
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Content, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self,filetoload='keywords'):
        '''
        Constructor
        '''
        self.filetoload=filetoload
        self.keywords=[]
        with open(self.filetoload,'r') as fr:
            for ligne in fr:
                self.keywords.append(ligne.strip())
    
    def analyse(self,ligne):
        if ligne.find('&') != -1:
            return 'keywords_and'
        else :
            return 'keyword_only'     
    
    def search(self,keyword,data):
            action=self.analyse(keyword)
            cs = Content_search(action,data)
            find=getattr(cs, action)(keyword)
            return find
            
                
            