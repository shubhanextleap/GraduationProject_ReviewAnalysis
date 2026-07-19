import pandas as pd
from google_play_scraper import Sort, reviews
import os

def fetch_playstore_reviews(app_id="in.swiggy.android", count=1000):
    print(f"Fetching {count} reviews for {app_id}...")
    try:
        result, continuation_token = reviews(
            app_id,
            lang='en', # English only
            country='in', # India only
            sort=Sort.NEWEST,
            count=count
        )
        
        # Extract relevant fields
        formatted_reviews = []
        for r in result:
            formatted_reviews.append({
                "source": "Play Store",
                "date": r["at"],
                "rating": r["score"],
                "text": r["content"],
                "author": r["userName"]
            })
            
        df = pd.DataFrame(formatted_reviews)
        
        # Ensure data directory exists
        os.makedirs(os.path.join(os.path.dirname(__file__), "..", "data"), exist_ok=True)
        
        # Save to CSV
        output_path = os.path.join(os.path.dirname(__file__), "..", "data", "raw_playstore_reviews.csv")
        df.to_csv(output_path, index=False)
        print(f"Saved {len(df)} reviews to {output_path}")
        
    except Exception as e:
        print(f"Error fetching Play Store reviews: {e}")

if __name__ == "__main__":
    fetch_playstore_reviews(count=500)
