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

from storage import ExternalNodeStorageBase
class ExternalNodeStorage(ExternalNodeStorageBase):
    def __init__(self, uri, node):
        pass

    def get_environment(self):
        return 'production'

    def get_classes(self):
        return ['cron','motd','apt','ssh::server','ssh::client']

    def get_parameters(self):
        return {
            'debian_suite': 'sid',
            'include_debian_sources': True
        }

    def get_additional_data(self):
        return {}
