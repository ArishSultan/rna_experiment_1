import os
import shutil
from src.utils.prepare_cwd import prepare_cwd


def main():
    if os.path.exists('models'):
        shutil.rmtree('models')

    if os.path.exists('reports'):
        shutil.rmtree('reports')

    os.mkdir('models')
    os.mkdir('reports')
    os.mkdir('reports/figures')


if __name__ == '__main__':
    prepare_cwd(__file__)
    main()
