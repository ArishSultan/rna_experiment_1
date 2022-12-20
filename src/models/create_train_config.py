import uuid
import click


@click.command()
@click.argument('filename', type=str, default='ml_experiment.yaml')
def main(filename):
    with open(filename, 'w') as file:
        file.write(f'id: {uuid.uuid4()}\n')
        file.write('algorithms:\n')
        file.write('  -\n')


if __name__ == '__main__':
    main()
