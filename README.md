# Daily News Agent

An intelligent news aggregation and summarization system powered by OpenAI. This project fetches technology news from NewsData.io API and generates AI-powered summaries for each article.

## Features

- **News Fetching**: Automatically fetches the latest technology news from NewsData.io API with pagination support (up to 3 pages)
- **Data Preprocessing**: Cleans and structures raw API responses for processing
- **AI-Powered Summarization**: Uses OpenAI's language models to generate concise 3-4 line summaries
- **REST API**: FastAPI-based REST endpoints for easy integration
- **Category Filtering**: Filter news by categories and list available categories
- **Caching**: Efficient caching system to avoid redundant API calls
- **Structured Output**: Saves both raw news data and summaries in JSON format
- **Individual Article Processing**: Summarizes each news article separately with metadata

## Project Structure

```
Daily News Agent/
├── agents/
│   └── summerizer_agent.py    # AI summarization agent
├── api/
│   └── main.py                # FastAPI REST API endpoints
├── app/
│   ├── config.py              # Configuration and environment variables
│   ├── dependencies.py        # LLM initialization
│   └── temp_main.py           # Standalone script runner
├── data/
│   ├── news_response.json     # Raw news data from API (generated)
│   └── news_summary.json      # AI-generated summaries (generated)
├── test/
│   ├── agent_test.py          # Test script for agent functionality
│   └── news_api_test.py       # Test script for news API
├── tools/
│   ├── category_filter.py     # Filter news by category
│   └── category_extractor.py  # Extract available categories
├── utils/
│   ├── fetcher.py             # News fetching with pagination (up to 3 pages)
│   ├── preprocessing.py       # Data preprocessing utilities
│   └── scheduler.py           # Job scheduler for daily news pipeline
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

### Option 1: Run as REST API (Recommended)

Start the FastAPI server:

```bash
uvicorn api.main:app --reload
```

The API will be available at `http://localhost:8000`

**API Endpoints:**

#### 1. `POST /news/refresh`

**Purpose:** Manually trigger news fetching and summarization pipeline

**Description:** This endpoint fetches fresh news from NewsData.io API (up to 3 pages), preprocesses the data, generates AI summaries using OpenAI, and saves the results to the cache file.

**Response:**

```json
{
  "message": "News refreshed successfully",
  "data": {
    "total_articles": 15,
    "summaries": [...]
  }
}
```

**Example:**

```bash
curl -X POST http://localhost:8000/news/refresh
```

---

#### 2. `GET /news/all`

**Purpose:** Retrieve all cached news summaries

**Description:** Returns all news articles with AI-generated summaries from the cache. This endpoint reads from `data/news_summary.json` without making new API calls.

**Response:**

```json
{
  "total_articles": 15,
  "summaries": [
    {
      "title": "AI Breakthrough in Natural Language Processing",
      "summary": "Researchers have developed a new model that achieves state-of-the-art results...",
      "category": ["technology", "ai"],
      "source": "TechCrunch",
      "date": "2025-12-29",
      "url": "https://example.com/article1"
    }
  ]
}
```

**Example:**

```bash
curl http://localhost:8000/news/all
```

---

#### 3. `GET /news/category/{category}`

**Purpose:** Filter news by specific category

**Description:** Returns only news articles that match the specified category. Categories are case-insensitive (e.g., "Technology", "technology", "TECHNOLOGY" all work).

**Parameters:**

- `category` (path parameter): The category name to filter by (e.g., "technology", "business", "sports")

**Response:**

```json
{
  "category": "technology",
  "total_articles": 8,
  "summaries": [
    {
      "title": "Tech Article Title",
      "summary": "Article summary...",
      "category": ["technology"],
      "source": "TechCrunch",
      "date": "2025-12-29",
      "url": "https://example.com/article"
    }
  ]
}
```

**Example:**

```bash
curl http://localhost:8000/news/category/technology
curl http://localhost:8000/news/category/business
curl http://localhost:8000/news/category/ai
```

---

#### 4. `GET /news/categories`

**Purpose:** List all available news categories

**Description:** Returns a list of all unique categories present in the cached news data, sorted alphabetically.

**Response:**

```json
{
  "total_categories": 5,
  "categories": ["ai", "business", "politics", "technology", "world"]
}
```

**Example:**

```bash
curl http://localhost:8000/news/categories
```

---

**Interactive API Documentation:**

Visit `http://localhost:8000/docs` for Swagger UI interactive documentation where you can:

- Test all endpoints directly from your browser
- View detailed request/response schemas
- See example responses
- Try different parameters

**Alternative Documentation:**

Visit `http://localhost:8000/redoc` for ReDoc alternative documentation with a different UI.

---

**Error Responses:**

If no cached data is available:

```json
{
  "detail": "No news data available. Please call /news/refresh first."
}
```

HTTP Status: `404 Not Found`

### Option 2: Run as Standalone Script

Run the complete news aggregation and summarization pipeline:

```bash
python app/temp_main.py
```

This will automatically:

1. Fetch fresh news articles from NewsData.io API (up to 3 pages)
2. Preprocess and clean the article data
3. Generate AI-powered summaries for each article
4. Save results to `data/news_summary.json`

### Option 3: Run Test Scripts

Run individual test scripts:

```bash
# Test the summarization agent
python -m test.agent_test

# Test the news API fetcher
python -m test.news_api_test
```

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
      "category": ["technology", "ai"],
      "source": "TechCrunch",
      "date": "2025-12-28",
      "url": "https://example.com/article"
    }
  ]
}
```

### API Response Format

**GET /news/all:**

```json
{
  "total_articles": 3,
  "summaries": [...]
}
```

**GET /news/category/{category}:**

```json
{
  "category": "technology",
  "total_articles": 2,
  "summaries": [...]
}
```

**GET /news/categories:**

```json
{
  "total_categories": 5,
  "categories": ["ai", "business", "science", "technology", "world"]
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

3. **No News Data Available (404 Error)**

   ```
   Solution: Run POST /news/refresh first to fetch and generate news data
   Or run: python app/temp_main.py
   ```

4. **FastAPI Server Issues**
   ```
   Solution: Ensure uvicorn is installed
   pip install uvicorn[standard]
   Check port 8000 is not in use
   ```
