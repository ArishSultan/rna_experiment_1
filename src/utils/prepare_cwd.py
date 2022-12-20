import os
from pathlib import Path


def prepare_cwd(file):
    file = Path(file)

    while file.name != 'rna_modification':
        file = file.parent

    os.chdir(file)
