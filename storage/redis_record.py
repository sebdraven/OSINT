# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 15:30:33 2013

@author: slarinier
"""
import redis

class RedisRecord(object):
    
    def __init__(self,host='localhost',port=6379,db=1):
        pool=redis.ConnectionPool(host=host,port=port,db=db)
        self.r=redis.Redis(connection_pool=pool)
        self.processus_tab=[]
    def delete(self,key):
        self.r.delete(key)        
    def get(self,key):
       return self.r.get(key)
    def put(self,key,value):
        self.r.set(key,value)
    def init(self,dbs):
        for i in dbs:
            self.flushdb(i)
    def flushdb(self,db_value):
        self.switchDB(db_value)
        self.r.flushdb()
    def rpush(self,listvalue,item):
        self.r.rpush(listvalue,item)
    def rpop(self,listvalue):
        return self.r.rpop(listvalue)
    def switchDB(self,db,host='localhost',port=6379):
        pool=redis.ConnectionPool(host=host,port=port,db=db)
        self.r=redis.Redis(connection_pool=pool)
    def currentDB(self):
        return self.r.connection_pool.get_connection(1).db