from utils.fetcher import fetch_news
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))


if __name__ == "__main__":
    fetch_news()
