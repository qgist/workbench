# -*- coding: utf-8 -*-

"""

QGIST WORK BENCH
QGis Plugin for Organizing Toolbars
https://github.com/qgist/workbench

    qgist/workbench/dtype_fsm.py: finite state machine

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
from ..config import config_class


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class dtype_fsm_class:

    def __init__(self, workbench_list, mainwindow, active_workbench = None, config = None):

        if not isinstance(workbench_list, list):
            raise TypeError('workbench_list must be a list')
        if any([not isinstance(item, dict) for item in workbench_list]):
            raise TypeError('items in workbench_list must be dicts')
        if not isinstance(mainwindow, QMainWindow):
            raise TypeError('mainwindow must be a QGis mainwindow')
        if not isinstance(active_workbench, str) and active_workbench is not None:
            raise TypeError('active_workbench must be a str or None')
        if active_workbench is not None and len(workbench_list) == 0:
            raise ValueError('active_workbench is not None while workbench_list is empty')
        if not isinstance(config, config_class) and config is not None:
            raise TypeError('config must be a config_class object or None')

        self._config = config

        self._workbench_dict = {
            item['name']: dtype_workbench_class(mainwindow = mainwindow, **item)
            for item in workbench_list
            }
        if active_workbench is not None and active_workbench not in self._workbench_dict.keys():
            raise ValueError('active_workbench does not exist')

        self._active_workbench = None

        self.keys = self._workbench_dict.keys

        if len(self) == 0:
            self.new_workbench(translate('global', 'user default'), mainwindow)
        elif active_workbench is not None:
            self.activate_workbench(active_workbench, mainwindow)
        else:
            self.activate_workbench(tuple(self._workbench_dict.keys())[0], mainwindow)

    def __getitem__(self, name):

        if not isinstance(name, str):
            raise TypeError('name must be str')
        if name not in self._workbench_dict.keys():
            raise ValueError('name is not a known workbench')

        return self._workbench_dict[name]

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

        self._update_config()

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

        self._update_config()

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

        self._update_config()

    def rename_workbench(self, old_name, new_name, mainwindow):

        if not isinstance(old_name, str):
            raise TypeError('old_name must be str')
        if not isinstance(new_name, str):
            raise TypeError('new_name must be str')
        if not isinstance(mainwindow, QMainWindow):
            raise TypeError('mainwindow must be a QGis mainwindow')
        if old_name not in self._workbench_dict.keys():
            raise ValueError('old_name is not a known workbench')
        if new_name in self._workbench_dict.keys():
            raise ValueError('new_name is a known workbench, i.e. already exists')
        if len(new_name) == 0:
            raise ValueError('new_name is empty')
        if old_name == new_name:
            return

        self._workbench_dict[new_name] = self._workbench_dict.pop(old_name)
        self._workbench_dict[new_name].name = new_name

        if self._active_workbench == old_name:
            self._active_workbench = new_name

        self._update_config()

    def save_workbench(self, name, mainwindow):

        if not isinstance(name, str):
            raise TypeError('name must be str')
        if not isinstance(mainwindow, QMainWindow):
            raise TypeError('mainwindow must be a QGis mainwindow')

        if self._active_workbench != name:
            raise ValueError('workbench must be active for being saved')

        self._workbench_dict[name].save(mainwindow)

        self._update_config()

    def _update_config(self):

        if self._config is None:
            return

        self._config['workbench_list'] = self.as_list()
        self._config['active_workbench'] = self._active_workbench

    @property
    def active_workbench(self):

        return self._active_workbench

    @active_workbench.setter
    def active_workbench(self, value):

        raise AttributeError('active_workbench must not be changed')
