'''
Created on Oct 2, 2012

@author: slarinier
'''
import random
class Random_user_agent(object):
    '''
    classdocs
    '''
    _instance = None
    def __init__(self,path_user_agent='harvesting/user_agents'):
        '''
        Constructor
        '''
        self.user_agent_list=[]
        self.path_user_agent=path_user_agent
        with open(self.path_user_agent,'r') as fr:
            for user_agent in fr:
                if user_agent.find('#') == -1:
                    self.user_agent_list.append(user_agent)
                
        
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Random_user_agent, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance
    
    def rand(self):
        return random.choice(self.user_agent_list)
    def randsleep(self):
        return random.randrange(1,3,2)