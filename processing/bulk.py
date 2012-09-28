import sys
import subprocess
from subprocess import Popen, PIPE

with open(sys.argv[1],'r') as fr:
    for ligne in fr:
        result=subprocess.Popen(['python' ,'main.py',sys.argv[1],ligne,'../geolocalization/GeoLiteCity.dat'],stdout=PIPE)       
        for ligne in result.stdout:
            print ligne
