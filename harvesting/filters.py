# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 17:40:53 2013

@author: slarinier
"""
class Filters(object):
    def __init__(self,pathextention='harvesting/filtered_extensions',pathscheme='harvesting/filtered_schemes',pathdomain='harvesting/filtered_domains'):
        self.pathdomain=pathdomain
        self.pathscheme=pathscheme
        self.pathextentions=pathextention
        self.domains=[]
        self.schemes=[]
        self.extentions=[]
    def load(self):
        with open(self.pathdomain,"r") as fr:
            self.domains=[line.strip() for line in fr]
        with open(self.pathscheme,"r") as fr:
            self.schemes=[line.strip() for line in fr]
        with open(self.pathextentions,"r") as fr:
            self.extentions=[line.strip() for line in fr]
    def isfilteredextention(self,path):
        try:
            for ext in self.extentions:
                if path.endswith(ext):
                    return True
            return False
        except:
            print "extension error"
        
    def isfilteredscheme(self,scheme):
            return scheme is self.schemes
    def isfiltereddomains(self,domain):
        try:        
            tokens=domain.split('.')[::-1]
            for d in self.domains:
                d_tokens=d.split('.')[::-1]
                d_reverse=d_tokens[0]+'.'+d_tokens[1]
                t_reverse=str(tokens[0]+'.'+tokens[1])    
                if d_reverse == t_reverse:
                    return True
        except IndexError as e:
            if domain.find('.') == -1:
                return True
        except AttributeError as e:
            print "test"
        return False