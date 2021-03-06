# -*- coding: utf-8 -*-

"""

QGIST WORKBENCH
QGIS Plugin for Organizing Toolbars and Dockwidgets
https://github.com/qgist/workbench

    qgist/workbench/ui_manager_base.py: workbench manager ui base class

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

from PyQt5.QtCore import (
    QSize,
    Qt,
    )
from PyQt5.QtGui import (
    QIcon,
    )
from PyQt5.QtWidgets import (
    QCheckBox,
    QDialog,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QToolButton,
    QVBoxLayout,
    )


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT (Internal)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from .const import WORKBENCH_WIDGET_WIDTH
from ..const import ICON_FLD
from ..util import translate


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class ui_manager_base_class(QDialog):

    def __init__(self, plugin_root_fld):

        super().__init__()

        self.setWindowTitle(translate('global', 'Workbench Configuration'))

        self._ui_dict = {
            'layout_0_v_root': QVBoxLayout(), # dialog
            'layout_1_h_toolbar': QHBoxLayout(), # toolbar - for buttons
            'layout_1_h_lists': QHBoxLayout(), # central - for list of workbenches left and lists of ui right
            'layout_2_v_uielements': QVBoxLayout(), # right - ui element lists (toolbars and dockwidgets)
            }
        self.setLayout(self._ui_dict['layout_0_v_root'])
        self._ui_dict['layout_0_v_root'].addLayout(self._ui_dict['layout_1_h_toolbar'])
        self._ui_dict['layout_0_v_root'].addLayout(self._ui_dict['layout_1_h_lists'])

        self._ui_dict['list_workbenches'] = ui_manager_base_class._get_workbenchlist()
        self._ui_dict['layout_1_h_lists'].addWidget(self._ui_dict['list_workbenches'])

        self._ui_dict['label_toolbars'] = QLabel(translate('global', 'Toolbars'))
        self._ui_dict['layout_2_v_uielements'].addWidget(self._ui_dict['label_toolbars'])
        self._ui_dict['list_toolbars'] = ui_manager_base_class._get_toolbarlist()
        self._ui_dict['layout_2_v_uielements'].addWidget(self._ui_dict['list_toolbars'])
        self._ui_dict['label_dockwidgets'] = QLabel(translate('global', 'Dockwidgets'))
        self._ui_dict['layout_2_v_uielements'].addWidget(self._ui_dict['label_dockwidgets'])
        self._ui_dict['list_dockwidgets'] = ui_manager_base_class._get_dockwidgetlist()
        self._ui_dict['layout_2_v_uielements'].addWidget(self._ui_dict['list_dockwidgets'])
        self._ui_dict['layout_1_h_lists'].addLayout(self._ui_dict['layout_2_v_uielements'])

        ui_manager_base_class._init_dialogtoolbar(
            self._ui_dict, self._ui_dict['layout_1_h_toolbar'], plugin_root_fld
            )

    @staticmethod
    def _init_dialogtoolbar(ui_dict, toolbar_layout, plugin_root_fld):

        toolbar_layout.setSpacing(0)
        toolbar_layout.setContentsMargins(0, 0, 0, 0)

        for name, title, icon in [
            ('new', translate('global', 'New workbench'), 'FileNew.svg'),
            ('delete', translate('global', 'Delete workbench'), 'Delete.svg'),
            ('save', translate('global', 'Save workbench'), 'Save.svg'),
            ('rename', translate('global', 'Rename workbench'), 'Rename.svg'),
            ('import', translate('global', 'Import workbench'), 'Import.svg'),
            ('export', translate('global', 'Export workbench'), 'Export.svg'),
            ]:

            toolbutton = QToolButton()
            toolbutton.setToolTip(title)
            toolbutton.setIcon(QIcon(os.path.join(
                plugin_root_fld, ICON_FLD, icon
            )))
            toolbutton.setIconSize(QSize(24, 24))  # TODO get icon size from QGis!!!
            toolbutton.setAutoRaise(True)
            toolbutton.setFocusPolicy(Qt.NoFocus)

            ui_dict['toolbutton_{NAME:s}'.format(NAME = name)] = toolbutton

            toolbar_layout.addWidget(toolbutton)

        toolbar_layout.addStretch()

        ui_dict['checkbox_unnamedwarning'] = QCheckBox(translate('global', 'Warn if UI elements can not be uniquely identified'))
        toolbar_layout.addWidget(ui_dict['checkbox_unnamedwarning'])

    @staticmethod
    def _get_workbenchlist():

        workbenchlist = QListWidget()
        workbenchlist.setFixedWidth(WORKBENCH_WIDGET_WIDTH)

        return workbenchlist

    @staticmethod
    def _get_toolbarlist():

        toolbarlist = QListWidget()

        return toolbarlist

    @staticmethod
    def _get_dockwidgetlist():

        dockwidgetlist = QListWidget()

        return dockwidgetlist
