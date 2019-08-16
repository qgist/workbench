# -*- coding: utf-8 -*-

"""

QGIST WORK BENCH
QGis Plugin for Organizing Toolbars
https://github.com/qgist/workbench

    qgist/workbench/dtype_workbench.py: workbench data type

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

import base64


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT (External Dependencies)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from PyQt5.QtWidgets import (
    QDockWidget,
    QMainWindow,
    QToolBar,
    )


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT (Internal)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from .dtype_uielement import dtype_uielement_class


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class dtype_workbench_class:

    def __init__(self,
        name = '',
        mainwindow_state = None,
        toolbars_list = None,
        dockwidgets_list = None,
        ):

        if not isinstance(name, str):
            raise TypeError('name must be str')
        if len(name) == 0:
            raise ValueError('name must not be empty')
        self._name = name

        if isinstance(mainwindow_state, str):
            self._mainwindow_state = base64.decodebytes(mainwindow_state.encode('ASCII'))
        elif isinstance(mainwindow_state, bytes):
            self._mainwindow_state = base64.decodebytes(mainwindow_state)
        else:
            raise TypeError('mainwindow_state must either be str or bytes')

        if not isinstance(toolbars_list, list):
            raise TypeError('toolbars_list must be a list')
        if not isinstance(dockwidgets_list, list):
            raise TypeError('dockwidgets_list must be a list')
        if any([not isinstance(item, dict) for item in toolbars_list]):
            raise TypeError('items in toolbars_list must be dicts')
        if any([not isinstance(item, dict) for item in dockwidgets_list]):
            raise TypeError('items in dockwidgets_list must be dicts')
        self._toolbars_dict = {
            b.name_internal: b
            for b in (dtype_uielement_class(**a) for a in toolbars_list)
            }
        self._dockwidgets_dict = {
            b.name_internal: b
            for b in (dtype_uielement_class(**a) for a in dockwidgets_list)
            }

    def activate(self, mainwindow):

        if not isinstance(mainwindow, QMainWindow):
            raise TypeError('mainwindow must be a QGis mainwindow')

        qtoolbars_dict = dtype_workbench_class._get_uielements_from_mainwindow(mainwindow, QToolBar)
        qdockwidgets_dict = dtype_workbench_class._get_uielements_from_mainwindow(mainwindow, QDockWidget)

        dtype_workbench_class._activate_uielements(qtoolbars_dict, self._toolbars_dict)
        dtype_workbench_class._activate_uielements(qdockwidgets_dict, self._dockwidgets_dict)

        mainwindow.restoreState(self._mainwindow_state)

    def save(self, mainwindow):

        if not isinstance(mainwindow, QMainWindow):
            raise TypeError('mainwindow must be a QGis mainwindow')

        qtoolbars_dict = dtype_workbench_class._get_uielements_from_mainwindow(mainwindow, QToolBar)
        qdockwidgets_dict = dtype_workbench_class._get_uielements_from_mainwindow(mainwindow, QDockWidget)

        dtype_workbench_class._save_uielements(qtoolbars_dict, self._toolbars_dict)
        dtype_workbench_class._save_uielements(qdockwidgets_dict, self._dockwidgets_dict)

        self._mainwindow_state = bytes(mainwindow.saveState())

    def as_dict(self):

        return dict(
            name = self._name,
            mainwindow_state = base64.encodebytes(self._mainwindow_state).decode('ASCII'),
            toolbars_list = [item.as_dict() for item in self._toolbars_dict.values()],
            dockwidgets_list = [item.as_dict() for item in self._dockwidgets_dict.values()],
            )

    @staticmethod
    def _activate_uielements(uiobjects_dict, uielements_dict):

        for name_internal, uiobject in uiobjects_dict.items():
            try:
                uielements_dict[name_internal].push_state_to_uiobject(uiobject)
            except KeyError:
                uielement = dtype_uielement_class.from_uiobject(uiobject)
                uielements_dict[uielement.name_internal] = uielement
        for name_internal in (uielements_dict.keys() - uiobjects_dict.keys()):
            uielements_dict[name_internal].existence = False

    @staticmethod
    def _get_uielements_from_mainwindow(mainwindow, uielement_type):

        return {
            toolbar.objectName(): toolbar
            for toolbar in mainwindow.findChildren(uielement_type)
            if toolbar.parent().objectName() == 'QgisApp'
            }

    @staticmethod
    def _save_uielements(uiobjects_dict, uielements_dict):

        for name_internal, uiobject in uiobjects_dict.items():
            try:
                uielements_dict[name_internal].pull_state_from_uiobject(uiobject)
            except KeyError:
                uielement = dtype_uielement_class.from_uiobject(uiobject)
                uielements_dict[uielement.name_internal] = uielement
        for name_internal in (uielements_dict.keys() - uiobjects_dict.keys()):
            uielements_dict[name_internal].existence = False

    @property
    def name(self):

        return self._name

    @name.setter
    def name(self, value):

        if not isinstance(name, str):
            raise TypeError('new value of name must be a str')
        if len(name) == 0:
            raise ValueError('new value of name is empty')

        self._name = value

    @staticmethod
    def from_mainwindow(
        name = '',
        mainwindow = None,
        ):

        if not isinstance(mainwindow, QMainWindow):
            raise TypeError('mainwindow must be a QGis mainwindow')

        toolbars_list = [
            dtype_uielement_class.from_uiobject(uiobject).as_dict()
            for _, uiobject in dtype_workbench_class._get_uielements_from_mainwindow(
                mainwindow, QToolBar
                ).items()
            ]

        dockwidgets_list = [
            dtype_uielement_class.from_uiobject(uiobject).as_dict()
            for _, uiobject in dtype_workbench_class._get_uielements_from_mainwindow(
                mainwindow, QDockWidget
                ).items()
            ]

        mainwindow_state = base64.encodebytes(bytes(mainwindow.saveState())).decode('ASCII')

        return dtype_workbench_class(
            name = name,
            mainwindow_state = mainwindow_state,
            toolbars_list = toolbars_list,
            dockwidgets_list = dockwidgets_list,
            )
