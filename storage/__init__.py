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

        self._roles = []
        self._data = {}

    def _merge(self, base, new):
        if base is None: return new
        if new is None: return base

        for key, value in new.iteritems():
            try:
                if key == 'states':
                    if value is None: continue
                    if key not in base: base[key] = []

                    # extend the existing list
                    # we do not use list.extend() because we want to support
                    # negating states with the '~' prefix, so:
                    for newstate in value:
                        if newstate[0] != '~':
                            # prevent duplicates:
                            if newstate not in base[key]:
                                base[key].append(newstate)
                        else:
                            try:
                                base[key].remove(newstate[1:])
                            except ValueError:
                                pass

                elif key == 'parameters' and key in base:
                    if value is None: continue

                    # parameters is a dictionary of dictionaries, keyed by class
                    # name (for parametrised states)
                    for klass, params in value.iteritems():
                        if klass in base[key]:
                            # the base dictionary already has a key for the
                            # given state, so we update:

                            # the problem is that list values should be
                            # extended, dictionary values updated, and only
                            # non-collection values overwritten:

                            for var, val in params.iteritems():
                                if var not in base[key][klass]:
                                    # no such variable exists yet, this is the
                                    # easy case:
                                    base[key][klass][var] = val
                                else:
                                    # now we use duck typing to try to extend
                                    # an existing list, update a dictionary,
                                    # or if both those fail, overwrite:
                                    try:
                                        val_tmp = val
                                        try:
                                            val.extend([]) #YUCK
                                        except AttributeError:
                                            # if the value isn't yet a list,
                                            # we must turn it into one for the
                                            # extend() call
                                            val_tmp = [val]
                                        base[key][klass][var].extend(val_tmp)

                                    except AttributeError:
                                        try:
                                            base[key][klass][var].update(val)
                                        except AttributeError:
                                            base[key][klass][var] = val
                        else:
                            # no existing key in base dictionary, so we can
                            # just set
                            base[key][klass] = params

                elif key == 'variables' and key in base:
                    # variables are a simple dictionary
                    base[key].update(value)

                else:
                    base[key] = value
            except TypeError, e:
                print >>sys.stderr, 'E: problem with key "%s" and value "%s": %s' %(key, value, e)
                sys.exit(posix.EX_CONFIG)

        return base

    def get_environment(self):
        return self._data.get('environment', DEFAULT_ENVIRONMENT)

    def get_states(self):
        return self._data.get('states', [])

    def get_parameters(self):
        ret = self._data.get('variables', {})
        ret.update(self._data.get('parameters', {}))
        return ret

    def get_roles(self):
        return self._roles

    def get_additional_data(self):
        return {}
