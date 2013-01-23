#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# yaml_fs — class implementing filesystem-based YAML node classification
#
# Copyright © 2010 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#
__name__ = 'yaml_fs'
__description__ = 'class implementing filesystem-based YAML node classification'
__version__ = '2010.07.29.2255'
__author__ = 'martin f. krafft <madduck@madduck.net>'
__copyright__ = 'Copyright © 2010 ' + __author__
__licence__ = 'Artistic Licence 2.0'

import os, sys, posix

try:
    from yaml import load
except ImportError:
    print >>sys.stderr, 'E: python-yaml module not found.'
    sys.exit(posix.EX_OSERR)

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from storage import ExternalNodeStorageBase
class ExternalNodeStorage(ExternalNodeStorageBase):

    def load_node(self, node):
        node_filename = os.path.join(self._node_uri, node)
        self._data.update(self._load_yaml_file(node_filename))

    def _load_yaml_file(self, filename):
        filename += '.yaml'
        try:
            f = open(filename, 'r')
        except IOError, e:
            print >>sys.stderr, 'E: no such file: %s' % filename
            sys.exit(posix.EX_OSFILE)

        ret = {}

        data = load(f, Loader=Loader)

        roles = data.pop('roles', [])
        for role in roles:
            if role in self._roles: continue
            role_filename = os.path.join(self._role_uri, role)
            d = self._load_yaml_file(role_filename)
            ret = self._merge(ret, d)
            self._roles.append(role)

        # the node data override/extend everything last
        return self._merge(ret, data)
