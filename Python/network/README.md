This is if_down.py script will be used to down the network interface which is set onboot=yes on network config
and network interface is down or not connetced.

1. shell script will generate the output in json format and the same output is captured in duplex.json file.
2. This script will read that output and disable the network interface based the condition.
3. python script if_down.py will be executed on list of machines using ansible playbook or use shell for loop command  

