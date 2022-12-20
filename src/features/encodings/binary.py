from typing import Any
from ..encoding import Encoding


def encode_binary(sequence: str) -> tuple[Any, ...]:
    encoded_seq = []

    for nucleotide in sequence:
        match nucleotide:
            case 'A':
                encoded_seq += [1, 0, 0, 0]
            case 'C':
                encoded_seq += [0, 1, 0, 0]
            case 'G':
                encoded_seq += [0, 0, 1, 0]
            case 'U':
                encoded_seq += [0, 0, 0, 1]
            case 'T':
                encoded_seq += [0, 0, 0, 1]
            case _:
                encoded_seq += [0, 0, 0, 0]

    return tuple(encoded_seq)


class Binary(Encoding):
    @property
    def name(self):
        return 'binary'

    def encode(self, sequence: str, label: bool = False):
        return encode_binary(sequence)
