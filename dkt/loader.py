import pandas as pd
import numpy as np

MAX_STEP = 50

def transform_sim_data(simulationLog, dql_model):
    records = []
    order_id = 1
    problem_id = 1

    # Iterate through each student 
    for studentId in range(len(simulationLog)):
        for taskIndex in range(len(simulationLog[studentId]["tasks"])):
            # Iterate through categories
            for category_i, (category_name, category_elements) in enumerate(dql_model.items()):
                # Iterate through elements in category
                for element_i, element in enumerate(category_elements):
                    # Get delta for this element
                    delta = simulationLog[studentId]["deltas"][taskIndex][category_name][element_i]
                    
                    # Create record with zero-padded IDs
                    # Calculate position: (category_i * elements_per_category) + element_i
                    skill_position = (category_i * len(category_elements)) + element_i + 1
                    record = {
                        'order_id': f'{order_id:08d}',
                        'user_id': f'{studentId+1:06d}',
                        'sequence_id': f'{studentId+1:06d}',
                        'skill_id': skill_position,
                        'problem_id': f'{problem_id:08d}',
                        'correct': 1 if delta > 0 else 0
                    }
                    records.append(record)
                    order_id += 1  
            problem_id += 1

    # Create and save dataframe
    df = pd.DataFrame(records)
    return df

def parse_all_seq(data):
    sequences = []
    raw_question = data.skill_id.unique().tolist()

# question id from 0 to (num_skill - 1)
    questions = { p: i for i, p in enumerate(raw_question) }
    
    # Group by user_id and process each student's data at once
    for user_id, student_data in data.groupby('user_id'):
        # Sort by order_id
        seq = student_data.sort_values('order_id')
        
        # Convert skill_id to question indices and get correct answers
        q = [questions[q] for q in seq.skill_id.tolist()]
        a = seq.correct.tolist()
        
        sequences.append((q, a))
    
    return sequences

def encode_onehot(sequences, num_questions):
    # Calculate the number of chunks (each of size max_step)
    chunks_per_seq = [max(1, (len(q) + MAX_STEP - 1) // MAX_STEP) for q, a in sequences]
    total_chunks = sum(chunks_per_seq)
    
    # Pre-allocate the result array
    result = np.zeros((total_chunks * MAX_STEP, 2 * num_questions))
    
    chunk_idx = 0
    for seq_idx, (q, a) in enumerate(sequences):
        
        # Fill in the onehot values
        for i, q_id in enumerate(q):
            index = int(q_id if a[i] > 0 else q_id + num_questions)
            result_idx = chunk_idx * MAX_STEP + i
            result[result_idx, index] = 1
        
        chunk_idx += chunks_per_seq[seq_idx]
    
    return result.reshape(-1, MAX_STEP, 2 * num_questions)