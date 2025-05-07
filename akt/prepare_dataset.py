from EduData import get_data
import random
import pandas as pd
import tqdm
import argparse
import os

parser = argparse.ArgumentParser(description='Prepare simulation data for DKT')
parser.add_argument('filename', type=str, help='Path to the dataset CSV file')
args = parser.parse_args()

base_filename = os.path.basename(args.filename).split('.')[0]
FILE_PREFIX = f'{base_filename}_'

data = pd.read_csv(
    args.filename + '.csv',
    usecols=['order_id', 'user_id', 'skill_id', 'problem_id', 'correct']
).dropna(subset=['skill_id', 'problem_id'])

# %%
'''
This is a example for pid.
If the dataset you use doesn't have the field of problem id, please remove problem id used in this example.
'''
raw_skill = data.skill_id.unique().tolist()
raw_problem = data.problem_id.unique().tolist()
num_skill = len(raw_skill)
n_problem = len(raw_problem)

# question id from 1 to #num_skill
skills = { p: i+1 for i, p in enumerate(raw_skill) }
problems = { p: i+1 for i, p in enumerate(raw_problem) }

print("number of skills: %d" % num_skill)
print("number of problems: %d" % n_problem)

# %%
def parse_all_seq(students):
    all_sequences = []
    for student_id in tqdm.tqdm(students, 'parse student sequence:\t'):
        student_sequence = parse_student_seq(data[data.user_id == student_id])
        all_sequences.extend([student_sequence])
    return all_sequences


def parse_student_seq(student):
    seq = student.sort_values('order_id')
    s = [skills[q] for q in seq.skill_id.tolist()]
    p = [problems[q] for q in seq.problem_id.tolist()]
    a = seq.correct.tolist()
    return s, p, a


# [(skill_seq_0, problem_seq_0, answer_seq_0), ..., (skill_seq_n, problem_seq_n, answer_seq_n)]
sequences = parse_all_seq(data.user_id.unique())

# %%
def train_test_split(data, train_size=.7, shuffle=True):
    if shuffle:
        random.shuffle(data)
    boundary = round(len(data) * train_size)
    return data[: boundary], data[boundary:]


train_sequences, test_sequences = train_test_split(sequences)

# %%
def sequences2l(sequences, trgpath):
    with open(trgpath, 'a', encoding='utf8') as f:
        for seq in tqdm.tqdm(sequences, 'write into file: '):
            skills, problems, answers = seq
            seq_len = len(skills)
            f.write(str(seq_len) + '\n')
            f.write(','.join([str(q) for q in problems]) + '\n')
            f.write(','.join([str(q) for q in skills]) + '\n')
            f.write(','.join([str(a) for a in answers]) + '\n')


# save triple line format for other tasks
sequences2l(train_sequences, FILE_PREFIX + 'train_pid.txt')
sequences2l(test_sequences,  FILE_PREFIX + 'test_pid.txt')



