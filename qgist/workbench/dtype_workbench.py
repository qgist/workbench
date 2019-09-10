# -*- coding: utf-8 -*-

"""

QGIST WORKBENCH
QGIS Plugin for Organizing Toolbars and Dockwidgets
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
from .error import QgistUnnamedElementError
from ..config import config_class
from ..error import (
    QgistTypeError,
    QgistValueError,
    Qgist_ALL_Errors,
    )
from ..msg import msg_warning
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
        config = None,
        ):

        if not isinstance(config, config_class) and config is not None:
            raise QgistTypeError(translate('global', '"config" must be a "config_class" object or None. (dtype_workbench)'))

        self._config = config

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

        show_unnamed_warning = False if self._config is None else self._config.get('show_unnamed_warning', False)

        dtype_workbench_class._activate_uielements(
            uiobjects_dict = qtoolbars_dict,
            uielements_dict = self._toolbars_dict,
            show_unnamed_warning = show_unnamed_warning,
            )
        dtype_workbench_class._activate_uielements(
            uiobjects_dict = qdockwidgets_dict,
            uielements_dict = self._dockwidgets_dict,
            show_unnamed_warning = show_unnamed_warning,
            )

        mainwindow.restoreState(self._mainwindow_state)

    def save(self, mainwindow):

        if not isinstance(mainwindow, QMainWindow):
            raise QgistTypeError(translate('global', '"mainwindow" must be a QGIS mainwindow. (dtype_workbench save)'))

        qtoolbars_dict = dtype_workbench_class._get_uielements_from_mainwindow(mainwindow, QToolBar)
        qdockwidgets_dict = dtype_workbench_class._get_uielements_from_mainwindow(mainwindow, QDockWidget)

        show_unnamed_warning = False if self._config is None else self._config.get('show_unnamed_warning', False)

        dtype_workbench_class._save_uielements(
            uiobjects_dict = qtoolbars_dict,
            uielements_dict = self._toolbars_dict,
            show_unnamed_warning = show_unnamed_warning,
            )
        dtype_workbench_class._save_uielements(
            uiobjects_dict = qdockwidgets_dict,
            uielements_dict = self._dockwidgets_dict,
            show_unnamed_warning = show_unnamed_warning,
            )

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
    def _activate_uielements(uiobjects_dict, uielements_dict, show_unnamed_warning):

        for name_internal, uiobject in uiobjects_dict.items():
            if name_internal in uielements_dict.keys():
                uielements_dict[name_internal].push_state_to_uiobject()
            else:
                """try/except-block fixes #7, Certain other plugins inhibit
                the start of Workbench because of unnamed UI elements"""
                try:
                    uielement = dtype_uielement_class.from_uiobject(uiobject)
                    uielements_dict[uielement.name_internal] = uielement
                except QgistUnnamedElementError as e:
                    """implementing #8, enabling the user to disable warnings
                    which are mainly caused by other plugins"""
                    if show_unnamed_warning:
                        msg_warning(e)
                except Qgist_ALL_Errors as e:
                    msg_warning(e)
        for name_internal in (uielements_dict.keys() - uiobjects_dict.keys()):
            uielements_dict[name_internal].existence = False

    @staticmethod
    def _get_uielements_from_mainwindow(mainwindow, uielement_type):

        def get_parent(el):
            """Fixes #6, Certain other plugins crash Workbench:
            Their UI's parent is exposed as a property instead of a method"""
            if hasattr(el.parent, '__call__'):
                return el.parent()
            return el.parent

        return {
            uielement.objectName(): uielement
            for uielement in mainwindow.findChildren(uielement_type)
            if get_parent(uielement).objectName() == 'QgisApp'
            }

    @staticmethod
    def _save_uielements(uiobjects_dict, uielements_dict, show_unnamed_warning):

        for name_internal, uiobject in uiobjects_dict.items():
            if name_internal in uielements_dict.keys():
                uielements_dict[name_internal].pull_state_from_uiobject()
            else:
                """try/except-block fixes #9, Certain other plugins inhibit
                saving a workbench because of unnamed UI element"""
                try:
                    uielement = dtype_uielement_class.from_uiobject(uiobject)
                    uielements_dict[uielement.name_internal] = uielement
                except QgistUnnamedElementError as e:
                    """implementing #8, enabling the user to disable warnings
                    which are mainly caused by other plugins"""
                    if show_unnamed_warning:
                        msg_warning(e)
                except Qgist_ALL_Errors as e:
                    msg_warning(e)
        for name_internal in (uielements_dict.keys() - uiobjects_dict.keys()):
            uielements_dict[name_internal].existence = False

    @property
    def name(self):

        return self._name

    @name.setter
    def name(self, value):

        if not isinstance(value, str):
            raise QgistTypeError(translate('global', 'New value of "name" must be a str. (dtype_workbench name)'))
        if len(value) == 0:
            raise QgistValueError(translate('global', 'New value of "name" must not be empty. (dtype_workbench name)'))

        self._name = value

    @staticmethod
    def from_mainwindow(
        name = '',
        mainwindow = None,
        config = None,
        ):

        # name is checked by dtype_workbench_class.__init__
        if not isinstance(mainwindow, QMainWindow):
            raise QgistTypeError(translate('global', '"mainwindow" must be a QGIS mainwindow. (dtype_workbench from_mainwindow)'))
        if not isinstance(config, config_class) and config is not None:
            raise QgistTypeError(translate('global', '"config" must be a "config_class" object or None. (dtype_workbench from_mainwindow)'))

        def uiobject_to_dict(_uiobject):
            try:
                return dtype_uielement_class.from_uiobject(_uiobject).as_dict()
            except QgistUnnamedElementError:
                return None

        toolbars_list = [ui_dict for ui_dict in (
            uiobject_to_dict(uiobject)
            for _, uiobject in dtype_workbench_class._get_uielements_from_mainwindow(
                mainwindow, QToolBar
                ).items()
            ) if ui_dict is not None]

        dockwidgets_list = [ui_dict for ui_dict in (
            uiobject_to_dict(uiobject)
            for _, uiobject in dtype_workbench_class._get_uielements_from_mainwindow(
                mainwindow, QDockWidget
                ).items()
            ) if ui_dict is not None]

        mainwindow_state = base64.encodebytes(bytes(mainwindow.saveState())).decode('ASCII')

        return dtype_workbench_class(
            name = name,
            mainwindow_state = mainwindow_state,
            toolbars_list = toolbars_list,
            dockwidgets_list = dockwidgets_list,
            mainwindow = mainwindow,
            config = config,
            )
