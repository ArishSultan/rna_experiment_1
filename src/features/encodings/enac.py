from typing import Any

from collections import Counter
from ..encoding import Encoding
from ...utils import get_nucleotides_from_kind, get_seq_kind


def encode_enac(sequence: str, window: int = 5) -> tuple[Any, ...]:
    encoded_seq = []

    nucleotides = get_nucleotides_from_kind(get_seq_kind(sequence))
    for j in range(len(sequence)):
        if j < len(sequence) and j + window <= len(sequence):
            count = Counter(sequence[j:j + window])

            for nucleotide in nucleotides:
                encoded_seq.append(count[nucleotide] / len(sequence[j:j + window]))

    return tuple(encoded_seq)


class ENAC(Encoding):
    def __init__(self, window: int = 5):
        self._window = window

    @property
    def name(self):
        return f'enac_{self._window}'

    def encode(self, sequence: str, label: bool = False):
        return encode_enac(sequence, self._window)
