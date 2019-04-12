
"""

# Only those are enable which are having "QGistApp" as prent
# i.e. only toolbars from QGIS main window and not from sub widgets.
currentToolBarWidget = [
    toolbar for toolbar in self.mMainWindow.findChildren(
        QToolBar, toolBarName
    ) if toolbar.parent().objectName() == 'QgisApp'
]

mw = iface.mainWindow()
tb_list = mw.findChildren(QToolBar)
dw_list = mw.findChildren(QDockWidget)

tb_list[0].windowTitle() # übersetzt
tb_list[0].objectName() # intern
dw_list[0].windowTitle()
dw_list[0].objectName()

sm = [i for i in mw.findChildren(QMenu) if i.objectName() == 'mSettingsMenu'][0]
sm_actions = [i for i in sm.actions()]

h[1].text() # dockwidgets
h[2].text() # toolbars

"""

class workbench:

    def __init__(self, iface, plugin_root_fld, os_name):
        pass
