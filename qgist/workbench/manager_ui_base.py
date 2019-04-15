
import os

from PyQt5.QtCore import (
    QSize,
    Qt,
    )
from PyQt5.QtGui import (
    QIcon,
    )
from PyQt5.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QListWidget,
    QToolButton,
    QVBoxLayout,
    )

from ..const import ICON_FLD
from ..util import translate

class manager_ui_base_class(QDialog):

    def __init__(self, plugin_fld):

        super().__init__()

        self.setWindowTitle(translate('global', 'Workbench Configuration'))

        self._ui_dict = {
            'layout_0_v_root': QVBoxLayout(), # dialog
            'layout_1_h_toolbar': QHBoxLayout(), # toolbar - for bottons
            'layout_1_h_lists': QHBoxLayout(), # central - for list of workbenches left and lists of ui right
            'layout_2_v_uielements': QVBoxLayout(), # right - ui element lists (toolbars and dockwidgets)
            }
        self.setLayout(self._ui_dict['layout_0_v_root'])
        self._ui_dict['layout_0_v_root'].addLayout(self._ui_dict['layout_1_h_toolbar'])
        self._ui_dict['layout_0_v_root'].addLayout(self._ui_dict['layout_1_h_lists'])

        self._ui_dict['list_workbenches'] = manager_ui_base_class._get_workbenchlist()
        self._ui_dict['layout_1_h_lists'].addWidget(self._ui_dict['list_workbenches'])
        self._ui_dict['list_toolbars'] = manager_ui_base_class._get_toolbarlist()
        self._ui_dict['layout_2_v_uielements'].addWidget(self._ui_dict['list_toolbars'])
        self._ui_dict['list_dockwidgets'] = manager_ui_base_class._get_dockwidgetlist()
        self._ui_dict['layout_2_v_uielements'].addWidget(self._ui_dict['list_dockwidgets'])
        self._ui_dict['layout_1_h_lists'].addLayout(self._ui_dict['layout_2_v_uielements'])

        manager_ui_base_class._init_dialogtoolbar(
            self._ui_dict, self._ui_dict['layout_1_h_toolbar']
            )

    @staticmethod
    def _init_dialogtoolbar(ui_dict, toolbar_layout, plugin_fld):

        toolbar_layout.setSpacing(0)
        toolbar_layout.setContentsMargins(0, 0, 0, 0)

        for name, title, text in [
            ('new', translate('global', 'New work bench'), 'FileNew.svg'),
            ('delete', translate('global', 'Delete work bench'), 'Delete.svg'),
            ('save', translate('global', 'Save work benches'), 'Save.svg'),
            ]:

            toolbutton = QToolButton()
            toolbutton.setToolTip(title)
            toolbutton.setIcon(QIcon(os.path.join(
                plugin_fld, ICON_FLD, icon
            )))
            toolbutton.setIconSize(QSize(24, 24))  # TODO get icon size from QGis!!!
            toolbutton.setAutoRaise(True)
            toolbutton.setFocusPolicy(Qt.NoFocus)

            ui_dict['toolbutton_{NAME:s}'.format(NAME = name)] = toolbutton

            toolbar_layout.addWidget(toolbutton)

        toolbar_layout.addStretch()

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
