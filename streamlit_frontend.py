import streamlit as st
import json
import os
from utils.scheduler import run_daily_job
from tools.category_filter import filter_news_by_category
from tools.category_extractor import get_all_categories

# Page configuration
st.set_page_config(page_title="Daily News Summarizer", page_icon="📰", layout="wide")

# Initialize session state
if "processing" not in st.session_state:
    st.session_state.processing = False

# Title
st.title(" Daily News Summarizer")
st.markdown("---")


def load_cached_news():
    """Load news summary from cached file."""
    cache_file = "data/news_summary.json"
    if not os.path.exists(cache_file):
        return None

    with open(cache_file, "r") as f:
        return json.load(f)


def display_article(article):
    """Display a single news article."""
    with st.container():
        st.subheader(article.get("title", "No Title"))
        st.write(article.get("summary", "No summary available"))

        col1, col2, col3 = st.columns(3)
        with col1:
            st.caption(f"**Source:** {article.get('source', 'Unknown')}")
        with col2:
            st.caption(f"**Date:** {article.get('date', 'Unknown')}")
        with col3:
            categories = ", ".join(article.get("category", []))
            st.caption(f"**Categories:** {categories}")

        if article.get("url"):
            st.link_button("Read Full Article", article.get("url"))

        st.markdown("---")


# Sidebar controls
with st.sidebar:
    st.header("Controls")

    if st.button(
        " Refresh News",
        type="primary",
        use_container_width=True,
        disabled=st.session_state.processing,
    ):
        st.session_state.processing = True
        st.rerun()

    # Process the job if processing flag is set
    if st.session_state.processing:
        with st.spinner("Fetching and summarizing news..."):
            try:
                result = run_daily_job()
                st.session_state.processing = False
                st.success("News refreshed successfully!")
                st.rerun()
            except Exception as e:
                st.session_state.processing = False
                st.error(f"Error refreshing news: {str(e)}")

    st.markdown("---")
    st.header("Filter by Category")

    # Load data to get categories
    data = load_cached_news()

    if data:
        categories_data = get_all_categories(data)
        categories_list = ["All"] + categories_data.get("categories", [])
        selected_category = st.selectbox(
            "Select Category", categories_list, key="category_filter"
        )
    else:
        selected_category = "All"
        st.warning("No data available. Click 'Refresh News' to fetch.")


# Main content area
if data is None:
    st.warning(" No news data available.")
    st.info("Click the ' Refresh News' button in the sidebar to fetch the latest news.")
else:
    # Display category statistics
    if selected_category == "All":
        st.info(f" Showing **{data.get('total_articles', 0)}** articles")
        articles_to_display = data.get("summaries", [])
    else:
        filtered_data = filter_news_by_category(data, selected_category)
        st.info(
            f" Showing **{filtered_data.get('total_articles', 0)}** articles in category: **{selected_category}**"
        )
        articles_to_display = filtered_data.get("summaries", [])

    # Display articles
    if articles_to_display:
        for article in articles_to_display:
            display_article(article)
    else:
        st.warning(f"No articles found for category: {selected_category}")

# Footer
st.markdown("---")
st.caption("Daily News Summarizer - Powered by AI")
