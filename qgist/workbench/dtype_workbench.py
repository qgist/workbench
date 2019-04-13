
import base64

from .dtype_uielement import dtype_uielement_class

from PyQt5.QtWidgets import (
    QDockWidget,
    QToolBar,
    )

class dtype_workbench_class:

    def __init__(self,
        name = '',
        mainwindow_state = None,
        toolbars_list = None,
        dockwidgets_list = None,
        main_window = None, # OPTIONAL
        ):

        if not isinstance(name, str):
            raise TypeError('name must be str')
        if len(name) == 0:
            raise ValueError('name must not be empty')
        self._name = name

        if main_window is not None and any([
            mainwindow_state is not None,
            toolbars_list is not None,
            dockwidgets_list is not None,
            ]):
            raise ValueError('provide main_window OR mainwindow_state,toolbars_list,dockwidgets_list')

        if main_window is not None:
            self._state_mainwindow = bytes(main_window.saveState())
        elif isinstance(mainwindow_state, str):
            self._state_mainwindow = base64.decodebytes(mainwindow_state.encode('ASCII'))
        elif isinstance(mainwindow_state, bytes):
            self._state_mainwindow = base64.decodebytes(mainwindow_state)
        else:
            raise TypeError('mainwindow_state must either be str or bytes')

        if main_window is not None:
            pass # TODO add defaults
        elif isinstance(toolbars_list, list) and isinstance(dockwidgets_list, list):
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
        else:
            raise TypeError('toolbars_list and dockwidgets_list must be lists')

    def activate(self, main_window):

        qtoolbars_dict = self._get_uielements_from_mainwindow(main_window, QToolBar)
        qdockwidgets_dict = self._get_uielements_from_mainwindow(main_window, QDockWidget)

        self._activate_uielements(qtoolbars_dict, self._toolbars_dict)
        self._activate_uielements(qdockwidgets_dict, self._dockwidgets_dict)

        main_window.restoreState(self._state_mainwindow) # TODO ... check!

    def as_dict(self):

        return dict(
            name = self._name,
            mainwindow_state = base64.encodebytes(self._state_mainwindow).decode('ASCII'),
            toolbars_list = [item.as_dict() for item in self._toolbars_dict.values()],
            dockwidgets_list = [item.as_dict() for item in self._dockwidgets_dict.values()],
            )

    @staticmethod
    def _activate_uielements(uiobjects_dict, uielements_dict)

        for name_internal, uiobject in uiobjects_dict:
            try:
                uielements_dict[name_internal].update_state(uiobject)
            except KeyError:
                uielement = dtype_uielement_class.from_uiobject(uiobject)
                uielements_dict[uielement.name_internal] = uielement
        for name_internal in (uielements_dict.keys() - uiobjects_dict.keys()):
            uielements_dict[name_internal].existence = False

    @staticmethod
    def _get_uielements_from_mainwindow(main_window, uielement_type):

        return {
            toolbar.objectName(): toolbar
            for toolbar in main_window.findChildren(uielement_type)
            if toolbar.parent().objectName() == 'QgisApp'
            }

    @staticmethod
    def from_data(
        name = '',
        mainwindow_state = None,
        toolbars_list = None,
        dockwidgets_list = None,
        ):

        return dtype_workbench_class(name, mainwindow_state, toolbars_list, dockwidgets_list)

    @staticmethod
    def from_mainwindow(
        name = '',
        main_window = None,
        ):

        return dtype_workbench_class(name, main_window = main_window)
