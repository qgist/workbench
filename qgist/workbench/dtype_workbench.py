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
from ..error import (
    QgistTypeError,
    QgistValueError,
    )
from ..util import translate


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class dtype_workbench_class:

    def __init__(self,
        name = '',
        mainwindow_state = None,
        toolbars_list = None,
        dockwidgets_list = None,
        mainwindow = None,
        ):

        if not isinstance(name, str):
            raise QgistTypeError(translate('global', '"name" must be str. (dtype_workbench)'))
        if len(name) == 0:
            raise QgistValueError(translate('global', '"name" must not be empty. (dtype_workbench)'))
        self._name = name

        if isinstance(mainwindow_state, str):
            self._mainwindow_state = base64.decodebytes(mainwindow_state.encode('ASCII'))
        elif isinstance(mainwindow_state, bytes):
            self._mainwindow_state = base64.decodebytes(mainwindow_state)
        else:
            raise QgistTypeError(translate('global', '"mainwindow_state" must either be str or bytes. (dtype_workbench)'))

        if not isinstance(mainwindow, QMainWindow):
            raise QgistTypeError(translate('global', '"mainwindow" must be a QGIS mainwindow. (dtype_workbench)'))

        if not isinstance(toolbars_list, list):
            raise QgistTypeError(translate('global', '"toolbars_list" must be a list. (dtype_workbench)'))
        if not isinstance(dockwidgets_list, list):
            raise QgistTypeError(translate('global', '"dockwidgets_list" must be a list. (dtype_workbench)'))
        if any([not isinstance(item, dict) for item in toolbars_list]):
            raise QgistTypeError(translate('global', 'Items in "toolbars_list" must be dicts. (dtype_workbench)'))
        if any([not isinstance(item, dict) for item in dockwidgets_list]):
            raise QgistTypeError(translate('global', 'Items in "dockwidgets_list" must be dicts. (dtype_workbench)'))

        tmp_toolbars_dict = dtype_workbench_class._get_uielements_from_mainwindow(mainwindow, QToolBar)
        self._toolbars_dict = {
            b.name_internal: b
            for b in (dtype_uielement_class(
                uiobject = tmp_toolbars_dict.get(a['name_internal'], None), **a
                ) for a in toolbars_list)
            }
        tmp_dockwidgets_dict = dtype_workbench_class._get_uielements_from_mainwindow(mainwindow, QDockWidget)
        self._dockwidgets_dict = {
            b.name_internal: b
            for b in (dtype_uielement_class(
                uiobject = tmp_dockwidgets_dict.get(a['name_internal'], None), **a
                ) for a in dockwidgets_list)
            }

        self.toolbars_keys = self._toolbars_dict.keys
        self.dockwidgets_keys = self._dockwidgets_dict.keys

    def __getitem__(self, value):

        if not isinstance(value, tuple):
            raise QgistValueError(translate('global', 'Not enough parameters, two expected. (dtype_workbench item)'))
        if len(value) != 2:
            raise QgistValueError(translate('global', 'Wrong number of parameters, two expected. (dtype_workbench item)'))

        item_type, item_name = value

        if not isinstance(item_type, str):
            raise QgistTypeError(translate('global', '"item_type" must be str. (dtype_workbench item)'))
        if item_type not in ('toolbars', 'dockwidgets'):
            raise QgistValueError(translate('global', 'Unknown "item_type". (dtype_workbench item)'))

        target_dict = getattr(self, '_{NAME:s}_dict'.format(NAME = item_type))

        if not isinstance(item_name, str):
            raise QgistTypeError(translate('global', '"item_name" must be str. (dtype_workbench item)'))
        if item_name not in target_dict.keys():
            raise QgistValueError(translate('global', '"item_name" is not a known item. (dtype_workbench item)'))

        return target_dict[item_name]

    def activate(self, mainwindow):

        if not isinstance(mainwindow, QMainWindow):
            raise QgistTypeError(translate('global', '"mainwindow" must be a QGIS mainwindow. (dtype_workbench activate)'))

        qtoolbars_dict = dtype_workbench_class._get_uielements_from_mainwindow(mainwindow, QToolBar)
        qdockwidgets_dict = dtype_workbench_class._get_uielements_from_mainwindow(mainwindow, QDockWidget)

        dtype_workbench_class._activate_uielements(qtoolbars_dict, self._toolbars_dict)
        dtype_workbench_class._activate_uielements(qdockwidgets_dict, self._dockwidgets_dict)

        mainwindow.restoreState(self._mainwindow_state)

    def save(self, mainwindow):

        if not isinstance(mainwindow, QMainWindow):
            raise QgistTypeError(translate('global', '"mainwindow" must be a QGIS mainwindow. (dtype_workbench save)'))

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

    def dockwidgets(self):

        return (self._dockwidgets_dict[name] for name in sorted(self.dockwidgets_keys()))

    def toolbars(self):

        return (self._toolbars_dict[name] for name in sorted(self.toolbars_keys()))

    @staticmethod
    def _activate_uielements(uiobjects_dict, uielements_dict):

        for name_internal, uiobject in uiobjects_dict.items():
            try:
                uielements_dict[name_internal].push_state_to_uiobject()
            except KeyError:
                uielement = dtype_uielement_class.from_uiobject(uiobject)
                uielements_dict[uielement.name_internal] = uielement
        for name_internal in (uielements_dict.keys() - uiobjects_dict.keys()):
            uielements_dict[name_internal].existence = False

    @staticmethod
    def _get_uielements_from_mainwindow(mainwindow, uielement_type):

        return {
            uielement.objectName(): uielement
            for uielement in mainwindow.findChildren(uielement_type)
            if uielement.parent().objectName() == 'QgisApp'
            }

    @staticmethod
    def _save_uielements(uiobjects_dict, uielements_dict):

        for name_internal, uiobject in uiobjects_dict.items():
            try:
                uielements_dict[name_internal].pull_state_from_uiobject()
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
            raise QgistTypeError(translate('global', 'New value of "name" must be a str. (dtype_workbench name)'))
        if len(name) == 0:
            raise QgistValueError(translate('global', 'New value of "name" must not be empty. (dtype_workbench name)'))

        self._name = value

    @staticmethod
    def from_mainwindow(
        name = '',
        mainwindow = None,
        ):

        if not isinstance(mainwindow, QMainWindow):
            raise QgistTypeError(translate('global', '"mainwindow" must be a QGIS mainwindow. (dtype_workbench from_mainwindow)'))

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
            mainwindow = mainwindow,
            )
