# -*- coding: utf -*-
"""
monitor.py

Simple script to monitor one or more output files from track_keywords.py

Based on:
https://github.com/seb-m/pyinotify/blob/master/python2/examples/transient_file.py

Kevin Driscoll, 2014
"""

import colors
import fileinput
import pyinotify
import time

global nextcolor

class ProcessTransientFile(pyinotify.ProcessEvent):

    def __init__(self, n):
        global nextcolor
        self.fg = nextcolor
        self.lastupdate = time.time() 

    def process_IN_MODIFY(self, event):
        now = time.time()
        report = "{0}s".format(str(round(now-self.lastupdate, 2)))
        self.lastupdate = now
        print colors.color(' '.join((event.name, report)), fg=self.fg)

    def process_default(self, event):
        print 'default: ', event.maskname


if __name__=="__main__":

    wm = pyinotify.WatchManager()
    notifier = pyinotify.Notifier(wm, read_freq=60) 

    for n, fn in enumerate(fileinput.input()):
        nextcolor = (n % 6) + 1
        wm.watch_transient_file(fn, pyinotify.IN_MODIFY, ProcessTransientFile)

    notifier.loop()
