def get_seq_kind(sequence: str):
    if 'U' in sequence:
        return 'RNA'
    else:
        return 'DNA'


def get_nucleotides_from_kind(kind: str):
    if kind == 'DNA':
        return 'ACGT'
    else:
        return 'ACGU'
