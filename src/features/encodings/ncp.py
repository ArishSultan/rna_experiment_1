from typing import Any
from ..encoding import Encoding


def encode_ncp(sequence: str) -> tuple[Any, ...]:
    encoded_seq = []
    for nucleotide in sequence:
        match nucleotide:
            case 'A':
                encoded_seq += [1, 1, 1]
            case 'T':
                encoded_seq += [0, 0, 1]
            case 'U':
                encoded_seq += [0, 0, 1]
            case 'G':
                encoded_seq += [1, 0, 0]
            case 'C':
                encoded_seq += [0, 1, 0]

    return tuple(encoded_seq)


class NCP(Encoding):
    @property
    def name(self):
        return 'ncp'

    def encode(self, sequence: str, label: bool = False):
        return encode_ncp(sequence)
