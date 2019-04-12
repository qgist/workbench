# -*- coding: utf-8 -*-

"""

QGIST WORK BENCH
QGis Plugin for Organizing Toolbars
https://github.com/qgist/workbench

    makefile.py: Helper routines for building and distributing the plugin

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
import subprocess

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CONST
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

TRANSLATION_FLD = 'i18n'


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# "PUBLIC" API
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def translate():
    tmpProFileName = 'qgist.pro'

    __writeProjectFile__(tmpProFileName)

    __runCommand__(['pylupdate5', '-noobsolete', '-verbose', tmpProFileName])
    __runCommand__(['lrelease-qt5', tmpProFileName])

    os.remove(tmpProFileName)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# INTERNAL ROUTINES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def __genQgistPythonFiles__():
    for path, _, filesList in os.walk('qgist'):
        for fileName in filesList:
            if not fileName.endswith('.py'):
                continue
            pythonFilePath = os.path.join(path, fileName)
            if not os.path.isfile(pythonFilePath):
                continue
            yield pythonFilePath


def __genQgistTranslationFiles__():
    for fileName in os.listdir(TRANSLATION_FLD):
        if not fileName.endswith('.ts'):
            continue
        translationPath = os.path.join(TRANSLATION_FLD, fileName)
        if not os.path.isfile(translationPath):
            continue
        yield translationPath


def __runCommand__(commandList):
    proc = subprocess.Popen(
        commandList, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    outs, errs = proc.communicate()
    print(outs.decode('utf-8'), errs.decode('utf-8'))


def __writeProjectFile__(fn):
    seperator = ' \\\n\t'

    with open(fn, 'w') as f:
        f.write(
            'SOURCES = %s\n\nTRANSLATIONS = %s\n' % (
                seperator.join(list(__genQgistPythonFiles__())),
                seperator.join(list(__genQgistTranslationFiles__()))
            )
        )
