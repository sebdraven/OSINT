import os
import subprocess
from subprocess import Popen, PIPE
import threading
import pymongo
from pymongo import Connection
from pastebinExtract import pastebinExtract
class pastebin():
    def __init__(self, url,keyword,casperJSScript):
        self.url=url
        self.keyword=keyword
        self.casperJSScript=casperJSScript
        self.urls=[]
        
    def pastebinArchive(self):
        result=subprocess.Popen(['casperjs' ,self.casperJSScript,self.url],stdout=PIPE)
        for ligne in result.stdout:
            if ligne.find('/')!=-1 and ligne.find('archive') == -1:
               self.urls.append('http://pastebin.com'+ligne.replace(' - ','').strip())
        print self.urls
               
    def pastebinAnalyse(self):
        i=0
        main_thread = threading.currentThread()
        for url in self.urls:
            print url
            pasteExtract=pastebinExtract(url)
            pasteExtract.start()
            i+=1
            if i % 30 ==0:
                for t in threading.enumerate():
                    if t is not main_thread:
                        t.join()
                
               
                    
        
