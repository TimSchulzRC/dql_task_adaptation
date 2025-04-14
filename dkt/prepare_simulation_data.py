# %%
from EduData import get_data
get_data("assistment-2009-2010-skill", "../data")

# %%
import random
import pandas as pd
import tqdm
import numpy as np


FILE_PREFIX = 'dkt_simulation_'


data = pd.read_csv(
    '../dataset.csv',
    # '../dataset.csv',
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


train_sequences, test_sequences = train_test_split(sequences)

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


