# -*- coding: utf-8 -*-

"""

QGIST WORK BENCH
QGis Plugin for Organizing Toolbars
https://github.com/qgist/workbench

    qgist/workbench/fsm.py: finite state machine

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

import json
import os


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT (Internal)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from .dtype_uielement import dtype_uielement_class
from .dtype_workbench import dtype_workbench_class


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class fsm_class:

    def __init__(self, workbench_list):

        if not isinstance(workbench_list, list):
            raise TypeError('workbench_list must be a list')
        if any([not isinstance(item, dict) for item in workbench_list]):
            raise TypeError('items in workbench_list must be dicts')

        self._workbench_dict = {item['name']: dtype_workbench_class(**item) for item in workbench_list}

    def as_list(self):

        return [item.as_dict() for item in self._workbench_dict.values()]

    def activate_workbench(self, name):
        pass

    def new_workbench(self, name):
        pass

    def delete_workbench(self, name):
        pass

    def save_workbench(self, name):
        pass

    @staticmethod
    def from_config_file(fn):

        if not isinstance(fn, str):
            raise TypeError('fn must be str')
        if not os.path.exists(fn):
            raise ValueError('fn must exists')
        if not os.path.isfile(fn):
            raise ValueError('fn must be a file')

        with open(fn, 'r', encoding = 'utf-8') as f:
            cfg_data = json.loads(f.read())

        if not isinstance(cfg_data, dict):
            raise TypeError('configuration must be a dict')
        workbench_list = cfg_data.get('workbenchs', list())

        return fsm_class(workbench_list)
