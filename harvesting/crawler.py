'''
Created on Jan 7, 2013

@author: slarinier
'''
from pholcidae import Pholcidae
from pymongo.connection import Connection
from threading import Thread
import redis
import threading
from pyfaup.faup import Faup
import time
class CrawlerThread(threading.Thread):
    def __init__(self,domain,db_value):
        threading.Thread.__init__(self)
        self.domain=domain    
    def run(self):
        cw=Crawler(self.domain,4)
        cw.start()
        
class Record(threading.Thread):
        def __init__(self,db_value):
            pool = redis.ConnectionPool(host='localhost', port=6379, db=4)
            self.r=redis.Redis(connection_pool=pool)
            self.connection=Connection('localhost',27017)
            self.db=self.connection[db_value]
            threading.Thread.__init__(self)
        def run(self):
            i=0
            while(True):
                i=i+1
                if i % 1000==0:
                    time.sleep(10)
                url=self.r.rpop('crawl')
                fex=Faup()
                if url:
                    fex.decode(url)
                    domain=fex.get_host()
                    entry = self.db.new_domaines.find_one({'domaine':domain})
                    if entry== None:
                        print "record: "+ domain
                        self.db.new_domaines.save({'domaine':domain,'urls':[url]})
                  #  for entry in entries:
                   #     print "domaine already found"               
                    #    urls_stored = entry['urls']
                     #   if not url in urls_stored:
                      #      urls_stored.append(url)
                       #     entry['urls']=urls_stored
                        #    self.db.new_domaines.save(entry)
                        
   
class Crawler(Pholcidae):
    '''
    classdocs
    '''

    
    def __init__(self,domain,db_int):
        '''
        Constructor
        '''
        self.settings={'domain':'','start_page':'/'}
        self.settings['domain'] = domain
        self.result=[]
        super(Crawler, self).__init__()
        pool = redis.ConnectionPool(host='localhost', port=6379, db=db_int)
        self.r=redis.Redis(connection_pool=pool)
    def crawl(self, data):
            self.r.rpush('crawl',data.url)
            
        