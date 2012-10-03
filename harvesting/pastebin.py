import os
import subprocess
from subprocess import Popen, PIPE
import threading
import pymongo
from pymongo import Connection
from pastebinExtract import pastebinExtract
from random_user_agent import Random_user_agent
import time
class pastebin():
    def __init__(self, url,keyword,casperJSScript):
        self.url=url
        self.keyword=keyword
        self.casperJSScript=casperJSScript
        self.urls=[]
        rua=Random_user_agent()
        self.ua=rua.rand()
        self.time = rua.randsleep()
        self.result=[]
    def pastebinArchive(self):
        result=subprocess.Popen(['casperjs' ,self.casperJSScript,self.url,'\''+self.ua+'\''],stdout=PIPE)
        for ligne in result.stdout:
            if ligne.find('/')!=-1 and ligne.find('archive') == -1:
                id=ligne.replace(' - /','').strip()
                id=id.replace('\n','')
                self.urls.append('http://pastebin.com/raw.php?i='+id)
        print self.urls
               
    def pastebinAnalyse(self):
        i=0
        main_thread = threading.currentThread()
        thread_pool=[]
        for url in self.urls:
            pasteExtract=pastebinExtract(url)
            time.sleep(self.time)
            pasteExtract.start()
            thread_pool.append(pasteExtract)
            i+=1
            if i % 500 ==0:
                for t in threading.enumerate():
                    if t is not main_thread:
                        t.join()
                        
        for t in thread_pool:
            result =getattr(t,'result')
            if result :
                self.result.append(result)
        return self.result
                    
        
