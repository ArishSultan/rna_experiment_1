from ..encoding import Encoding


def encode_nd(sequence: str):
    """
    Encodes nucleotide sequence to ND (nucleotide density).

    :param sequence:
    :return:
    """
    result = []

    for i in range(len(sequence)):
        result.append(sequence[:i].count(sequence[i]) / (i + 1))

    return tuple(result)


class ND(Encoding):
    @property
    def name(self) -> str:
        return 'nd'

    def encode(self, sequence: str, label: bool = False) -> tuple[float, ...]:
        return encode_nd(sequence)
