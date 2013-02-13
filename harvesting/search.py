from pymongo import Connection
from subprocess import PIPE
from white_list import white_list
import re
import subprocess
import threading
from random_user_agent import Random_user_agent

class search(threading.Thread):
    def __init__(self,limit,criteria,scriptjs,db,url_pattern='((https?|ftp|gopher|telnet|file|notes|ms-help):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&])*)'):
        threading.Thread.__init__(self)
        self.result=[]
        self.limit=limit    
        self.criteria=criteria
        self.scriptjs=scriptjs
        self.connection=Connection('localhost',27017)
        self.db=self.connection[db]
        self.whitelist=white_list(db)
        self.regex_url=re.compile(url_pattern)
        rua=Random_user_agent()
        self.ua=rua.rand()
        self.urls_by_domaine={}
            
    def run(self):
        i=0
        while i < self.limit:
            result=subprocess.Popen(['casperjs' ,self.scriptjs,str(i),self.criteria,self.ua],stdout=PIPE)
            for ligne in result.stdout:
                if ligne.find('/')!=-1 and ligne.find('http://') != -1:
                    url_information=self.regex_url.search(ligne)
                    url=url_information.group(1)
                    domaine=url.split('/')[2]
                    tokens=domaine.split('.')
                    racine=tokens[len(tokens)-2]+'.'+tokens[len(tokens)-1]
                    
                    print "domain found: "+ domaine
                    
                    if not racine in getattr(self.whitelist, 'white_domaine'):
                        if domaine in self.urls_by_domaine:
                            urls= self.urls_by_domaine[domaine]
                            urls.append(url)
                            self.urls_by_domaine[domaine]=urls
                        else:
                            self.urls_by_domaine[domaine]=[url]
                            
            i=i+10
                            
    def record(self):    
        print "#######################record############################"
        domaines = iter(self.urls_by_domaine)    
        for domaine in domaines:
            entry = self.db.new_domaines.find_one({'domaine':domaine})
            if entry== None:
                self.db.new_domaines.save({'domaine':domaine,'urls':self.urls_by_domaine[domaine],'criteria':[self.criteria]})
            else:
                    
                try:
                    urls_stored = entry['urls']
                    urls=self.urls_by_domaine[domaine]
                    urls_to_store=list(set(urls_stored + urls))
                    criteria=entry['criteria']
                    criteria=list(set(criteria.append(self.criteria)))
                    entry['criteria']=criteria
                    self.db.new_domaines.save(entry)
                except :
                    criteria=[]
                    try :
                        criteria=entry['criteria']
                        criteria=list(set(criteria.append(self.criteria)))
                    except:
                        criteria.append(self.criteria)
                        pass
                    
                    entry['criteria']=criteria
                    self.db.new_domaines.save({'domaine':domaine,'urls':self.urls_by_domaine[domaine],'criteria':criteria})   
            
        