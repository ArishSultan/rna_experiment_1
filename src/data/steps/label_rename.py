from ..transformer import DataTransformerStep, DataTransformerResult


class LabelRename(DataTransformerStep):
    def _apply(self, result: DataTransformerResult) -> DataTransformerResult:
        new_result = DataTransformerResult()

        for key, value in result.iter():
            if len(value.columns) > 2:
                new_value = value.rename(columns={'class': 'label'})
                new_value['label'] = new_value['label'].replace({'POS': 1, 'Neg': 0})
            else:
                new_value = value.rename(columns={0: 'sequence', 1: 'label'})

            new_result.set(key, new_value)

        return new_result
