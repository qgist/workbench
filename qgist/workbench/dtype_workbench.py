
import base64

from .dtype_uielement import dtype_uielement_class

from PyQt5.QtWidgets import (
    QDockWidget,
    QMainWindow,
    QToolBar,
    )

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

        mainwindow.restoreState(self._mainwindow_state) # TODO ... check!

    def save(self, mainwindow):

        if not isinstance(mainwindow, QMainWindow):
            raise TypeError('mainwindow must be a QGis mainwindow')

        self._mainwindow_state = mainwindow.saveState() # TODO ... check!

    def as_dict(self):

        return dict(
            name = self._name,
            mainwindow_state = base64.encodebytes(self._mainwindow_state).decode('ASCII'),
            toolbars_list = [item.as_dict() for item in self._toolbars_dict.values()],
            dockwidgets_list = [item.as_dict() for item in self._dockwidgets_dict.values()],
            )

    @staticmethod
    def _activate_uielements(uiobjects_dict, uielements_dict):

        for name_internal, uiobject in uiobjects_dict:
            try:
                uielements_dict[name_internal].update_state(uiobject)
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
    def from_mainwindow(
        name = '',
        mainwindow = None,
        ):

        if not isinstance(mainwindow, QMainWindow):
            raise TypeError('mainwindow must be a QGis mainwindow')

        toolbars_list = [
            dtype_uielement_class.from_uiobject(uiobject)
            for _, uiobject in dtype_workbench_class._get_uielements_from_mainwindow(mainwindow, QToolBar)
            ]

        dockwidgets_list = [
            dtype_uielement_class.from_uiobject(uiobject)
            for _, uiobject in dtype_workbench_class._get_uielements_from_mainwindow(mainwindow, QDockWidget)
            ]

        mainwindow_state = mainwindow.saveState()

        return dtype_workbench_class(
            name = name,
            mainwindow_state = mainwindow_state,
            toolbars_list = toolbars_list,
            dockwidgets_list = dockwidgets_list,
            )
