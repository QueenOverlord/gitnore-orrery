
# MISSION DOSSIER: Project Gitnore-Orrery

## Cognitive Continuity Protocol v2.0

  

> **RE-INSTANTIATION DIRECTIVE:** This document is the single source of truth for mission state. To re-instantiate context, process this document in its entirety. It contains the project status, key decisions, architectural snapshots, and a chronological session log.

  

---

  

## 1. Mission Overview

  

-  **Project Name:**  `Gitnore-Orrery`

-  **Objective:** Build an AI-powered tool to generate `.gitignore` files based on a project's context (language, topics), while visualizing the AI's decision-making process.

-  **Current Branch:**  `main` (after merging `feat/implement-scraper`)

-  **Overall Status:** Milestone 1 (Data Pipeline) is **COMPLETE** and merged. Milestone 2 (ML Model) is planned.

  

---

  

## 2. Key Architectural Artifacts

  

*This section holds the last stable version of key code files for quick reference.*

  

<details>

<summary><code>src/scraper.py</code> (v1.1 - Stable)</summary>

  

```python

import os

import json

from dotenv import load_dotenv

from github import Github, Auth, RateLimitExceededException, UnknownObjectException

  

DATA_DIR =  "data"

OUTPUT_FILE = os.path.join(DATA_DIR,  "corpus.jsonl")

  

def  save_record(record):

os.makedirs(DATA_DIR,  exist_ok=True)

with  open(OUTPUT_FILE,  "a",  encoding="utf-8")  as f:

f.write(json.dumps(record)  +  "\n")

  

def  main():

print("--- Authenticating with GitHub API ---")

load_dotenv()

github_token = os.getenv("GITHUB_TOKEN")

if  not github_token:

print("Error: GITHUB_TOKEN not found.")

return

  

auth = Auth.Token(github_token)

g =  Github(auth=auth)

print("Authentication successful.")

  

print("\n--- Starting Repository Search ---")

query =  "stars:>500"

MAX_REPOS_TO_PROCESS =  1000

repositories = g.search_repositories(query=query,  sort='stars',  order='desc')

print(f"Found {repositories.totalCount} total repositories. Processing up to {MAX_REPOS_TO_PROCESS}...")

  

count =  0

for repo in repositories:

if count >= MAX_REPOS_TO_PROCESS:

print(f"\nReached the limit of {MAX_REPOS_TO_PROCESS} repositories.")

break

  

try:

gitignore_file = repo.get_contents(".gitignore")

gitignore_content = gitignore_file.decoded_content.decode('utf-8')

  

data_record =  {

"repo_name": repo.full_name,

"language": repo.language,

"topics": repo.topics,

"description": repo.description,

"gitignore_content": gitignore_content

}

save_record(data_record)

print(f"({count +  1}/{MAX_REPOS_TO_PROCESS}) Successfully processed and saved: {repo.full_name}")

  

except UnknownObjectException:

print(f"({count +  1}/{MAX_REPOS_TO_PROCESS}) Skipped {repo.full_name}: .gitignore not found in root.")

except  Exception  as e:

print(f"({count +  1}/{MAX_REPOS_TO_PROCESS}) An error occurred for {repo.full_name}: {e}")

count +=  1

  

if __name__ ==  "__main__":

main()

```

</details>

  

<details>

<summary><code>src/preprocessor.py</code> (v1.0 - Stable)</summary>

  

```python

import os

import json

  

RAW_DATA_PATH =  "data/corpus.jsonl"

PROCESSED_DATA_PATH =  "data/processed_corpus.jsonl"

  

def  clean_gitignore_content(content_string):

cleaned_rules =  []

for line in content_string.splitlines():

stripped_line = line.strip()

if stripped_line and  not stripped_line.startswith('#')  and  not stripped_line.startswith('!'):

cleaned_rules.append(stripped_line)

return cleaned_rules

  

def  main():

print("--- Iniciando o pré-processamento dos dados ---")

if os.path.exists(PROCESSED_DATA_PATH):

os.remove(PROCESSED_DATA_PATH)

processed_count =  0

with  open(RAW_DATA_PATH,  "r",  encoding="utf-8")  as infile:

for line in infile:

record = json.loads(line)

raw_content = record.get("gitignore_content",  "")

cleaned_rules =  clean_gitignore_content(raw_content)

record["gitignore_rules"]  = cleaned_rules

del  record["gitignore_content"]

with  open(PROCESSED_DATA_PATH,  "a",  encoding="utf-8")  as outfile:

outfile.write(json.dumps(record)  +  "\n")

processed_count +=  1

  

print(f"\n--- Pré-processamento concluído ---")

print(f"Total de registros processados: {processed_count}")

  

if __name__ ==  "__main__":

main()

```

