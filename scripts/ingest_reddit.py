import praw
import pandas as pd
import os
from dotenv import load_dotenv

def fetch_reddit_discussions():
    load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
    
    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET")
    user_agent = os.getenv("REDDIT_USER_AGENT", "InstamartResearchBot/1.0")
    
    if not all([client_id, client_secret]):
        print("Warning: Reddit API credentials missing in .env. Please add them to run the Reddit scraper.")
        return
        
    try:
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )
        
        print("Searching Reddit for Swiggy Instamart discussions...")
        search_query = "Swiggy Instamart OR Blinkit OR Zepto"
        subreddits = ["bangalore", "mumbai", "india", "delhi"]
        
        formatted_posts = []
        
        for sub in subreddits:
            print(f"Scanning r/{sub}...")
            try:
                subreddit = reddit.subreddit(sub)
                for submission in subreddit.search(search_query, limit=50, sort="new"):
                    formatted_posts.append({
                        "source": f"Reddit - r/{sub}",
                        "date": pd.to_datetime(submission.created_utc, unit='s'),
                        "rating": submission.score, # Upvotes
                        "text": submission.title + " " + (submission.selftext if submission.selftext else ""),
                        "author": str(submission.author)
                    })
            except Exception as e:
                print(f"Error accessing r/{sub}: {e}")
                
        if formatted_posts:
            df = pd.DataFrame(formatted_posts)
            os.makedirs(os.path.join(os.path.dirname(__file__), "..", "data"), exist_ok=True)
            output_path = os.path.join(os.path.dirname(__file__), "..", "data", "raw_reddit_discussions.csv")
            df.to_csv(output_path, index=False)
            print(f"Saved {len(df)} Reddit posts to {output_path}")
        else:
            print("No Reddit posts found or extracted.")
            
    except Exception as e:
        print(f"Failed to connect to Reddit API: {e}")

if __name__ == "__main__":
    fetch_reddit_discussions()
