# Gitnore-Orrery: An AI-Powered .gitignore Generator

> **What if you could watch an AI think?** Gitnore-Orrery is a smart `.gitignore` generator that not only creates files for your project but also visualizes its decision-making process, offering a unique glimpse into the "mind" of the machine.

---

## 1. The Premise: Utility Meets Insight

Every developer needs `.gitignore` files, but creating a comprehensive one is a recurring, manual task. Existing generators are static templates. We can do better.

**Gitnore-Orrery** uses a Sequence-to-Sequence model to learn patterns from thousands of real-world `.gitignore` files. It doesn't just copy-paste; it generates the file line-by-line based on the project's context (language, topics).

The magic, however, is the **"Orrery"**: a planned feature for real-time visualization of the AI's "thought process." For each line it adds, you'll see the probability scores of other likely candidates—the "ghosts" of the lines not chosen. It's a practical utility and a fascinating educational tool in one.

## 2. The Product: A Smarter Command-Line Tool

The goal is a simple, elegant CLI that solves a real developer problem.

-   **Input:** `orrery --lang python --topics django,api > .gitignore`
-   **Process:**
    1.  The user specifies a context (language, frameworks). This acts as the initial prompt.
    2.  The pre-trained PyTorch model generates a `.gitignore` file line by line.
    3.  (Future) As it generates, it optionally prints its "thought process" to the console.
-   **Output:** A clean, comprehensive `.gitignore` file, ready for use.

*(A placeholder for a future animated GIF showcasing the tool in action)*

## 3. The Architecture

-   **Language:** Python 3.x
-   **Core ML Framework:** PyTorch
-   **Model:** A Sequence-to-Sequence (Seq2Seq) model with LSTM cells.
-   **Data:** A corpus of `.gitignore` files and repository metadata from over 1,000 public GitHub repositories.

## 4. Project Roadmap & Milestones

This project is under active development.

---

### ✅ **Milestone 1: The Data Pipeline**
*Status: 100% Complete*

-   **Phase 1: Scraper (`src/scraper.py`):** Built a tool using the `PyGithub` API to collect `.gitignore` files and their corresponding repository metadata (language, topics).
-   **Phase 2: Preprocessor (`src/preprocessor.py`):** Developed a script to clean, tokenize, and structure the raw data into a consistent format (`processed_corpus.jsonl`).
-   **Phase 3: Mapper (`src/mapper.py`):** Created vocabularies to map context tokens and gitignore rules to integers, preparing the data for the model.

---

### ⏳ **Milestone 2: The Core Engine (Model v0.1)**
*Status: In Progress*

> **Action Plan: Building the Seq2Seq Brain**
>
> -   **Phase 4: The Dataset Class:** Implement a custom PyTorch `Dataset` class (`src/dataset.py`) to load, vectorize, and serve the processed data as tensors for the model.
> -   **Phase 5: The Model Architecture:** Define the `Encoder`, `Decoder`, and `Seq2Seq` modules in PyTorch (`src/model.py`), which form the core of our neural network.
> -   **Phase 6: The Training Loop:** Write the script (`src/train.py`) to feed data to the model, calculate loss, and update weights, ultimately teaching the model how to generate `.gitignore` files.

---

### 🗓️ **Milestone 3: The Application (CLI v0.1)**
*Status: Planned*

-   Build the command-line interface using Python's `argparse`.
-   Implement the generation logic that loads the trained model and produces a `.gitignore` file.
-   Implement the "Orrery" visualization.

---

### 🗓️ **Milestone 4: Refinement & Packaging**
*Status: Planned*

-   Package the project for easy installation via `pip`.
-   Add comprehensive unit tests.
-   Refine the CLI and add more features.

---

## 5. Usage (Example)

*This section will be populated once the MVP is complete.*

```bash
# Clone the repository
git clone https://github.com/YourUsername/Gitnore-Orrery.git
cd Gitnore-Orrery

# Install dependencies
pip install -r requirements.txt

# Generate a .gitignore file
python orrery.py --lang python > .gitignore
```

---
Project by [Polliana Pavloski](https://www.linkedin.com/in/polliana-pavloski/)
---
