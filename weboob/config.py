# -*- coding: utf-8 -*-

"""
Copyright(C) 2010  Romain Bignon

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, version 3 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

"""

from __future__ import with_statement

import yaml

class ConfigError(Exception): pass

class Config:
    def __init__(self, path):
        self.path = path
        self.values = {}

    def load(self):
        with open(self.path, 'r') as f:
            self.values = yaml.load(f)

    def get(self, *args, **kwargs):
        create = False
        if 'create' in kwargs:
            create = kwargs['create']

        v = self.values
        for a in args:
            try:
                v = v[a]
            except KeyError:
                if create:
                    v = v[a] = {}
                else:
                    raise ConfigError()
            except TypeError:
                raise ConfigError()

        return v

    def set(self, *args):
        v = self.values
        for a in args[:-2]:
            try:
                v = v[a]
            except KeyError:
                v = v[a] = {}
            except TypeError:
                raise ConfigError()

        v[args[-2]] = args[-1]

    def save(self):
        with open(self.path, 'w') as f:
            yaml.dump(self.values, f)
