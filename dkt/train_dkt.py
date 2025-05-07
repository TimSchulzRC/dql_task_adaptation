# coding: utf-8
# 2021/4/24 @ zengxiaonan
import logging
import numpy as np
import torch
import torch.utils.data as Data
import argparse

from EduKTM import DKT

# Parse command line arguments
parser = argparse.ArgumentParser(description='Train DKT model')
parser.add_argument('--dataset', type=str, default='dataset', help='Dataset name (will be used as file prefix)')
parser.add_argument('--epochs', type=int, default=10, help='Number of training epochs')
args = parser.parse_args()

# Define file prefix with dataset name
FILE_PREFIX = args.dataset + '_'

NUM_QUESTIONS = 9
BATCH_SIZE = 64
HIDDEN_SIZE = 10
NUM_LAYERS = 1

def get_train_val_loaders(batch_size, val_split=0.2, shuffle=True, data_percentage=1.0):
    # Load the entire dataset
    data = torch.FloatTensor(np.load(FILE_PREFIX + 'train_data.npy'))
    
    # Apply data_percentage to reduce dataset size if needed
    if data_percentage < 1.0:
        total_samples = len(data)
        samples_to_keep = int(total_samples * data_percentage)
        if shuffle:
            indices = torch.randperm(total_samples)[:samples_to_keep]
            data = data[indices]
        else:
            data = data[:samples_to_keep]
    
    # Get dataset size and calculate split
    dataset_size = len(data)
    val_size = int(dataset_size * val_split)
    train_size = dataset_size - val_size
    
    # Split the dataset
    if shuffle:
        indices = torch.randperm(dataset_size)
        train_indices = indices[:train_size]
        val_indices = indices[train_size:]
        train_data = data[train_indices]
        val_data = data[val_indices]
    else:
        train_data = data[:train_size]
        val_data = data[train_size:]
    
    # Create data loaders
    train_loader = Data.DataLoader(train_data, batch_size=batch_size, shuffle=shuffle)
    val_loader = Data.DataLoader(val_data, batch_size=batch_size, shuffle=False)
    
    print(f"Training samples: {train_size}, Validation samples: {val_size}")
    
    return train_loader, val_loader

def get_test_data_loader(batch_size, shuffle=False, data_percentage=1.0):
    data = torch.FloatTensor(np.load(FILE_PREFIX + 'test_data.npy'))
    # Select only a percentage of the data
    if data_percentage < 1.0:
        total_samples = len(data)
        samples_to_keep = int(total_samples * data_percentage)
        if shuffle:
            indices = torch.randperm(total_samples)[:samples_to_keep]
            data = data[indices]
        else:
            data = data[:samples_to_keep]
    
    data_loader = Data.DataLoader(data, batch_size=batch_size, shuffle=shuffle)
    return data_loader

def get_data_loader(data_path, batch_size, shuffle=False):
    data = torch.FloatTensor(np.load(data_path))
    data_loader = Data.DataLoader(data, batch_size=batch_size, shuffle=shuffle)
    return data_loader

train_loader, val_loader = get_train_val_loaders(BATCH_SIZE)
test_loader = get_test_data_loader(BATCH_SIZE)

logging.getLogger().setLevel(logging.INFO)

dkt = DKT(NUM_QUESTIONS, HIDDEN_SIZE, NUM_LAYERS)
print(f"Training for {args.epochs} epochs")
dkt.train(train_loader, test_loader, epoch=args.epochs)
dkt.save("dkt.params")

dkt.load("dkt.params")
auc = dkt.eval(test_loader)
print("auc: %.6f" % auc)
