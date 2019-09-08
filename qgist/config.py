# -*- coding: utf-8 -*-

"""

QGIST WORKBENCH
QGIS Plugin for Organizing Toolbars and Dockwidgets
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
# IMPORT (QGIS)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from qgis.core import QgsApplication


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT (Internal)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from .const import (
    QGIS_CONFIG_FLD,
    QGIST_CONFIG_FLD,
    )
from .error import (
    QgistConfigFormatError,
    QgistConfigKeyError,
    QgistTypeError,
    QgistValueError,
    )
from .util import translate


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def get_config_path():

    root_fld = QgsApplication.qgisSettingsDirPath()
    if os.path.exists(root_fld) and not os.path.isdir(root_fld):
        raise QgistValueError(translate('global', 'QGIS settings path does not point to a directory. (config path)'))
    if not os.path.exists(root_fld):
        raise QgistValueError(translate('global', 'QGIS settings path does not exist. (config path)')) # TODO create?

    root_qgis_fld = os.path.join(root_fld, QGIS_CONFIG_FLD)
    if os.path.exists(root_qgis_fld) and not os.path.isdir(root_qgis_fld):
        raise QgistValueError(translate('global', 'QGIS plugin configuration path exists but is not a directory. (config path)'))
    if not os.path.exists(root_qgis_fld):
        os.mkdir(root_qgis_fld)

    root_qgis_qgist_fld = os.path.join(root_qgis_fld, QGIST_CONFIG_FLD)
    if os.path.exists(root_qgis_qgist_fld) and not os.path.isdir(root_qgis_qgist_fld):
        raise QgistValueError(translate('global', 'QGIST configuration path exists but is not a directory. (config path)'))
    if not os.path.exists(root_qgis_qgist_fld):
        os.mkdir(root_qgis_qgist_fld)

    return root_qgis_qgist_fld


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class config_class:

    def __init__(self, fn):

        if not isinstance(fn, str):
            raise QgistTypeError(translate('global', '"fn" must be str. (config)'))

        self._fn = fn

        if not os.path.exists(fn):
            if not os.path.exists(os.path.dirname(fn)):
                raise QgistValueError(translate('global', 'Parent of "fn" must exists. (config)'))
            if not os.path.isdir(os.path.dirname(fn)):
                raise QgistValueError(translate('global', 'Parent of "fn" must be a directory. (config)'))
            self._data = {}
            self._save()
        else:
            if not os.path.isfile(fn):
                raise QgistValueError(translate('global', '"fn" must be a file. (config)'))
            with open(fn, 'r', encoding = 'utf-8') as f:
                data = f.read()
            try:
                self._data = json.loads(data)
            except:
                raise QgistConfigFormatError(translate('global', 'Config does not contain valid JSON. (config)'))
            if not isinstance(self._data, dict):
                raise QgistTypeError(translate('global', 'Configuration data must be a dict. (config)'))

    def __getitem__(self, name):

        if not isinstance(name, str):
            raise QgistTypeError(translate('global', '"name" must be str. (config getitem)'))
        if name not in self._data.keys():
            raise QgistConfigKeyError(translate('global', 'Unknown configuration field "name". (config getitem)'))

        return copy.deepcopy(self._data[name])

    def __setitem__(self, name, value):

        if not isinstance(name, str):
            raise QgistTypeError(translate('global', '"name" must be str. (config setitem)'))
        if not config_class._check_value(value):
            raise QgistTypeError(translate('global', '"value" contains not allowed types. (config setitem)'))

        self._data[name] = value
        self._save()

    def get(self, name, default):

        try:
            return self[name]
        except QgistConfigKeyError:
            return default

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

        backup_fn = None
        if os.path.exists(self._fn):
            backup_fn = self._fn + '.backup'
            max_attempts = 100
            attempt = 0
            attempt_ok = False
            while attempt < max_attempts:
                backup_fn_numbered = '{NAME:s}{NUMBER:02d}'.format(NAME = backup_fn, NUMBER = attempt)
                if not os.path.exists(backup_fn_numbered):
                    attempt_ok = True
                    backup_fn = backup_fn_numbered
                    break
                attempt += 1
            if not attempt_ok:
                raise QgistValueError(translate('global', 'Could not backup old configuration before saving new - too many old backups. (config save)'))
            os.rename(self._fn, backup_fn)

        with open(self._fn, 'w', encoding = 'utf-8') as f:
            f.write(json.dumps(self._data, indent = 4, sort_keys = True))

        if backup_fn is not None:
            os.unlink(backup_fn)

    @staticmethod
    def import_config(fn):

        if not isinstance(fn, str):
            raise QgistTypeError(translate('global', '"fn" must be str. (config import)'))
        if not os.path.exists(fn):
            raise QgistValueError(translate('global', '"fn" must exists. (config import)'))
        if not os.path.isfile(fn):
            raise QgistValueError(translate('global', '"fn" must be a file. (config import)'))

        with open(fn, 'r', encoding = 'utf-8') as f:
            raw = f.read()

        try:
            value = json.loads(raw)
        except:
            raise QgistConfigFormatError(translate('global', '"fn" does not contain valid JSON. (config import)'))

        return value

    @staticmethod
    def export_config(fn, value):

        if not isinstance(fn, str):
            raise QgistTypeError(translate('global', '"fn" must be str. (config export)'))
        if not os.path.exists(os.path.dirname(fn)):
            raise QgistValueError(translate('global', 'Parent of "fn" must exists. (config export)'))
        if not os.path.isdir(os.path.dirname(fn)):
            raise QgistValueError(translate('global', 'Parent of "fn" must be a directory. (config export)'))
        if not config_class._check_value(value):
            raise QgistTypeError(translate('global', '"value" contains not allowed types. (config export)'))

        with open(fn, 'w', encoding = 'utf-8') as f:
            f.write(json.dumps(value, indent = 4, sort_keys = True))
