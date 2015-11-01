'''
Created on 14 mai 2014

@author: slarinier
'''
from libnmap.parser import NmapParser
from libnmap.process import NmapProcess

class Networks(object):
    '''
    classdocs
    '''


    def __init__(self, targets,options):
        self.nmap=NmapProcess(targets,options)
    def run(self):
        self.nmap.run()
        
    def make_report(self):
        report=NmapParser.parse(self.nmap.stdout)
        result=[]
        for host in report.hosts:
            temp={}
            print host
            print  host.scripts_results
            temp['ip']=host.ipv4
            print [(service.state,service.port,service.scripts_results) for service in host.services]
#             for service in host.services:
#                 for k in service.scripts_results:
#                     if k.find('.'):
#                         v=service.scripts_results[k]
#                         del service.scripts_resutls[k]
#                         service.scripts_resutls[k.replace('.','_')]=v
#                 temp['services']=[(service.state,service.port,service.scripts_results)]
#             result.append(temp)
#         return result
    def record_report(self,records,cache,coll):
        for r in records:
            doc=cache[r['ip']]
            doc['service']=r
            try:
                coll.save(doc)
            except:
                print doc