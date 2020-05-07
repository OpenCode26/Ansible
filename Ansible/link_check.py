#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: link_check

short_description: This module will check ethernet device status

version_added: "1.0"

description:
    - "link_check module will will help to identify network link status, speed and duplex"

options:
    device:
        description:
            - This this should be ethernet device like eth0, eth1 etc.
        required: true
    speed:
        description:
            - To list the network devices under specified network speed. ex 100, 1000 etc.
        required: false
        default: 1000

author:
    - Ravi Jeyachandran (ravi.jravichandran@gmail.com)
'''

EXAMPLES = '''
# Check link status, speed and duplex
- name: check link status of eth0
  link_check:
    device: "eth0"

# Check link status and display link speed below 1000MBs 
- name: Test with a message and changed output
  my_test:
    device: "eth0"
    speed: 1000
'''

import re
from ansible.module_utils.basic import AnsibleModule


def run_module():
    module_args = dict(
        device=dict(type='str', required=True),
        speed=dict(type='int', required=False, default=1000)
    )
    result = dict(
        changed=False,
        original_message='',
        message=''
    )
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    etool = module.get_bin_path('ethtool', required=True)
    args = [etool, module.params['device']]
    rc, stdout, stderr = module.run_command(args)
    net = re.split('\n|\t', stdout)
    link_stats = []
    if module.check_mode:
        module.exit_json(**result)

    result['original_message'] = "Status for " +  module.params['device']

    if rc == 75:
        result['message'] = 'No Device Found'
        module.fail_json(msg='Please check network device', **result)

    if module.params['device']:
        for line in net:
            if 'Link detected: yes' in line:
                link_stats.append(line)
            if line.startswith("Speed"):
                a = line.lstrip('Speed: ')
                if int(a.rstrip('Mb/s')) < module.params['device']:
                    link_stats.append(line)
            if line.startswith("Duplex"):
                d = line.lstrip('Duplex: ')
                if d == "Half" or d == "Unknown":
                    link_stats.append(line)                   
 
    result['changed'] = False
    result['message'] = link_stats 

    if module.params['device'] == 'fail_me':
        module.fail_json(msg='Your, requested this to fail', **result)

    module.exit_json(**result)


def main():
    run_module()

if __name__ == '__main__':
    main()
