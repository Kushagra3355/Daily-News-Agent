# Daily News Agent

An intelligent news aggregation and summarization system powered by OpenAI. This project fetches technology news from NewsData.io API and generates AI-powered summaries for each article.

## Features

- **News Fetching**: Automatically fetches the latest technology news from NewsData.io API with pagination support (up to 3 pages)
- **Data Preprocessing**: Cleans and structures raw API responses for processing
- **AI-Powered Summarization**: Uses OpenAI's language models to generate concise 3-4 line summaries
- **Structured Output**: Saves both raw news data and summaries in JSON format
- **Individual Article Processing**: Summarizes each news article separately with metadata

## Project Structure

```
Daily News Agent/
├── agents/
│   └── summerizer_agent.py    # AI summarization agent
├── app/
│   ├── config.py              # Configuration and environment variables
│   └── dependencies.py        # LLM initialization
├── data/
│   ├── news_response.json     # Raw news data from API
│   └── news_summary.json      # AI-generated summaries
├── test/
│   └── agent_test.py          # Main execution script
│   └── news_api_test.py       #Checks and loads the news 
├── utils/
│   ├── fetcher.py             # Utility functions for news fetching
│   └── preprocessing.py       # Data preprocessing utilities
├── requirements.txt           # Project dependencies
└── .env                       # Environment variables (not in repo)
```

## Prerequisites

- Python 3.8+
- OpenAI API Key
- NewsData.io API Key

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/Kushagra3355/Daily-News-Agent.git
   cd Daily-News-Agent
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv

   # On Windows
   venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   Create a `.env` file in the root directory:

   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   NEWS_API_KEY=your_newsdata_api_key_here
   MODEL_NAME=gpt-4o-mini
   TEMPERATURE=0
   ```

   **Get your API keys:**

   - OpenAI API Key: https://platform.openai.com/api-keys
   - NewsData.io API Key: https://newsdata.io/register

## Configuration

### Environment Variables

| Variable         | Description              | Default       |
| ---------------- | ------------------------ | ------------- |
| `OPENAI_API_KEY` | Your OpenAI API key      | Required      |
| `NEWS_API_KEY`   | Your NewsData.io API key | Required      |
| `MODEL_NAME`     | OpenAI model to use      | `gpt-4o-mini` |
| `TEMPERATURE`    | LLM temperature (0-1)    | `0`           |

### News Fetching Configuration

Modify parameters in `utils/fetcher.py`:

- **Query**: Change the topic (default: "technology")
- **Language**: Set language preference (default: "en")
- **Pagination**: Fetches up to 3 pages of results automatically
- **API Endpoint**: NewsData.io API v1

### Preprocessing Configuration

Adjust in `utils/preprocessing.py`:

- **Limit**: Number of articles to process (default: 5)

## Usage

### Running the Application

The simplest way to run the complete news aggregation and summarization pipeline:

```bash
python app/main.py
```

Or using the module syntax:

```bash
python -m app.main
```

This will automatically:

1. Fetch fresh news articles from NewsData.io API (up to 3 pages)
2. Preprocess and clean the article data
3. Generate AI-powered summaries for each article
4. Save results to `data/news_summary.json`

### Basic Usage

Alternatively, you can run individual test scripts:

```bash
python -m test.agent_test
```

This will:

1. Load news data from `data/news_response.json`
2. Preprocess the articles
3. Generate AI summaries for each article
4. Save results to `data/news_summary.json`

### Fetch Fresh News

To fetch new news articles (automatically fetches up to 3 pages):

```python
from utils.fetcher import fetch_news

# Fetch news with pagination and save to data/news_response.json
news_data = fetch_news()
```

## Output Format

### news_summary.json Structure

```json
{
  "total_articles": 3,
  "summaries": [
    {
      "title": "Article Title",
      "summary": "AI-generated 3-4 line summary...",
      "category": "technology",
      "source": "TechCrunch",
      "date": "2025-12-28",
      "url": "https://example.com/article"
    }
  ]
}
```

## Customization

### Change News Topic

Edit `utils/fetcher.py`:

```python
params = {
    "apikey": NEWS_API_KEY,
    "q": "artificial intelligence",  # Change topic here
    "language": "en"
}
# Automatically fetches up to 3 pages for the specified topic
```

### Adjust Summary Length

Modify the prompt in `agents/summerizer_agent.py`:

```python
"system": "You are a news summarizer. Summarize the given article in 5-6 lines."
```

### Change AI Model

Update `.env`:

```env
MODEL_NAME=gpt-4o
```

## Troubleshooting

### Common Issues

1. **Import Errors**

   ```
   Solution: Ensure all dependencies are installed
   pip install -r requirements.txt
   ```

2. **API Key Errors**

   ```
   Solution: Check .env file has correct keys
   Verify keys are active on respective platforms
   ```
