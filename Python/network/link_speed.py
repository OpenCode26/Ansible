#!/usr/bin/python
import re
import subprocess
import json

link_stats = []
inface_list = []
a = subprocess.Popen(['sh', '/etc/ansible/facts.d/i22_duplex.fact'],
                     stdout=subprocess.PIPE)
out, err = a.communicate()
i22_duplex_inf = json.loads(out)
for k, v in i22_duplex_inf.items():
    if v == '0':
        inface = k.split('_')
        x = inface.pop()
        inface_list.append(x)

def link_args(inf):
    import re
    a = subprocess.Popen(['ethtool', inf], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    st = a.communicate()
    li = list(st)
    s = str(li[0])
    #net = re.split('\n|\t', s)
    return re.split('\n|\t', s)


def link_detect(net):
    for line in net:
        if 'Link detected: yes' in line:
            link_stats.append(line)
            return True

def speed(net):
    for line in net:
        if line.startswith("Speed"):
            a = line.lstrip('Speed: ')
            if int(a.rstrip('Mb/s')) < 1000:
                link_stats.append(line)
                return True


def dup(net):
    for line in net:
        if line.startswith("Duplex"):
            d = line.lstrip('Duplex: ')
            if d == "Half" or d == "Unknown":
                link_stats.append(line)
                return True

def main():
    for inf in inface_list:
        net = link_args(inf)
        if link_detect(net):
            speed(net)
            dup(net)
            print(link_stats)

if __name__ == '__main__':
    main()

