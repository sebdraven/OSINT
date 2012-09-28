import sys
file_ref = sys.argv[1]
file_to_compare = sys.argv[2]
file_result = sys.argv[3]
file_marque = sys.argv[4]

map_file_ref = {}

with open(file_ref, 'r') as fr:
    for ligne in fr:
        ligne = ligne.strip()
        tokens = ligne.split(',')
        ip = tokens[1]
        domaine = tokens[2]
        if ip in map_file_ref:
            domaines = map_file_ref[ip]
            domaines.append(domaine)
        else :
            map_file_ref[ip] = [domaine]

