# -*- coding: utf -*-
"""
monitor.py

Simple script to monitor one or more output files from track_keywords.py

Based on:
https://github.com/seb-m/pyinotify/blob/master/python2/examples/transient_file.py

Kevin Driscoll, 2014
"""

import colors
import pyinotify
import sys
import time

global nextcolor

class ProcessTransientFile(pyinotify.ProcessEvent):

    def __init__(self, n):
        global nextcolor
        self.fg = nextcolor
        self.lastupdate = time.time() 
        self.freq = 0

    def process_IN_MODIFY(self, event):
        now = time.time()
        report = "{0}s".format(str(round(now-self.lastupdate, 2)))
        self.lastupdate = now
        self.freq += 1
        if not self.freq % 50:
            print colors.color(' '.join((event.name, report)), fg=self.fg)

    def process_default(self, event):
        print 'default: ', event.maskname

if __name__=="__main__":

    filenames = sys.argv[1:]
    wm = pyinotify.WatchManager()
    notifier = pyinotify.Notifier(wm)

    print "Tracking..."
    for n, fn in enumerate(filenames):
        print fn
        nextcolor = (n % 6) + 1
        wm.watch_transient_file(fn, pyinotify.IN_MODIFY, ProcessTransientFile)
    print

    notifier.loop()
