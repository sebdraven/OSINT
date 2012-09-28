import os
import subprocess
from subprocess import Popen, PIPE
import threading

class pastebinExtract(threading.Thread):
    def __init__(self,url,casperJSScript='pastebintext.js'):
        threading.Thread.__init__(self)
        self.url=url
        self.casperJSScript=casperJSScript
        
        
    def run(self):
        print self.url
        result=subprocess.Popen(['casperjs' ,self.casperJSScript,self.url],stdout=PIPE)
        for ligne in result.stdout:
                print ligne
