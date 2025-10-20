import os
import json

# Define os caminhos de entrada e saída
PROCESSED_DATA_PATH = "data/processed_corpus.jsonl"
CONTEXT_VOCAB_PATH = "data/context_vocab.json"
RULES_VOCAB_PATH = "data/rules_vocab.json"

def main():
    """
    Função principal para criar os vocabulários a partir dos dados processados.
    """
    print("--- Iniciando a criação dos vocabulários ---")

    # Usar sets para coletar tokens únicos e evitar duplicatas
    context_tokens = set()
    rule_tokens = set()

    # Ler o arquivo de dados processados
    with open(PROCESSED_DATA_PATH, "r", encoding="utf-8") as infile:
        for line in infile:
            record = json.loads(line)
            
            # Coletar tokens de contexto (linguagem e tópicos)
            if record.get("language"):
                context_tokens.add(record["language"].lower()) # Normalizar para minúsculas
            
            for topic in record.get("topics", []):
                context_tokens.add(topic.lower()) # Normalizar para minúsculas
            
            # Coletar tokens de regras
            for rule in record.get("gitignore_rules", []):
                rule_tokens.add(rule)

    print(f"Encontrados {len(context_tokens)} tokens de contexto únicos.")
    print(f"Encontradas {len(rule_tokens)} regras de .gitignore únicas.")

    # Criar os mapeamentos de token para inteiro
    # Começamos com 0 para o token "desconhecido" (UNK) e 1 para o "padding" (PAD)
    # Isso é uma prática comum em NLP/ML
    context_vocab = {token: i + 2 for i, token in enumerate(sorted(list(context_tokens)))}
    context_vocab["<unk>"] = 0
    context_vocab["<pad>"] = 1

    rules_vocab = {token: i + 2 for i, token in enumerate(sorted(list(rule_tokens)))}
    rules_vocab["<unk>"] = 0
    rules_vocab["<pad>"] = 1

    # Salvar os vocabulários em arquivos JSON
    with open(CONTEXT_VOCAB_PATH, "w", encoding="utf-8") as f:
        json.dump(context_vocab, f, indent=2)
    print(f"Vocabulário de contexto salvo em: '{CONTEXT_VOCAB_PATH}'")

    with open(RULES_VOCAB_PATH, "w", encoding="utf-8") as f:
        json.dump(rules_vocab, f, indent=2)
    print(f"Vocabulário de regras salvo em: '{RULES_VOCAB_PATH}'")

if __name__ == "__main__":
    main()
