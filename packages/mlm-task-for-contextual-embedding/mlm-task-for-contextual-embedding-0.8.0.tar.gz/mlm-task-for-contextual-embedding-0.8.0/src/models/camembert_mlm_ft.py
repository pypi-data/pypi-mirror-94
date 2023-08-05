import gc
import glob
import logging
import os
from datetime import datetime
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
from logging.config import fileConfig

import click
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as f
import torch.optim as optim
import wandb
from numpy import mean
from sklearn.model_selection import KFold
from torch.utils.data import DataLoader
from transformers import AutoModelForMaskedLM

from src.data.camembert_mlm_dataset import CamemBERTMaskedLMDataset
from src.models.utils import count_parameters, init_tokenizer

fileConfig('src/log_config.ini')
logger = logging.getLogger(__name__)


# pylint: disable=too-many-arguments, too-many-locals
def init_model(model_name, device):
    logger.info("🍌 Loading model...")
    model = AutoModelForMaskedLM.from_pretrained(model_name)
    model.to(device)
    logger.info(f'The model has {count_parameters(model):,} trainable parameters')
    return model


def compute_loss(predictions, targets, criterion=None):
    predictions = predictions[:, :-1, :].contiguous()
    targets = targets[:, 1:]
    rearranged_output = predictions.view(predictions.shape[0] * predictions.shape[1], -1)
    rearranged_target = targets.contiguous().view(-1)
    loss = criterion(rearranged_output, rearranged_target)
    return loss


def train_model(model, dataloader, optimizer, criterion, device, id_fold, epochs):
    model.train()
    epoch_loss = []

    for epoch in range(epochs):
        logger.info("Starting epoch {}".format(epoch + 1))
        for batch in dataloader:
            optimizer.zero_grad()
            predictions = model(input_ids=batch['masked_tokens'].to(device),
                        attention_mask=batch['attention_mask'].to(device))
            predictions_scores = f.log_softmax(predictions.logits, dim=2)
            loss = compute_loss(predictions_scores, batch['output_label'].to(device), criterion)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            wandb.log({"loss {}".format(id_fold): loss.item()})
            epoch_loss.append(loss.item())

    logger.info('train epoch loss : {}'.format(mean(epoch_loss)))


def eval_model(model, dataloader, criterion, device):
    model.eval()
    epoch_loss = []
    with torch.no_grad():
        for batch in dataloader:
            predictions = model(input_ids=batch['masked_tokens'].to(device),
                        attention_mask=batch['attention_mask'].to(device))
            predictions_scores = f.log_softmax(predictions.logits, dim=2)
            loss = compute_loss(predictions_scores, batch['output_label'].to(device), criterion)
            epoch_loss.append(loss.item())
    return mean(epoch_loss)


@click.command()
@click.option('--learning-rate')
@click.option('--batch-size')
@click.option('--num-epochs')
@click.option('--folds')
@click.option('--model-name')
@click.option('--model-path')
@click.option('--dataset-path')
def main(learning_rate,
         batch_size,
         num_epochs,
         folds,
         model_name,
         model_path,
         dataset_path):
    hyperparameter_defaults = dict(
        lr=float(learning_rate),
        batch_size=int(batch_size),
        num_epochs=int(num_epochs),
        folds=int(folds),
        model_name=model_name,
        model_path=model_path,
    )
    wandb.init(project="360-masked-lm-task", config=hyperparameter_defaults)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    dataset = pd.concat([pd.read_pickle(file) for file in glob.glob(dataset_path + '/*.pickle')])
    logger.info("Using device: {}".format(device))
    logger.info("Using tokenizer from model : {}".format(model_name))
    tokenizer = init_tokenizer(hyperparameter_defaults['model_name'])
    criterion = nn.NLLLoss()
    folds = KFold(n_splits=hyperparameter_defaults['folds'], shuffle=False)
    cv_scores_loss = []
    for id_fold, fold in enumerate(folds.split(dataset)):
        logger.info('beginning fold n°{}'.format(id_fold + 1))
        model = init_model(hyperparameter_defaults['model_name'], device)
        optimizer = optim.Adam(model.parameters(), lr=hyperparameter_defaults['lr'])
        train_fold, eval_fold = fold
        train_fold = dataset.iloc[train_fold]
        eval_fold = dataset.iloc[eval_fold]
        train_dataset = CamemBERTMaskedLMDataset(train_fold, tokenizer)
        eval_dataset = CamemBERTMaskedLMDataset(eval_fold, tokenizer)

        train_dataloader = DataLoader(dataset=train_dataset,
                                      batch_size=hyperparameter_defaults["batch_size"],
                                      shuffle=False, drop_last=True,
                                      collate_fn=train_dataset.masked_lm_collate)
        eval_dataloader = DataLoader(dataset=eval_dataset,
                                     batch_size=hyperparameter_defaults["batch_size"],
                                     shuffle=False, drop_last=True,
                                     collate_fn=eval_dataset.masked_lm_collate)

        wandb.watch(model)
        train_model(model, train_dataloader, optimizer, criterion, device, id_fold,
                        hyperparameter_defaults['num_epochs'])
        logger.info("Saving model ..")
        current_datetime = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        save_location = hyperparameter_defaults['model_path']
        model_name = f'{model_name}-' \
                     f'{current_datetime}-fold-{id_fold + 1}.bin'
        if not os.path.exists(save_location):
            os.makedirs(save_location)
        save_location = os.path.join(save_location, model_name)
        torch.save(model, save_location)
        wandb.save(save_location)
        cv_score_loss = eval_model(model, eval_dataloader, criterion, device)
        del model
        gc.collect()
        torch.cuda.empty_cache()
        cv_scores_loss.append(cv_score_loss)
        wandb.log({"cv score loss": cv_score_loss})
    logger.info('CV score loss : {}'.format(cv_scores_loss))


if __name__ == '__main__':
    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]
    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())
    # pylint: disable=no-value-for-parameter
    main()
