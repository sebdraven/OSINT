import threading

from harvesting import search

class search_on_network(threading.Thread):

	def __init__(self,network_ip,criterius,script,limit,db):
		threading.Thread.__init__(self)
		self.gs=search.search(limit,criterius,script,db)
		self.network_ip=network_ip
		self.network_all_ready=[]
	def run(self):
		if not str(self.network_ip) in self.network_all_ready:
			self.network_all_ready.append(str(self.network_ip))
			for ip in self.network_ip:
				setattr(self.gs,'criteria','ip:'+str(ip))
				self.gs.run()                        
			
		
