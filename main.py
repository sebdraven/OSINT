#!/usr/bin/python
'''
Created on Sep 25, 2012

@author: slarinier
'''
from harvesting import search
from mongodb import mongodb
from network import networks
from processing import metadataextract
from network import make_networks
from processing.create_result import Create_Result
from pymongo.connection import Connection
import argparse
import sys
import threading

#def search_ip(domaine_ip,network_all_ready):    
#    keys = domaine_ip
#    list_whois=["whois.arin.net","whois.ripe.net","whois.apnic.net","whois.lacnic.net","whois.registro.br","whois.nic.ad.jp"]        
#    networks_ip=[]    
#    for key in keys:
#            print key
#             Whois = whois.WhoisConsumer(key)
#             whois.WhoisRequest(Whois, "whois.ripe.net")
#             whois.asyncore.loop()
#             pattern = 'inetnum: (.*)'                
#             reg_CIDR=re.compile(pattern)
#             m=reg_CIDR.search(Whois.text)
#             if m:
#                cidr=m.group(1)    
#                print cidr
#        if cidr.find('0.0.0.0') == -1:
#                     ips = IP(cidr)
#             son=search_on_network.search_on_network(ips,'',scriptsJS[1],50,db)
#             son.start()
#                 #if not str(ips) in network_all_ready:
                  #  network_all_ready.append(str(ips))
                   # for ip in ips:
                    #    print ip
            #result=gs.makesearch(200,'ip:'+str(ip)    ,)                        
            #print result
        #else: 
#            print 'ip non categorise:' +key + 'cidr: '+cidr
#            print Whois.text

def create_network(db):
    network=make_networks.make_networks('localhost', db)
    network.createNetworks('new_domaines')
    network.exportFile(db+'_network.log')

def create_result(db,collection,criteria):
    createResult=Create_Result(db,criteria)
    if collection=='scanners':
        createResult.processScanners(collection)
        return
    createResult.process(collection)
    
def metasearch(criteria,script,db,geoloc):
    print "########### Meta Search ###########"
    
    thread_pool=[]
    for criterius in criteria:
        for script in scriptsJS:
            gs=search.search(100,criterius,script,db)
            gs.start()
            thread_pool.append(gs)
    for t in threading.enumerate():
        if t is not main_thread:
            t.join()
    for t in thread_pool:
        t.record()
    print "########### Search terminated ###########"

    print "########### Resolve IP ############"
    networks.resolve(geoloc,db)
    
def search_ip(db_value,geoloc,scriptsJS):
    print "########### Search by IP ###########"
    ips=[]
    connection=Connection('localhost',27017)
    db=connection[db_value]
    domaines=db.new_domaines.find()
    for domaine in domaines:
        try:    
            ips.append(domaine['ip'])
        except KeyError:
            print domaine
    i=0
    print 'les IPS sont: '+ str(ips)
    for ip in set(ips):
        if ip != '0.0.0.0':
            i+=1
        gs=search.search(20,'ip:'+str(ip),scriptsJS[1],db_value)
        gs.start()
        if i % 10 ==0:
            for t in threading.enumerate():
                if t is not main_thread:
                    t.join()
                
    print "########### Search by network ###########"
#search_ip(ips,[])
    print "########### Resolve IP ############"
    networks.resolve(geoloc,db_value)


'''
reset()
'''

def metadata_exctract(db):
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

def reset():
    connection=Connection('localhost',27017)
    db=connection.connection[db]
    for domaine in db.new_domaines.find():
        domaine['meta']=None
        db.update(domaine,'new_domaines')

if __name__ == '__main__':
    scriptsJS=['harvesting/googlesearch.js','harvesting/bingsearch.js','harvesting/yahoosearch.js']
    result=[]
    domaine_ip={}

#limit=sys.argv[4]
    main_thread = threading.currentThread()

    parser = argparse.ArgumentParser(description='metaharvester')
    parser.add_argument('--db', dest='db', help='db in mongo to store informations')
    parser.add_argument('--geoloc', dest='geoloc')
    parser.add_argument('--action', dest='action')
    parser.add_argument('--criteria', dest='criteria')
    parser.add_argument('--collection', dest='collection')
    args = parser.parse_args()
    db=args.db
    criteria=args.criteria
    geoloc=args.geoloc
    collection=args.collection
    if args.action=='reset':
        reset()
    elif args.action=='metasearch':
        if criteria and scriptsJS and db and geoloc:
            criteria=criteria.split(',')
            metasearch(criteria,scriptsJS,db,geoloc)    
    elif args.action=='search_ip':
        search_ip(db, geoloc,scriptsJS)
    elif args.action =='create_network':
        create_network(db)    
    elif args.action=='metadata':
        metadata_exctract(db)
    elif args.action == 'create_result':
        if not criteria and not db:
            parser.print_help()
        else:
            if collection:
                create_result(db,collection,criteria)    
    else:
        parser.print_help()
        sys.exit(1)