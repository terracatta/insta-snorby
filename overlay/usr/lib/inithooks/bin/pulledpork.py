#!/usr/bin/python
# Copyright (c) 2010 Jason Meller <jason.meller@gmail.com> - all rights reserved
"""Configure and Install and Run Pulled Pork

TODO Options:
	
	
"""

import sys
import getopt

import socket
import fcntl
import struct

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

from executil import system
from dialog_wrapper import Dialog

def usage(s=None):
    if s:
        print >> sys.stderr, "Error:", s
    print >> sys.stderr, "Syntax: %s [options]" % sys.argv[0]
    print >> sys.stderr, __doc__
    sys.exit(1)

def main():
    response = ""
    if not response:
        d = Dialog('Insta-Snorby - First boot configuration')
	response = d.yesno("Automatically Update Rules Everyday?","Snorby can update the configured ruleset on a daily basis. Snorby supports this through intergration with Pulled Pork, a simple popular Snort rule update script\n\nEnable Pulled Pork?")

	if response:
		d.infobox('Configuring Pulled Pork to run everyday at 2:00AM local time')
		system("crontab -l > /root/crontmp")
		system("echo '0 2 * * * /root/pulledpork-0.6.1/pulledpork.pl -c /root/pulledpork-0.6.1/etc/pulledpork.conf -H -v >> /var/log/pulledpork 2>&1 #Update Snort Rules' >> /root/crontmp")
		system("crontab /root/crontmp")

		d.infobox('Running Pulled Pork now! Logs are stored at /var/log/pulledpork')
		system("/root/pulledpork-0.6.1/pulledpork.pl -c /root/pulledpork-0.6.1/etc/pulledpork.conf -H -v >> /var/log/pulledpork 2>&1")

if __name__ == "__main__":
    main()

