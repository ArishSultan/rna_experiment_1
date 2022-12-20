from ..transformer import DataTransformerStep, DataTransformerResult
from sklearn.model_selection import train_test_split
from pandas import concat


class Splitter(DataTransformerStep):
    def _apply(self, result: DataTransformerResult) -> DataTransformerResult:
        new_result = DataTransformerResult()

        for key, value in result.iter():
            if 'set' in value.columns:
                new_result.set(
                    f'{key}>train',
                    value[value['set'] == 'train'].drop('set', axis=1)
                )
                new_result.set(
                    f'{key}>valid',
                    value[value['set'] == 'valid'].drop('set', axis=1)
                )
                new_result.set(
                    f'{key}>test',
                    value[value['set'] == 'test'].drop('set', axis=1)
                )
                new_result.set(f'{key}>all', value.drop('set', axis=1))
            else:
                new_result.set(f'{key}>all', value)

                x_train, x_test, y_train, y_test = train_test_split(
                    value.drop('label', axis=1), value['label'],
                    test_size=.2, train_size=.8
                )
                new_result.set(
                    f'{key}>test',
                    concat([x_test, y_test], axis=1)
                )

                x_train, x_valid, y_train, y_valid = train_test_split(
                    x_train, y_train,
                    test_size=.1, train_size=.9
                )

                new_result.set(
                    f'{key}>train',
                    concat([x_train, y_train], axis=1)
                )
                new_result.set(
                    f'{key}>valid',
                    concat([x_valid, y_valid], axis=1)
                )



        return new_result
