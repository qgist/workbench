# -*- coding: utf-8 -*-

"""

QGIST WORK BENCH
QGis Plugin for Organizing Toolbars
https://github.com/qgist/workbench

    qgist/config.py: QGIST config class

    Copyright (C) 2017-2019 QGIST project <info@qgist.org>

<LICENSE_BLOCK>
The contents of this file are subject to the GNU General Public License
Version 2 ("GPL" or "License"). You may not use this file except in
compliance with the License. You may obtain a copy of the License at
https://www.gnu.org/licenses/old-licenses/gpl-2.0.txt
https://github.com/qgist/workbench/blob/master/LICENSE

Software distributed under the License is distributed on an "AS IS" basis,
WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License for the
specific language governing rights and limitations under the License.
</LICENSE_BLOCK>

"""

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT (Python Standard Library)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import copy
import json
import os


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class config_class:

    def __init__(self, fn):

        if not isinstance(fn, str):
            raise TypeError('fn must be str')

        self._fn = fn

        if not os.path.exists(fn):
            if not os.path.exists(os.path.dirname(fn)):
                raise ValueError('parent of fn must exists')
            if not os.path.isdir(os.path.dirname(fn)):
                raise ValueError('parent of fn must be a directory')
            self._data = {}
            self._save()
        else:
            if not os.path.isfile(fn):
                raise ValueError('fn must be a file')
            with open(fn, 'r', encoding = 'utf-8') as f:
                self._data = json.loads(f.read())
            if not isinstance(self._data, dict):
                raise TypeError('configuration data must be a dict')

    def __getitem__(self, name):

        if not isinstance(name, str):
            raise TypeError('name must be str')
        if name not in self._data.keys():
            raise ValueError('unknown name')

        return copy.deepcopy(self._data[name])

    def __setitem__(self, name, value):

        if not isinstance(name, str):
            raise TypeError('name must be str')
        if not config_class._check_value(value):
            raise TypeError('value contains not allowed types')

        self._data[name] = value
        self._save()

    @staticmethod
    def _check_value(value):

        if type(value) not in (int, float, bool, str, list, dict) and value is not None:
            return False

        if isinstance(value, list):
            for item in value:
                if not config_class._check_value(item):
                    return False

        if isinstance(value, dict):
            for k, v in value.items():
                if not config_class._check_value(k) or not config_class._check_value(v):
                    return False

        return True

    def _save(self):

        with open(self._fn, 'w', encoding = 'utf-8') as f:
            f.write(json.dumps(self._data, indent = 4, sort_keys = True))
