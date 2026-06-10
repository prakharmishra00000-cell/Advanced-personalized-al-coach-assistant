import streamlit as st
from backend_agent import HyperPersonalizedLDBot
import os

st.set_page_config(page_title="Custom AI L&D Coach", layout="wide", initial_sidebar_state="expanded")

# Initialize Session State
if "coach" not in st.session_state:
    st.session_state.coach = HyperPersonalizedLDBot()

if "generated" not in st.session_state:
    st.session_state.generated = False

if "markdown_output" not in st.session_state:
    st.session_state.markdown_output = ""

if "html_output" not in st.session_state:
    st.session_state.html_output = ""

# Sidebar Controls
st.sidebar.title("⚙️ L&D Configuration Engine")
st.sidebar.markdown("Configure enterprise learning settings below.")

# Curriculum Complexity Tier
selected_difficulty = st.sidebar.selectbox(
    "🧠 Curriculum Complexity Tier",
    options=["Beginner / Foundational", "Production-Ready", "Enterprise Architect"],
    index=1
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔑 System Integrity Check")
api_key_status = os.getenv("GROQ_API_KEY") or (st.session_state.coach.client.api_key if st.session_state.coach.client else None)
if api_key_status:
    st.sidebar.success("Groq API Key Detected")
else:
    st.sidebar.error("Configure your GROQ_API_KEY environment variable inside Render.")

st.sidebar.markdown("---")
st.sidebar.markdown("### 💡 Instructions")
st.sidebar.info("Enter a specific skill, tool, or architecture framework in the main box and hit **Generate Training Curriculum**.")

# Main Page Layout
st.markdown("<h1>🎓 Hyper-Personalized AI L&D Course Generator</h1>", unsafe_allow_html=True)
st.markdown("<p>Accelerating workforce readiness with real-time web intelligence and video courses.</p>", unsafe_allow_html=True)

user_prompt = st.text_input("Enter target domain, skill, or framework:", placeholder="e.g., Deploying Distributed Redis Clusters")

if st.button("🚀 Generate Training Curriculum", type="primary"):
    if not user_prompt:
        st.warning("Please enter a target domain or skill to generate a curriculum.")
    else:
        with st.spinner("⚡ Compiling real-time textbook, labs, and streaming assets..."):
            md_out, html_out, videos, playlists = st.session_state.coach.execute_unlimited_generation(
                user_prompt, 
                difficulty=selected_difficulty
            )
            
            if "🚨 Groq API Error" in md_out or "⚠️ Setup Error" in md_out:
                st.error(md_out)
            else:
                st.session_state.markdown_output = md_out
                st.session_state.html_output = html_out
                st.session_state.generated = True

# Display Course Workspace if Generated
if st.session_state.generated:
    st.success("✨ Curriculum successfully compiled! View the embedded interactive workspace below.")
    
    # UI Button for Interactive Quiz
    st.markdown("---")
    st.markdown("<h2>⚡ Advanced Features</h2>", unsafe_allow_html=True)
    if st.button("📝 Generate Interactive Chapter Quiz", type="secondary"):
        with st.spinner("🤖 Assembling knowledge benchmark test..."):
            quiz_markdown = st.session_state.coach.generate_quiz(user_prompt)
            st.markdown("### 🧠 Generated Mastery Quiz")
            st.markdown(quiz_markdown)
    
    st.markdown("---")
    st.markdown("<h2>🖥️ Interactive Training Workspace</h2>", unsafe_allow_html=True)
    
    # Render the Mobile-Compatible HTML Output
    st.components.v1.html(st.session_state.html_output, height=1100, scrolling=True)

    st.markdown("---")
    st.download_button(
        label="💾 Download Course Markdown",
        data=st.session_state.markdown_output,
        file_name="LND_Course_Output.md",
        mime="text/markdown"
    )
