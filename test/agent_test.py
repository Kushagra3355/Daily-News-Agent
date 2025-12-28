import json
import os, sys
from utils.preprocessing import preprocess_news
from agents.summerizer_agent import run_summarizer


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Load existing news data
print("Loading news data from file...")
with open("data/news_response.json", "r") as f:
    api_response = json.load(f)

# Preprocess news
print("Preprocessing news...")
news_data = preprocess_news(api_response, limit=15)

# Run summarizer agent
print("\nRunning summarizer agent...\n")
result = run_summarizer(news_data)

# Save summary to JSON
os.makedirs("data", exist_ok=True)
with open("data/news_summary.json", "w") as f:
    json.dump(result, f, indent=2)

print("\n=== SUMMARY ===")
print(f"Total articles summarized: {result['total_articles']}")
for i, summary in enumerate(result["summaries"], 1):
    print(f"\n--- Article {i} ---")
    print(f"Title: {summary['title']}")
    print(f"Summary: {summary['summary']}")
    print(f"Source: {summary['source']}")

print("\n✓ Summary saved to data/news_summary.json")
print("\n✓ Summary saved to data/news_summary.json")
