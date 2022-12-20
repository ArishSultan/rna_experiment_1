from typing import Any

from .knc import encode_knc, KNC


def encode_tnc(sequence: str) -> tuple[Any, ...]:
    return encode_knc(sequence, 3)


class TNC(KNC):
    def __init__(self):
        super().__init__(3)
