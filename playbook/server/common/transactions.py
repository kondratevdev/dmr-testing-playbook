from collections.abc import Iterator
from contextlib import contextmanager
from typing import final

from django.db import transaction


@final
class TransactionAtomic:
    """Provide an atomic transaction as an injectable dependency."""

    @contextmanager
    def __call__(self) -> Iterator[None]:
        """Run the enclosed section in one database transaction."""
        with transaction.atomic():
            yield
