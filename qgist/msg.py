# -*- coding: utf-8 -*-

"""

QGIST WORK BENCH
QGis Plugin for Organizing Toolbars
https://github.com/qgist/workbench

    qgist/msg.py: QGIST ui error messages

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

from PyQt5.Qt import QWidget
from PyQt5.QtWidgets import QMessageBox


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT (Internal)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from .error import QgistTypeError
from .util import translate


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def msg_critical(exception, widget = None):

    _msg('critical', translate('global', 'Critical error'), exception, widget)

def msg_warning(exception, widget = None):

    _msg('warning', translate('global', 'Warning'), exception, widget)

def _msg(msg_type, msg_title, exception, widget = None):

    if not isinstance(exception, Exception):
        raise QgistTypeError(translate('global', '"exception" must be of type Exception. (msg)'))
    if not isinstance(widget, QWidget) and widget is not None:
        raise QgistTypeError(translate('global', '"widget" must be of type QWidget or None. (msg)'))

    if len(exception.args) == 0:
        msg = translate('global', 'Internal error. No description can be provided. Please file a bug. (msg)')
    else:
        msg = str(exception.args[0])

    getattr(QMessageBox, msg_type)(
        widget,
        msg_title,
        msg,
        QMessageBox.Ok
        )
