from typing import Any
from ..encoding import Encoding


EIIP_DICT = {
    'A': 0.1260,
    'C': 0.1340,
    'G': 0.0806,
    'T': 0.1335,
    'U': 0.1335,
}


def encode_eiip(sequence: str) -> tuple[float | Any]:
    return tuple(EIIP_DICT.get(nucleotide, 0.0) for nucleotide in sequence)


class EIIP(Encoding):
    @property
    def name(self):
        return 'eiip'

    def encode(self, sequence: str, label: bool = False) -> tuple[float | Any]:
        return encode_eiip(sequence)
