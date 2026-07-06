import streamlit as st

st.set_page_config(page_title="Script Generator", page_icon="🎬", layout="centered")

st.title("🎬 Invincible 911 Script Studio")
st.caption("Generate high-retention short-form video scripts instantly.")

with st.sidebar:
    st.header("⚙️ Script Settings")
    content_type = st.selectbox(
        "Select Content Category:",
        ["Daily Motivation", "Pro Gaming Strategy", "Tech & Coding Tips", "Custom Concept"]
    )
    
    video_tone = st.radio(
        "Choose Video Vibe:",
        ["🔥 High Energy / Hype", "🧘 Calm / Focused", "🧠 Analytical / Educational"]
    )
    
    include_cta = st.checkbox("Include Call to Action (CTA)", value=True)

st.markdown("### 📝 Video Blueprint Creator")
main_topic = st.text_input("What is the central topic or theme of your video?", placeholder="e.g., How to stay consistent, Alcatraz squad wipes, Python automation tricks...")

if st.button("🚀 Construct Script Blueprint", type="primary", use_container_width=True):
    if not main_topic:
        st.warning("Please enter a central topic to generate your script format!")
    else:
        st.success("Video Blueprint Generated successfully!")
        
        # Determine specific prompt logic variables based on user side-panel input
        if content_type == "Daily Motivation":
            hook = f"🚨 \"Most people quit right before the breakthrough. If you're watching this on July 6, 2026, this is your sign to keep pushing.\""
            body = f"• [0:05 - Visual: Fast-paced background transition]\n• Focus 100% of your energy on execution today. Cut out the noise, mute the distractions, and build in silence. Your future self is depending on the work you put in right now."
            cta_text = "👉 Drop a '100' if you needed to hear this today, and follow for daily reminders."
            tags = "#motivation #discipline #mindset #growth #focus #shorts"
            
        elif content_type == "Pro Gaming Strategy":
            hook = f"🚨 \"Stop making this massive mistake on the map. This one minor rotation adjustment will instantly secure your next win.\""
            body = f"• [0:05 - Visual: Split-second gameplay drop execution]\n• When the final circles close in tight zones like Alcatraz, stop chasing mid-map fights. Hold the high ground anchors, clear the perimeter lines first, and let the remaining squads eliminate each other while you gatekeep."
            cta_text = "👉 Share this blueprint with your favorite squad mate, and hit that follow button for layout breakdowns!"
            tags = "#gaming #progameplay #tactical #loadout #clutch #gamers"
            
        elif content_type == "Tech & Coding Tips":
            hook = f"🚨 \"You don't need a massive framework to build cool software. You can deploy live Python data apps in minutes.\""
            body = f"• [0:05 - Visual: Clean IDE code screen scrolling]\n• By combining lightweight script layouts with automated micro-APIs, you can build dynamic global match centers, news monitors, or utility toolkits directly from your phone. Stop overcomplicating the setup."
            cta_text = "👉 Save this video for your next coding session, and comment what feature we should build next!"
            tags = "#programming #python #developer #softwareengineer #code #buildinpublic"
            
        else:
            hook = f"🚨 \"Here is the truth about {main_topic} that nobody wants to tell you.\""
            body = f"• [0:05 - Visual: Dynamic zoom on main concept]\n• Let's break down the core elements of {main_topic}. The trick isn't overthinking the strategy—it's mastering the fundamentals consistently until the results stack up."
            cta_text = "👉 What are your thoughts on this? Drop a comment below and subscribe!"
            tags = f"#{main_topic.lower().replace(' ', '')} #trending #creator #insights"

        # Display output template inside structured presentation cards
        st.markdown("---")
        
        with st.container(border=True):
            st.markdown("### 🪝 1. The 3-Second Hook")
            st.info(hook)
            
        with st.container(border=True):
            st.markdown("### 📦 2. Core Body Content")
            st.write(body)
            st.caption(f"🎨 Selected Pacing Vibe: {video_tone}")
            
        if include_cta:
            with st.container(border=True):
                st.markdown("### 📣 3. Call to Action")
                st.warning(cta_text)
                
        with st.container(border=True):
            st.markdown("### 🏷️ Optimized Tags")
            st.code(tags, language="text")
          
