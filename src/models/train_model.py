import json
import os.path

import yaml
import click
import hashlib
import seaborn as sns
from pathlib import Path
from pandas import read_csv
from sklearn.metrics import classification_report
from sklearn.model_selection import StratifiedKFold

from utils.make_model import make_model
from utils.model_variants import prepare_variants, make_variant_name
from utils.resolve_dataset import resolve_datasets, resolve_species
from src.utils.prepare_cwd import prepare_cwd
from src.visualization.visualize import generate_cv_auc

sns.set_style()


# def read_models(models_file: str):
#     if os.path.exists(models_file):
#         with open(models_file) as file:
#             return json.loads(file.read())
#     else:
#         return dict()
#
#
# def train_model(name, dataset, variant):
#     data = read_csv(dataset)
#     x = data.drop('label', axis=1)
#     y = data['label']
#
#     model = make_model(name, variant)
#     k_fold = StratifiedKFold(n_splits=10)
#
#     reports = []
#     for fold, (train, test) in enumerate(k_fold.split(x, y)):
#         model.fit(x.iloc[train], y.iloc[train])
#
#         y_true = y.iloc[test]
#         y_pred = model.predict(x.iloc[test])
#
#         reports.append((y_true, y_pred))
#
#     return reports
#
#
# def generate_classification_report(reports):
#     score_sum = classification_report(reports[0][0], reports[0][1], output_dict=True, zero_division=0)
#     for report in reports[1:]:
#         score = classification_report(report[0], report[1], output_dict=True, zero_division=0)
#
#         score_sum['0']['precision'] += score['0']['precision']
#         score_sum['0']['recall'] += score['0']['recall']
#         score_sum['0']['f1-score'] += score['0']['f1-score']
#         score_sum['0']['support'] += score['0']['support']
#
#         score_sum['1']['precision'] += score['1']['precision']
#         score_sum['1']['recall'] += score['1']['recall']
#         score_sum['1']['f1-score'] += score['1']['f1-score']
#         score_sum['1']['support'] += score['1']['support']
#
#         score_sum['accuracy'] += score['accuracy']
#
#         score_sum['macro avg']['precision'] += score['macro avg']['precision']
#         score_sum['macro avg']['recall'] += score['macro avg']['recall']
#         score_sum['macro avg']['f1-score'] += score['macro avg']['f1-score']
#         score_sum['macro avg']['support'] += score['macro avg']['support']
#
#         score_sum['weighted avg']['precision'] += score['weighted avg']['precision']
#         score_sum['weighted avg']['recall'] += score['weighted avg']['recall']
#         score_sum['weighted avg']['f1-score'] += score['weighted avg']['f1-score']
#         score_sum['weighted avg']['support'] += score['weighted avg']['support']
#
#     score_sum['0']['precision'] /= len(reports)
#     score_sum['0']['recall'] /= len(reports)
#     score_sum['0']['f1-score'] /= len(reports)
#     score_sum['0']['support'] /= len(reports)
#
#     score_sum['1']['precision'] /= len(reports)
#     score_sum['1']['recall'] /= len(reports)
#     score_sum['1']['f1-score'] /= len(reports)
#     score_sum['1']['support'] /= len(reports)
#
#     score_sum['accuracy'] /= len(reports)
#
#     score_sum['macro avg']['precision'] /= len(reports)
#     score_sum['macro avg']['recall'] /= len(reports)
#     score_sum['macro avg']['f1-score'] /= len(reports)
#     score_sum['macro avg']['support'] /= len(reports)
#
#     score_sum['weighted avg']['precision'] /= len(reports)
#     score_sum['weighted avg']['recall'] /= len(reports)
#     score_sum['weighted avg']['f1-score'] /= len(reports)
#     score_sum['weighted avg']['support'] /= len(reports)
#
#     return score_sum

def read_history(history_file: Path):
    if history_file.exists():
        file = open(history_file)
        history_data = json.load(file)
        file.close()

        return history_data
    else:
        return dict()


def load_config_file(input_file):
    file = open(input_file)
    file_data = yaml.load(file, yaml.SafeLoader)
    file.close()

    return file_data


@click.command()
@click.argument('cleanup', type=bool, default=False)
@click.argument('input_file', type=click.Path(exists=True))
@click.argument('models_dir', type=click.Path(exists=True))
@click.argument('reports_dir', type=click.Path(exists=True))
def main(input_file, model_dir, report_dir, cleanup):
    config = load_config_file(input_file)

    models_history = read_history(Path(model_dir) / f'{config["id"]}.json')
    reports_history = read_history(Path(report_dir) / f'{config["id"]}.json')

    # for algorithm in file_data['algorithms']:
    #     name = algorithm['name']
    #     props = algorithm['props']
    #     species = algorithm.get('species', 'all')
    #     encodings = algorithm.get('encodings', 'numeric')
    #     extra_props = algorithm.get('extra_props', dict())
    #     ignore_combinations = algorithm.get('ignore_combinations', list())
    #
    #     variants = prepare_variants(props, extra_props, ignore_combinations)
    #     species = list(resolve_species(species))
    #     datasets = list(resolve_datasets(species, encodings))
    #
    #     for dataset in datasets:
    #         dataset = str(Path(dataset))
    #         for (variant, extra_props) in variants:
    #             variant_name = make_variant_name(name, dataset, variant)
    #             variant_name_hash = hashlib.md5(variant_name.encode()).hexdigest()
    #
    #             print(f'[TRAINING] {variant_name}', end='')
    #             if variant_name_hash in model_data:
    #                 print('\r\r\r\r\r\r\r\r\r\r\r\r\r', end='')
    #                 print(f'[SKIPPING] {variant_name}')
    #                 continue
    #
    #             reports = train_model(name, dataset, variant | extra_props)
    #             reports_data[variant_name_hash] = generate_classification_report(reports)
    #             generate_cv_auc(reports, variant_name_hash)
    #
    #             model_data[variant_name_hash] = {
    #                 'name': name,
    #                 'variant': variant,
    #                 'dataset': dataset,
    #                 'id': variant_name,
    #             }
    #
    #             with open(f'{model_dir}/{file_id}.json', 'w') as file:
    #                 file.write(json.dumps(model_data))
    #                 file.flush()
    #
    #             with open(f'{report_dir}/{file_id}.json', 'w') as file:
    #                 file.write(json.dumps(reports_data))
    #                 file.flush()
    #
    #             print('\r\r\r\r\r\r\r\r\r\r\r\r\r', end='')
    #             print(f'[TRAINED] {variant_name}')


if __name__ == '__main__':
    prepare_cwd(__file__)
    main()
