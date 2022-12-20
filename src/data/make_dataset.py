from pathlib import Path

from pandas import read_csv

from src.utils.prepare_cwd import prepare_cwd
from src.features import encodings
from src.data import DataTransformer, steps


RAW_DATA_DIR = Path('data') / 'raw'
PROCESSED_DATA_DIR = Path('data') / 'processed'

FILES = {
    'H.sapiens100': True,
    'H.sapiens495': False,
    'M.musculus472': False,
    'S.cerevisiae100': True,
    'S.cerevisiae314': False,
}


def main():
    data_transformer = DataTransformer(steps=[
        steps.LabelRename(),
        steps.EncodeSequence(encodings=[
            encodings.ANF(),
            encodings.Binary(),
            encodings.CKSNAP(gap=2, kind='RNA'),
            encodings.CKSNAP(gap=3, kind='RNA'),
            encodings.CKSNAP(gap=4, kind='RNA'),
            encodings.EIIP(),
            encodings.ENAC(window=2),
            encodings.ENAC(window=3),
            encodings.ENAC(window=4),
            encodings.ENAC(window=5),
            encodings.ENAC(window=6),
            encodings.ENAC(window=7),
            encodings.Kmer(k=2, kind='RNA'),
            encodings.Kmer(k=3, kind='RNA'),
            encodings.Kmer(k=4, kind='RNA'),
            encodings.KmerText(k=1),
            encodings.KmerText(k=2),
            encodings.KmerText(k=3),
            encodings.KmerText(k=4),
            encodings.KNC(k=2),
            encodings.KNC(k=3),
            encodings.KNC(k=4),
            encodings.MCN(),
            encodings.MCN(split=True),
            encodings.NAC(),
            encodings.NCP(),
            encodings.ND(),
            encodings.PseEIIP(kind='RNA'),
            encodings.RCKmer(k=2),
            encodings.RCKmer(k=3),
            encodings.RCKmer(k=4),
            # encodings.PSDP(),
            # encodings.PseKNC(),
            # encodings.PSNP(),
            # encodings.PSTP(),
        ]),
        steps.Splitter(),
    ])

    for file, flag in FILES.items():
        filename = str(RAW_DATA_DIR / file) + '.csv'
        data = read_csv(filename, header='infer' if flag else None)

        print(file)
        result = data_transformer.transform(data)
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


if __name__ == '__main__':
    prepare_cwd(__file__)
    main()
