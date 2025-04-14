# %%
from EduData import get_data
import argparse
import os
import sys

def download_data():
    get_data("assistment-2009-2010-skill", "../data")

# %%
import random
import pandas as pd
import tqdm

def load_data(filename=None):
    if filename is None:
        # Use the default path if no filename is provided
        filepath = '../data/2009_skill_builder_data_corrected/skill_builder_data_corrected.csv'
    else:
        filepath = filename
    
    data = pd.read_csv(
        filepath,
        usecols=['order_id', 'user_id', 'skill_id', 'problem_id', 'correct'],
        encoding='utf-8',
    ).dropna(subset=['skill_id', 'problem_id'])
    return data

# %%
'''
This is a example for pid.
If the dataset you use doesn't have the field of problem id, please remove problem id used in this example.
'''
def process_data(data):
    raw_skill = data.skill_id.unique().tolist()
    raw_problem = data.problem_id.unique().tolist()
    num_skill = len(raw_skill)
    n_problem = len(raw_problem)

    # question id from 1 to #num_skill
    skills = { p: i+1 for i, p in enumerate(raw_skill) }
    problems = { p: i+1 for i, p in enumerate(raw_problem) }

    print("number of skills: %d" % num_skill)
    print("number of problems: %d" % n_problem)
    return skills, problems

# %%
def parse_all_seq(students, data, skills, problems):
    all_sequences = []
    for student_id in tqdm.tqdm(students, 'parse student sequence:\t'):
        student_sequence = parse_student_seq(data[data.user_id == student_id], skills, problems)
        all_sequences.extend([student_sequence])
    return all_sequences


def parse_student_seq(student, skills, problems):
    seq = student.sort_values('order_id')
    s = [skills[q] for q in seq.skill_id.tolist()]
    p = [problems[q] for q in seq.problem_id.tolist()]
    a = seq.correct.tolist()
    return s, p, a


# %%
def train_test_split(data, train_size=.7, shuffle=True):
    if shuffle:
        random.shuffle(data)
    boundary = round(len(data) * train_size)
    return data[: boundary], data[boundary:]

# %%
def sequences2l(sequences, trgpath):
    with open(trgpath, 'w', encoding='utf8') as f:
        for seq in tqdm.tqdm(sequences, 'write into file: '):
            skills, problems, answers = seq
            seq_len = len(skills)
            f.write(str(seq_len) + '\n')
            f.write(','.join([str(q) for q in problems]) + '\n')
            f.write(','.join([str(q) for q in skills]) + '\n')
            f.write(','.join([str(a) for a in answers]) + '\n')

def main():
    parser = argparse.ArgumentParser(description='Prepare dataset for knowledge tracing')
    parser.add_argument('filename', nargs='?', type=str, 
                        help='Path to the input CSV file (optional)')
    parser.add_argument('--download', action='store_true',
                        help='Download the default dataset first')
    args = parser.parse_args()
    
    if args.download:
        download_data()
        
    data = load_data(args.filename)
    
    skills, problems = process_data(data)
    
    # [(skill_seq_0, problem_seq_0, answer_seq_0), ..., (skill_seq_n, problem_seq_n, answer_seq_n)]
    sequences = parse_all_seq(data.user_id.unique(), data, skills, problems)
    
    train_sequences, test_sequences = train_test_split(sequences)
    
    # Use input filename to name output files
    base_name = "dataset"
    if args.filename:
        base_name = os.path.splitext(os.path.basename(args.filename))[0]
    
    # save triple line format for other tasks
    sequences2l(train_sequences, f'{base_name}_train_pid.txt')
    sequences2l(test_sequences, f'{base_name}_test_pid.txt')
    print(f"Files created: {base_name}_train_pid.txt and {base_name}_test_pid.txt")

if __name__ == "__main__":
    main()

    

