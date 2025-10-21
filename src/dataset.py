import json
import torch
from torch.utils.data import Dataset

class GitignoreDataset(Dataset):
    """
    Custom Dataset class for loading gitignore data.
    It reads a JSONL file containing contextual data (language, topics)
    and gitignore rules, then converts them into numerical tensors
    based on pre-built vocabularies.
    """
    def __init__(self, data_path, context_vocab_path, rules_vocab_path):
        """
        Initializes the dataset.
        
        Args:
            data_path (str): Path to the processed_data.jsonl file.
            context_vocab_path (str): Path to the context_vocab.json file.
            rules_vocab_path (str): Path to the rules_vocab.json file.
        """
        # Load vocabularies
        with open(context_vocab_path, 'r') as f:
            self.context_vocab = json.load(f)
        with open(rules_vocab_path, 'r') as f:
            self.rules_vocab = json.load(f)

        # Load the dataset line by line
        self.data = []
        with open(data_path, 'r') as f:
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
        # Combine language and topics into a single list of context tokens
        context_tokens = [record['language']] + record['topics']
        
        # Convert context tokens to their integer representations using the vocab
        # Use vocab.get(token, 0) to handle unknown tokens by mapping them to index 0 (UNK)
        context_integers = [self.context_vocab.get(token, 0) for token in context_tokens]
        
        # Create a PyTorch tensor from the list of integers
        input_tensor = torch.tensor(context_integers, dtype=torch.long)

        # --- 2. Process Rules (Target) ---
        # Get the list of gitignore rules
        rules_tokens = record['gitignore_rules'] # Assumes this is already a list of strings
        
        # Convert rule tokens to their integer representations
        rules_integers = [self.rules_vocab.get(token, 0) for token in rules_tokens]
        
        # Create a PyTorch tensor from the list of integers
        target_tensor = torch.tensor(rules_integers, dtype=torch.long)

        return {
            'input': input_tensor,
            'target': target_tensor
        }


