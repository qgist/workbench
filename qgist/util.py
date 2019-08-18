# -*- coding: utf-8 -*-

"""

QGIST WORK BENCH
QGis Plugin for Organizing Toolbars
https://github.com/qgist/workbench

    qgist/util.py: QGIST utilities

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
    QCoreApplication,
    QSettings,
    QTranslator,
)
from PyQt5.QtWidgets import QApplication


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT (Internal Dependencies)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from .error import QgistTranslationError


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINES: TRANSLATION
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def setupTranslation(translationsPath):
    """
    Setup translation system for current Qgis Plugin.
    TODO: add support for regions (e.g. English for US and UK)
    """

    def getTranslationPath(language):
        outPath = os.path.join(
            translationsPath, 'qgist_%s.qm' % language
        )
        if not os.path.exists(outPath):
            raise QgistTranslationError('Translation not found: %s' % outPath)
        return outPath

    userLocale = QSettings().value('locale/userLocale')
    if '_' in userLocale:
        language, region = userLocale.split('_')
    else:
        language, region = userLocale, None

    try:  # Try current language first
        localePath = getTranslationPath(language)
    except:  # Fall back to English
        try:
            localePath = getTranslationPath('en')
        except:
            return None, None

    translator = QTranslator()
    translator.load(localePath)
    QCoreApplication.installTranslator(translator)
    return translator, localePath

def translate(context, key):
    """
    http://pyqt.sourceforge.net/Docs/PyQt5/i18n.html#differences-between-pyqt5-and-qt
    """

    return QApplication.translate(context, key)
