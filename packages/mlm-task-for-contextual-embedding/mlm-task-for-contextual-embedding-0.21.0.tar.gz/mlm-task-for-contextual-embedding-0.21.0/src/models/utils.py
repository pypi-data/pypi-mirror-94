import logging
from logging.config import fileConfig

from transformers import AutoTokenizer
import torch

fileConfig('src/log_config.ini')
logger = logging.getLogger(__name__)


def count_parameters(mdl):
    return sum(p.numel() for p in mdl.parameters() if p.requires_grad)


def init_tokenizer(model_name):
    logger.info("🍌 Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
    return tokenizer


def mask_tokens(inputs, tokenizer):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    inputs = inputs.to(device)
    labels = inputs.clone().to(device)
    probability_matrix = torch.full(labels.shape, 0.15).to(device)
    masked_indices = torch.bernoulli(probability_matrix).bool().to(device)
    labels[~masked_indices] = -100  # We only compute loss on masked tokens

    # 80% of the time, we replace masked input tokens with tokenizer.mask_token ([MASK])
    indices_replaced = torch.bernoulli(torch.full(labels.shape, 0.8)).bool().to(device) \
                       & masked_indices
    inputs[indices_replaced] = tokenizer.get_vocab()['<mask>']

    # 10% of the time, we replace masked input tokens with random word
    indices_random = (torch.bernoulli(torch.full(labels.shape, 0.1)).bool().to(device)
                      & masked_indices & ~indices_replaced).to(device)
    random_words = torch.randint(len(tokenizer.get_vocab()) - 1,
                                 labels.shape, dtype=torch.long).to(device)
    inputs[indices_random] = random_words[indices_random]

    # The rest of the time (10% of the time) we keep the masked input tokens unchanged
    return inputs.tolist(), labels.tolist()
