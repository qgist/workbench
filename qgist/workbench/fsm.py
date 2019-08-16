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
# IMPORT (External Dependencies)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from PyQt5.QtWidgets import (
    QMainWindow,
    )


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT (Internal)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from .dtype_workbench import dtype_workbench_class
from ..util import translate


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class fsm_class:

    def __init__(self, workbench_list, mainwindow, last_workbench = None):

        if not isinstance(workbench_list, list):
            raise TypeError('workbench_list must be a list')
        if any([not isinstance(item, dict) for item in workbench_list]):
            raise TypeError('items in workbench_list must be dicts')
        if not isinstance(mainwindow, QMainWindow):
            raise TypeError('mainwindow must be a QGis mainwindow')
        if not isinstance(last_workbench, str) and last_workbench is not None:
            raise TypeError('last_workbench must be a str or None')
        if last_workbench is not None and len(workbench_list) == 0:
            raise ValueError('last_workbench is not None while workbench_list is empty')
        if last_workbench is not None and last_workbench not in self._workbench_dict.keys():
            raise ValueError('last_workbench does not exist')

        self._workbench_dict = {item['name']: dtype_workbench_class(**item) for item in workbench_list}
        self._active_workbench = None

        self.keys = self._workbench_dict.keys

        if len(self) == 0:
            self.new_workbench(translate('global', 'user default'), mainwindow)
        elif last_workbench is not None:
            self.activate_workbench(last_workbench, mainwindow)
        else:
            self.activate_workbench(tuple(self._workbench_dict.keys())[0], mainwindow)

    def __len__(self):

        return len(self._workbench_dict)

    def as_list(self):

        return [item.as_dict() for item in self._workbench_dict.values()]

    def activate_workbench(self, name, mainwindow, force = False):

        if not isinstance(name, str):
            raise TypeError('name must be str')
        if not isinstance(mainwindow, QMainWindow):
            raise TypeError('mainwindow must be a QGis mainwindow')

        if name not in self._workbench_dict.keys():
            raise ValueError('name is not a known workbench')
        if self._active_workbench == name and not force:
            return

        self._workbench_dict[name].activate(mainwindow)
        self._active_workbench = name

    def new_workbench(self, name, mainwindow):

        if not isinstance(name, str):
            raise TypeError('name must be str')
        if not isinstance(mainwindow, QMainWindow):
            raise TypeError('mainwindow must be a QGis mainwindow')

        if name in self._workbench_dict.keys():
            raise ValueError('name is a known workbench, i.e. already exists')
        if len(name) == 0:
            raise ValueError('name is empty')

        self._workbench_dict[name] = dtype_workbench_class.from_mainwindow(name, mainwindow)
        self._active_workbench = name

    def delete_workbench(self, name, mainwindow):

        if not isinstance(name, str):
            raise TypeError('name must be str')
        if not isinstance(mainwindow, QMainWindow):
            raise TypeError('mainwindow must be a QGis mainwindow')

        if name not in self._workbench_dict.keys():
            raise ValueError('name is not a known workbench')
        if len(self) <= 1:
            raise ValueError('only one workbench left, can not be deleted')
        if name == self._active_workbench:
            other_name = tuple(self._workbench_dict.keys() - set((name,)))[0]
            self.activate_workbench(other_name, mainwindow)

        self._workbench_dict.pop(name)

    def rename_workbench(self, old_name, new_name, mainwindow):

        pass # TODO

    def save_workbench(self, name, mainwindow):

        if not isinstance(name, str):
            raise TypeError('name must be str')
        if not isinstance(mainwindow, QMainWindow):
            raise TypeError('mainwindow must be a QGis mainwindow')

        if self._active_workbench != name:
            raise ValueError('workbench must be active for being saved')

        self._workbench_dict[name].save(mainwindow)

    @property
    def active_workbench(self):

        return self._active_workbench

    @active_workbench.setter
    def active_workbench(self, value):

        raise AttributeError('active_workbench must not be changed')
