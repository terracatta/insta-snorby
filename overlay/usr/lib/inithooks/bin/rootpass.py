#!/usr/bin/python
# Copyright (c) 2010 Alon Swartz <alon@turnkeylinux.org> - all rights reserved
"""Configure Root password

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
        opts, args = getopt.gnu_getopt(sys.argv[1:], "hp:", ['help', 'pass='])
    except getopt.GetoptError, e:
        usage(e)

    password = ""
    for opt, val in opts:
        if opt in ('-h', '--help'):
            usage()
        elif opt in ('-p', '--pass'):
            password = val

    if not password:
        d = Dialog('Insta-Snorby - First boot configuration')
        password = d.get_password("Root Password",
                                  "Please enter new password for the root account.")

    # ugly hack to support lenny
    import lsb_release
    codename = lsb_release.get_distro_information()['CODENAME']

    if codename == 'lenny':
        system('echo root:%s | chpasswd -m' % password)
    else:
        system('echo root:%s | chpasswd' % password)

if __name__ == "__main__":
    main()

