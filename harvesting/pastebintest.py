#!/usr/bin/python
import pastebin
import geolocatisation


paste=pastebin.pastebin('http://pastebin.com/archive',[],'pastebin.js')
paste.pastebinArchive()
#setattr(paste,'casperJSScript','pastebintext.js')
paste.pastebinAnalyse()
