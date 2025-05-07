from load_data import DATA, PID_DATA
import logging
from EduKTM import AKT
import argparse
import numpy as np

# Parse command line arguments
parser = argparse.ArgumentParser(description='Train DKVMN model')
parser.add_argument('--dataset', type=str, default='dataset', help='Dataset name (will be used as file prefix)')
parser.add_argument('--epochs', type=int, default=2, help='Number of training epochs')
args = parser.parse_args()

FILE_PREFIX = args.dataset + '_'

batch_size = 64
model_type = 'pid'
n_question = 9
n_pid = 300724
seqlen = 900
n_blocks = 1
d_model = 256
dropout = 0.05
kq_same = 1
l2 = 1e-5
maxgradnorm = -1

def load_train_val_data(dat):
    train_pid = dat.load_data(FILE_PREFIX + 'train_pid.txt')
    # Split train_pid into training and validation data (80/20 split)
    total_samples = train_pid[0].shape[0]
    val_size = int(total_samples * 0.2)  # 20% for validation
    indices = np.arange(total_samples)
    np.random.shuffle(indices)

    train_indices = indices[val_size:]
    val_indices = indices[:val_size]

    # Extract train and validation data
    train_data = [x[train_indices] for x in train_pid]
    val_data = [x[val_indices] for x in train_pid]
    return train_data, val_data

if model_type == 'pid':
    dat = PID_DATA(n_question=n_question, seqlen=seqlen, separate_char=',')
else:
    dat = DATA(n_question=n_question, seqlen=seqlen, separate_char=',')
train_data = dat.load_data(FILE_PREFIX + 'train_pid.txt')
test_data, val_data = load_train_val_data(dat)

logging.getLogger().setLevel(logging.INFO)



akt = AKT(n_question, n_pid, n_blocks, d_model, dropout, kq_same, l2, batch_size, maxgradnorm)
akt.train(train_data, val_data, epoch=args.epochs)
akt.save("akt.params")

akt.load("akt.params")
_, auc, accuracy = akt.eval(test_data)
print("auc: %.6f, accuracy: %.6f" % (auc, accuracy))
