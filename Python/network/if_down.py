#!/usr/bin/env python3
import json
import os
import subprocess


onboot = ['onboot=no', 'onboot="no"', "onboot='no'"]
inface_list = []

with open('duplex.json') as f:
    i22_duplex_inf = json.load(f)
    for k, v in i22_duplex_inf.items():
        if v == '0':
            inface = k.split('_')
            x = 'ifcfg-' + inface.pop()
            inface_list.append(x)

def check_onboot():
    print('Checking interface onboot status')
    for inf in inface_list:
        inface_config = os.path.join('/etc/sysconfig/network-scripts/', inf)
    with open(inface_config, 'r') as f:
        for lines in f:
            for match in onboot:
                if match in lines.lower():
                    return match, True

def network_manager():
    if check_onboot():
        for inf in inface_list:
            print('Checking Network Manager status...')
            nmcli_status = subprocess.run(['nmcli', 'device', 'status'], stdout=subprocess.PIPE)
            if nmcli_status.returncode == 0:
               print('NetworkManager is running')
               print('->->->Stoping Network Manager')
               nm_stop = subprocess.run(['systemctl', 'stop', 'NetworkManager'], stdout=subprocess.PIPE)
               down = subprocess.run(['ifdown', inf], stdout=subprocess.PIPE)
            elif nmcli_status.returncode != 0:
               print(nmcli_status.stdout)
               print('Disabling network interface')
               down = subprocess.run(['ifdown', inf], stdout=subprocess.PIPE)
               print(down.stdout)

if __name__ == '__main__':
    network_manager()

