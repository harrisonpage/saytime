#!/usr/bin/env python
#
# Simple countdown timer for OS X. 
# Smooshed together using borrowed code snippits from here, there. 
#
# Usage: python saytime.py every 30s for 30m
#
# Harrison Page <harrisonpage@gmail.com>
# https://github.com/harrisonpage/saytime
# 13-Oct-2014
# 

import sys
import re
from datetime import timedelta
import time
import threading
from os import system

"""
https://mail.python.org/pipermail/python-list/2009-October/556280.html
"""
class Timer(threading.Thread):
    def __init__(self, delay, stop_time):
        threading.Thread.__init__(self)
        self.regex = re.compile(r'((?P<hours>\d+?)h)?((?P<minutes>\d+?)m)?((?P<seconds>\d+?)s)?')
        self.event = threading.Event()
        self.delay = self.parse_time(delay).total_seconds()
        self.stop_time = time.time() + self.parse_time(stop_time).total_seconds()

    """
    http://stackoverflow.com/a/4628148
    """
    def parse_time(self,time_str):
        parts = self.regex.match(time_str)
        if not parts:
            return
        parts = parts.groupdict()
        time_params = {}
        for (name, param) in parts.iteritems():
            if param:
                time_params[name] = int(param)
        return timedelta(**time_params)

    def run(self):
        while not self.event.is_set():
            now = time.strftime("%I:%M", time.localtime()).lstrip('0')
            print(now)
            system('say ' + now)
            now = time.time()
            if now >= self.stop_time:
                self.stop()
            else:
                self.event.wait(self.delay)

    def stop(self):
        self.event.set()

def usage(prog):
    print("Usage: {prog} every [interval] for [internal]".format(prog=prog))
    sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) != 5 or sys.argv[1] != 'every' or sys.argv[3] != 'for' or sys.platform != 'darwin':
        usage(sys.argv[0])
    timer = Timer(sys.argv[2], sys.argv[4])
    timer.start()
