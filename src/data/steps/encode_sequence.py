from typing import List
from pandas import DataFrame, concat, Series
from src.features.encoding import Encoding

from ..transformer import DataTransformerStep, DataTransformerResult


class EncodeSequence(DataTransformerStep):
    def __init__(self, encodings: List[Encoding]):
        self._encodings = encodings

    def _apply(self, result: DataTransformerResult) -> DataTransformerResult:
        new_result = DataTransformerResult()

        for key, value in result.iter():
            for encoding in self._encodings:
                print('\r\r\r\r' + encoding.name, end='')

                encoded_seq = []
                for row in value.iterrows():
                    encoded_seq.append(encoding.encode(row[1]['sequence'], row[1]['label']))

                encoded_features = DataFrame(
                    Series(encoded_seq).to_list(),
                    columns=_generate_column_names(len(encoded_seq[0]))
                )

                new_result.set(
                    f'{key}>{encoding.name}',
                    concat([encoded_features, value.drop('sequence', axis=1)], axis=1)
                )

        return new_result


def _generate_column_names(length: int):
    return [f'x{x + 1}' for x in range(length)]
