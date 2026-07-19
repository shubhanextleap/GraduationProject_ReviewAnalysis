import os
import json
from dotenv import load_dotenv
from groq import Groq

def generate_insights():
    # 1. Setup Environment
    env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
    load_dotenv(env_path, override=True)
    
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("Error: GROQ_API_KEY not found in .env file.")
        return
        
    try:
        # The groq library automatically handles headers and authorization properly
        client = Groq(api_key=api_key)
    except Exception as e:
        print(f"Failed to initialize Groq client: {e}")
        return

    # 2. Load Clustered Data
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    input_file = os.path.join(data_dir, "clustered_themes.json")
    
    if not os.path.exists(input_file):
        print("Error: clustered_themes.json not found! Run Phase 3 first.")
        return
        
    with open(input_file, 'r') as f:
        clustered_data = json.load(f)
        
    if not clustered_data:
        print("No clusters found to analyze.")
        return
        
    print(f"Loaded {len(clustered_data)} clusters for LLM analysis.")
    
    # 3. Construct the System Prompt
    system_prompt = """
You are a Senior Growth Product Manager at Swiggy Instamart. 
Your goal is to solve "Category Inertia" (users repeatedly buying the same items and rarely exploring new categories).
You are analyzing unstructured feedback (Play Store, Reddit) that has been grouped into thematic clusters using Machine Learning.

Based ONLY on the provided cluster data, answer the following 8 strategic questions:
1. Why do users repeatedly buy from the same categories?
2. What prevents users from exploring new categories?
3. How do users discover products today?
4. What role do habits play in shopping behavior?
5. What information do users need before trying a new category?
6. What frustrations emerge repeatedly?
7. Which user segments are more likely to experiment?
8. What unmet needs emerge consistently across discussions?

RULES:
- Answer each question directly as a Product Manager.
- You MUST provide direct quotes from the provided data as citations for your claims. Do not hallucinate quotes.
- Return the output in valid JSON format. The keys should be "Q1" through "Q8", and each value should be an object containing an "insight" string and a "citations" list of exact strings.
"""

    user_prompt = f"Here is the clustered user feedback:\n{json.dumps(clustered_data, indent=2)}"
    
    # 4. Call the Groq LLM
    print("Sending structured data to Groq API (Llama 3.3 70b)...")
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2, # Low temperature for highly analytical, non-hallucinated consistency
            response_format={"type": "json_object"}
        )
        
        response_json = json.loads(completion.choices[0].message.content)
        
        # 5. Save the final insights
        output_path = os.path.join(data_dir, "final_insights.json")
        with open(output_path, 'w') as f:
            json.dump(response_json, f, indent=4)
            
        print(f"Success! Final insights saved to {output_path}")
        
    except Exception as e:
        print(f"Error calling Groq API: {e}")

if __name__ == "__main__":
    generate_insights()
