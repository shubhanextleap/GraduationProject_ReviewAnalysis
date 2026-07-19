import pandas as pd
import re
import os

def is_pure_english(text):
    if not isinstance(text, str):
        return False
    try:
        # If it can't be encoded to ascii, it contains emojis or other languages
        text.encode('ascii')
        return True
    except UnicodeEncodeError:
        return False

def clean_text(text):
    if not isinstance(text, str):
        return ""
    
    # Remove newlines and extra spaces
    text = re.sub(r'\s+', ' ', text)
    
    # Lowercase and strip whitespace
    text = text.lower().strip()
    return text

def process_data():
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    playstore_file = os.path.join(data_dir, "raw_playstore_reviews.csv")
    reddit_file = os.path.join(data_dir, "raw_reddit_discussions.csv")
    
    dfs = []
    
    if os.path.exists(playstore_file):
        df_play = pd.read_csv(playstore_file)
        dfs.append(df_play)
        print(f"Loaded {len(df_play)} Play Store reviews.")
    else:
        print("Play Store data not found. Skipping...")
    
    if os.path.exists(reddit_file):
        df_reddit = pd.read_csv(reddit_file)
        dfs.append(df_reddit)
        print(f"Loaded {len(df_reddit)} Reddit discussions.")
    else:
        print("Reddit data not found. Skipping...")
        
    if not dfs:
        print("No raw data found in the data/ directory! Please run the ingestion scripts first.")
        return
        
    # Combine all datasets
    combined_df = pd.concat(dfs, ignore_index=True)
    print(f"\nTotal raw records before cleaning: {len(combined_df)}")
    
    # 1. Drop NA texts
    combined_df = combined_df.dropna(subset=['text'])
    
    # 2. Drop reviews that contain emojis or non-English characters
    combined_df = combined_df[combined_df['text'].apply(is_pure_english)]
    print(f"Records after dropping emojis & non-English: {len(combined_df)}")
    
    # 3. Clean text (lowercase, strip)
    combined_df['clean_text'] = combined_df['text'].apply(clean_text)
    
    # 3. Filter short reviews (< 8 words)
    combined_df['word_count'] = combined_df['clean_text'].apply(lambda x: len(x.split()))
    filtered_df = combined_df[combined_df['word_count'] >= 8].copy()
    
    # 4. Remove any strings that are completely empty after cleaning
    filtered_df = filtered_df[filtered_df['clean_text'].str.strip() != ""]
    
    print(f"Total records remaining after cleaning and filtering (<8 words): {len(filtered_df)}")
    
    # Save the cleaned dataset
    output_path = os.path.join(data_dir, "clean_reviews.csv")
    filtered_df.to_csv(output_path, index=False)
    print(f"Saved cleaned data to {output_path}")

if __name__ == "__main__":
    process_data()
