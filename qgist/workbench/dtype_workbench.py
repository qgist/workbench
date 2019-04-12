

class dtype_workbench_class:

    def __init__(self, name):

        self._name = name

    def asdict(self):

        return dict(
            name = self._name,
            ) # TODO
