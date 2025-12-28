from app.dependencies import llm
from langchain_core.prompts import ChatPromptTemplate


def run_summarizer(news_data: list) -> dict:
    """Main function to run the summarizer"""

    summaries = []

    # Create prompt for individual article summarization
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a news summarizer. Summarize the given article in 3-4 lines. Keep facts accurate.",
            ),
            (
                "human",
                "Summarize this article:\n\nTitle: {title}\nDescription: {description}\n",
            ),
        ]
    )

    chain = prompt | llm()

    # Process each article
    for article in news_data:
        try:
            response = chain.invoke(
                {
                    "title": article.get("title", "N/A"),
                    "description": article.get("description", "N/A"),
                    "category": article.get("category", "N/A"),
                    "source": article.get("source", "N/A"),
                    "date": article.get("date", "N/A"),
                }
            )

            summaries.append(
                {
                    "title": article.get("title", "N/A"),
                    "summary": response.content,
                    "category": article.get("category", "N/A"),
                    "source": article.get("source", "N/A"),
                    "date": article.get("date", "N/A"),
                    "url": article.get("url", "N/A"),
                }
            )
        except Exception as e:
            print(f"Error summarizing article: {e}")
            continue

    return {"total_articles": len(summaries), "summaries": summaries}
