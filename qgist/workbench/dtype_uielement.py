# -*- coding: utf-8 -*-

"""

QGIST WORK BENCH
QGis Plugin for Organizing Toolbars
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
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class dtype_uielement_class:

    def __init__(self,
        name_internal = '',
        name_translated = '',
        visibility = True,
        existence = True,
        ):

        if not isinstance(name_internal, str):
            raise TypeError('internal name must be str')
        if len(name_internal) == 0:
            raise ValueError('unnamed UI element')
        self._name_internal = name_internal

        if not isinstance(name_translated, str):
            raise TypeError('translated name must be str')
        self._name_translated = name_translated

        if not isinstance(visibility, bool):
            raise TypeError('visibility must be bool')
        self._visibility = visibility

        self.existence = existence # type check in setter

    def as_dict(self):

        return dict(
            name_internal = self._name_internal,
            name_translated = self._name_translated,
            visibility = self._visibility,
            existence = self._existence,
            )

    def pull_state_from_uiobject(self, uiobject):

        if not (isinstance(uiobject, QToolBar) or isinstance(uiobject, QDockWidget)):
            raise TypeError('uiobject must be either QToolBar or QDockWidget')

        self.existence = True # type check in setter
        self._visibility = uiobject.isVisible()

    def push_state_to_uiobject(self, uiobject):

        if not (isinstance(uiobject, QToolBar) or isinstance(uiobject, QDockWidget)):
            raise TypeError('uiobject must be either QToolBar or QDockWidget')

        self.existence = True # type check in setter
        uiobject.setVisible(self._visibility)

    @property
    def existence(self):

        return self._existence

    @existence.setter
    def existence(self, value):

        if not isinstance(value, bool):
            raise TypeError('existence must be bool')

        self._existence = value

    @property
    def name_internal(self):

        return self._name_internal

    @name_internal.setter
    def name_internal(self, value):

        raise AttributeError('name_internal must not be changed')

    @staticmethod
    def from_uiobject(uiobject):

        if not (isinstance(uiobject, QToolBar) or isinstance(uiobject, QDockWidget)):
            raise TypeError('uiobject must be either QToolBar or QDockWidget')

        return dtype_uielement_class(
            name_internal = uiobject.objectName(),
            name_translated = uiobject.windowTitle(),
            visibility = uiobject.isVisible(),
            existence = True,
            )
