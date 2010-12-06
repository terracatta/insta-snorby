#!/usr/bin/python
# Copyright (c) 2010 Jason Meller <jason.meller@gmail.com> - all rights reserved
"""Configure MySQL Root password

Options:
    -p --pass=    if not provided, will ask interactively
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
        opts, args = getopt.gnu_getopt(sys.argv[1:], "hp:", ['help', 'password='])
    except getopt.GetoptError, e:
        usage(e)

    mysqlpassword = ""
    for opt, val in opts:
        if opt in ('-h', '--help'):
            usage()
        elif opt in ('-o', '--pass'):
            mysqlpassword = val

    if not mysqlpassword:
        d = Dialog('Insta-Snorby - First boot configuration')
	mysqlpassword = d.get_password("Enter MySQL Password","Please enter your desired MySQL password.")
 	
	system("mysqladmin -u root password %s" % mysqlpassword)
	system("sed -i 's/MYSQLPASS/%s/g' /var/www/snorby/config/database.yml" % mysqlpassword)
        system("sed -i 's/MYSQLPASS/%s/g' /etc/snort/barnyard2.conf" % mysqlpassword)

if __name__ == "__main__":
    main()

