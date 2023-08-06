import torch
from torch.utils.data import Dataset


class CamemBERTMaskedLMDataset(Dataset):
    def __init__(self, dataset, tokenizer):
        self.tokenizer = tokenizer
        self.dataset = dataset
        self.pad_id = tokenizer.pad_token_id

    def __getitem__(self, index):
        line = self.dataset.iloc[index]
        return {
            'tokens': line['tokens'],
            'masked_tokens': line['masked tokens'],
            'output_label': line['output label'],
            'attention_mask': []

        }

    def __len__(self):
        return len(self.dataset)

    def masked_lm_collate(self, batch):
        max_len = max(len(el['masked_tokens']) for el in batch)
        res_batch = {'tokens': [], 'attention_mask': [], 'masked_tokens': [], 'output_label': []}
        for input_batch in batch:
            vector = input_batch['masked_tokens']
            padded_list = [self.pad_id] * (max_len - len(vector))
            masked_tokens_res = input_batch['masked_tokens'] + padded_list
            res_batch['masked_tokens'].append(
                torch.LongTensor(masked_tokens_res))
            res_batch['output_label'].append(
                torch.LongTensor(input_batch['output_label'] + [-100] * (max_len - len(vector))))
            res_batch['tokens'].append(torch.LongTensor(input_batch['tokens'] + padded_list))
            res_batch['attention_mask'].append(torch.LongTensor([1 if token != self.pad_id else 0
                                                                 for token in masked_tokens_res]))
        res_batch = {k: (torch.stack(v) if isinstance(v[0], torch.Tensor) else v)
                     for k, v in res_batch.items()}
        return res_batch
