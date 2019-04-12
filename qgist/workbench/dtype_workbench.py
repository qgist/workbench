
import base64

from PyQt5.QtWidgets import (
    QDockWidget,
    QToolBar,
    )

from .dtype_uielement import dtype_uielement_class

class dtype_workbench_class:

    def __init__(self,
        name = '',
        state_mainwindow = None,
        list_toolbars = None,
        list_dockwidgets = None,
        main_window = None, # OPTIONAL
        ):

        if not isinstance(name, str):
            raise TypeError('name must be str')
        if len(name) == 0:
            raise ValueError('name must not be empty')
        self._name = name

        if main_window is not None and any([
            state_mainwindow is not None,
            list_toolbars is not None,
            list_dockwidgets is not None,
            ]):
            raise ValueError('provide main_window OR state_mainwindow,list_toolbars,list_dockwidgets')

        if main_window is not None:
            self._state_mainwindow = bytes(main_window.saveState())
        elif isinstance(state_mainwindow, str):
            self._state_mainwindow = base64.decodebytes(state_mainwindow.encode('ASCII'))
        elif isinstance(state_mainwindow, bytes):
            self._state_mainwindow = base64.decodebytes(state_mainwindow)
        else:
            raise TypeError('state_mainwindow must either be str or bytes')

        if main_window is not None:
            pass # TODO add defaults
        elif isinstance(list_toolbars, list) and isinstance(list_dockwidgets, list):
            if any([not isinstance(item, dict) for item in list_toolbars])
                raise TypeError('items in list_toolbars must be dicts')
            if any([not isinstance(item, dict) for item in list_dockwidgets])
                raise TypeError('items in list_dockwidgets must be dicts')
            self._list_toolbars = [dtype_uielement_class(**item) for item in list_toolbars]
            self._list_dockwidgets = [dtype_uielement_class(**item) for item in list_dockwidgets]
        else:
            raise TypeError('list_toolbars and list_dockwidgets must be lists')

    def activate(self, main_window):

        tb_list = self._get_toolbars_from_mainwindow(main_window)
        dw_list = self._get_dockwidgets_from_mainwindow(main_window)

        # 

        main_window.restoreState(self._state_mainwindow)

    def as_dict(self):

        return dict(
            name = self._name,
            state_mainwindow = base64.encodebytes(self._state_mainwindow).decode('ASCII'),
            list_toolbars = [item.as_dict() for item in self._list_toolbars],
            list_dockwidgets = [item.as_dict() for item in self._list_toolbars],
            )

    @staticmethod
    def _get_toolbars_from_mainwindow(main_window):

        return [
            toolbar
            for toolbar in main_window.findChildren(QToolBar)
            if toolbar.parent().objectName() == 'QgisApp'
            ]

    @staticmethod
    def _get_dockwidgets_from_mainwindow(main_window):

        return [
            toolbar
            for toolbar in main_window.findChildren(QDockWidget)
            if toolbar.parent().objectName() == 'QgisApp'
            ]

    @staticmethod
    def from_data(
        name = '',
        state_mainwindow = None,
        list_toolbars = None,
        list_dockwidgets = None,
        ):

        return dtype_workbench_class(name, state_mainwindow, list_toolbars, list_dockwidgets)

    @staticmethod
    def from_mainwindow(
        name = '',
        main_window = None,
        ):

        return dtype_workbench_class(name, main_window = main_window)
