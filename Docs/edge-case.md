# Edge Cases & Mitigation Strategy: AI-Powered Discovery Engine

This document outlines the potential corner cases, failure modes, and edge cases for the AI-Powered Discovery Engine, along with proposed strategies to mitigate them. Identifying these early ensures the system is resilient before any code is written.

---

## 1. Data Ingestion Edge Cases
| Edge Case | Description | Mitigation Strategy |
| :--- | :--- | :--- |
| **API Rate Limiting** | Platforms like Reddit or Play Store may throttle or block requests if we pull data too fast. | Implement exponential backoff and retry logic (e.g., using the `tenacity` library). Use time-delays between requests. |
| **Geo-Fencing & Localization** | Pulling reviews might default to global instead of India (Swiggy's market). | Hardcode region parameters (`country='in'`) in scraper configurations to ensure relevance. |
| **Empty or Null Responses** | APIs might return empty datasets due to maintenance or lack of recent activity. | Add validation checks before saving to CSV. If empty, the script should log a warning rather than overwriting existing valid data with an empty file. |
| **DOM/HTML Changes** | Custom web scrapers for forums might break if the target website changes its layout. | Rely on official APIs (`praw`) or highly maintained wrappers (`google-play-scraper`) where possible. Use `try/except` blocks to handle parsing errors gracefully. |

## 2. Data Normalization & Cleaning Edge Cases
| Edge Case | Description | Mitigation Strategy |
| :--- | :--- | :--- |
| **"Hinglish" & Mixed Languages** | Indian users frequently mix Hindi and English (e.g., *"Bhai order late tha"*). Standard English NLP models might fail. | Use a robust language detection library. For MVP, explicitly filter for high-confidence English. For future scope, use multilingual embedding models (e.g., `paraphrase-multilingual-MiniLM`). |
| **Bot Spam & Fake Reviews** | Repeated "Nice app" or random characters (e.g., "asdfghjkl") polluting the dataset. | Filter out reviews under 8 words. Apply basic entropy checks or regex to drop repetitive character spam. |
| **Extremely Long Rants** | A user writes a 1,000-word essay about a bad delivery, which could skew clustering. | Truncate reviews to a maximum token length (e.g., 150 words) before feeding them to the embedding model to preserve context window space. |

## 3. Semantic Clustering Edge Cases
| Edge Case | Description | Mitigation Strategy |
| :--- | :--- | :--- |
| **The "Junk" Cluster** | HDBSCAN often groups noisy, unrelated data into a "-1" outlier cluster, which can confuse the LLM. | Explicitly exclude the "-1" (noise) cluster from being passed to the LLM for theme generation. |
| **Overlapping Themes** | "App is slow" and "Navigation is bad" might cluster together, diluting the specific UI insight. | Tune the UMAP dimensionality and HDBSCAN `min_cluster_size` parameters iteratively until the clusters are highly distinct. |

## 4. AI Reasoning (LLM) Edge Cases
| Edge Case | Description | Mitigation Strategy |
| :--- | :--- | :--- |
| **Hallucinated Quotes** | The LLM might invent a user quote that sounds realistic but doesn't exist in the raw data. | Use strict Prompt Engineering: *"You MUST ONLY quote directly from the provided text. Do not generate your own quotes."* Implement a post-processing script to string-match LLM quotes against the original CSV. |
| **Context Window Overflow** | Passing an entire cluster of 500 reviews to the Groq API might exceed the token limit. | Sample the top 50 most representative reviews (closest to the cluster centroid) to send to the LLM, rather than the entire cluster. |
| **Generic/Vague Insights** | The LLM outputs unhelpful advice like "Make the app better" instead of actionable Growth PM insights. | Assign a strong system persona in the prompt: *"You are a Senior Growth PM at Swiggy. Provide specific, actionable UI/UX nudges to solve category inertia."* |

## 5. System & UI Edge Cases
| Edge Case | Description | Mitigation Strategy |
| :--- | :--- | :--- |
| **Missing Environment Variables** | Script crashes because `GROQ_API_KEY` or `REDDIT_CLIENT_ID` is missing from the `.env` file. | Add a startup check in the scripts that immediately raises a clear error `ValueError("Missing GROQ_API_KEY")` before executing logic. |
| **Stale Dashboard Data** | The Render UI shows outdated insights because the pipeline hasn't run in a week. | Display a "Last Updated: [Timestamp]" on the UI so evaluators know exactly when the data was ingested. |
