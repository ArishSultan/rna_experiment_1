_BASE_URL = "https://raw.githubusercontent.com/jerryji1993/DNABERT/master/src/transformers/dnabert-config"

VOCAB_FILES_NAMES = {"vocab_file": "vocab.txt"}

PRETRAINED_VOCAB_FILES_MAP = {
    "vocab_file": {
        # TODO: Try uncommenting if not work
        # "dna3": "bert-config-3/vocab.txt",
        "dna3": f"{_BASE_URL}/bert-config-3/vocab.txt",
        "dna4": f"{_BASE_URL}/bert-config-4/vocab.txt",
        "dna5": f"{_BASE_URL}/bert-config-5/vocab.txt",
        "dna6": f"{_BASE_URL}/bert-config-6/vocab.txt"
    }
}

PRETRAINED_POSITIONAL_EMBEDDINGS_SIZES = {
    "dna3": 512,
    "dna4": 512,
    "dna5": 512,
    "dna6": 512
}

PRETRAINED_INIT_CONFIGURATION = {
    "dna3": {"do_lower_case": False},
    "dna4": {"do_lower_case": False},
    "dna5": {"do_lower_case": False},
    "dna6": {"do_lower_case": False}
}

VOCAB_KMER = {
    "69": "3",
    "261": "4",
    "1029": "5",
    "4101": "6"
}
