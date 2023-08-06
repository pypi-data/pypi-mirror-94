from typing import Mapping, Container, Iterator, Tuple, TypeVar

T = TypeVar('T')
U = TypeVar('U')


def filter_keys(source: Mapping[T, U], keys: Container[T]) -> Iterator[Tuple[T, U]]:
    """return the kvps from source if the key is in keys."""
    yield from ((k, source[k]) for k in source if k in keys)
