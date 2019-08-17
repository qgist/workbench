# -*- coding: utf-8 -*-

"""

QGIST WORK BENCH
QGis Plugin for Organizing Toolbars
https://github.com/qgist/workbench

    qgist/workbench/ui_manager.py: workbench manager ui class

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

import os


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT (External Dependencies)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from PyQt5.QtWidgets import (
    QComboBox,
    QInputDialog,
    QMainWindow,
    )

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT (Internal)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from .dtype_fsm import dtype_fsm_class
from .ui_manager_base import ui_manager_base_class
from ..util import translate


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class ui_manager_class(ui_manager_base_class):

    def __init__(self, plugin_root_fld, mainwindow, combobox_workbench, combobox_workbench_update, fsm):

        if not isinstance(plugin_root_fld, str):
            raise TypeError('plugin_root_fld must be str')
        if not os.path.exists(plugin_root_fld):
            raise ValueError('plugin_root_fld must exists')
        if not os.path.isdir(plugin_root_fld):
            raise ValueError('plugin_root_fld must be a directory')
        if not isinstance(mainwindow, QMainWindow):
            raise TypeError('mainwindow must be a QGis mainwindow')
        if not isinstance(combobox_workbench, QComboBox):
            raise TypeError('combobox_workbench must be a QGis mainwindow')
        if not hasattr(combobox_workbench_update, '__call__'):
            raise TypeError('combobox_workbench_update must be callable')
        if not isinstance(fsm, dtype_fsm_class):
            raise TypeError('fsm must be a workbench finite state machine')

        super().__init__(plugin_root_fld)

        self._plugin_root_fld = plugin_root_fld
        self._mainwindow = mainwindow
        self._combobox_workbench = combobox_workbench
        self._fsm = fsm
        self._combobox_workbench_update = combobox_workbench_update

        self._connect_ui()

    def _connect_ui(self):

        for item in ('new', 'delete', 'save'):
            self._ui_dict['toolbutton_{NAME:s}'.format(NAME = item)].clicked.connect(
                getattr(self, '_toolbutton_{NAME:s}_clicked'.format(NAME = item))
                )

        self._ui_dict['list_workbenches'].currentRowChanged.connect(self._list_workbenches_currentrowchanged)

        self._update_content()

    def _list_workbenches_currentrowchanged(self):

        if not bool(self._ui_dict['list_workbenches'].isEnabled()):
            return

        new_name = self._workbench_index_to_name(self._ui_dict['list_workbenches'].currentRow())

        if new_name == self._fsm.active_workbench:
            return

        self._fsm.activate_workbench(new_name, self._mainwindow)
        self._combobox_workbench.setCurrentText(self._fsm.active_workbench)
        # self._update_content()

    def _toolbutton_new_clicked(self):

        new_name, user_ok = QInputDialog.getText(
            self,
            translate('global', 'New work bench'),
            translate('global', 'Name of new workbench')
            )

        if not user_ok:
            return

        self._fsm.new_workbench(new_name, self._mainwindow)
        self._update_content()

    def _toolbutton_delete_clicked(self):

        name = self._workbench_index_to_name(self._ui_dict['list_workbenches'].currentRow())

        self._fsm.delete_workbench(name, self._mainwindow)
        self._update_content()

    def _toolbutton_save_clicked(self):

        name = self._workbench_index_to_name(self._ui_dict['list_workbenches'].currentRow())

        self._fsm.save_workbench(name, self._mainwindow)
        self._update_content()

    def _update_content(self):

        self._ui_dict['list_workbenches'].setEnabled(False)
        self._ui_dict['list_workbenches'].clear()
        for item in sorted(self._fsm.keys()):
            self._ui_dict['list_workbenches'].addItem(item)
        self._ui_dict['list_workbenches'].setCurrentRow(
            self._workbench_name_to_index(self._fsm.active_workbench)
            )
        self._ui_dict['list_workbenches'].setEnabled(True)

        self._combobox_workbench_update()

    def _uptdate_items(self):

        self._ui_dict['list_dockwidgets'].setEnabled(False)
        self._ui_dict['list_toolbars'].setEnabled(False)
        self._ui_dict['list_dockwidgets'].clear()
        self._ui_dict['list_toolbars'].clear()

        for item in self._fsm[self._fsm.active_workbench].dockwidgets_keys():
            pass

        for item in self._fsm[self._fsm.active_workbench].toolbars_keys():
            pass

        self._ui_dict['list_dockwidgets'].setEnabled(True)
        self._ui_dict['list_toolbars'].setEnabled(True)

    def _workbench_index_to_name(self, index):

        return list(sorted(self._fsm.keys()))[index]

    def _workbench_name_to_index(self, name):

        return list(sorted(self._fsm.keys())).index(name)
