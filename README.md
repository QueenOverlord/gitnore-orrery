# Gitnore-Orrery: An AI-Powered .gitignore Generator That Shows Its Work

> [!shield] **What if you could watch an AI think?** Gitnore-Orrery is a smart `.gitignore` generator that not only creates files for your project but also visualizes its decision-making process in real-time, offering a unique glimpse into the "mind" of the machine.

---

## 1. The Premise: Utility Meets Insight

Every developer needs `.gitignore` files, but creating a comprehensive one is a recurring, manual task. Existing generators are static templates. We can do better.

**Git-Orrery** uses a simple Recurrent Neural Network (RNN) to learn the patterns from thousands of real-world `.gitignore` files. It doesn't just copy-paste a template; it generates the file line-by-line based on statistical patterns.

The magic, however, is the **"Orrery"**: a real-time visualization of the AI's "thought process." For each line it adds, you see the probability scores of the other likely candidates—the "ghosts" of the lines not chosen. It's a practical utility and a fascinating educational tool in one.

This project is a real-world application of the **"Cognitive Pressure"** framework, demonstrating how a simple prompt (`--lang python`) can act as a "cognitive gravity," shaping the AI's output.

## 2. The Product: A Smarter Command-Line Tool

The goal is a simple, elegant CLI that solves a real developer problem.

*   **Input:** `orrery --lang python --min-prob 0.85 > .gitignore`
*   **Process:**
    1.  The user specifies a language or framework. This acts as the initial "seed" or prompt.
    2.  The pre-trained PyTorch model generates a `.gitignore` file line by line.
    3.  As it generates, it optionally prints its "thought process" to the console, showing the chosen line and its probability score.
*   **Output:** A clean, comprehensive `.gitignore` file, ready for use.

![GIF of future demo showing the generation process]
*(A placeholder for a future animated GIF showcasing the tool in action)*

## 3. The Architecture

*   **Language:** Python 3
*   **Core ML Framework:** PyTorch
*   **Model:** A Line-Level Recurrent Neural Network (LSTM), trained to predict the next line of a `.gitignore` file.
*   **Data:** A large corpus of `.gitignore` files from public repositories.

## 4. Project Roadmap & Milestones

This project is under active development.

-   [ ] **Milestone 1: The Data Pipeline**
    -   [ ] Write a Python script (`scraper.py`) using the GitHub API (or a library like `PyGithub`) to find and download thousands of `.gitignore` files from popular repositories.
    -   [ ] Write a pre-processing script to clean and consolidate the scraped data into a single, massive training file (`training_corpus.txt`).
    -   [ ] Create the data-to-integer mapping required for the model.

-   [ ] **Milestone 2: The Core Engine (Model v0.1)**
    -   [ ] Design and build the LSTM model architecture in PyTorch.
    -   [ ] Write the training loop to train the model on `training_corpus.txt`.
    -   [ ] Save the trained model for later use.

-   [ ] **Milestone 3: The Application (CLI v0.1)**
    -   [ ] Build the command-line interface (`orrery.py`) using Python's `argparse`.
    -   [ ] Implement the generation logic that loads the trained model and produces a `.gitignore` file.
    -   [ ] Implement the "Orrery" visualization, printing the probability scores during generation.

-   [ ] **Milestone 4: Refinement & Packaging**
    -   [ ] Package the project for easy installation via `pip`.
    -   [ ] Add comprehensive unit tests.
    -   [ ] Refine the CLI and add more features (e.g., combining multiple languages).

## 5. Usage

*This section will be populated once the MVP is complete.*

```bash
# Example of future usage
git clone https://github.com/QueenOverlord/Git-Orrery.git
cd Git-Orrery

# Install dependencies
pip install -r requirements.txt

# Run the scraper to build your own dataset (optional )
python scraper.py --query "language:python" --max-repos 1000

# Train the model on the new data (optional)
python train.py

# Generate a .gitignore file
python orrery.py --lang python > .gitignore
```
 