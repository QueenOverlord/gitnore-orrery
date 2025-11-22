import json
import torch
from torch.utils.data import Dataset

class GitignoreDataset(Dataset):
    """
    Custom Dataset class for loading gitignore data.
    It reads a JSONL file containing contextual data (language, topics)
    and gitignore rules, then converts them into numerical tensors
    based on pre-built vocabularies.
    
    Version: 1.1 - Refactored for robustness.
    """
    def __init__(self, data_path, context_vocab_path, rules_vocab_path):
        """
        Initializes the dataset.
        
        Args:
            data_path (str): Path to the processed_corpus.jsonl file.
            context_vocab_path (str): Path to the context_vocab.json file.
            rules_vocab_path (str): Path to the rules_vocab.json file.
        """
        # --- 1. Load Vocabularies ---
        with open(context_vocab_path, 'r', encoding='utf-8') as f:
            self.context_vocab = json.load(f)
        with open(rules_vocab_path, 'r', encoding='utf-8') as f:
            self.rules_vocab = json.load(f)
            
        # --- 2. Define Special Token Indices for Robustness ---
        # Explicitly get the index for the unknown token. Default to 1 if not found.
        self.context_unk_idx = self.context_vocab.get('<unk>', 1)
        self.rules_unk_idx = self.rules_vocab.get('<unk>', 1)

        # --- 3. Load the Dataset ---
        self.data = []
        with open(data_path, 'r', encoding='utf-8') as f:
            for line in f:
                self.data.append(json.loads(line))

    def __len__(self):
        """Returns the total number of samples in the dataset."""
        return len(self.data)

    def __getitem__(self, idx):
        """
        Retrieves the sample at the given index and converts it to tensors.
        
        Args:
            idx (int): The index of the sample to retrieve.
            
        Returns:
            A dictionary containing the input and target tensors.
        """
        # Get the raw data record
        record = self.data[idx]

        # --- 1. Process Context (Input) ---
        # Combine language and topics, ensuring they are Lowercase to match the vocab
        context_tokens = []
        
        # Handle Language (check for None, then lower)
        if record['language']:
            context_tokens.append(record['language'].lower())
            
        # Handle Topics (lower all)
        if record['topics']:
            context_tokens.extend([t.lower() for t in record['topics']])
        
        # Convert context tokens to their integer representations
        # Default to 0 (<unk>) if not found
        context_integers = [self.context_vocab.get(token, 0) for token in context_tokens]
        
        # Create a PyTorch tensor from the list of integers
        input_tensor = torch.tensor(context_integers, dtype=torch.long)

        # --- 2. Process Rules (Target) ---
        rules_tokens = record.get('gitignore_rules', []) # Use .get() for safety
        
        # Convert rule tokens to their integer representations
        # We will add Start-of-Sequence and End-of-Sequence tokens here, which is a
        # standard practice for sequence generation tasks.
        sos_token = self.rules_vocab.get('<sos>', 2)
        eos_token = self.rules_vocab.get('<eos>', 3)
        rules_integers = [sos_token] + [self.rules_vocab.get(token, self.rules_unk_idx) for token in rules_tokens] + [eos_token]
        
        # Create a PyTorch tensor from the list of integers
        target_tensor = torch.tensor(rules_integers, dtype=torch.long)

        return {
            'input': input_tensor,
            'target': target_tensor
        }
