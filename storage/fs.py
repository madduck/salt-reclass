#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# fs.py — class implementing filesystem-based node classification
#
# Copyright © 2010 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#
__name__ = 'fs.py'
__description__ = 'class implementing filesystem-based node classification'
__version__ = '2010.07.29.2255'
__author__ = 'martin f. krafft <madduck@madduck.net>'
__copyright__ = 'Copyright © 2010 ' + __author__
__licence__ = 'Artistic Licence 2.0'

DEFAULT_ENVIRONMENT = 'production'

import os, sys, posix

from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

class ExternalNodeStorage(object):
    def __init__(self, node_uri, role_uri):
        if node_uri is None:
            print >>sys.stderr, 'E: node URI not defined.'
            sys.exit(posix.EX_USAGE)
        self._node_uri = node_uri

        if role_uri is None:
            print >>sys.stderr, 'E: role URI not defined.'
            sys.exit(posix.EX_USAGE)
        self._role_uri = role_uri

    def load_node(self, node):
        node_filename = os.path.join(self._node_uri, node)
        self._data = self._load_yaml_file(node_filename)

    def _load_yaml_file(self, filename):
        try:
            f = open(filename, 'r')
        except IOError, e:
            print >>sys.stderr, 'E: no such file: %s' % filename
            sys.exit(posix.EX_OSFILE)

        ret = {}

        data = load(f, Loader=Loader)

        roles = data.pop('roles', [])
        for role in roles:
            role_filename = os.path.join(self._role_uri, role)
            d = self._load_yaml_file(role_filename)
            ret = self._merge(ret, d)

        # the node data override/extend everything last
        return self._merge(ret, data)

    def _merge(self, base, new):
        for kvpair in new.iteritems():
            if kvpair[0] == 'classes' and base.has_key('classes'):
                base['classes'].extend(kvpair[1])
            elif kvpair[0] == 'parameters' and base.has_key('parameters'):
                base['parameters'].update(kvpair[1])
            else:
                base[kvpair[0]] = kvpair[1]

        return base

    def get_environment(self):
        return self._data.get('environment', DEFAULT_ENVIRONMENT)

    def get_classes(self):
        return self._data.get('classes', [])

    def get_parameters(self):
        return self._data.get('parameters', {})

    def get_additional_data(self):
        return {}
