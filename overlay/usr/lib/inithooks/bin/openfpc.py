#!/usr/bin/python
# Copyright (c) 2010 Jason Meller <jason.meller@gmail.com> - all rights reserved
"""Configure and Install OpenFPC & Download/Install VRT rules 

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
    fpcuser = ""
    fpcpassword = ""
    if not fpcpassword and not fpcuser:
        d = Dialog('Insta-Snorby - First boot configuration')
	response = d.yesno("Enable OpenFPC?","Snorby supports intergration with OpenFPC, a lightweight full-packet network traffic recorder & buffering system.\nInsta-Snorby can install and configure OpenFPC so that full pcaps of alerts will be made available inside the Snorby application.\n\n Would you like to enable OpenFPC?")

	if response:
		fpcuser = d.inputbox("Create OpenFPC Username","Please enter your desired OpenFPC username.")
		fpcpassword = d.get_password("Create OpenFPC password", "Please enter your desired OpenFPC password.")
 	

    if fpcuser and fpcpassword:
	ipaddress = get_ip_address('eth0')
	d.infobox('Installing OpenFPC 0.6-314')
	system('htpasswd -b -c /etc/openfpc/apache2.passwd %s %s > /dev/null' % (fpcuser[1], fpcpassword) )
	system('cd /root/openfpc-0.6-314/ &&  /root/openfpc-0.6-314/openfpc-install.sh install > /dev/null')
	system("sed -i 's/GUIUSER=openfpc/#GUIUSER=openfpc/g' /etc/openfpc/openfpc-default.conf")
	system("sed -i 's/GUIPASS=openfpc/#GUIUSER=openfpc/g' /etc/openfpc/openfpc-default.conf")
	system("sed -i 's/USER=openfpc=openfpc/USER=%s=%s/g' /etc/openfpc/openfpc-default.conf" % (fpcuser[1], fpcpassword))
	system("sed -i 's/AuthType Basic/#AuthType Basic/g' /etc/apache2/sites-enabled/openfpc.apache2.site")
	system("sed -i 's/AuthName/#AuthName/g' /etc/apache2/sites-enabled/openfpc.apache2.site")
	system("sed -i 's/AuthUserFile/#AuthUserFile/g' /etc/apache2/sites-enabled/openfpc.apache2.site")
	system("sed -i 's/Require valid-user/#Require valid-user/g' /etc/apache2/sites-enabled/openfpc.apache2.site")
	d.infobox('Starting OpenFPC 0.6-314')
	system("openfpc -action start > /dev/null")
	d.infobox('Configuring Snorby...')
	system("cd /var/www/snorby && /usr/local/bin/rails runner 'Setting.set(:packet_capture, 1)' > /dev/null 2>&1")
	system("cd /var/www/snorby && /usr/local/bin/rails runner \"Setting.set(:packet_capture_url, 'https://%s/openfpc/cgi-bin/extract.cgi')\" > /dev/null 2>&1" % ipaddress)
	system("cd /var/www/snorby && /usr/local/bin/rails runner \"Setting.set(:packet_capture_type, 'openfpc')\" > /dev/null 2>&1")
        system("cd /var/www/snorby && /usr/local/bin/rails runner 'Setting.set(:packet_capture_auto_auth, 1)' > /dev/null 2>&1")
	system("cd /var/www/snorby && /usr/local/bin/rails runner \"Setting.set(:packet_capture_user, '%s')\" > /dev/null 2>&1" % fpcuser[1])
	system("cd /var/www/snorby && /usr/local/bin/rails runner \"Setting.set(:packet_capture_password, '%s')\" > /dev/null 2>&1" % fpcpassword)

if __name__ == "__main__":
    main()

