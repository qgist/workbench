
# from .error import QgistUnnamedUiELement

class dtype_uielement_class:

    def __init__(self
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

        if not isinstance(existence, bool):
            raise TypeError('existence must be bool')
        self._existence = existence

    def as_dict(self):

        return dict(
            name_internal = self._name_internal,
            name_translated = self._name_translated,
            visibility = self._visibility,
            existence = self._existence,
            )

    def update_state(self, object_handle):

        pass

    @property
    def name_internal(self):

        return self._name_internal

    @name_internal.setter
    def name_internal(self, value):

        raise AttributeError('name_internal must not be changed')

    @staticmethod
    def from_uielement(self, uielement):

        return dtype_uielement_class(
            name_internal = uielement.objectName(),
            name_translated = uielement.windowTitle(),
            visibility = uielement.isVisible(),
            existence = True,
            )
