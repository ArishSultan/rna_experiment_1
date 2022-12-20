from typing import Any

from .kmer import generate_all_kmers
from ..encoding import Encoding
from ...data import DataTransformer
from ...utils import kmer_to_dict, get_nucleotides_from_kind


def encode_cksnap(sequence: str, gap: int = 0, kind: str = 'DNA', kmer_cache=None) -> tuple[Any, ...]:
    if gap < 0:
        raise '`gap` should be >= 0'

    encoded_seq = []
    kmers = generate_all_kmers(2, kind, False) if kmer_cache is None else kmer_cache
    nucleotides = get_nucleotides_from_kind(kind)

    for g in range(gap + 1):
        kmer_dict = kmer_to_dict(kmers, 0)

        seq_sum = 0
        for i in range(len(sequence)):
            j = i + g + 1
            if i < len(sequence) and j < len(sequence) and sequence[i] in nucleotides and sequence[j] in nucleotides:
                kmer_dict[sequence[i] + sequence[j]] = kmer_dict[sequence[i] + sequence[j]] + 1
                seq_sum = seq_sum + 1

        for kmer in kmers:
            if seq_sum != 0:
                encoded_seq.append(kmer_dict[kmer] / seq_sum)
            else:
                encoded_seq.append(0)

    return tuple(encoded_seq)


class CKSNAP(Encoding):
    def __init__(self, gap: int = 0, kind: str = 'DNA'):
        self._gap = gap
        self._kind = kind
        self._kmer_cache = DataTransformer.get_cache('kmer_2', lambda _: generate_all_kmers(k=2, kind=kind))

    @property
    def name(self):
        return f'cksnap_{self._gap}'

    def encode(self, sequence: str, label: bool = False):
        return encode_cksnap(sequence, self._gap, self._kind, kmer_cache=self._kmer_cache)
