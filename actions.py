'''
Created on Feb 1, 2013

@author: slarinier
'''

from libnmap.parser import NmapParser
from libnmap.process import NmapProcess
import pymongo
from pymongo.connection import Connection
import threading

from harvesting import search
from harvesting.crawler import Record, CrawlerThread
import mongodb
from network import make_networks, networks
from network.IPy import IP
from processing import metadataextract
from processing.clean_db import Cleandb
from processing.create_result import Create_Result
from processing.dnstree import DNSTree
from screenshots.screenshots import Screenshots
from scanners.networks import Networks

class Actions(object):
    '''
    classdocs
    '''
    def __init__(self,db_value):
        self.db_value=db_value
        connection=Connection('localhost',27017)
        self.db=connection[db_value]
    def create_network(self):
        network=make_networks.make_networks('localhost', self.db_value)
        network.createNetworks('new_domaines')
        network.exportFile(self.db_value+'_network.log')

    def create_result(self,collection,criteria):
        createResult=Create_Result(self.db_value,criteria)
        if collection=='scanners':
            createResult.processScanners(collection)
            return
        createResult.process(collection)
    
    def metasearch(self,criteria,scriptsJS,geoloc):
        print "########### Meta Search ###########"
        main_thread = threading.currentThread()
        thread_pool=[]
        for criterius in criteria:
            for script in scriptsJS:
                gs=search.search(100,criterius,script,self.db_value)
                gs.start()
                thread_pool.append(gs)
            for t in threading.enumerate():
                if t is not main_thread:
                    t.join()
            for t in thread_pool:
                t.record()
        print "########### Search terminated ###########"

        print "########### Resolve IP ############"
        networks.resolve(geoloc,self.db_value)
    
    def search_ip(self,geoloc,scriptsJS,ip_range):
        main_thread = threading.currentThread()
        print "########### Search by IP ###########"
        ips=[]
        domaines=self.db.new_domaines.find()
        thread_pool=[]
        cache={}
        for domaine in domaines:
            try:    
                ips.append(domaine['ip'])
    
            except KeyError:
                print domaine
        i=0
        print 'les IPS sont: '+ str(ips)
        ip_to_add=[]
        if ip_range:
            ip_to_add=[str(x) for x in IP(ip_range)]
            ips[len(ips):]=ip_to_add
        for ip in set(ips):
            if ip != '0.0.0.0':
                i+=1
                gs=search.search(20,'ip:'+str(ip),scriptsJS[1],self.db_value)
                gs.start()
                thread_pool.append(gs)
            if i % 10 ==0:
                for t in threading.enumerate():
                    if t is not main_thread:
                        t.join()
                for t in thread_pool:
                    t.record()
        print "########### Search terminated ###########"         
        print "########### Search by network ###########"

        print "########### Resolve IP ############"
        networks.resolve(geoloc,self.db_value)

    def scan_network(self):
        pass
    def scan_nmap(self,ip_range,options):
        ips=[]
        domaines=self.db.new_domaines.find()
        thread_pool=[]
        cache={}
        for domaine in domaines:
            try:    
                ips.append(domaine['ip'])
                cache[domaine['ip']]=domaine
            except KeyError:
                print domaine
        net=Networks(list(set(ips)),options)        
        net.run()
        report=net.make_report()
        #net.record_report(report,cache,self.db.new_domaines)       
        pass
    def screenshots(self,db_value,threadpool):
        connection=Connection('localhost',27017)
        db=connection[db_value]
        domaines=db.new_domaines.distinct('domaine')
        i=0
        main_thread = threading.currentThread()
        print "print "+ str(len(domaines))+ " screenshots"
        for domaine in domaines:
            i+=1    
            screen=Screenshots(domaines, 'screenshots/screenshots.js', 'screenshots/screenshots/'+db_value, domaine)
            screen.start()
            if i % int(threadpool)==0:
                for t in threading.enumerate():
                    if t is not main_thread:
                        t.join()
    
    def metadata_exctract(self,db):
        main_thread = threading.currentThread()
        print "########## Meta Data IP ##########"
        mdb=mongodb.mongodb('localhost',27017,db)
        i=0

        for domaine in mdb.selectall('new_domaines'):
            i+=1
            url=domaine['url']
            domaine_value=domaine['domaine']
            print url
            if not 'meta' in domaine:
                domaine['meta']='ok'
                mtd=metadataextract.metadataextract('harvesting/metaextract.js',db,domaine_value,url)
                mtd.start()
                if i % 30==0:
                    for t in threading.enumerate():
                        if t is not main_thread:
                            t.join(2)

    def dnstree(self,db_value):
        dnst=DNSTree(db_value)
        dnst.process()
    
    def crawl(self,list_domains):
        main_thread = threading.currentThread()
        #domaines=self.db.new_domaines.distinct('domaine')
        domains=list_domains.split(',')
        threadpool=[]
        lock=threading.Lock()
        rec=Record(self.db_value,lock)
        rec.start()
        i=0
        for domain in domains:
            i=i+1
            cw=CrawlerThread(domain,self.db,lock)        
            cw.run()        
        
            if i % 5==0:
                for t in threading.enumerate():
                    if t is not main_thread:
                        t.join(2)
        stop=True
    
        while(stop):
            for t in threadpool:
                if not t.IsActive():
                    threadpool.remove(t)
                if len(threadpool)==0:
                    stop=False
                    
    def clean_db(self,pathfilters):
        print "#####Clean DB####"        
        directory = "screenshots/screenshots/"+self.db_value
        filters=[]
        with open(pathfilters,'r') as fw:
            for ligne in fw:
                filters.append(ligne.strip())        
            cl=Cleandb(self.db_value, directory, filters)
            cl.clean()
    
    def reset(self):
        
        for domaine in self.db.new_domaines.find():
            domaine['meta']=None
            self.db.update(domaine,'new_domaines')
        
    def init(self,db,coll,attrib):
        
        self.db.create_collection(coll)
        self.db[coll].ensure_index([(attrib,pymongo.ASCENDING)],unique=True)
        