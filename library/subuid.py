#!/usr/bin/python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: utf-8 -*-

# Module to gather info about subuid and subgid assignments for
# a given user.

DOCUMENTATION = '''
---
module: subuid
author: Rafael Rivero
version_added: "2.0.0"
short_description: Manage users' subuids / subgids
requirements: [ usermod ]
description:
    - Manage subuids and subgids assigned to users
options:
    name:
        required: true
        description:
            - Name of the user to manage.
'''

EXAMPLES = '''
# Example subuid command from Ansible Playbooks
- subuid: name=someuser
'''

class Subuid(object):

    def __init__(self, module):
        self.module = module
        self.name  = module.params['name']
        # Removed: only gather facts.
        #self.state = module.params['state']
        #self.start = module.params['start']
        #self.range = module.params['range']
        #self.check = module.check_mode
        self.fail  = False
        # Gather facts
        self._gather()


    def _parse(self, filename):
        """Returns a triplet (username, subuid_start, subuid_range)"""
        prefix = "%s:" % self.name
        with open(filename, 'r') as subuid:
            for line in subuid.readlines():
                if line.startswith(prefix):
                    # Elimino el "\n" del fin de linea, y divido por los ':'
                    values = line.strip().split(":")
                    # Devuelvo los indices de primer uid y rango como enteros
                    return (int(values[1]), int(values[2]))
        return None

    def _gather(self):
        """Gather facts about current status of subuid / subgid
        
        self.subuid: current (start, range)
        self.subgid: current (start, range)
        self.changed: whether current params differ from module params
        """
        self.subuid  = self._parse('/etc/subuid')
        self.subgid  = self._parse('/etc/subgid')
        self.changed = False
        # Removed: only gather facts
        #if self.state=='present':
        #    if (
        #        not self.subuid or
        #        not self.subgid or
        #        self.subuid[0] != self.start or
        #        self.subuid[1] != self.range or
        #        self.subgid[0] != self.start or
        #        self.subgid[1] != self.range
        #    ):
        #        self.changed = True
        #elif self.subuid or self.subgid:
        #    self.changed = True

    def apply(self):
        """Concept for updating subuids"""

        # disabled
        return

        if (not self.changed) or self.module.check_mode:
            return

        # Add new subuids / subgids
        update = False
        if self.state == 'present':
            cmd = [self.module.get_bin_path('usermod', True)]
            cmd.append('-v')
            cmd.append("%s-%s" % (self.start, self.start + self.range))
            cmd.append('-w')
            cmd.append("%s-%s" % (self.start, self.start + self.range))
            self.rc, self.out, self.err = self.execute_command(cmd)
            if self.rc != 0:
                self.fail = True
            else:
                update = True

        # Remove previous subuids - subgids
        if not self.fail and (self.subuid or self.subgid):
            cmd = [self.module.get_bin_path('usermod', True)]
            if self.subuid:
                cmd.append('-V')
                cmd.append("%s-%s" % (
                    self.subuid[0], self.subuid[0] + self.subuid[1]))
            if self.suguid:
                cmd.append('-W')
                cmd.append("%s-%s" % (
                    self.subgid[0], self.subgid[0] + self.subgid[1]))
            self.rc, self.out, self.err = self.execute_command(cmd)
            if self.rc != 0:
                self.fail = True

        # Update subuid / subgid values, when applicable.
        if update:
            self.subuid = (self.start, self.range)
            self.subgid = (self.start, self.range)


def main():

    module = AnsibleModule(
        argument_spec = dict(
            name=dict(required=True, type='str')
            # Removed: gather facts only
            #start=dict(required=False, type='int', default=150000),
            #range=dict(required=False, type='int', default=65536),
            #state=dict(required=False,
            #    choices=['present', 'absent'], type='str', default='present')
        ),
        supports_check_mode=True
    )

    subuid = Subuid(module)
    result = dict()
    result['name']    = subuid.name
    # Removed: gather facts only
    #result['state']   = subuid.state
    result['changed'] = subuid.changed
    try:
        if not module.check_mode:
            # Do not apply - only gather facts
            # subuid.apply()
            # result['rc']  = subuid.rc
            # result['out'] = subuid.out
            # result['err'] = subuid.err
            pass
        s = subuid
        result['ansible_facts'] = {
            'user_subuid_start': (None if not s.subuid else s.subuid[0]),
            'user_subuid_range': (None if not s.subuid else s.subuid[1]),
            'user_subgid_start': (None if not s.subgid else s.subgid[0]),
            'user_subgid_range': (None if not s.subgid else s.subgid[1]),
        }
    except:
        result['rc'] = -1
        subuid.fail  = True
        subuid.err   = format_exc()

    if subuid.fail:
        module.fail_json(msg=subuid.err)
    else:
        module.exit_json(**result)


from ansible.module_utils.basic import *
main()
