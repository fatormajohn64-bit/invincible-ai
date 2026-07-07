import streamlit as st
import requests

# ==========================================
# 1. API CONFIGURATIONS & ROUTING
# ==========================================
# Here you define different APIs so you don't overload just one.
# Each model gets its own endpoint and API key.

API_CONFIGS = {
    "Model Fast (API 1)": {
        "url": "https://api.example.com/v1/fast-model/chat",
        "key": "YOUR_API_KEY_HERE_1",
        "format": "json" # Add formatting rules if needed
    },
    "Model Pro (API 2)": {
        "url": "https://api.example.com/v1/pro-model/chat",
        "key": "YOUR_API_KEY_HERE_2",
        "format": "json"
    },
    "Custom Module (API 3)": {
        "url": "https://api.different-provider.com/generate",
        "key": "YOUR_API_KEY_HERE_3",
        "format": "json"
    }
}

def get_ai_response(prompt, selected_model):
    """Handles sending the request to the correct API based on user choice."""
    config = API_CONFIGS[selected_model]
    
    headers = {
        "Authorization": f"Bearer {config['key']}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "messages": [{"role": "user", "content": prompt}]
    }
    
    try:
        # NOTE: This is a generic POST request. You might need to tweak the 
        # payload structure depending on the exact API provider you use.
        response = requests.post(config['url'], headers=headers, json=payload)
        
        if response.status_code == 200:
            # Assuming the API returns a standard JSON with the message
            return response.json().get("choices", [{}])[0].get("message", {}).get("content", "Success, but no text found.")
        else:
            return f"API Error: {response.status_code} - {response.text}"
            
    except Exception as e:
        # Fallback response for testing the UI before you add real API keys
        return f"[Simulated Response from {selected_model}]\nYou said: {prompt}"

# ==========================================
# 2. USER INTERFACE (STREAMLIT)
# ==========================================

st.set_page_config(page_title="Multi-API Chat Demo", page_icon="🤖")

st.title("Multi-API AI Chat ✍️")
st.markdown("Switch between different models to balance your API usage.")

# Sidebar for selecting the API module
st.sidebar.header("Settings")
selected_model = st.sidebar.selectbox(
    "Choose your AI Module:",
    list(API_CONFIGS.keys())
)

# Initialize chat history in session state so it doesn't disappear on refresh
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==========================================
# 3. CHAT LOGIC
# ==========================================

# React to user input
if prompt := st.chat_input("Write your message here..."):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # Call the routing function to get the response from the chosen API
        full_response = get_ai_response(prompt, selected_model)
        
        # Display the response
        message_placeholder.markdown(full_response)
        
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
        
