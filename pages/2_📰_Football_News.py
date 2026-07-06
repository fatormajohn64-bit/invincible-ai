import streamlit as st
import requests

st.set_page_config(page_title="Football News", page_icon="📰", layout="centered")

st.title("📰 Invincible 911 News Room")
st.caption("Latest breaking football headlines filtered globally.")

# Securely grab the key from your Streamlit secrets
NEWS_API_KEY = st.secrets.get("NEWS_API_KEY", None)

if not NEWS_API_KEY:
    st.warning("⚠️ News API Key Not Configured")
    st.markdown(
        "To fetch real-time breaking news, register for a free key at **NewsData.io** "
        "and add it to your Streamlit secrets."
    )
    
    # Elegant design preview for app testing
    st.markdown("### 🏆 Top Headlines (Demo Mode)")
    st.info("Showing mock layout. Connect your API key to bring this to life!")
    
    with st.container(border=True):
        st.subheader("Messi Leads Inter Miami to Another Clean Victory")
        st.caption("Source: Global Sports News | Published: Just now")
        st.write(
            "An incredible performance tonight kept fans on their feet as the football legend "
            "secured a brilliant brace in the second half of the match..."
        )
        st.link_button("Read Full Article", "https://google.com")
else:
    try:
        # NewsData.io endpoint targeting live sports articles matching 'football'
        url = "https://newsdata.io/api/1/latest"
        params = {
            "apikey": NEWS_API_KEY,
            "q": "football",
            "category": "sports",
            "language": "en"
        }
        
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        articles = data.get("results", [])
        
        if not articles:
            st.info("No new football articles found in the last few hours. Check back shortly!")
        else:
            st.markdown(f"### ⚡ Breaking Headlines")
            
            for article in articles:
                title = article.get("title", "No Title Available")
                description = article.get("description", "")
                source = article.get("source_id", "Unknown Source")
                pub_date = article.get("pubDate", "")
                link = article.get("link", "#")
                image_url = article.get("image_url", None)
                
                # Render each article inside a clean visual container card
                with st.container(border=True):
                    if image_url:
                        st.image(image_url, use_container_width=True)
                    
                    st.subheader(title)
                    st.caption(f"Source: {source.upper()} | Published: {pub_date}")
                    
                    if description:
                        # Truncate overly dense summaries to maintain clean UI scannability
                        short_desc = description[:250] + "..." if len(description) > 250 else description
                        st.write(short_desc)
                        
                    st.link_button("Read Full Story ➡️", link)
                    
    except Exception as e:
        st.error(f"Could not sync with the news engine: {e}")

# Manual page refresh
if st.button("🔄 Refresh News Room", type="primary", use_container_width=True):
    st.rerun()
  
