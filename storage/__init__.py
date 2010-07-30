#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# storage — base class for external node classification
#
# Copyright © 2010 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#
__name__ = 'storage'
__description__ = 'base class for external node classification'
__version__ = '2010.07.29.2255'
__author__ = 'martin f. krafft <madduck@madduck.net>'
__copyright__ = 'Copyright © 2010 ' + __author__
__licence__ = 'Artistic Licence 2.0'

DEFAULT_ENVIRONMENT = 'production'

import sys, posix

class ExternalNodeStorageBase(object):
    def __init__(self, node_uri, role_uri):
        if node_uri is None:
            print >>sys.stderr, 'E: node URI not defined.'
            sys.exit(posix.EX_USAGE)
        self._node_uri = node_uri

        if role_uri is None:
            print >>sys.stderr, 'E: role URI not defined.'
            sys.exit(posix.EX_USAGE)
        self._role_uri = role_uri

    def _merge(self, base, new):
        if base is None: return new
        if new is None: return base

        for key, value in new.iteritems():
            if key == 'classes' and key in base:
                # extend the existing list
                base[key].extend(value)
                # if base has no such key, we can just let the full list be
                # copied further down

            elif key == 'parameters' and key in base:
                # parameters is a dictionary of dictionaries, keyed by class
                # name (for parametrised classes)
                for klass, params in value.iteritems():
                    if klass in base[key]:
                        base[key][klass].update(params)
                    else:
                        base[key][klass] = params

            elif key == 'variables' and key in base:
                # variables are a simple dictionary
                base[key].update(value)

            else:
                base[key] = value

        return base

    def get_environment(self):
        return self._data.get('environment', DEFAULT_ENVIRONMENT)

    def get_classes(self):
        return self._data.get('classes', [])

    def get_parameters(self):
        ret = self._data.get('variables', {})
        for klass, params in self._data.get('parameters', {}).iteritems():
            ret.update([('%s_%s' % (klass.replace('::', '_'), var), val)
                        for var, val in params.iteritems()])
        return ret

    def get_additional_data(self):
        return {}
