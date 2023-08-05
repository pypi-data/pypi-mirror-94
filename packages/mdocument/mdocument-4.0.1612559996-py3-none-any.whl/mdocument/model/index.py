import typing


class Index:
    def __init__(self, keys: typing.Tuple[typing.Tuple[str, int]], **kwargs):
        self.keys = keys
        self.kwargs = kwargs

    def __eq__(self, other):
        if isinstance(other, Index):
            return self.keys == other.keys and self.kwargs == other.kwargs
        return False

    def __hash__(self):
        return hash(self.keys) + hash(
            tuple([(key, value) for key, value in self.kwargs.items()])
        )
