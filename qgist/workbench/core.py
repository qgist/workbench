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

from PyQt5.QtWidgets import (
    QAction,
    )


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT (Internal)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from ..const import TRANSLATION_FLD
from ..util import translate, setupTranslation


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
        self._cleanup_actions = []

        self._ui_dict['action_management'] = QAction(translate('global', '&Workbench Management'))
        # self._ui_dict['action_management'].triggered.connect(self.workBenchManagementDialog)

        workBenchMenuText = translate('global', 'Qgist Work&Bench')
        self._iface.addPluginToMenu(workBenchMenuText, self._ui_dict['action_management'])
        self._cleanup_actions.append(
            lambda: self._iface.removePluginMenu(workBenchMenuText, self._ui_dict['action_management'])
            )

        """
        # Create Workbench management toolbutton to hold a reference management dialog
        self.mManageToolButton = QToolButton(self.mMainWindow)
        self.mManageToolButton.setIcon(QIcon(os.path.join(
            self.mPluginDirectory, ICON_FLD, PLUGIN_ICON_FN
        )))
        self.mManageToolButton.setToolTip(
            translate('global', 'Manage workbenches')
        )
        self.mManageToolButton.setIconSize(QSize(20, 20))
        self.mManageToolButton.clicked.connect(self.workBenchManagementDialog)

        # Create Confguration toolbutton to hold a reference to call Configuration GUI
        self.mConfigureToolButton = QToolButton(self.mMainWindow)
        self.mConfigureToolButton.setIcon(QIcon(os.path.join(
            self.mPluginDirectory, ICON_FLD, PLUGIN_CONFIG_ICON_FN
        )))
        self.mConfigureToolButton.setToolTip(
            translate('global', 'Configure workbenches')
        )
        self.mConfigureToolButton.setIconSize(QSize(20, 20))
        self.mConfigureToolButton.clicked.connect(self.workbenchConfigurationsDialog)

        # Create Workbench dropdown list and fill it with values from Config file.
        self.mWorkBenchCombobox = QComboBox(self.mMainWindow)
        self.mWorkBenchCombobox.setMaximumWidth(WORKBENCH_WIDGET_WIDTH)
        self.mWorkBenchCombobox.setToolTip(PLUGIN_NAME)
        self.fillWorkBenchComboBox()

        # Activate Current workbench which was save during the last QGIS session (if available)
        # self.mWorkBenchCombobox.currentIndexChanged.connect(self.changeWorkBench)
        self.mWorkBenchCombobox.activated.connect(self.changeWorkBench)
        self.mWorkBenchCombobox.setCurrentIndex(self.mConfigData['lastIndex'])

        # Prepare corner widget to be added in QGIS Top right corner
        # add previously created workbench dropdown list and setting widget to cornerwidget
        self.mCornerWidget = QWidget()
        cornerLayout = QHBoxLayout()
        cornerLayout.setContentsMargins(0, 0, 10, 0)  # 10 pix margen on right side
        cornerLayout.addWidget(self.mWorkBenchCombobox)
        cornerLayout.addWidget(self.mManageToolButton)
        cornerLayout.addWidget(self.mConfigureToolButton)
        self.mCornerWidget.setLayout(cornerLayout)

        # Check whether user want to add it as corner widget or as toolbar
        # On windows/Linux default is corner widget
        # TODO: Check current OS before setting as Corner widget- FP. 29.09.2018
        # if its macos then always add as toolbar
        self.mIsCornerWidget = False  # QUICK FIX:
        if self.mCurrentOS != "Darwin" and self.mConfigData['asCornerWidget']:
            self.mMainWindow.menuBar().setCornerWidget(self.mCornerWidget)
            self.mCornerWidget.setVisible(True)
            self.mIsCornerWidget = True
        else:
            self.mWorkBenchToolBar = self.mIface.addToolBar(
                translate('global', 'Qgist Work&Bench')
            )
            # Set autoraise and NO Fcous to match QGIS toolbar styles.
            self.mConfigureToolButton.setAutoRaise(True)
            self.mConfigureToolButton.setFocusPolicy(Qt.NoFocus)
            self.mManageToolButton.setAutoRaise(True)
            self.mManageToolButton.setFocusPolicy(Qt.NoFocus)
            self.mWorkBenchToolBar.setObjectName(WORKBENCHTOOLBAR_NAME)
            self.mWorkBenchToolBar.addWidget(self.mCornerWidget)
            self.mIsCornerWidget = False
        """

    def unload(self):
        """
        QGis Plugin Interface Routine
        """

        # save config to disk

        for cleanup_action in self._cleanup_actions:
            cleanup_action()
