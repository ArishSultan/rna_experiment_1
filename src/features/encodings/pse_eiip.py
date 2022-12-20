from typing import Any

from .tnc import encode_tnc
from .eiip import EIIP_DICT
from .kmer import generate_all_kmers
from ..encoding import Encoding
from ...utils import get_seq_kind
from ...data.transformer import DataTransformer


def encode_pse_eiip(sequence: str, kmer_cache=None) -> tuple[Any, ...]:
    tnc = encode_tnc(sequence)
    tri_nucleotides = generate_all_kmers(3, get_seq_kind(sequence)) if kmer_cache is None else kmer_cache

    tnc_dict = {}
    eiip_dict = {}

    for i in range(len(tri_nucleotides)):
        item = tri_nucleotides[i]

        tnc_dict[item] = tnc[i]
        eiip_dict[item] = EIIP_DICT[item[0]] + EIIP_DICT[item[1]] + EIIP_DICT[item[2]]

    return tuple(eiip_dict[item] * tnc_dict[item] for item in tri_nucleotides)


class PseEIIP(Encoding):
    def __init__(self, kind='DNA'):
        self._kmer_cache = DataTransformer.get_cache('kmer_3', lambda _: generate_all_kmers(k=3, kind=kind))

    @property
    def name(self):
        return 'pse_eiip'

    def encode(self, sequence: str, label: bool = False):
        return encode_pse_eiip(sequence, self._kmer_cache)
