import streamlit as st
import streamlit.components.v1 as components
from backend_agent import HyperPersonalizedLDBot

st.set_page_config(page_title="Hyper-Personalized AI L&D Coach", page_icon="🎓", layout="wide")

st.markdown("""
    <style>
    .main-title { font-size: 2.8rem; color: #1e3a8a; font-weight: 800; margin-bottom: 0.5rem; text-align: center; }
    .sub-title { font-size: 1.2rem; color: #475569; text-align: center; margin-bottom: 2.5rem; }
    div.stButton > button:first-child { background-color: #2563eb; color: white; font-weight: bold; padding: 0.6rem 2.5rem; border-radius: 8px; border: none; width: 100%; transition: all 0.2s ease; }
    div.stButton > button:first-child:hover { background-color: #1d4ed8; transform: translateY(-1px); }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🎓 Hyper-Personalized AI L&D Coach</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Real-Time Continuous Up-skilling Engine with Multi-Model Cluster Failover</div>', unsafe_allow_html=True)

if "coach" not in st.session_state:
    st.session_state.coach = HyperPersonalizedLDBot()
if "workspace_md" not in st.session_state:
    st.session_state.workspace_md = ""
if "workspace_html" not in st.session_state:
    st.session_state.workspace_html = ""

user_input = st.text_input("💡 What precise technology matrix, leadership skill, or operational standard are you mastering today?", placeholder="e.g., Deploying High-Performance Distributed Redis Clusters on Kubernetes")

if st.button("🚀 Synthesize Customized Curriculum Asset Stack"):
    if not user_input.strip():
        st.warning("⚠️ Please provide an actionable operational learning prompt target.")
    else:
        with st.spinner("⚡ Scouring live web channels and rotating across your failover model cluster..."):
            md_out, html_out, _, _ = st.session_state.coach.execute_unlimited_generation(user_input)
            
            st.session_state.workspace_md = md_out
            st.session_state.workspace_html = html_out

if st.session_state.workspace_md:
    if "Setup Error" in st.session_state.workspace_md or "Network Cluster Limit" in st.session_state.workspace_md:
        st.error(st.session_state.workspace_md)
    else:
        tab1, tab2 = st.tabs(["🖥️ Interactive Training Workspace", "📄 Clean Markdown Notebook View"])
        
        with tab1:
            st.info("💡 Pro Tip: Use the 'Export as PDF' button inside the layout workspace to instantly save your technical blueprint textbook.")
            components.html(st.session_state.workspace_html, height=1200, scrolling=True)
            
        with tab2:
            st.code(st.session_state.workspace_md, language="markdown")
