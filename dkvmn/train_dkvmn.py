from EduKTM import DKVMN
from load_data import Data
import argparse

# Parse command line arguments
parser = argparse.ArgumentParser(description='Train DKVMN model')
parser.add_argument('--dataset', type=str, default='dataset', help='Dataset name (will be used as file prefix)')
args = parser.parse_args()

# Define file prefix with dataset name
FILE_PREFIX = args.dataset + '_'

params = {
    'max_iter': 3, # 'number of iterations'
    'init_std': 0.1, # 'weight initialization std'
    'init_lr': 0.01, # 'initial learning rate'
    'lr_decay': 0.75, # 'learning rate decay'
    'final_lr': 1E-5, # 'learning rate will not decrease after hitting this threshold'
    'momentum': 0.9, # 'momentum rate'
    'maxgradnorm': 50.0, # 'maximum gradient norm'
    'final_fc_dim': 50, # 'hidden state dim for final fc layer'
    'key_embedding_dim': 50, # 'question embedding dimensions'
    'batch_size': 64, # 'the batch size'
    'value_embedding_dim': 200, # 'answer and question embedding dimensions'
    'memory_size': 20, # 'memory size'
    'n_question': 9, # 'the number of unique questions in the dataset'
    'seqlen': 900, # 'the allowed maximum length of a sequence'
    'data_name': '', # 'data set name'
    'load': 'dkvmn.params', # 'model file to load'
    'save': 'dkvmn.params' # 'path to save model'
}

params['lr'] = params['init_lr']
params['key_memory_state_dim'] = params['key_embedding_dim']
params['value_memory_state_dim'] = params['value_embedding_dim']

dat = Data(n_question=params['n_question'], seqlen=params['seqlen'], separate_char=',') 

train_data_path = FILE_PREFIX + "train.txt"
test_data_path = FILE_PREFIX + "test.txt"
train_data = dat.load_data(train_data_path)
test_data = dat.load_data(test_data_path)

dkvmn = DKVMN(n_question=params['n_question'],
                  batch_size=params['batch_size'],
                  key_embedding_dim=params['key_embedding_dim'],
                  value_embedding_dim=params['value_embedding_dim'],
                  memory_size=params['memory_size'],
                  key_memory_state_dim=params['key_memory_state_dim'],
                  value_memory_state_dim=params['value_memory_state_dim'],
                  final_fc_dim=params['final_fc_dim'])

dkvmn.train(params, train_data)
dkvmn.save(params['save'])

dkvmn.load(params['load'])
dkvmn.eval(params, test_data)
