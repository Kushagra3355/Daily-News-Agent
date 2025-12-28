# Daily News Agent

An intelligent news aggregation and summarization system powered by LangChain and OpenAI. This project fetches technology news from NewsData.io API and generates AI-powered summaries for each article.

## Features

- **News Fetching**: Automatically fetches the latest technology news from NewsData.io API
- **Data Preprocessing**: Cleans and structures raw API responses for processing
- **AI-Powered Summarization**: Uses OpenAI's language models via LangChain to generate concise 3-4 line summaries
- **Structured Output**: Saves both raw news data and summaries in JSON format
- **Individual Article Processing**: Summarizes each news article separately with metadata

## Project Structure

```
Daily News Agent/
├── agents/
│   ├── fetcher_agent.py       # News fetching functionality
│   └── summerizer_agent.py    # AI summarization agent
├── app/
│   ├── config.py              # Configuration and environment variables
│   └── dependencies.py        # LLM initialization
├── data/
│   ├── news_response.json     # Raw news data from API
│   └── news_summary.json      # AI-generated summaries
├── test/
│   └── agent_test.py          # Main execution script
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
- **API Endpoint**: NewsData.io API v1

### Preprocessing Configuration

Adjust in `utils/preprocessing.py`:

- **Limit**: Number of articles to process (default: 5)

## Usage

### Basic Usage

Run the news fetching and summarization pipeline:

```bash
python -m test.agent_test
```

This will:

1. Load news data from `data/news_response.json`
2. Preprocess the articles
3. Generate AI summaries for each article
4. Save results to `data/news_summary.json`

### Fetch Fresh News

To fetch new news articles:

```python
from utils.fetcher import fetch_news

# Fetch news and save to data/news_response.json
news_data = fetch_news()
```

### Custom Summarization

```python
from agents.summerizer_agent import run_summarizer
from utils.preprocessing import preprocess_news

# Load and preprocess data
with open("data/news_response.json", "r") as f:
    api_response = json.load(f)

news_data = preprocess_news(api_response, limit=5)

# Generate summaries
result = run_summarizer(news_data)

print(f"Summarized {result['total_articles']} articles")
for summary in result['summaries']:
    print(f"Title: {summary['title']}")
    print(f"Summary: {summary['summary']}\n")
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

## Dependencies

Core dependencies:

- `langchain` - LLM framework
- `langchain-core` - Core LangChain functionality
- `langchain-openai` - OpenAI integration
- `langchainhub` - Pre-built prompts and chains
- `requests` - HTTP requests for API calls
- `python-dotenv` - Environment variable management

See `requirements.txt` for complete list.

## API Details

### NewsData.io API

- **Endpoint**: `https://newsdata.io/api/1/news`
- **Parameters**:
  - `apikey`: Your API key
  - `q`: Search query (e.g., "technology")
  - `language`: Language code (e.g., "en")
- **Rate Limits**: Check NewsData.io documentation

### OpenAI API

- **Models Supported**:
  - `gpt-4o-mini` (recommended for cost-efficiency)
  - `gpt-4o`
  - `gpt-3.5-turbo`
- **Usage**: Summarization tasks

## Workflow

```
1. Fetch News (fetcher.py)
   ↓
2. Save Raw Data (data/news_response.json)
   ↓
3. Preprocess Articles (preprocessing.py)
   ↓
4. AI Summarization (summerizer_agent.py)
   ↓
5. Save Summaries (data/news_summary.json)
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

3. **No News Data**
   ```
   Solution: Run news fetcher first
   python -c "from utils.fetcher import fetch_news; fetch_news()"
   ```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).

## Author

**Kushagra** - [GitHub Profile](https://github.com/Kushagra3355)

## Acknowledgments

- NewsData.io for news API
- OpenAI for language models
- LangChain for the LLM framework

## Support

For issues, questions, or contributions, please open an issue on the [GitHub repository](https://github.com/Kushagra3355/Daily-News-Agent/issues).

---

**Happy News Summarizing! 📰🤖**
