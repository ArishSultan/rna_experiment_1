from ..encoding import Encoding


def encode_mcn(sequence: str, is_modified: bool = False, split: bool = True):
    center = len(sequence) // 2
    new_sequence = sequence[:center] + ('Y' if is_modified else 'N') + sequence[center + 1:]
    # new_sequence = sequence

    if split:
        return tuple(new_sequence)
    else:
        return tuple([new_sequence])


class MCN(Encoding):
    def __init__(self, split: bool = True):
        self._split = split

    @property
    def name(self) -> str:
        return 'mcn'

    def encode(self, sequence: str, label: bool = False) -> tuple[str]:
        return encode_mcn(sequence, is_modified=label, split=self._split)
