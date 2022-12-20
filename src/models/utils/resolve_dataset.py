import os
import glob


def resolve_species(species):
    if species == 'all':
        return os.listdir('data/processed')
    elif species == 'human':
        return filter(lambda x: 'H.sapiens' in x, os.listdir('data/processed'))
    elif species == 'mouse':
        return filter(lambda x: 'M.musculus' in x, os.listdir('data/processed'))
    elif species == 'yeast':
        return filter(lambda x: 'S.cerevisiae' in x, os.listdir('data/processed'))
    elif type(species) == list:
        return species


def resolve_datasets(species, encodings):
    if encodings == 'all':
        results = glob.iglob(f'data/processed/**/all.csv', recursive=True)
    elif encodings == 'numeric':
        results = filter(
            lambda x: 'text' not in x and 'mcn' not in x,
            glob.iglob(f'data/processed/**/all.csv', recursive=True)
        )
    elif encodings == 'text':
        results = filter(lambda x: 'text' in x, glob.iglob(f'data/processed/**/all.csv', recursive=True))
    elif type(encodings) == list:
        results = []
        temp_results = glob.iglob(f'data/processed/**/all.csv', recursive=True)

        for result in temp_results:
            for encoding in encodings:
                if encoding in result:
                    results.append(result)
    else:
        results = []

    for result in results:
        for specie in species:
            if specie in result:
                yield result
                break
