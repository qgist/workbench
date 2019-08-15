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
# CLASS: WORKBENCH CORE
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class workbench:

    def __init__(self, iface, plugin_root_fld):

        if not hasattr(iface, 'mainWindow'):
            raise TypeError('iface must be a QGIS iface object')
        if not isinstance(plugin_root_fld, str):
            raise TypeError('plugin_root_fld must be str')
        if not os.path.exists(plugin_root_fld):
            raise TypeError('plugin_root_fld must exists')
        if not os.path.isdir(plugin_root_fld):
            raise TypeError('plugin_root_fld must be a directory')

        self._iface = iface
        self._plugin_root_fld = plugin_root_fld

        self._system = platform.system()

    def initGui(self):
        """
        QGis Plugin Interface Routine
        """

        pass

    def unload(self):
        """
        QGis Plugin Interface Routine
        """

        pass
