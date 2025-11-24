import os
import json
import time
from dotenv import load_dotenv
from github import Github, Auth, RateLimitExceededException, UnknownObjectException

# --- CONFIGURATION ---
DATA_DIR = "data"
OUTPUT_FILE = os.path.join(DATA_DIR, "corpus.jsonl")

# The Target List (The "Gatling Gun" Barrels)
TARGET_LANGUAGES = ["Python", "JavaScript", "Java", "Go", "Rust", "C++"]
REPOS_PER_LANG = 800  # 6 langs * 800 = ~4800 files
MIN_STARS = 100

def save_record(record):
    """Appends a single data record to the output file."""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")

def main():
    try:
        # --- 1. Authentication ---
        print("--- Authenticating with GitHub API ---")
        load_dotenv()
        github_token = os.getenv("GITHUB_TOKEN")
        if not github_token:
            print("Error: GITHUB_TOKEN not found in .env file.")
            return

        auth = Auth.Token(github_token)
        g = Github(auth=auth)
        print("Authentication successful.")

        # --- 2. The Gatling Gun Loop ---
        total_collected = 0
        
        # Check if file exists to maybe resume (simple check)
        if os.path.exists(OUTPUT_FILE):
             print(f"Note: Appending to existing {OUTPUT_FILE}")

        for lang in TARGET_LANGUAGES:
            print(f"\n" + "="*40)
            print(f"🎯 TARGET LOCKED: {lang}")
            print("="*40)
            
            # Construct Query: Specific Language + Min Stars
            query = f"language:{lang} stars:>{MIN_STARS}"
            
            try:
                # Search
                repositories = g.search_repositories(query=query, sort='stars', order='desc')
                print(f"Found {repositories.totalCount} candidates. Harvesting top {REPOS_PER_LANG}...")

                lang_count = 0
                
                # Iterate
                for repo in repositories:
                    if lang_count >= REPOS_PER_LANG:
                        break # Target met for this language
                    
                    try:
                        # Attempt to fetch .gitignore
                        # We try root first
                        try:
                            contents = repo.get_contents(".gitignore")
                            gitignore_content = contents.decoded_content.decode('utf-8')
                        except UnknownObjectException:
                            # Skip if not found
                            # print(f"    [SKIP] {repo.full_name} (No .gitignore)")
                            continue
                            
                        # Assemble Record
                        data_record = {
                            "repo_name": repo.full_name,
                            "language": lang, # Force the tag to be our target language
                            "topics": repo.topics,
                            "description": repo.description,
                            "gitignore_content": gitignore_content
                        }
                        
                        save_record(data_record)
                        lang_count += 1
                        total_collected += 1
                        
                        # Progress Bar for Language
                        if lang_count % 10 == 0:
                            print(f"    [+ {lang}] Collected {lang_count}/{REPOS_PER_LANG} (Total: {total_collected}) - {repo.full_name}")

                    except RateLimitExceededException:
                        raise # Bubble up to main handler
                    except Exception as e:
                        print(f"    [ERR] {repo.full_name}: {e}")
                        continue
                
                print(f"✅ Finished harvesting {lang}. Cooldown for 2 seconds...")
                time.sleep(2) # Be polite to API between language switches

            except RateLimitExceededException:
                print("\n🛑 CRITICAL: Rate Limit Hit. The script must stop.")
                print(f"Total collected so far: {total_collected}")
                break
            except Exception as e:
                print(f"Error searching for {lang}: {e}")

    except Exception as e:
        print(f"\nAn unexpected critical error occurred: {e}")

if __name__ == "__main__":
    main()