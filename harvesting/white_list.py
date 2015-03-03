from mongodb import mongodb
import os
import glob
class white_list():

    def __init__(self,db):
        self.mdb=mongodb.mongodb('localhost',27017,db)
        self.white_list=[]
        self.white_domaine=['msn.com','google.com','wikipedia.fr','free.fr','linkedin.com']
        
    def loadWhiteList(self):
        domaines=self.mdb.selectall('white_list')
        for domaine in domaines:
           self. white_domaine.append(domaine['domaine'])
			
    def makeWhiteList(self,path):
        list_files=os.walk(path)
        for root,dirs,files in list_files:
            category=''
            for fl in files:
                if fl=='domains':
                    with open(root+'/'+fl,'r') as fr:
                        root=root.replace(path,'')
                        if '/' in root:
                            category=root.replace('/','_')
                        else:
                            category=root
                        for ligne in fr:
                            item={'domaine':ligne.strip(),'category':category}
                            self.mdb.update(item,'white_list')
    def	searchInWhiteList(self,domaine):
        result=self.mdb.selectbycreteria('domaine',domaine,'white_list')
        if result is not None:
            category=result[0]
            print category['category']
            return category
	#def compare_white_list()		
		