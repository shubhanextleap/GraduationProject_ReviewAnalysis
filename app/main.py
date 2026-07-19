import os
import json
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
from groq import Groq

# Setup Environment
env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(env_path, override=True)
api_key = os.getenv("GROQ_API_KEY")

app = FastAPI()

def load_clusters():
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    input_file = os.path.join(data_dir, "clustered_themes.json")
    if not os.path.exists(input_file):
        return None
    with open(input_file, 'r') as f:
        return json.load(f)

# The HTML UI
html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Swiggy Pulse | Instamart Analytics</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <style>
        body {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 40px;
            box-sizing: border-box;
        }
        .dashboard {
            background: rgba(255, 255, 255, 0.85);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            padding: 50px;
            border-radius: 24px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.08), border: 1px solid rgba(255,255,255,0.3);
            width: 100%;
            max-width: 850px;
        }
        .brand-badge {
            display: inline-block;
            background-color: #fc8019;
            color: white;
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            padding: 6px 12px;
            border-radius: 20px;
            margin-bottom: 20px;
        }
        .header {
            color: #1a1a1a;
            font-size: 36px;
            font-weight: 700;
            margin: 0 0 10px 0;
            letter-spacing: -1px;
        }
        .subtitle {
            color: #666;
            font-size: 16px;
            font-weight: 300;
            margin-bottom: 40px;
        }
        .search-container {
            display: flex;
            gap: 12px;
            position: relative;
        }
        input {
            flex: 1;
            padding: 20px 24px;
            border: 1px solid #e1e4e8;
            border-radius: 12px;
            font-size: 16px;
            background: #ffffff;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px rgba(0,0,0,0.02);
            font-family: 'Inter', sans-serif;
        }
        input:focus {
            outline: none;
            border-color: #fc8019;
            box-shadow: 0 0 0 4px rgba(252, 128, 25, 0.1);
        }
        button {
            background: linear-gradient(135deg, #fc8019 0%, #e27317 100%);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 0 32px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(252, 128, 25, 0.3);
        }
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(252, 128, 25, 0.4);
        }
        button:active {
            transform: translateY(0);
        }
        .result-box {
            margin-top: 40px;
            padding: 30px;
            background-color: #ffffff;
            border-radius: 16px;
            border: 1px solid #eee;
            box-shadow: 0 10px 30px rgba(0,0,0,0.03);
            font-size: 16px;
            line-height: 1.8;
            color: #333;
            display: none;
            animation: fadeIn 0.5s ease;
        }
        .result-box h1, .result-box h2, .result-box h3 {
            color: #1a1a1a;
            margin-top: 0;
        }
        .result-box strong {
            color: #fc8019;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .loading-text {
            color: #fc8019;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 10px;
        }
    </style>
</head>
<body>
    <div class="dashboard">
        <div class="brand-badge">Internal Tool</div>
        <h1 class="header">Swiggy Pulse</h1>
        <p class="subtitle">Query real-time user sentiment and category analysis for Instamart.</p>
        
        <div class="search-container">
            <input type="text" id="query" placeholder="Ask a question about the Instamart data..." onkeydown="if(event.key === 'Enter') fetchInsight()">
            <button onclick="fetchInsight()">Analyze</button>
        </div>

        <div id="result" class="result-box"></div>
    </div>

    <script>
        async function fetchInsight() {
            const query = document.getElementById('query').value;
            if (!query) return;
            
            const resultBox = document.getElementById('result');
            resultBox.style.display = 'block';
            resultBox.innerHTML = "<div class='loading-text'>⏳ Synthesizing insights from cluster data...</div>";
            
            try {
                const response = await fetch(`/api/ask?question=${encodeURIComponent(query)}`);
                const data = await response.json();
                
                if (data.error) {
                    resultBox.innerHTML = `<span style="color:#d93025; font-weight:600;">Error: ${data.error}</span>`;
                } else {
                    resultBox.innerHTML = marked.parse(data.answer);
                }
            } catch (err) {
                resultBox.innerHTML = `<span style="color:#d93025; font-weight:600;">Network Error: ${err.message}</span>`;
            }
        }
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def home():
    return html_content

@app.get("/api/ask")
def ask_ai(question: str):
    if not api_key:
        return {"error": "GROQ_API_KEY is not configured in .env"}
        
    clustered_data = load_clusters()
    if not clustered_data:
        return {"error": "No clustered data found. Run Phase 3 first."}

    try:
        client = Groq(api_key=api_key)
        
        system_prompt = """
You are an AI Analyst analyzing Swiggy Instamart "Category Inertia" (users repeatedly buying the same items and rarely exploring new categories).
You are analyzing unstructured feedback (Play Store, Reddit) that has been grouped into thematic clusters using Machine Learning.

GUARDRAIL RULE: You are STRICTLY scoped to Swiggy Instamart, grocery delivery, and user shopping habits (Category Inertia). 
If the user asks a question that is NOT related to these topics (e.g., sports, politics, general knowledge, generic programming, FIFA), you MUST refuse to answer. 
Reply exactly with: 'I am an AI Discovery Engine focused on Swiggy Instamart. I cannot answer unrelated questions.'

If the question is relevant, answer it directly based ONLY on the provided cluster data.
TONE CONSTRAINT: Your response must be highly objective, analytical, and business-focused. Do NOT pretend to be a human or use conversational filler.
STYLE RULE: Do NOT mention the words 'cluster', 'data', or 'JSON'. Do not explicitly say 'Cluster_0'. Present the insights as direct business facts occurring on the platform.
LENGTH CONSTRAINT: Keep the response short, crisp, clear, and to the point. No fluff.

FORMATTING RULE (CRITICAL): You MUST format your answer EXACTLY according to this structure every single time, using a Markdown table. Do not write paragraphs.
1. **🎯 Core Insight:** [One bold sentence summarizing the answer]
2. **📊 Evidence Matrix:** [A markdown table with two columns: 'Friction Point' | 'Real User Quote'. Pull exact quotes from the data.]
3. **🚀 Actionable Takeaway:** [One bullet point on what a PM should do]
"""
        user_prompt = f"Here is the clustered user feedback:\n{json.dumps(clustered_data, indent=2)}\n\nUSER QUESTION:\n{question}"
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2 # Low temp for consistent, strict guardrail adherence
        )
        
        answer = completion.choices[0].message.content
        return {"answer": answer}
        
    except Exception as e:
        return {"error": str(e)}
