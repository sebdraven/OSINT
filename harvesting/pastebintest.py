#!/usr/bin/python
import pastebin

paste=pastebin.pastebin('http://pastebin.com/archive',[],'pastebin.js')
paste.pastebinArchive()
setattr(paste,'casperJSScript','pastebintext.js')
result=paste.pastebinAnalyse()
print result
