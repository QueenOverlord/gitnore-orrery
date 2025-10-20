import os
import json

# Define os caminhos de entrada e saída
RAW_DATA_PATH = "data/corpus.jsonl"
PROCESSED_DATA_PATH = "data/processed_corpus.jsonl"

def clean_gitignore_content(content_string):
    """
    Recebe o conteúdo bruto de um .gitignore e retorna uma lista limpa de regras.
    """
    cleaned_rules = []
    for line in content_string.splitlines():
        # Remove espaços em branco no início/fim da linha
        stripped_line = line.strip()
        
        # Ignora linhas vazias, comentários (#) e regras de negação (!)
        if stripped_line and not stripped_line.startswith('#') and not stripped_line.startswith('!'):
            cleaned_rules.append(stripped_line)
            
    return cleaned_rules

def main():
    """
    Função principal para ler, processar e salvar os dados.
    """
    print("--- Iniciando o pré-processamento dos dados ---")
    
    # Certificar-se de que o arquivo de saída está limpo antes de começar
    if os.path.exists(PROCESSED_DATA_PATH):
        os.remove(PROCESSED_DATA_PATH)
        print(f"Arquivo antigo '{PROCESSED_DATA_PATH}' removido.")

    processed_count = 0
    # Abrir o arquivo de dados brutos para leitura
    with open(RAW_DATA_PATH, "r", encoding="utf-8") as infile:
        # Ler o arquivo linha por linha
        for line in infile:
            # Converter a string JSON da linha em um dicionário Python
            record = json.loads(line)
            
            # Limpar o conteúdo do gitignore
            raw_content = record.get("gitignore_content", "")
            cleaned_rules = clean_gitignore_content(raw_content)
            
            # Atualizar o registro com a lista de regras limpas
            record["gitignore_rules"] = cleaned_rules
            del record["gitignore_content"] # Remove o campo antigo e bagunçado
            
            # Salvar o registro processado no novo arquivo .jsonl
            with open(PROCESSED_DATA_PATH, "a", encoding="utf-8") as outfile:
                outfile.write(json.dumps(record) + "\n")
            
            processed_count += 1

    print(f"\n--- Pré-processamento concluído ---")
    print(f"Total de registros processados: {processed_count}")
    print(f"Dados limpos salvos em: '{PROCESSED_DATA_PATH}'")

if __name__ == "__main__":
    main()
