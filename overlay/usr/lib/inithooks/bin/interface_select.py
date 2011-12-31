#!/usr/bin/python
# Copyright (c) 2010 Jason Meller <jason.meller@gmail.com> - all rights reserved
"""Configure which interface you want snort to listen to 

TODO Options:
	
	
"""
import array
import sys
import getopt
import socket
import fcntl
import struct
import dialog
from executil import system

SIOCGIFCONF = 0x8912  #define SIOCGIFCONF
BYTES = 4096          # Simply define the byte size


def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

# get_iface_list function definition 
# this function will return array of all 'up' interfaces 
def get_iface_list():
    # create the socket object to get the interface list
    sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # prepare the struct variable
    names = array.array('B', '\0' * BYTES)

    # the trick is to get the list from ioctl
    bytelen = struct.unpack('iL', fcntl.ioctl(sck.fileno(), SIOCGIFCONF, struct.pack('iL', BYTES, names.buffer_info()[0])))[0]

    # convert it to string
    namestr = names.tostring()

    # return the interfaces as array
    return [namestr[i:i+32].split('\0', 1)[0] for i in range(0, bytelen, 32)]

# now, use the function to get the 'up' interfaces array
ifaces = get_iface_list()

# well, what to do? print it out maybe... 

def iface_list():
     list = []
     for iface in ifaces:
         list.append((iface, get_ip_address(iface)))
     return list

def interface_menu(d, text, interfaces):
    while 1:
        (code, tag) = d.menu(
            text,
            width=60,
            choices=interfaces)
        if handle_exit_code(d, code):
            break
    return tag

def usage(s=None):
    if s:
        print >> sys.stderr, "Error:", s
    print >> sys.stderr, "Syntax: %s [options]" % sys.argv[0]
    print >> sys.stderr, __doc__
    sys.exit(1)

def main():
    interface = ""
    if not interface:
 	d = dialog.Dialog(dialog="dialog")
    	d.add_persistent_args(["--backtitle", "Insta-Snorby - First boot configuration"])
	interface = interface_menu(d,"Please select an interface to monitor", iface_list())
	system("echo " + interface)
	system("sed -i 's/eth0/%s/g' /etc/snort/barnyard2.conf" % interface)
	system("sed -i 's/eth0/%s/g' /usr/lib/inithooks/everyboot.d/88snortstart" % interface)
	system("sed -i 's/eth0/%s/g' /root/pulledpork-0.6.1/etc/pulledpork.conf" % interface)
	system("sed -i 's/eth0/%s/g' /root/openfpc-0.6-314/etc/openfpc-default.conf" % interface)



def handle_exit_code(d, code):
    # d is supposed to be a Dialog instance
    if code in (d.DIALOG_CANCEL, d.DIALOG_ESC):
        if code == d.DIALOG_CANCEL:
            msg = "Do you really want to quit?"
        else:
            msg = "You pressed ESC in the last dialog box. Do really want to quit?"
        # "No" or "ESC" will bring the user back to the demo.
        # DIALOG_ERROR is propagated as an exception and caught in main().
        # So we only need to handle OK here.
        if d.yesno(msg) == d.DIALOG_OK:
            sys.exit(0)
        return 0
    else:
        return 1                        # code is d.DIALOG_OK
        

if __name__ == "__main__":
    main()

