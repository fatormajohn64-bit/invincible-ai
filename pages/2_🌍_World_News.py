import streamlit as st
import requests

st.set_page_config(page_title="World News", page_icon="🌍", layout="wide")

# Sidebar Configuration
st.sidebar.header("🌍 News Settings")
country_input = st.sidebar.text_input("🔎 Search by country name", "")
# You can map country codes for the API
countries = {"USA": "us", "UK": "gb", "India": "in", "Canada": "ca", "Nigeria": "ng"}
selected_country = st.sidebar.selectbox("Or select from list", list(countries.keys()))

def fetch_news(query, country_code):
    # Replace with your actual NewsAPI key
    api_key = st.secrets.get("NEWS_API_KEY") 
    url = f"https://newsapi.org/v2/top-headlines?country={country_code}&q={query}&apiKey={api_key}"
    response = requests.get(url)
    return response.json().get("articles", [])

st.title("📰 Global News Feed")

# Logic to choose search term or country
search_term = country_input if country_input else ""
code = countries[selected_country]

articles = fetch_news(search_term, code)

if articles:
    for article in articles:
        with st.container(border=True):
            col1, col2 = st.columns([1, 3])
            if article.get("urlToImage"):
                col1.image(article["urlToImage"], use_container_width=True)
            col2.subheader(article["title"])
            col2.write(article.get("description", "No description available."))
            col2.link_button("Read More", article["url"])
else:
    st.info("No news found. Try a different search term or country.")
  
