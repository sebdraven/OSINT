from pymongo import Connection
import pygeoip
import pymongo
import re
import socket
import whois

def port_connexion_by_hostname(hostname,port):
    try:
        http_socket = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
        http_socket.connect ( ( hostname, port ) )
        return True
    except socket.gaierror:
        return False    
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
        if ar!=None:
            geo=str(ar['latitude'])+'_'+str(ar['longitude'])
        return ''
    except pygeoip.GeoIPError:
        print "Erreur de geoloc"
    return geo
def geolocCountry(pathgeoloc,ip):
    geo=None
    glc = pygeoip.GeoIP(pathgeoloc)
    try:
        ar=glc.record_by_addr(ip)
        if ar != None:
            geo=ar['country_code3']
        else:
            return ''
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
       
def resolve(pathgeoloc,db_value):
    connection=Connection('localhost',27017)    
    db=connection[db_value]
    
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
                    netname=None
                    if not 'Whois'in domaine:
                        pattern_netname='netname: (.*)'
                        netname=extract_whois_information(pattern_netname,whois_text)
                        domaine['netname']=netname
                    network=None
                    if whois_text !=None:
             	      pattern_network = 'inetnum: (.*)'				
             	      network=extract_whois_information(pattern_network,whois_text)
             	    if network != None:
                 	  domaine['network']=network
                    try:   
                        db.new_domaines.save(domaine)
                    except:
                         print domaine
        except TypeError:
                print 'Error type '+domaine_value            
        except pymongo.errors.OperationFailure:
            print 'Error pymongo ' +domaine
