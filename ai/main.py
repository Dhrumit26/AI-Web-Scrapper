import streamlit as st
from scrape import (scrape_website, extract_text_from_html, clean_body_content, split_dom_content)
from parse import parse_with_ollama

st.title("AI Web Scrapper")
url = st.text_input("Enter the Website URL:")

if st.button("Scrape"):
    st.write(f"Scraping data......")
    result = scrape_website(url)
    body_content = extract_text_from_html(result)
    cleaned_content = clean_body_content(body_content)

    st.session_state.cleaned_content = cleaned_content

    with st.expander("View Cleaned Content"):
        st.text_area("Cleaned Content", cleaned_content, height=300)

if "cleaned_content" in st.session_state:
    prased_description = st.text_area("Describe what you want to do with the content", height=100)
    if st.button("Prase Content"):
        st.write("prasing the content....")
        
        dom_chunks = split_dom_content(st.session_state.cleaned_content)
        result = parse_with_ollama(dom_chunks, prased_description)
        st.write(result)
        



