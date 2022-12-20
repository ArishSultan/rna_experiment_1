from typing import Any
from ..encoding import Encoding


def encode_anf(sequence: str) -> tuple[Any, ...]:
    encoded_seq = []

    for j in range(len(sequence)):
        encoded_seq.append(sequence[0: j + 1].count(sequence[j]) / (j + 1))

    return tuple(encoded_seq)


class ANF(Encoding):
    @property
    def name(self):
        return 'anf'

    def encode(self, sequence: str, label: bool = False):
        return encode_anf(sequence)
