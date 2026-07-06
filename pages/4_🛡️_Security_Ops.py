"""
4_🛡️_Security_Ops.py
====================
Educational Security & Hardening Module
"""

import streamlit as st
import hashlib

st.set_page_config(page_title="Security Research", page_icon="🛡️")

st.title("🛡️ Ethical Security Research Lab")

# Integrated Security News Feed
st.subheader("Live Security Intelligence (RSS)")
# You can use the same news logic here, but with 'cybersecurity' as the query
if st.button("Fetch Latest Security Briefings"):
    st.write("Fetching feeds from The Hacker News/Security Weekly...")
    # [Insert your news_api logic here, but use 'cybersecurity' as the query string]

st.markdown("---")

# Module Sections
tab1, tab2, tab3 = st.tabs(["Password Security (Entropy)", "Hash Analysis", "Security Checklist"])

with tab1:
    st.header("Password Entropy Lab")
    st.write("Learn why complexity matters. This tool calculates password strength.")
    pwd = st.text_input("Enter a test password:", type="password")
    if pwd:
        # Simple logical check
        score = len(pwd) * 2
        if any(c.isupper() for c in pwd): score += 10
        if any(c.isdigit() for c in pwd): score += 10
        
        st.progress(min(score/100, 1.0))
        if score > 50: st.success("Good entropy.")
        else: st.warning("Vulnerable to brute-force.")

with tab2:
    st.header("Hash Verification (Data Integrity)")
    st.write("Understand how files are verified. Paste text to see its SHA-256 hash.")
    text = st.text_area("Input data:")
    if text:
        hashed = hashlib.sha256(text.encode()).hexdigest()
        st.code(hashed)

with tab3:
    st.header("Device Hardening Checklist")
    st.markdown("""
    *   **[ ] Network Audit:** Are you using a VPN on public Wi-Fi?
    *   **[ ] Permissions:** Have you audited app permissions on your phone?
    *   **[ ] Encryption:** Is your drive encrypted (BitLocker/FileVault)?
    """)
    
