
from .error import QgistUnnamedUiELement

class dtype_uielement_class:

    def __init__(self
        name_internal = '',
        name_translated = '',
        visibility = True,
        existence = True,
        # handle = None,
        ):

        if not isinstance(name_internal, str):
            raise TypeError('internal name must be str')
        if not isinstance(name_translated, str):
            raise TypeError('translated name must be str')
        if not isinstance(visibility, bool):
            raise TypeError('visibility must be bool')
        if not isinstance(existence, bool):
            raise TypeError('existence must be bool')

        if len(name_internal) == 0:
            QgistUnnamedUiELement('Unnamed UI element: "%s" / "%s"' % (name_internal, name_translated))

        self._name_internal = name_internal
        self._name_translated = name_translated
        self._visibility = visibility
        self._existence = existence
        # self._handle = handle # Handle on actual object

    def set_state(self, object_handle):

        pass

    def asdict(self):

        return dict(
            name_internal = self._name_internal,
            name_translated = self._name_translated,
            visibility = self._visibility,
            existence = self._existence,
            )