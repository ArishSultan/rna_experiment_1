from collections import Counter

from .knc import encode_knc, KNC


def encode_nac(sequence: str):
    return encode_knc(sequence, 1)


class NAC(KNC):
    def __init__(self):
        super().__init__(1)
