import streamlit as st
import json
from backend_agent import HyperPersonalizedLDBot

st.set_page_config(
    page_title="Hyper-Personalized AI L&D Coach",
    page_icon="🎓",
    layout="wide"
)

# Initialize Core Processing Agent
if "coach" not in st.session_state:
    st.session_state.coach = HyperPersonalizedLDBot()

# --- JAVASCRIPT LOCALSTORAGE INTEGRATION SYNC LAYER ---
st.components.v1.html("""
<script>
    const savedData = localStorage.getItem("ld_coach_history_v3");
    if (savedData) {
        window.parent.postMessage({type: "LOAD_STORAGE", data: savedData}, "*");
    } else {
        window.parent.postMessage({type: "LOAD_STORAGE", data: "[]"}, "*");
    }

    window.addEventListener("message", function(event) {
        if (event.data.type === "SAVE_STORAGE") {
            localStorage.setItem("ld_coach_history_v3", event.data.data);
        }
        if (event.data.type === "CLEAR_STORAGE") {
            localStorage.removeItem("ld_coach_history_v3");
            window.parent.postMessage({type: "LOAD_STORAGE", data: "[]"}, "*");
        }
    });
</script>
""", height=0)

# Initialize Session History Storage Structures Securely
if "chat_history_registry" not in st.session_state:
    st.session_state.chat_history_registry = []
if "incoming_sync_done" not in st.session_state:
    st.session_state.incoming_sync_done = False
if "active_view_index" not in st.session_state:
    st.session_state.active_view_index = -1

if not st.session_state.incoming_sync_done:
    st.caption("🔒 Confirming local sandbox parameters...")
    st.session_state.incoming_sync_done = True
    st.rerun()

# --- SIDEBAR HISTORY EXPLORER PANEL ---
with st.sidebar:
    st.title("📚 Course History")
    st.caption("Securely persisted on your device")
    
    if st.session_state.chat_history_registry:
        st.markdown("---")
        for idx, item in enumerate(st.session_state.chat_history_registry):
            button_label = f"📖 {item['topic'][:25]}..."
            if st.button(button_label, key=f"hist_btn_{idx}", use_container_width=True):
                st.session_state.active_view_index = idx
                
        st.markdown("---")
        if st.button("🗑️ Clear Local History", type="secondary", use_container_width=True):
            st.components.v1.html("<script>window.parent.postMessage({type: 'CLEAR_STORAGE'}, '*');</script>", height=0)
            st.session_state.chat_history_registry = []
            st.session_state.active_view_index = -1
            st.success("History deleted locally!")
            st.rerun()
    else:
        st.info("No past courses saved on this device yet.")

# --- MAIN ENGINE APPLICATION WORKSPACE INTERFACE ---
st.title("🎓 Advanced AI L&D Coach & Course Architect")
st.caption("🚀 Live Diagnostics | Playlists & Courses | Sandboxed Device History Storage")

user_input = st.text_area(
    "Define your target position, career goal, or technical focus area:",
    placeholder="e.g., Deep dive learning plan for mastering production-grade Kubernetes deployments...",
    height=120
)

col_gen, col_share = st.columns([4, 1])

with col_gen:
    generate_clicked = st.button("Generate Bespoke Training System", type="primary", use_container_width=True)

if generate_clicked:
    if not user_input.strip():
        st.warning("Please specify an objective first.")
    else:
        with st.spinner("🤖 Scanning internet data configurations, full course playlists, and writing textbook curricula..."):
            md, html, videos, playlists = st.session_state.coach.execute_unlimited_generation(user_input)
            if html:
                new_entry = {
                    "topic": user_input,
                    "md_result": md,
                    "html_result": html,
                    "video_list": videos,
                    "playlist_list": playlists
                }
                st.session_state.chat_history_registry.append(new_entry)
                st.session_state.active_view_index = len(st.session_state.chat_history_registry) - 1
                
                serialized_data = json.dumps(st.session_state.chat_history_registry)
                st.components.v1.html(f"<script>window.parent.postMessage({{type: 'SAVE_STORAGE', data: `{serialized_data}`}}, '*');</script>", height=0)
            else:
                st.error(md)

with col_share:
    if st.session_state.active_view_index >= 0:
        share_js = """
        <script>
        function sendShare() {
            if (navigator.share) {
                navigator.share({
                    title: 'My Custom AI L&D Course Profile',
                    text: 'Take a look at this customized curriculum program generated instantly by my AI Coach!',
                    url: window.parent.location.href
                });
            } else {
                alert("📋 Native window sharing limit hit! Simply copy your browser address bar link to share.");
            }
        }
        </script>
        <button onclick="sendShare()" style="width:100%; height:42px; background-color:#16a34a; color:white; border:none; border-radius:6px; font-weight:bold; cursor:pointer;">📲 Share Chat</button>
        """
        st.components.v1.html(share_js, height=45)
    else:
        st.button("📲 Share Chat", disabled=True, use_container_width=True)

# --- WORKSPACE RENDER BLOCK ---
if st.session_state.active_view_index >= 0:
    active_data = st.session_state.chat_history_registry[st.session_state.active_view_index]
    
    st.markdown("---")
    st.success(f"🏁 Displaying Course System Profile: **{active_data['topic']}**")
    
    st.download_button(
        label="📥 Download Complete Courseware, Documents & Training Module Package",
        data=active_data['html_result'],
        file_name="hyper_personalized_ld_workspace.html",
        mime="text/html",
        use_container_width=True
    )
    
    # 1. Display Aggregated Complete Course Playlists
    if "playlist_list" in active_data and active_data["playlist_list"]:
        st.subheader("📂 Comprehensive Training Playlist Tracks")
        for p in active_data["playlist_list"]:
            with st.get_container():
                st.markdown(f"##### 💚 COURSE SERIES: {p['title']}")
                st.caption(f"Curriculum Host: {p['channel']}")
                st.video(p['url'])
                st.write(p['snippet'])
                st.markdown("---")

    # 2. Display Focused Single Laboratory Video Assets
    if active_data['video_list']:
        st.subheader("📺 Sequenced Core Laboratories & Walkthroughs")
        for v in active_data['video_list']:
            with st.expander(f"🎬 VIDEO LAB: {v['title']}"):
                st.caption(f"Source Channel: {v['publisher']} | Duration: {v['duration']}")
                st.video(v['url'])
                st.write(v['snippet'])
                
    st.subheader("📖 Generated Program Curricula & Textbook Resources")
    st.markdown(active_data['md_result'])
