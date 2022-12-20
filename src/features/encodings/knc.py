from typing import Any

from .kmer import encode_kmer, generate_all_kmers
from ..encoding import Encoding
from ...data import DataTransformer


def encode_knc(sequence: str, k: int = 2, kmer_cache=None) -> tuple[Any, ...]:
    return encode_kmer(sequence, k, upto=False, normalize=True, kmer_cache=kmer_cache)


class KNC(Encoding):
    def __init__(self, k: int = 2, kind='DNA'):
        if k < 1:
            raise 'K should be greater than 0'

        self._k = k
        self._kmer_cache = DataTransformer.get_cache(f'kmer_{k}', lambda _: generate_all_kmers(k=k, kind=kind))

    @property
    def name(self):
        if self._k == 1:
            return 'nac'
        elif self._k == 2:
            return 'dnc'
        elif self._k == 3:
            return 'tnc'
        return f'knc_{self._k}'

    def encode(self, sequence: str, label: bool = False):
        return encode_knc(sequence, self._k, kmer_cache=self._kmer_cache)
