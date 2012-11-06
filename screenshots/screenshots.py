import subprocess
from subprocess import Popen, PIPE
import threading
import time
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 12:24:14 2012

@author: slarinier
"""

class screenshots(threading.Thread):
	def __init__(self,listofwebsites,jsfile,location,website):
		self.listofwebsites=listofwebsites
		self.jsfile=jsfile
		self.location=location
		self.website=website
		threading.Thread.__init__(self)
		
	def makescreenshots(self):
        	for host in set(self.listofwebsites):
			print "prise de la copie d'ecran: "+host    
			cmd='casperjs '+self.jsfile+' '+host +' http://'+host +' '+self.location
			print cmd
			args=cmd.split()
			print args
			result=subprocess.Popen(args,stdout=PIPE)
			for ligne in result.stdout:
				print ligne
	def run(self):
		cmd='casperjs '+self.jsfile+' '+self.website +' http://'+self.website +' '+self.location
		print cmd
		args=cmd.split()
		print args
		result=subprocess.Popen(args,stdout=PIPE)
		time.sleep(3)			
	