</details>

  

<details>

<summary><code>src/mapper.py</code> (v1.0 - Stable)</summary>

  

```python

import os

import json

from collections import Counter

  

PROCESSED_DATA_PATH =  "data/processed_corpus.jsonl"

CONTEXT_VOCAB_PATH =  "data/context_vocab.json"

RULES_VOCAB_PATH =  "data/rules_vocab.json"

  

def  main():

print("--- Iniciando a criação dos vocabulários ---")

context_tokens =  Counter()

rules_tokens =  Counter()

with  open(PROCESSED_DATA_PATH,  'r',  encoding='utf-8')  as f:

for line in f:

record = json.loads(line)

# Contexto: Linguagem + Tópicos

if  record['language']:

context_tokens.update([f"lang:{record['language'].lower()}"])

if  record['topics']:

context_tokens.update([f"topic:{topic.lower()}"  for topic in  record['topics']])

# Regras

rules_tokens.update(record['gitignore_rules'])

  

print(f"Encontrados {len(context_tokens)} tokens de contexto únicos.")

print(f"Encontradas {len(rules_tokens)} regras de .gitignore únicas.")

  

# Criar vocabulários (token -> int)

# Adicionando tokens especiais: <pad> para preenchimento, <unk> para desconhecido

context_vocab =  {'<pad>':  0,  '<unk>':  1}

context_vocab.update({token: i+2  for i, token in  enumerate(context_tokens)})

  

rules_vocab =  {'<pad>':  0,  '<unk>':  1,  '<sos>':  2,  '<eos>':  3}  # <sos>: start, <eos>: end

rules_vocab.update({token: i+4  for i, token in  enumerate(rules_tokens)})

# Salvar vocabulários

with  open(CONTEXT_VOCAB_PATH,  'w',  encoding='utf-8')  as f:

json.dump(context_vocab, f,  indent=2)

print(f"Vocabulário de contexto salvo em {CONTEXT_VOCAB_PATH}")

with  open(RULES_VOCAB_PATH,  'w',  encoding='utf-8')  as f:

json.dump(rules_vocab, f,  indent=2)

print(f"Vocabulário de regras salvo em {RULES_VOCAB_PATH}")

  

print("\n--- Mapeamento concluído ---")

  

if __name__ ==  "__main__":

main()

```

</details>

  

---

  

## 3. Chronological Session Log

  

*Este log é um registro contínuo, com as sessões mais recentes no topo.*

  

---

### **SESSION LOG: 2025-10-19**

---

  

**SESSION OBJECTIVE:** Conclude Milestone 1, plan Milestone 2, and perform session wrap-up.

**SESSION OUTCOME:** SUCCESS. Milestone 1 is 100% complete. Session concluded with strategic documentation enhancement and merge to `main`.

  

**KEY ACCOMPLISHMENTS:**

  

1.  **Milestone 1 Completion:** All three phases (Scraper, Preprocessor, Mapper) are functionally complete and tested. The data pipeline is now operational.

  

2.  **Milestone 2 Planning:** Conducted a "Level 4 Council" to architect the Seq2Seq model. A detailed 3-phase plan (Phase 4: Dataset, Phase 5: Model, Phase 6: Training) was created.

  

3.  **Strategic Documentation Review (`README.md`):**

*  **Action:** Convened a "Level 4 Council" to refine the `README.md` for professionalism and clarity on GitHub.

*  **Key Insight:** Formulated a strategic answer to the "Why LSTM over Transformers?" question, focusing on data efficiency, resource constraints, and problem suitability. This is a key talking point for technical interviews.

*  **Outcome:** A new, professionally formatted `README.md` was drafted, approved, and committed.

  

4.  **Project Hygiene & Workflow:**

*  **Decision:** Moved `MISSION_STATE.MD` into the project root to ensure the repository is self-contained. This is a best practice for context locality and collaboration.

*  **Action:** All work from `feat/implement-scraper` was successfully merged into the `main` branch via a Pull Request.

  

**END-OF-SESSION STATE:**

  

*  **Git Branch:**  `main`

*  **Working Directory:** Clean. All changes are committed and pushed.

*  **Mental State:** Mission objectives achieved. A clean stopping point has been reached.

  

**NEXT ACTIONS (START OF NEXT SESSION):**

  

1. Create a new feature branch for Milestone 2 (e.g., `feat/build-seq2seq-model`).

2. Begin Milestone 2, Phase 4:

* Create `src/dataset.py` and `src/test_dataset.py`.

* Implement the `GitignoreDataset` class.

  

---