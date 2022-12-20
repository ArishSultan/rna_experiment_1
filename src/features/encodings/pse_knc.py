from ..encoding import Encoding


def encode_pse_knc(sequence):
    encoded_seq = []

    for i in range(len(sequence)):
        nucleotide = sequence[i]

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

        encoded_seq.append(sequence[:i].count(sequence[i]) / (i + 1))
    return encoded_seq


class PseKNC(Encoding):
    @property
    def name(self) -> str:
        return 'pse_knc'

    def encode(self, sequence: str, label: bool = False) -> tuple[float, ...]:
        return encode_pse_knc(sequence)

