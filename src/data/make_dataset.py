from pathlib import Path

from pandas import read_csv

from src.utils import prepare_cwd
from src.features import encodings
from src.data import DataTransformer, steps


RAW_DATA_DIR = Path('data') / 'raw'
PROCESSED_DATA_DIR = Path('data') / 'processed'

_HUMAN_FILE = {
    'H.sapiens100': True,
    'H.sapiens495': False,
}

_MOUSE_FILE = {'M.musculus472': False}

_YEAST_FILE = {
    'S.cerevisiae100': True,
    'S.cerevisiae314': False,
}

_FILES = {
    **_HUMAN_FILE,
    **_MOUSE_FILE,
    **_YEAST_FILE,
}


def _transform_and_save(files: dict, transformer: DataTransformer):
    for file, flag in files.items():
        filename = str(RAW_DATA_DIR / file) + '.csv'
        data = read_csv(filename, header='infer' if flag else None)

        print(file)
        result = transformer.transform(data)
        print()

        for key, value in result.iter():
            sub_path = key.replace('>', '/')
            if sub_path[0] == '/':
                sub_path = sub_path[1:]

            sub_path = Path(sub_path)

            filename = PROCESSED_DATA_DIR / file / sub_path.parent
            filename.mkdir(parents=True, exist_ok=True)

            if len(key) == 0:
                filename = filename / 'all'
            else:
                filename = filename / sub_path.name

            print('Writing', filename)
            value.to_csv(str(filename) + '.csv', index=False)


def main():
    _transform_and_save(_FILES, DataTransformer(steps=[
        steps.LabelRename(),
        steps.EncodeSequence(encodings=[
            encodings.MWPText(),
            encodings.ANF(),
            encodings.Binary(),
            encodings.CKSNAP(gap=1, kind='RNA'),
            encodings.CKSNAP(gap=2, kind='RNA'),
            encodings.CKSNAP(gap=3, kind='RNA'),
            encodings.CKSNAP(gap=4, kind='RNA'),
            encodings.CKSNAP(gap=5, kind='RNA'),
            encodings.EIIP(),
            encodings.ENAC(window=2),
            encodings.ENAC(window=3),
            encodings.ENAC(window=4),
            encodings.ENAC(window=5),
            encodings.ENAC(window=6),
            encodings.ENAC(window=7),
            encodings.Kmer(k=1, kind='RNA'),
            encodings.Kmer(k=2, kind='RNA'),
            encodings.Kmer(k=3, kind='RNA'),
            encodings.Kmer(k=4, kind='RNA'),
            encodings.Kmer(k=5, kind='RNA'),
            encodings.KmerText(k=1),
            encodings.KmerText(k=2),
            encodings.KmerText(k=3),
            encodings.KmerText(k=4),
            encodings.KNC(k=1),
            encodings.KNC(k=2),
            encodings.KNC(k=3),
            encodings.KNC(k=4),
            encodings.KNC(k=5),
            encodings.MCN(),
            encodings.MCN(split=True),
            encodings.NAC(),
            encodings.NCP(),
            encodings.ND(),
            encodings.PseEIIP(kind='RNA'),
            encodings.RCKmer(k=1),
            encodings.RCKmer(k=2),
            encodings.RCKmer(k=3),
            encodings.RCKmer(k=4),
            encodings.RCKmer(k=5),
            encodings.PseKNC(),
        ]),
        steps.Splitter(),
    ]))

    _transform_and_save(_HUMAN_FILE, DataTransformer(steps=[
        steps.LabelRename(),
        steps.EncodeSequence(encodings=[
            encodings.PSNP(species='hs'),
            encodings.PSDP(species='hs'),
            encodings.PSTP(species='hs'),
        ]),
        steps.Splitter(),
    ]))

    _transform_and_save(_MOUSE_FILE, DataTransformer(steps=[
        steps.LabelRename(),
        steps.EncodeSequence(encodings=[
            encodings.PSNP(species='mm'),
            encodings.PSDP(species='mm'),
            encodings.PSTP(species='mm'),
        ]),
        steps.Splitter(),
    ]))

    _transform_and_save(_YEAST_FILE, DataTransformer(steps=[
        steps.LabelRename(),
        steps.EncodeSequence(encodings=[
            encodings.PSNP(species='sc'),
            encodings.PSDP(species='sc'),
            encodings.PSTP(species='sc'),
        ]),
        steps.Splitter(),
    ]))


if __name__ == '__main__':
    prepare_cwd(__file__)
    main()
