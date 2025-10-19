import os
from dotenv import load_dotenv
from github import Github, Auth, RateLimitExceededException

# This function will be our main entry point
def main():
    """
    Main function to authenticate with the GitHub API and check the connection.
    """
    try:
        # --- Authentication ---
        load_dotenv()
        github_token = os.getenv("GITHUB_TOKEN")
        
        if not github_token:
            print("Error: GITHUB_TOKEN not found in environment variables.")
            return

        auth = Auth.Token(github_token)
        g = Github(auth=auth)

        # --- Verification ---
        user = g.get_user()
        print(f"Authentication successful for user: {user.login}")

        # Get the rate limit object and access the 'rate' attribute
        rate_limit = g.get_rate_limit()
        
        # The correct structure is rate_limit.rate
        print(f"API Rate Limit: {rate_limit.rate.remaining}/{rate_limit.rate.limit}")
        print(f"Reset time: {rate_limit.rate.reset}")

    except RateLimitExceededException:
        print("GitHub API rate limit has been exceeded.")
    except Exception as e:
        print(f"An error occurred: {e}")

# This standard Python construct ensures that main() is called when the script is executed
if __name__ == "__main__":
    main()
