# Swiggy Pulse: AI Discovery Engine

Swiggy Pulse is an AI-powered internal analytics dashboard designed to combat "Category Inertia" on Swiggy Instamart. By leveraging unsupervised machine learning (HDBSCAN/UMAP) on unstructured user feedback and processing the clusters through a Large Language Model (Llama 3.3), this tool provides real-time, data-grounded insights for Product Managers.

## Architecture

1. **Ingestion**: Scrapes unstructured data from Google Play Store and Reddit.
2. **Processing**: Cleans and filters text data using NLP pipelines.
3. **Clustering**: Groups semantic themes using `sentence-transformers`, `umap-learn`, and `hdbscan`.
4. **Insights Engine**: Uses Groq (Llama-3.3-70b-versatile) with strict guardrails to answer strategic PM queries based solely on the clustered data.
5. **Dashboard**: A highly optimized FastAPI backend serving a custom HTML/CSS frontend.

## Local Development

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Environment Variables
Create a `.env` file in the root directory and add your Groq API key:
```env
GROQ_API_KEY="your_api_key_here"
```

### 3. Run the Server
```bash
uvicorn app.main:app --reload
```
Navigate to `http://localhost:8000` to view the Swiggy Pulse dashboard.

## Deployment
This application is containerized and configured for deployment on Railway via the provided `Dockerfile` and `railway.json`.
