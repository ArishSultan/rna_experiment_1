from ..encoding import Encoding


def encode_mwp_text(sequence: str):
    count = len(sequence) // 2
    return sequence[:count], sequence[count + 1:]


class MWPText(Encoding):
    @property
    def name(self) -> str:
        return 'mwp_text'

    def encode(self, sequence: str, label: bool = False) -> tuple[float, ...]:
        return encode_mwp_text(sequence)

