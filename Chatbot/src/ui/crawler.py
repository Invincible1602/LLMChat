import streamlit as st
from src.api.client import RagAPIClient

def render_crawler_tab():
    """Render the web crawler tab"""
    
    st.header("Web Crawler")
    st.markdown("Enter a URL to crawl and index its content for later retrieval.")
    
    # Initialize API client
    api_client = RagAPIClient()
    
    # Use a form to stabilize input position
    with st.form("crawl_form", clear_on_submit=False):
        col1, col2 = st.columns([4, 1])
        url = col1.text_input(
            "URL to Crawl", 
            placeholder="https://example.com", 
            key="crawl_url"
        )
        submit = col2.form_submit_button("Crawl")
        
        if submit:
            if url:
                with st.spinner("Crawling and indexing the website..."):
                    result = api_client.crawl_url(url)
                    if "error" not in result:
                        st.success(f"Successfully crawled and indexed: {result.get('url', url)}")
                        st.info(f"Chunks created: {result.get('chunk_count', 0)}, Documents indexed: {result.get('indexed_count', 0)}")
                    else:
                        st.error(f"Failed to crawl the URL: {result.get('error')}")
            else:
                st.warning("Please enter a URL to crawl")