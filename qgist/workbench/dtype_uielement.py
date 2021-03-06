# -*- coding: utf-8 -*-

"""

QGIST WORKBENCH
QGIS Plugin for Organizing Toolbars and Dockwidgets
https://github.com/qgist/workbench

    qgist/workbench/dtype_uielement.py: ui element data type

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
    QDockWidget,
    QToolBar,
    )


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT (Internal)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from .error import QgistUnnamedElementError
from ..error import (
    QgistAttributeError,
    QgistTypeError,
    QgistValueError,
    )
from ..util import translate


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class dtype_uielement_class:

    def __init__(self,
        name_internal = '',
        name_translated = '',
        visibility = True,
        uiobject = None,
        ):

        if not isinstance(name_internal, str):
            raise QgistTypeError(translate('global', '"internal_name" must be str. (dtype_uielement)'))
        if len(name_internal) == 0:
            raise QgistUnnamedElementError(translate('global', 'Unnamed UI element. (dtype_uielement)'))
        self._name_internal = name_internal

        if not isinstance(name_translated, str):
            raise QgistTypeError(translate('global', '"translated_name" must be str. (dtype_uielement)'))
        self._name_translated = name_translated

        if not isinstance(visibility, bool):
            raise QgistTypeError(translate('global', '"visibility" must be bool. (dtype_uielement)'))
        self._visibility = visibility

        if uiobject is not None:
            if not (isinstance(uiobject, QToolBar) or isinstance(uiobject, QDockWidget)):
                raise QgistTypeError(translate('global', '"uiobject" must be either QToolBar or QDockWidget. (dtype_uielement)'))
            self._uiobject = uiobject
        else:
            self._uiobject = None

        if self._uiobject is not None:
            actual_name_translated = uiobject.windowTitle()
            if self._name_translated != actual_name_translated:
                self._name_translated = actual_name_translated

        self._existence = uiobject is not None

    def as_dict(self):

        return dict(
            name_internal = self._name_internal,
            name_translated = self._name_translated,
            visibility = self._visibility,
            )

    def pull_state_from_uiobject(self):

        if not self._existence:
            return

        self._visibility = self._uiobject.isVisible()

    def push_state_to_uiobject(self):

        if not self._existence:
            return

        self._uiobject.setVisible(self._visibility)

    def setVisible(self, value):

        if not isinstance(value, bool):
            raise QgistTypeError(translate('global', '"value" must be bool. (dtype_uielement setVisible)'))

        if not self._existence:
            return

        self._uiobject.setVisible(value)

    @property
    def existence(self):

        return self._existence

    @existence.setter
    def existence(self, value):

        if not isinstance(value, bool):
            raise QgistTypeError(translate('global', '"value" must be bool. (dtype_uielement existence)'))
        if value:
            raise QgistValueError(translate('global', '"value" can only be set to false. (dtype_uielement existence)'))

        self._existence = False
        self._uiobject = None

    @property
    def name_internal(self):

        return self._name_internal

    @name_internal.setter
    def name_internal(self, value):

        raise QgistAttributeError(translate('global', '"name_internal" must not be changed. (dtype_uielement name_internal)'))

    @property
    def name_translated(self):

        return self._name_translated

    @name_translated.setter
    def name_translated(self, value):

        raise QgistAttributeError(translate('global', '"name_translated" must not be changed. (dtype_uielement name_translated)'))

    @property
    def visibility(self):

        return self._visibility

    @visibility.setter
    def visibility(self, value):

        if not isinstance(value, bool):
            raise QgistTypeError(translate('global', '"visibility" must be bool. (dtype_uielement visibility)'))

        self._visibility = value

    @staticmethod
    def from_uiobject(uiobject):

        if not (isinstance(uiobject, QToolBar) or isinstance(uiobject, QDockWidget)):
            raise QgistTypeError(translate('global', '"uiobject" must be either QToolBar or QDockWidget. (dtype_uielement from_uiobject)'))

        return dtype_uielement_class(
            name_internal = str(uiobject.objectName()),
            name_translated = str(uiobject.windowTitle()),
            visibility = bool(uiobject.isVisible()),
            uiobject = uiobject,
            )
