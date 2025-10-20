import os
import json
from dotenv import load_dotenv
from github import Github, Auth, RateLimitExceededException, UnknownObjectException

# Defines the output path for our data
DATA_DIR = "data"
OUTPUT_FILE = os.path.join(DATA_DIR, "corpus.jsonl")

def save_record(record):
    """Appends a single data record to the output file."""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")

def main():
    """
    Main function to search for repositories, extract data, and save it.
    """
    try:
        # --- 1. Authentication ---
        print("--- Authenticating with GitHub API ---")
        load_dotenv()
        github_token = os.getenv("GITHUB_TOKEN")
        if not github_token:
            print("Error: GITHUB_TOKEN not found.")
            return

        auth = Auth.Token(github_token)
        g = Github(auth=auth)
        print("Authentication successful.")

        # --- 2. Search and Process ---
        print("\n--- Starting Repository Search ---")
        
        # The search is now repository-centric query
        query = "stars:>500"
        
        MAX_REPOS_TO_PROCESS = 50
        
        repositories = g.search_repositories(query=query, sort='stars', order='desc')
        print(f"Found {repositories.totalCount} total repositories. Processing up to {MAX_REPOS_TO_PROCESS}...")

        count = 0
        for repo in repositories:
            if count >= MAX_REPOS_TO_PROCESS:
                print(f"\nReached the limit of {MAX_REPOS_TO_PROCESS} repositories.")
                break

            try:
                # Get the .gitignore file content
                gitignore_file = repo.get_contents(".gitignore")
                gitignore_content = gitignore_file.decoded_content.decode('utf-8')

                # Assemble the data record
                data_record = {
                    "repo_name": repo.full_name,
                    "language": repo.language,
                    "topics": repo.topics,
                    "description": repo.description,
                    "gitignore_content": gitignore_content
                }
                
                # Save the record to our file
                save_record(data_record)
                
                print(f"({count + 1}/{MAX_REPOS_TO_PROCESS}) Successfully processed and saved: {repo.full_name}")

            except UnknownObjectException:
                # This is now an EXPECTED and COMMON outcome.
                # It just means the popular repo doesn't have a .gitignore in its root.
                print(f"({count + 1}/{MAX_REPOS_TO_PROCESS}) Skipped {repo.full_name}: .gitignore not found in root.")
            except Exception as e:
                print(f"({count + 1}/{MAX_REPOS_TO_PROCESS}) An error occurred for {repo.full_name}: {e}")
            
            count += 1

    except RateLimitExceededException:
        print("\nCRITICAL: GitHub API rate limit has been exceeded. Please wait for it to reset.")
    except Exception as e:
        print(f"\nAn unexpected critical error occurred: {e}")

if __name__ == "__main__":
    main()
