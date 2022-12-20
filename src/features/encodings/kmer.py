from typing import Any
from itertools import product
from collections import Counter

from ..encoding import Encoding
from ...utils import get_seq_kind
from ...data.transformer import DataTransformer


def generate_all_kmers(k: int = 2, kind: str = 'DNA', upto: bool = False) -> tuple[Any, ...]:
    """
    Generate all possible nucleotide pairs of either DNA or RNA with length k, length of output
    is always 4^k, i.e. generate_kmers(2) produces 4^2 (16) mers.

    Example:
      * generate_kmers(2) -> AA,  AU,  AC,  AG ...
      * generate_kmers(3) -> AAA, AAU, AAC, AAG ...
      * ...

    :param k determines length of mers (must be > 0)
    :param kind determines the kind of sequence can be either DNA or RNA
    :param upto determines whether to generate all mers of length upto k i.e.
           generate_kmers(2, upto=True) will generate all mers of length 1 and 2
    """

    assert k > 0
    match kind:
        case 'DNA':
            nucleotides = 'ACGT'
        case 'RNA':
            nucleotides = 'ACGU'
        case _:
            print(f'WARNING: unsupported kind "{kind}", only '
                  'supported ones are DNA and RNA, will default to DNA')
            nucleotides = 'ATCG'

    if upto:
        repeats = list(range(1, k + 1))
    else:
        repeats = [k]

    results = []
    for i in repeats:
        results += [''.join(x) for x in product(nucleotides, repeat=i)]

    return tuple(results)


def generate_kmers(sequence: str, k: int = 2, upto: bool = False) -> tuple[Any, ...]:
    """
    Generate all possible nucleotide pairs of either DNA or RNA with length k, length of output
    is always 4^k, i.e. generate_kmers(2) produces 4^2 (16) mers.

    Example:
    * generate_kmers(2) -> AA,  AU,  AC,  AG ...
    * generate_kmers(3) -> AAA, AAU, AAC, AAG ...
    * ...

    :param sequence any DNA or RNA sequence
    :param k determines length of mers (must be > 0)
    :param upto determines whether to generate all mers of length upto k i.e.
           generate_kmers(2, upto=True) will generate all mers of length 1 and 2
    """

    assert k > 0

    if upto:
        repeats = list(range(1, k + 1))
    else:
        repeats = [k]

    results = []
    for i in repeats:
        results += [sequence[j: j + i] for j in range(len(sequence) - i + 1)]

    return tuple(results)


def encode_kmer(sequence: str, k: int = 2, upto: bool = False, normalize: bool = False, kmer_cache=None) \
        -> tuple[Any, ...]:
    """
    Encodes dna / rna sequence to kmers format.

    :param sequence any dna or rna sequence
    :param k determines length of mers (must be > 0)
    :param upto determines whether to generate all mers of length upto k i.e.
           generate_kmers(2, upto=True) will generate all mers of length 1 and 2
    :param normalize determines whether to normalize all the values or not
           (values are divided by average for normalization)
    :param kmer_cache khk
    """
    seq_mers = generate_kmers(sequence, k, upto)
    all_mers = generate_all_kmers(k, get_seq_kind(sequence), upto) if kmer_cache is None else kmer_cache

    counter = Counter()
    counter.update(seq_mers)

    result = []
    for mer in all_mers:
        if mer in counter:
            if normalize:
                result.append(counter[mer] / len(seq_mers))
            else:
                result.append(counter[mer])
        else:
            result.append(0)

    return tuple(result)


class Kmer(Encoding):
    def __init__(self, k: int = 2, upto: bool = False, normalize: bool = False, kind: str = 'DNA'):
        self._k = k
        self._upto = upto
        self._normalize = normalize
        self._kmer_cache = DataTransformer.get_cache(f'kmer_{k}', lambda _: generate_all_kmers(k=k, kind=kind))

    @property
    def name(self):
        return f'kmer{"_upto_" if self._upto else ""}_{self._k}{"_n" if self._normalize else ""}'

    def encode(self, sequence: str, label: bool = False):
        return encode_kmer(sequence, self._k, self._upto, self._normalize, kmer_cache=self._kmer_cache)


class KmerText(Encoding):
    def __init__(self, k: int = 2, upto: bool = False):
        self._k = k
        self._upto = upto

    @property
    def name(self):
        return f'kmer_text{"_upto_" if self._upto else ""}_{self._k}'

    def encode(self, sequence: str, label: bool = False):
        return generate_kmers(sequence, self._k, self._upto)
