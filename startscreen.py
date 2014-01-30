__author__ = 'joel'

# Example:
# python startscreen.py -sSERVER -uUSERNAME -wPASSWORD -pPORT

import os
from rutorrent.rutorrent import ruTorrent
from tracker.tracker import Tracker
from optparse import OptionParser
from files.files import find_all_files
from files.finder import FileFinder
from time import sleep
import shutil
from datetime import datetime
import paramiko

import settings


parser = OptionParser()

parser.add_option('-s', '--host', dest='host', default=None)
parser.add_option('-u', '--username', dest='username', default=None)
parser.add_option('-w', '--password', dest='password', default=None)
parser.add_option('-p', '--port', dest='port', default=None)
parser.add_option('-c', '--command', dest='command', default=None)

(options, args) = parser.parse_args()


client = paramiko.SSHClient()
client.load_system_host_keys()
client.set_missing_host_key_policy(paramiko.WarningPolicy())
print '*** Connecting...', options.host, options.port, options.username, options.password
client.connect(options.host, int(options.port), options.username, options.password)

client.exec_command('screen -wipe')

stdin, stdout, strerr = client.exec_command('screen -ls | grep "rfinder"')
screen_existed = False
for l in stdout:
    print l
    screen_existed = True

if(screen_existed == False):
    print 'No screen exists. lets role one!'
    cmd = "screen -S rfinder -d -m {command}".format(
        command = options.command or "~/scripts/rfinder/seedboxco_watcher.sh"
    )
    print "** Executing command: ", cmd
    client.exec_command(cmd)
else:
    print 'Screen existed, do nothing.'

client.close()
