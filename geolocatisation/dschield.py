import urllib2
import re
class dschield(object):
	
	def __init__(self,url):
		self.url=url	
	
	def response(self,ip):
		dschieldContent=urllib2.urlopen(self.url+ip)
		value=dschieldContent.read()
		patern='country= (\w+)'
		
		reg =re.compile(patern)
		m = reg.search(value)
		country=''		
		if m:
			 country=m.group(1)
		patern='asname= (.+)'		
		reg =re.compile(patern)
		m = reg.search(value)
		asname=''
		if m:
			asname=m.group(1)
		patern='network= (.+)'
		reg =re.compile(patern)
		m = reg.search(value)
		network=''
		if m:
			network=m.group(1)
			network=network.split(' ')[0]
		if country != '' and asname !='' and network !='':		
				return (ip,country,asname,network)
		return ('127.0.0.1','mars','alien','nothing')
