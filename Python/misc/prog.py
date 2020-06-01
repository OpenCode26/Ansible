import sys
import argparse
import subprocess
from getpass import getpass


class Password:

    DEFAULT = 'Prompt if not specified'

    def __init__(self, value):
        if value == self.DEFAULT:
            value = getpass('NTID Password: ')
        self.value = value

    def __str__(self):
        return self.value

parser = argparse.ArgumentParser(description="Updating Decommission ticket with server status", prog='DECOMM', usage='%(prog)s [options]') 
parser.add_argument('-t', '--ticket', type=str, help='Decommision ticket', metavar='INFR-123', required=True)
parser.add_argument('-V', '--version', action='version', version='%(prog)s 1.0')
parser.add_argument('-u', '--username', help='Username for jira')
parser.add_argument('-p', '--password', type=Password, default=Password.DEFAULT, help='Password for user')
parser.add_argument('-o', '--option', help='Select application', default='1')
args = parser.parse_args()

if args.ticket:
    proc = subprocess.Popen(["bash", "sc.sh"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    proc.stdin.write('{}\n'.format(args.ticket).encode('utf-8'))
    proc.stdin.write('{}\n'.format(args.username).encode('utf-8'))
    proc.stdin.write('{}\n'.format(args.password).encode('utf-8'))
    proc.stdin.write('{}\n'.format(args.option).encode('utf-8'))
    out, err = proc.communicate()
    proc.stdin.close()
    print(out.decode('utf-8')) 

