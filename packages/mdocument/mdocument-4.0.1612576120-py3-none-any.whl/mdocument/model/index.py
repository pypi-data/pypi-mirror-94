import typing


class Index:
    def __init__(self, keys: typing.Tuple[typing.Tuple[str, int]], **kwargs):
        self.keys = keys
        self.kwargs = kwargs
        self.model = None
        self.name = None

    def __eq__(self, other):
        if isinstance(other, Index):
            return self.keys == other.keys and self.kwargs == other.kwargs
        return False

    def __hash__(self):
        return hash(self.keys) + hash(
            tuple([(key, value) for key, value in self.kwargs.items()])
        )

    def connect_to_model(self, model: typing.Type["Model"], name: str):
        """Saves field model relation."""

        self.model = model
        self.name = name
