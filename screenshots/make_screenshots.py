#!/usr/bin/python	
import screenshots
import sys
import threading

file_list_websites=sys.argv[1]
jsfile=sys.argv[2]	
emplacement=sys.argv[3]
threadpool=sys.argv[4]
domaines=[]
main_thread = threading.currentThread()
with open(file_list_websites,'r') as fr:
	for ligne in fr:
		domaines.append(ligne.replace('\r\n',''))
print domaines
i=0
for domaine in domaines:
	i+=1	
	screen=screenshots.Screenshots(domaines,jsfile,emplacement,domaine)
	screen.start()
	if i % int(threadpool):
		for t in threading.enumerate():
			if t is not main_thread:
				t.join()
						
