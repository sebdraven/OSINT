import os
import subprocess
from subprocess import Popen, PIPE
import threading
from content import Content
from random_user_agent import Random_user_agent

class pastebinExtract(threading.Thread):
    def __init__(self,url,casperJSScript='pastebintext.js'):
        threading.Thread.__init__(self)
        self.url=url
        self.casperJSScript=casperJSScript
        self.content=Content()
        self.data=[]
        rua=Random_user_agent()
        self.ua=rua.rand()
        self.result=None
   
    def run(self):
        result=subprocess.Popen(['casperjs' ,self.casperJSScript,self.url,'\''+self.ua+'\''],stdout=PIPE)
        for ligne in result.stdout:
                record=ligne.strip()                
                self.data.append(record.lower())
                
        keywords=getattr(self.content,'keywords')
        for keyword in keywords:
            if self.content.search(keyword,str(self.data)):
                self.result={'url': self.url, 'data': self.data}