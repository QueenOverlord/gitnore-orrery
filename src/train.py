import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torch.nn.utils.rnn import pad_sequence

import os
import json
import time
import random

# Import our custom modules
from dataset import GitignoreDataset
from model import Encoder, Decoder, Seq2Seq

# --- CONFIGURATION ---
# Hyperparameters (The dials we turn to tune performance)
BATCH_SIZE = 2
LEARNING_RATE = 0.001
N_EPOCHS = 10
HID_DIM = 256
EMB_DIM = 128
N_LAYERS = 2
DROPOUT = 0.5

# Paths
DATA_DIR = "data"
PROCESSED_DATA = os.path.join(DATA_DIR, "processed_corpus.jsonl")
CONTEXT_VOCAB = os.path.join(DATA_DIR, "context_vocab.json")
RULES_VOCAB = os.path.join(DATA_DIR, "rules_vocab.json")
MODEL_SAVE_PATH = "models/gitignore_model.pth"

# Ensure models directory exists
os.makedirs("models", exist_ok=True)

# --- 1. THE COLLATOR (The Packer) ---
def collate_fn(batch):
    """
    Takes a list of samples and pads them to make them square.
    """
    # Separate inputs and targets
    inputs = [item['input'] for item in batch]
    targets = [item['target'] for item in batch]
    
    # Pad inputs
    # batch_first=True means output shape is [batch_size, seq_len]
    # padding_value=1 (Assuming 1 is <pad> in our vocab)
    inputs_padded = pad_sequence(inputs, batch_first=True, padding_value=1)
    
    # Pad targets
    targets_padded = pad_sequence(targets, batch_first=True, padding_value=1)
    
    return inputs_padded, targets_padded

# --- 2. THE TRAINING LOOP (The Workout) ---
def train(model, iterator, optimizer, criterion, clip):
    model.train() # Turn on training mode (dropout active)
    
    epoch_loss = 0
    
    for i, (src, trg) in enumerate(iterator):
        # src, trg are already on the correct device (handled in main loop usually, but we do it here)
        
        optimizer.zero_grad() # Clear old gradients
        
        # Forward pass
        # trg is [batch_size, trg_len]
        output = model(src, trg)
        
        # Reshape for loss calculation
        # output shape: [batch_size, trg_len, output_dim] -> [batch_size * trg_len, output_dim]
        output_dim = output.shape[-1]
        output = output[:, 1:].reshape(-1, output_dim) # Skip <sos> token
        
        # trg shape: [batch_size, trg_len] -> [batch_size * trg_len]
        trg = trg[:, 1:].reshape(-1) # Skip <sos> token
        
        # Calculate loss
        loss = criterion(output, trg)
        
        # Backward pass
        loss.backward()
        
        # Clip gradients (prevent exploding gradients)
        torch.nn.utils.clip_grad_norm_(model.parameters(), clip)
        
        # Update weights
        optimizer.step()
        
        epoch_loss += loss.item()
        
    return epoch_loss / len(iterator)

# --- MAIN EXECUTION ---
def main():
    # Check for GPU
    # FORCE CPU due to MX350 incompatibility
    device = torch.device('cpu')
    print(f"Training on: {device}")
    
    # 1. Load Data
    print("Loading dataset...")
    dataset = GitignoreDataset(PROCESSED_DATA, CONTEXT_VOCAB, RULES_VOCAB)
    
    # Create the DataLoader (The conveyor belt)
    train_loader = DataLoader(
        dataset, 
        batch_size=BATCH_SIZE, 
        shuffle=True, 
        collate_fn=collate_fn
    )
    
    # 2. Setup Model
    # Get vocab sizes from the dataset files (loaded inside dataset class, but we need the size here)
    # We'll cheat slightly and read the json files again for the sizes
    with open(CONTEXT_VOCAB, 'r') as f:
        input_dim = len(json.load(f))
    with open(RULES_VOCAB, 'r') as f:
        output_dim = len(json.load(f))
        
    print(f"Input Vocab: {input_dim}, Output Vocab: {output_dim}")
    
    enc = Encoder(input_dim, EMB_DIM, HID_DIM, N_LAYERS, DROPOUT)
    dec = Decoder(output_dim, EMB_DIM, HID_DIM, N_LAYERS, DROPOUT)
    model = Seq2Seq(enc, dec, device).to(device)
    
    # 3. Setup Optimizer & Loss
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)
    
    # Ignore the <pad> token (index 1) when calculating loss
    PAD_IDX = 1
    criterion = nn.CrossEntropyLoss(ignore_index=PAD_IDX)
    
    # 4. Run Training
    print("Starting training...")
    best_valid_loss = float('inf')
    
    for epoch in range(N_EPOCHS):
        start_time = time.time()
        
        train_loss = train(model, train_loader, optimizer, criterion, clip=1)
        
        end_time = time.time()
        epoch_mins, epoch_secs = divmod(end_time - start_time, 60)
        
        print(f'Epoch: {epoch+1:02} | Time: {int(epoch_mins)}m {int(epoch_secs)}s')
        print(f'\tTrain Loss: {train_loss:.3f}')
        
        # Save checkpoint
        torch.save(model.state_dict(), MODEL_SAVE_PATH)
        
    print(f"Training complete. Model saved to {MODEL_SAVE_PATH}")

if __name__ == "__main__":
    main()