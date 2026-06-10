import streamlit as st
import os
from backend_agent import HyperPersonalizedLDBot

st.set_page_config(page_title="Elite Enterprise AI Training Assistant", layout="wide")

st.markdown("""
    <style>
    /* Dark Futuristic High-End CSS Override */
    .main-title {
        font-size: 3em;
        color: #38bdf8;
        font-weight: 900;
        text-align: center;
        letter-spacing: -0.05em;
        text-transform: uppercase;
        text-shadow: 0 0 25px rgba(56, 189, 248, 0.5);
        margin-bottom: 20px;
    }
    .stApp {
        background-color: #050810;
        color: #f8fafc;
    }
    .stTextInput>div>div>input, .stTextArea>div>textarea {
        background-color: #090d1a;
        color: #38bdf8;
        border: 1px solid #0ea5e9;
        border-radius: 12px;
        box-shadow: 0 0 10px rgba(14, 165, 233, 0.2);
        font-family: 'Fira Code', monospace;
        font-size: 1em;
        padding: 14px;
    }
    .stTextInput>div>div>input:focus, .stTextArea>div>textarea:focus {
        border-color: #38bdf8;
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.6);
    }
    .stSelectbox>div>div>div {
        background-color: #090d1a;
        color: #38bdf8;
        border: 1px solid #0ea5e9;
        border-radius: 12px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 14px;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        border: 1px solid #38bdf8;
        background: linear-gradient(135deg, #0369a1, #0ea5e9);
        color: #ffffff;
        padding: 14px;
        box-shadow: 0 4px 20px rgba(14, 165, 233, 0.4);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .stButton>button:hover {
        transform: translateY(-4px) scale(1.02);
        box-shadow: 0 0 30px rgba(56, 189, 248, 0.8);
        background: linear-gradient(135deg, #0ea5e9, #38bdf8);
        border-color: #ffffff;
    }
    h2, h3 {
        color: #38bdf8;
        text-shadow: 0 0 8px rgba(56, 189, 248, 0.2);
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-title'>🛡️ Enterprise Cyber-Deck Workspace</div><br>", unsafe_allow_html=True)

# Initialize Backend Agent
bot = HyperPersonalizedLDBot()

with st.sidebar:
    st.image("https://api.dicebear.com/7.x/bottts/svg?seed=CyberpunkAI", width=140)
    st.header("⚙️ Cyber Operational Configs")
    selected_difficulty = st.selectbox("Select Cyber Domain Tier", ["Beginner", "Production-Ready", "Enterprise Architect"])
    st.divider()
    st.markdown("### 👑 Elite Tools Directory")
    st.caption("Advanced high-end operational workspace.")

user_query = st.text_input("Ingress target domain, systems technology or operational architecture:", placeholder="e.g., Distributed Kubernetes Deployments, Rust Microservices, AWS Infrastructure")

if "markdown_content" not in st.session_state:
    st.session_state.markdown_content = ""
if "html_content" not in st.session_state:
    st.session_state.html_content = ""

if st.button("🚀 Ingress Elite Custom Training Module"):
    if user_query:
        with st.spinner("Compiling high-end cyber-deck masterclass curriculum, diagnostics, and labs..."):
            md, html_out, _, _ = bot.execute_unlimited_generation(user_query, selected_difficulty)
            st.session_state.markdown_content = md
            st.session_state.html_content = html_out
            st.rerun()
    else:
        st.warning("Please enter a valid target training system/module.")

if st.session_state.html_content:
    st.markdown("## 📖 Interactive Visual L&D Matrix")
    st.components.v1.html(st.session_state.html_content, height=900, scrolling=True)
    
    st.divider()
    st.markdown("### 🌟 Super Advanced Autonomic Tools")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🧠 Elite Technical Quiz"):
            with st.spinner("Engineering assessment modules..."):
                quiz = bot.generate_quiz(user_query)
                st.markdown("### 📝 Evaluative Knowledge Benchmark")
                st.markdown(quiz)
                
    with col2:
        if st.button("🚀 Enterprise Architecture Blueprint"):
            with st.spinner("Assembling production-grade infrastructure topology..."):
                blueprint = bot.generate_system_blueprint(user_query)
                st.markdown("### 🏗️ Enterprise System Infrastructure")
                st.code(blueprint, language="json")
                
    with col3:
        if st.button("👑 Export to Corporate LMS (SCORM.zip)"):
            with st.spinner("Packaging e-learning files..."):
                scorm = bot.generate_scorm_package(user_query, st.session_state.markdown_content)
                st.code(scorm, language="xml")

    st.divider()
    st.markdown("### 🤖 Neuro-Adaptive Behavioral Scenario Simulator")
    user_sandbox = st.text_area("Simulate an operational response, threat response, or deployment step:")
    if st.button("🧠 Launch Real-Time Neuro-Adaptive Simulation"):
        with st.spinner("Scanning cognitive behavioral and physiological matrix..."):
            sim_data = bot.generate_neuro_adaptive_simulation(st.session_state.markdown_content, user_sandbox)
            if "error" not in sim_data:
                st.info(f"**Coaching Feedback Intervention:** {sim_data.get('coaching_feedback')}")
                st.warning(f"**Stakeholder Persona Simulation:** {sim_data.get('next_persona_state')}")
                st.success(f"**Recommended Complexity Scale:** {sim_data.get('adjusted_complexity')}")
            else:
                st.error(sim_data.get("error"))
