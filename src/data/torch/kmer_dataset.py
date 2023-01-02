from pathlib import Path

import torch
from pandas import read_csv
from torch.utils.data import Dataset
from transformers import BertTokenizer

class KmerDataset(Dataset):
    def __init__(self, data_dir: Path, dataset: str, set_type: str, k: str, tokenizer: BertTokenizer):
        self.tokenizer = tokenizer

        data = read_csv(data_dir / 'processed' / dataset / f'kmer_text_{k}' / f'{set_type}.csv')

        self.sequences = data['x1']
        self.labels = data['label']

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, index):
        tokenized_seq = self.tokenizer.encode_plus(self.sequences.iloc[index], None, return_token_type_ids=True)

        return (
            torch.tensor(tokenized_seq['input_ids'], dtype=torch.long),
            torch.tensor(tokenized_seq['attention_mask'], dtype=torch.long),
            torch.tensor(tokenized_seq['token_type_ids'], dtype=torch.long),
            torch.tensor(self.labels.iloc[index], dtype=torch.long),
        )
