'''
Created on Oct 2, 2012

@author: slarinier
'''
import re
class Content_search(object):
    '''
    classdocs
    '''


    def __init__(self,action,data):
        '''
        Constructor
        '''
        self.action=action
        self.data=data
            
    def keyword_only(self,keyword):
        tokens=re.findall(keyword, self.data)
        if len(tokens) > 0:
            return True
        return False
    
    def keywords_and(self,keywords):
        keywords=keywords.split('&')
        
        for keyword in keywords:
            if self.keyword_only(keyword) == False:
                return False
        return True
                
        
    