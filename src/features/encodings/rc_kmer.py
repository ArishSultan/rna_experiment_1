import itertools
from typing import Any
from collections import Counter
from ..encoding import Encoding


def kmerArray(sequence, k):
    kmer = []
    for i in range(len(sequence) - k + 1):
        kmer.append(sequence[i:i + k])
    return kmer


def RC(kmer):
    myDict = {
        'A': 'T',
        'C': 'G',
        'G': 'C',
        'T': 'A'
    }
    return ''.join([myDict[nc] for nc in kmer[::-1]])


def generateRCKmer(kmerList):
    rckmerList = set()
    myDict = {
        'A': 'T',
        'C': 'G',
        'G': 'C',
        'T': 'A'
    }
    for kmer in kmerList:
        rckmerList.add(sorted([kmer, ''.join([myDict[nc] for nc in kmer[::-1]])])[0])
    return sorted(rckmerList)


def encode_rc_kmer(sequence, k=2, upto=False, normalize=True):
    encoding = []
    header = ['#', 'label']
    NA = 'ACGT'

    if k < 1:
        print('Error: the k-mer value should larger than 0.')
        return 0

    if upto == True:
        for tmpK in range(1, k + 1):
            tmpHeader = []
            for kmer in itertools.product(NA, repeat=tmpK):
                tmpHeader.append(''.join(kmer))
            header = header + generateRCKmer(tmpHeader)
        myDict = {}
        for kmer in header[2:]:
            rckmer = RC(kmer)
            if kmer != rckmer:
                myDict[rckmer] = kmer
        # encoding.append(header)
        count = Counter()
        for tmpK in range(1, k + 1):
            kmers = kmerArray(sequence, tmpK)
            for j in range(len(kmers)):
                if kmers[j] in myDict:
                    kmers[j] = myDict[kmers[j]]
            count.update(kmers)
            if normalize == True:
                for key in count:
                    if len(key) == tmpK:
                        count[key] = count[key] / len(kmers)
        code = []
        for j in range(2, len(header)):
            if header[j] in count:
                code.append(count[header[j]])
            else:
                code.append(0)
        encoding.append(code)
    else:
        tmpHeader = []
        for kmer in itertools.product(NA, repeat=k):
            tmpHeader.append(''.join(kmer))
        header = header + generateRCKmer(tmpHeader)
        myDict = {}
        for kmer in header[2:]:
            rckmer = RC(kmer)

            if kmer != rckmer:
                myDict[rckmer] = kmer

        # encoding.append(header)
        kmers = kmerArray(sequence, k)
        for j in range(len(kmers)):
            if kmers[j] in myDict:
                kmers[j] = myDict[kmers[j]]
        count = Counter()
        count.update(kmers)
        if normalize == True:
            for key in count:
                count[key] = count[key] / len(kmers)
        code = []
        for j in range(2, len(header)):
            if header[j] in count:
                code.append(count[header[j]])
            else:
                code.append(0)
        encoding.append(code)
    return tuple(encoding[0])


class RCKmer(Encoding):
    def __init__(self, k=2, upto=False, normalize=True):
        if k < 1:
            raise '`k` should >= 1'

        self._k = k
        self._upto = upto
        self._normalize = normalize

    @property
    def name(self):
        return f'rc_kmer{"_upto_" if self._upto else ""}_{self._k}'

    def encode(self, sequence: str, label: bool = False) -> tuple[Any, ...]:
        return encode_rc_kmer(sequence)
