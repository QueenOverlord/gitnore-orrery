import os
from dataset import GitignoreDataset

def main():
    """
    Main function to run a sanity check on the GitignoreDataset class.

    This script performs the following actions:
    1. Defines the paths to the necessary data and vocabulary files.
    2. Initializes an instance of the GitignoreDataset.
    3. Verifies that the dataset loads without errors and reports the total number of samples.
    4. Retrieves the first sample (at index 0) from the dataset.
    5. Inspects and prints the structure, shape, and data type of the resulting
       input and target tensors to confirm they are correctly formatted for PyTorch.
    """
    print("--- Initializing GitignoreDataset ---")

    # Define paths relative to the project root directory
    DATA_DIR = "data"
    PROCESSED_DATA_PATH = os.path.join(DATA_DIR, "processed_corpus.jsonl")
    CONTEXT_VOCAB_PATH = os.path.join(DATA_DIR, "context_vocab.json")
    RULES_VOCAB_PATH = os.path.join(DATA_DIR, "rules_vocab.json")

    # --- 1. Dataset Initialization Test ---
    try:
        dataset = GitignoreDataset(
            data_path=PROCESSED_DATA_PATH,
            context_vocab_path=CONTEXT_VOCAB_PATH,
            rules_vocab_path=RULES_VOCAB_PATH
        )
        print(f"Dataset loaded successfully with {len(dataset)} samples.")
    except FileNotFoundError as e:
        print(f"Error: A data file was not found. Please ensure all paths are correct.")
        print(f"Details: {e}")
        return # Exit if dataset fails to load

    # --- 2. Sample Retrieval and Inspection Test ---
    print("\n--- Retrieving and inspecting the first sample (index 0) ---")

    if len(dataset) == 0:
        print("Dataset is empty. Cannot retrieve a sample.")
        return

    # Retrieve the first processed sample
    first_sample = dataset[0]

    # --- 3. Verification Prints ---
    # Check the overall structure of the returned sample
    print(f"Type of sample: {type(first_sample)}")
    print(f"Keys in sample: {first_sample.keys()}")

    # Inspect the 'input' tensor
    print("\nInput Tensor:")
    print(f"  - Tensor: {first_sample['input']}")
    print(f"  - Shape: {first_sample['input'].shape}")
    print(f"  - Dtype: {first_sample['input'].dtype}")

    # Inspect the 'target' tensor
    print("\nTarget Tensor:")
    print(f"  - Tensor: {first_sample['target']}")
    print(f"  - Shape: {first_sample['target'].shape}")
    print(f"  - Dtype: {first_sample['target'].dtype}")

# Standard Python entry point guard.
# This ensures the main() function is called only when the script is executed directly.
if __name__ == "__main__":
    main()
