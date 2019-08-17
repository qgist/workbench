# -*- coding: utf-8 -*-

"""

QGIST WORK BENCH
QGis Plugin for Organizing Toolbars
https://github.com/qgist/workbench

    qgist/workbench/core.py: QGIST workbench core

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
import platform


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT (External Dependencies)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from PyQt5.QtGui import (
    QIcon,
    )
from PyQt5.QtWidgets import (
    QAction,
    QComboBox,
    QHBoxLayout,
    QToolButton,
    QWidget,
    )


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT (Internal)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from .const import (
    PLUGIN_ICON_FN,
    PLUGIN_NAME,
    WORKBENCH_WIDGET_WIDTH,
    )
from .dtype_fsm import dtype_fsm_class
from .ui_manager import ui_manager_class
from ..const import (
    ICON_FLD,
    TRANSLATION_FLD,
    )
from ..util import (
    translate,
    setupTranslation,
    )


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS: WORKBENCH CORE
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class workbench:

    def __init__(self, iface, plugin_root_fld):

        if not hasattr(iface, 'mainWindow'):
            raise TypeError('iface must be a QGIS iface object')
        if not isinstance(plugin_root_fld, str):
            raise TypeError('plugin_root_fld must be str')
        if not os.path.exists(plugin_root_fld):
            raise ValueError('plugin_root_fld must exists')
        if not os.path.isdir(plugin_root_fld):
            raise ValueError('plugin_root_fld must be a directory')

        self._iface = iface
        self._plugin_root_fld = plugin_root_fld

        self._mainwindow = self._iface.mainWindow()
        self._system = platform.system()

    def initGui(self):
        """
        QGis Plugin Interface Routine
        """

        setupTranslation(os.path.join(
            self._plugin_root_fld, TRANSLATION_FLD
            ))

        self._ui_dict = {}
        self._ui_cleanup = []

        self._ui_dict['action_manage'] = QAction(translate('global', '&Workbench Management'))

        workBenchMenuText = translate('global', 'Qgist Work&Bench')
        self._iface.addPluginToMenu(workBenchMenuText, self._ui_dict['action_manage'])
        self._ui_cleanup.append(
            lambda: self._iface.removePluginMenu(workBenchMenuText, self._ui_dict['action_manage'])
            )

        self._ui_dict['toolbutton_save'] = QToolButton()
        self._ui_dict['toolbutton_save'].setIcon(QIcon(os.path.join(
            self._plugin_root_fld, ICON_FLD, 'Save.svg'
            )))
        self._ui_dict['toolbutton_save'].setToolTip(translate('global', 'Save work benche'))

        self._ui_dict['toolbutton_manage'] = QToolButton()
        self._ui_dict['toolbutton_manage'].setIcon(QIcon(os.path.join(
            self._plugin_root_fld, ICON_FLD, PLUGIN_ICON_FN
            )))
        self._ui_dict['toolbutton_manage'].setToolTip(translate('global', 'Manage workbenches'))

        self._ui_dict['combobox_workbench'] = QComboBox()
        self._ui_dict['combobox_workbench'].setMaximumWidth(WORKBENCH_WIDGET_WIDTH)
        self._ui_dict['combobox_workbench'].setToolTip(PLUGIN_NAME)

        self._ui_dict['layout_0_v_root'] = QHBoxLayout()
        self._ui_dict['layout_0_v_root'].setContentsMargins(0, 0, 10, 0) # 10 px margin on right side
        self._ui_dict['layout_0_v_root'].addWidget(self._ui_dict['combobox_workbench'])
        self._ui_dict['layout_0_v_root'].addWidget(self._ui_dict['toolbutton_save'])
        self._ui_dict['layout_0_v_root'].addWidget(self._ui_dict['toolbutton_manage'])

        self._ui_dict['widget_corner'] = QWidget()
        self._ui_dict['widget_corner'].setLayout(self._ui_dict['layout_0_v_root'])

        # TODO handle Darwin, allow widget_corner to become a toolbar
        self._mainwindow.menuBar().setCornerWidget(self._ui_dict['widget_corner'])
        self._ui_dict['widget_corner'].setVisible(True)
        self._ui_cleanup.extend([
            lambda: self._mainwindow.menuBar().setCornerWidget(QWidget()),
            lambda: self._ui_dict['widget_corner'].setVisible(False)
            ])

        self._wait_for_mainwindow = True
        self._ui_dict['action_manage'].setEnabled(False)
        self._ui_dict['combobox_workbench'].setEnabled(False)
        self._iface.initializationCompleted.connect(self._connect_ui)

    def unload(self):
        """
        QGis Plugin Interface Routine
        """

        # TODO save config to disk

        for cleanup_action in self._ui_cleanup:
            cleanup_action()

    def _connect_ui(self):

        if not self._wait_for_mainwindow:
            return
        self._wait_for_mainwindow = False
        self._ui_dict['action_manage'].setEnabled(True)
        self._ui_dict['combobox_workbench'].setEnabled(True)
        self._iface.initializationCompleted.disconnect(self._connect_ui)

        self._fsm = dtype_fsm_class(list(), self._mainwindow) # TODO load from config, zero-init issue ...

        self._combobox_workbench_updade()
        self._ui_dict['combobox_workbench'].activated.connect(self._combobox_workbench_activated)

        self._ui_dict['action_manage'].triggered.connect(self._open_manager)
        self._ui_dict['toolbutton_manage'].clicked.connect(self._open_manager)
        self._ui_dict['toolbutton_save'].clicked.connect(self._save_workbench)

    def _combobox_workbench_activated(self):

        if not bool(self._ui_dict['combobox_workbench'].isEnabled()):
            return

        new_name = str(self._ui_dict['combobox_workbench'].currentText())
        if new_name != self._fsm.active_workbench:
            self._fsm.activate_workbench(new_name, self._mainwindow)

    def _combobox_workbench_updade(self):

        enabled = bool(self._ui_dict['combobox_workbench'].isEnabled())

        if enabled:
            self._ui_dict['combobox_workbench'].setEnabled(False)

        self._ui_dict['combobox_workbench'].clear()
        for name in sorted(self._fsm.keys()):
            self._ui_dict['combobox_workbench'].addItem(name)
        self._ui_dict['combobox_workbench'].setCurrentText(self._fsm.active_workbench)

        if enabled:
            self._ui_dict['combobox_workbench'].setEnabled(True)

    def _open_manager(self):

        self._ui_dict['combobox_workbench'].setEnabled(False)

        try:
            ui_manager_class(
                self._plugin_root_fld,
                self._mainwindow,
                self._ui_dict['combobox_workbench'],
                self._combobox_workbench_updade,
                self._fsm,
                ).exec_()
        finally:
            self._ui_dict['combobox_workbench'].setEnabled(True)

    def _save_workbench(self):

        self._fsm.save_workbench(self._fsm.active_workbench, self._mainwindow)
