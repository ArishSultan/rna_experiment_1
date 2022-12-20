from abc import ABC
from typing import List
from pandas import DataFrame


class InvalidOperationResultFinalization(Exception):
    def __init__(self):
        super().__init__('Do not finalize [OperationResult] manually'
                         ', it will be finalized automatically')


class DataTransformerResult:
    def __init__(self):
        self._dict = dict()
        self._finalized = False

    def iter(self):
        for key in self._dict:
            yield key, self._dict[key]

    def get(self, key: str):
        return self._dict[key]

    def set(self, key: str, value):
        DataTransformerResult._check_finalized(self)
        self._dict[key] = value

    def clear(self):
        DataTransformerResult._check_finalized(self)
        self._dict.clear()

    def finalize(self):
        DataTransformerResult._check_finalized(self)
        self._finalized = True

    @staticmethod
    def _check_finalized(self):
        if self._finalized:
            raise 'This result has been finalized and can not longer be mutated'


class DataTransformerStep(ABC):
    def _apply(self, result: DataTransformerResult) -> DataTransformerResult:
        pass

    def apply(self, result: DataTransformerResult) -> DataTransformerResult:
        return DataTransformerStep._finalize_result(self._apply(result))

    @staticmethod
    def _finalize_result(result: DataTransformerResult) -> DataTransformerResult:
        try:
            result.finalize()
        except InvalidOperationResultFinalization as error:
            raise error

        return result


def _prepare_data(value) -> DataTransformerResult:
    result = DataTransformerResult()
    result.set('', value)
    return result


class DataTransformer:
    cache = dict()

    @staticmethod
    def get_cache(key: str, value):
        if key in DataTransformer.cache:
            return DataTransformer.cache[key]
        else:
            resolved_value = value(None)
            DataTransformer.cache[key] = resolved_value
            return resolved_value

    def __init__(self, steps: List[DataTransformerStep]):
        self._steps = steps

    def transform(self, value: DataFrame) -> DataTransformerResult:
        result = _prepare_data(value)
        for step in self._steps:
            result = step.apply(result)

        return result
