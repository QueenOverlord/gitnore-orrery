# MISSION DOSSIER: Gitnore-Orrery
> **Last Updated:** 2025-11-22
> **Protocol:** Knowledge Forge v1.1
> **Status:** ACTIVE - MILESTONE 2 (The Engine)

---

## 1. Project Overview (The "Why")

**Gitnore-Orrery** is an AI-powered command-line tool designed to solve a mundane developer problem—generating `.gitignore` files—while serving as a real-time educational visualization of Machine Learning.

* **The Utility:** Unlike static templates, it uses a Recurrent Neural Network (RNN/LSTM) to generate file rules line-by-line based on the specific context of your project (Language + Topics).
* **The Insight (The "Orrery"):** The tool visualizes its own "thought process." As it generates each line, it displays the probability scores of the alternative choices (the "ghosts" of lines not chosen), offering users a glimpse into the probabilistic mind of the AI.
* **The Core Thesis:** By applying "Cognitive Pressure" (context prompts), we demonstrate how a simple seed (`python`, `django`) shapes the entire gravitational pull of the generation process.

---

## 2. Operational Status

**Current Phase: MILESTONE 2 - THE CORE ENGINE**
We have successfully built the fuel lines (Data Pipeline) and are now constructing the engine block (The Neural Network).

### The Checklist
- [x] **Milestone 1: The Data Pipeline** (COMPLETED)
    - [x] Scrape GitHub for `.gitignore` files + metadata (`scraper.py`).
    - [x] Clean and normalize rules (`preprocessor.py`).
    - [x] Build Integer Vocabularies for Context and Rules (`mapper.py`).
- [ ] **Milestone 2: The Model (Current Focus)**
    - [x] Build the PyTorch Dataset Loader (`dataset.py`).
    - [x] Verify Data Loading (`test_dataset.py`).
    - [ ] **Design LSTM Architecture (`model.py`)** <- *IMMEDIATE NEXT STEP*
    - [ ] Implement Training Loop (`train.py`).
- [ ] **Milestone 3: The Interface**
    - [ ] Build CLI with `argparse`.
    - [ ] Implement "Orrery" Visualization.

---

## 3. Architecture & Assets

### The Data Layer (Fuel)
* **Source:** `data/corpus.jsonl` (Raw scrapes)
* **Processed:** `data/processed_corpus.jsonl` (Cleaned JSON)
* **Vocabs:** `data/context_vocab.json` & `data/rules_vocab.json` (The translator keys)

### The Codebase (`src/`)
| File | Status | Purpose |
| :--- | :--- | :--- |
| `scraper.py` | **Stable** | Fetches raw data from GitHub API. |
| `preprocessor.py`| **Stable** | Cleans noise, comments, and whitespace. |
| `mapper.py` | **Stable** | Maps words to integers (Tokenization). |
| `dataset.py` | **Stable** | PyTorch `Dataset` class. Handles vectorization. |
| `test_dataset.py`| **Stable** | Sanity check to ensure tensor shapes are correct. |
| `model.py` | *Pending* | **(Next)** The Seq2Seq LSTM Neural Network. |
| `train.py` | *Pending* | The training loop to teach the model. |

---

## 4. Session Log

**Session: The Resurrection (2025-11-22)**
* **Context:** Project resumed after a hiatus.
* **Action:** Verified the integrity of the virtual environment (`venv`) and the existing codebase.
* **Verification:** Ran analysis on `dataset.py` and verified the logic for converting JSON contexts into PyTorch tensors.
* **Decision:** The "Data Loader" phase is marked complete. The Council approved moving immediately to **Phase 5: Model Architecture**.

---

## 5. Next Immediate Objective

**Build the Brain (`src/model.py`).**
We need to define the `Encoder`, `Decoder`, and `Seq2Seq` classes to process the input tensors prepared by our dataset.