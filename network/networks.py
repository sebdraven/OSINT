from pymongo import Connection
import pygeoip
import pymongo
import re
import socket
import whois

def resolve_dns(hostname):
    ip=None
    try:
        ip=socket.gethostbyname(hostname)
    except socket.gaierror:
        print "DNS Resolution Failure: "+hostname
    return ip 

def geolocIP(pathgeoloc,ip):
    geo=None
    glc = pygeoip.GeoIP(pathgeoloc)
    try:
        ar=glc.record_by_addr(ip)
        geo=str(ar['latitude'])+'_'+str(ar['longitude'])
    except pygeoip.GeoIPError:
        print "Erreur de geoloc"
    return geo
    
def whoisIP(whois_service,ip):
    result=None
    try:
        Whois = whois.WhoisConsumer(ip)
        whois.WhoisRequest(Whois,whois_service)
        whois.asyncore.loop()
        result=Whois.text
    except socket.gaierror:    
        print "Whois Failure: "+ip
    return result
    
    #pattern = 'inetnum: (.*)'				
    #reg_CIDR=re.compile(pattern)
    
def extract_whois_information(pattern,whois_text):
    reg_CIDR=re.compile(pattern)
    m=reg_CIDR.search(whois_text)
    information=None
    if m:
        information=m.group(1)
    return information
       
def resolve(pathgeoloc,db):
    connection=Connection('localhost',27017)
    db=connection[db]
    domaines=db.new_domaines.find()
    for domaine in domaines:
        try:       	
            domaine_value=domaine['domaine']
            if not 'ip' in domaine:
                print 'resolution '+domaine_value
                ip=resolve_dns(domaine['domaine'])
                if ip != None or ip != '0.0.0.0':
                    print 'ip du domaine ' + domaine_value +' '+ ip 
                    domaine['ip']=ip
                    key = geolocIP(pathgeoloc,ip)
                    domaine['geoloc']=key
                    whois_text=whoisIP("whois.ripe.net",ip)
                    network=None
                    if whois_text !=None:
             	        pattern_network = 'inetnum: (.*)'				
             	        network=extract_whois_information(pattern_network,whois_text)
             	    if network != None:
                 	    domaine['network']=network
                    db.new_domaines.save(domaine)
        except TypeError:
                print 'Error type '+domaine_value            
        except pymongo.errors.OperationFailure:
            print 'Error pymongo ' +domaine
