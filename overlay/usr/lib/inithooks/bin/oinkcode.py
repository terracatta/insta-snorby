#!/usr/bin/python
# Copyright (c) 2010 Jason Meller <jason.meller@gmail.com> - all rights reserved
"""Configure Oinkcode & Download/Install VRT rules 

Options:
    -o --oink=    if not provided, will ask interactively
"""

import sys
import getopt

from executil import system
from dialog_wrapper import Dialog

def usage(s=None):
    if s:
        print >> sys.stderr, "Error:", s
    print >> sys.stderr, "Syntax: %s [options]" % sys.argv[0]
    print >> sys.stderr, __doc__
    sys.exit(1)

def main():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "hp:", ['help', 'oink='])
    except getopt.GetoptError, e:
        usage(e)

    oinkcode = ""
    for opt, val in opts:
        if opt in ('-h', '--help'):
            usage()
        elif opt in ('-o', '--oink'):
            oinkcode = val

    if not oinkcode:
        d = Dialog('Insta-Snorby - First boot configuration')
	response = d.yesno("Enter Oinkcode?","Snorby can automatically download and install Sourcefire's VRT rules. In order to do this, you need obtain and enter your Oinkcode from snort.org. \n\nWould you like to enter your oink code?")

	if response:
		oinkcode = d.inputbox("Enter Oinkcode","Please enter your 40 character Oinkcode")
 	

    if oinkcode:
        
	system('echo %s > /root/oinkcode' % oinkcode[1])
	d.infobox('VRT rules are downloading...')
	try:
		 system('wget http://www.snort.org/reg-rules/snortrules-snapshot-edge.tar.gz/%s -o /dev/null -O /root/snortrules.tar.gz' % oinkcode[1])
	except:
		d.error("Could not download VRT rules.")
	
	d.infobox('Download complete! VRT rules are extracting...')
	system('tar zxf /root/snortrules.tar.gz -C /root/')
	system('cp /root/rules/* /etc/snort/rules/')
	system('cp -f /root/snortvrt.conf /etc/snort/snort.conf')
	system('cat /root/etc/sid-msg.map >> /etc/snort/sid-msg.map')
	system("sed -i 's/<oinkcode>/%s/g' /root/vrtpulledpork.conf" % oinkcode[1])
	system("cp /root/vrtpulledpork.conf /root/pulledpork-0.6.1/etc/pulledpork.conf")

if __name__ == "__main__":
    main()

