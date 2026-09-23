import importlib
from typing import Any, final

import punq


class HasContainer:
    """Provide a per-controller dependency container."""

    __slots__ = ('_container',)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Populate dependencies before constructing a controller."""
        super().__init__(*args, **kwargs)
        implemented = importlib.import_module('server.implemented')
        self._container = implemented.populate_dependencies(punq.Container())

    @final
    def resolve[Thing](self, thing: type[Thing]) -> Thing:
        """Resolve an application dependency."""
        return self._container.resolve(thing)  # type: ignore[no-any-return]
