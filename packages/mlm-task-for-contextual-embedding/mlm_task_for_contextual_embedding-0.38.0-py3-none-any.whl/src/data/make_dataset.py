import glob
import logging
import re
from logging.config import fileConfig
from pathlib import Path
from os import path
import click
from dotenv import find_dotenv, load_dotenv
from tqdm import tqdm

import pandas as pd
from src.models.utils import init_tokenizer, mask_tokens

fileConfig(path.join(path.dirname(__file__), '../resources/log_config.ini'))
logger = logging.getLogger(__name__)


@click.command()
@click.option('--input-filepath', type=click.Path(), required=True)
@click.option('--output-filepath', type=click.Path(), required=True)
@click.option('--model-name', required=True)
def main(input_filepath, output_filepath, model_name):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger.info('making final data set from raw data')
    tokenizer = init_tokenizer(model_name)
    for file_path in tqdm(glob.glob(input_filepath + '/*.txt'),
                          position=0, desc='number of files'):
        data = []
        csv = []
        with open(file_path, 'r') as file:
            for line in tqdm(file.readlines(), position=1, leave=False, desc='file parsing'):
                if len(line) > 5 and len(line.split(' ')) > 10:
                    line = re.sub('[ \n]', '', line).strip().lower()
                    tokens = tokenizer.encode(line, truncation=True,
                                              add_special_tokens=False,
                                              return_tensors='pt').squeeze()
                    masked_tokens, output_label = mask_tokens(tokens, tokenizer)
                    data.append([tokens.tolist(), masked_tokens, output_label])
                    csv.append([line, tokenizer.decode(tokens), tokenizer.decode(masked_tokens),
                                output_label])
            dataset = pd.DataFrame(data=data,
                                   columns=['tokens', 'masked tokens', 'output label'])
            dataset_csv = pd.DataFrame(data=csv,
                                   columns=['sentences', 'tokens', 'masked tokens', 'output label'])
            dataset_csv.to_csv(f'{output_filepath}/{Path(file_path).stem}.csv')
            dataset.to_pickle(f'{output_filepath}/{Path(file_path).stem}.pickle')


if __name__ == '__main__':
    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]
    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())
    # pylint: disable=no-value-for-parameter
    main()
