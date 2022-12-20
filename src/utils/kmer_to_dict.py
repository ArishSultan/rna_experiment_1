from typing import Any


def kmer_to_dict(kmers: tuple[Any, ...] | list[Any, ...], initializer: str | int | float = 'index'):
    new_dict = {}

    for i in range(len(kmers)):
        new_dict[kmers[i]] = initializer if initializer != 'index' else i

    return new_dict
