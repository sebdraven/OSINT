import sys
requests=[]
with open(sys.argv[1],'r') as fr:
    for ligne in fr:
        ligne=ligne.strip()
        requests.append('site:'+ligne+'.com,' +sys.argv[1]+' and '+ligne)
      
with open(sys.argv[2],'w') as fw:
    for request in requests:
        fw.write(request+'\n')
