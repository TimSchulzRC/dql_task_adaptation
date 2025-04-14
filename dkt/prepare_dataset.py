# %%
from EduData import get_data
import argparse
import os

# Add command line argument parsing
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Prepare simulation data for DKT')
    parser.add_argument('filename', type=str, help='Path to the dataset CSV file')
    parser.add_argument('--output_prefix', type=str, default=None, help='Prefix for output files (default: derived from input filename)')
    parser.add_argument('--train_size', type=float, default=0.7, help='Proportion of data to use for training (default: 0.7)')
    args = parser.parse_args()
else:
    # For notebook mode
    class Args:
        def __init__(self):
            self.filename = '../dataset.csv'
            self.output_prefix = None
            self.train_size = 0.7
    args = Args()

# Get Assistment data if needed (only in notebook mode)
if '__file__' not in globals():
    get_data("assistment-2009-2010-skill", "../data")

# %%
import random
import pandas as pd
import tqdm
import numpy as np

# Set output file prefix based on input filename if not specified
if args.output_prefix is None:
    base_filename = os.path.basename(args.filename).split('.')[0]
    FILE_PREFIX = f'{base_filename}_'
else:
    FILE_PREFIX = args.output_prefix

print(f"Using file: {args.filename}")
print(f"Output files will be prefixed with: {FILE_PREFIX}")

data = pd.read_csv(
    args.filename,
    usecols=['order_id', 'user_id', 'sequence_id', 'skill_id', 'correct'],
    encoding='utf-8'
).dropna(subset=['skill_id'])

# %%
raw_question = data.skill_id.unique().tolist()
num_skill = len(raw_question)

# question id from 0 to (num_skill - 1)
questions = { p: i for i, p in enumerate(raw_question) }

print("number of skills: %d" % num_skill)

# %%
from loader import parse_all_seq

# [(question_sequence_0, answer_sequence_0), ..., (question_sequence_n, answer_sequence_n)]
sequences = parse_all_seq(data)

# %%
def train_test_split(data, train_size=.7, shuffle=True):
    if shuffle:
        random.shuffle(data)
    boundary = round(len(data) * train_size)
    return data[: boundary], data[boundary:]


train_sequences, test_sequences = train_test_split(sequences, train_size=args.train_size)

# %%
def sequences2tl(sequences, trgpath):
    with open(trgpath, 'a', encoding='utf8') as f:
        for seq in tqdm.tqdm(sequences, 'write into file: '):
            questions, answers = seq
            seq_len = len(questions)
            f.write(str(seq_len) + '\n')
            f.write(','.join([str(q) for q in questions]) + '\n')
            f.write(','.join([str(a) for a in answers]) + '\n')


# save triple line format for other tasks
sequences2tl(train_sequences, FILE_PREFIX + 'train.txt')
sequences2tl(test_sequences, FILE_PREFIX + 'test.txt')

# %%
from loader import encode_onehot

train_data = encode_onehot(train_sequences, num_skill)
test_data = encode_onehot(test_sequences, num_skill)

# %%
print("train data shape: ", train_data.shape)
print("test data shape: ", test_data.shape)

# %%
# save onehot data
np.save(FILE_PREFIX + 'train_data.npy', train_data)
np.save(FILE_PREFIX + 'test_data.npy', test_data)


