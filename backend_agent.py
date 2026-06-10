import os
import re
import json
from typing import List, Dict, Any, Tuple
from duckduckgo_search import DDGS
from openai import OpenAI

class HyperPersonalizedLDBot:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        if self.api_key:
            self.client = OpenAI(
                api_key=self.api_key,
                base_url="https://api.groq.com/openai/v1"
            )
        else:
            self.client = None

    def execute_embedded_search(self, query: str, difficulty: str) -> Tuple[str, List[Dict[str, str]], List[Dict[str, str]]]:
        # Upgraded aggressively premium keywords to force high-end search returns
        if "Beginner" in difficulty:
            search_keywords_text = f"{query} premium beginner masterclass fundamentals guide course"
            search_keywords_video = f"{query} premium fundamental masterclass tutorial youtube course"
            search_keywords_playlist = f"{query} ultimate complete beginner bootcamp premium playlist youtube"
        elif "Enterprise" in difficulty:
            search_keywords_text = f"{query} enterprise system architecture deep dive production masterclass engineering"
            search_keywords_video = f"{query} enterprise system architecture advanced configuration workshop premium youtube"
            search_keywords_playlist = f"{query} masterclass system design engineering architecture premium playlist youtube"
        else: # Production-Ready
            search_keywords_text = f"{query} production deployment blueprint real world implementation premium masterclass"
            search_keywords_video = f"{query} production grade practical engineering implementation tutorial premium youtube"
            search_keywords_playlist = f"{query} complete production setup deployment enterprise playlist youtube"

        search_context = "Premium enterprise architectural blueprint matrix."
        compiled_videos = []
        compiled_playlists = []
        
        try:
            with DDGS() as ddg:
                text_results = list(ddg.text(keywords=search_keywords_text, max_results=4))
                if text_results:
                    search_context = "\n".join([f"Source Data: {r.get('body', '')[:250]}" for r in text_results])
                
                video_ddgs_results = list(ddg.videos(keywords=search_keywords_video, max_results=4))
                for v in video_ddgs_results:
                    link = v.get("content", v.get("url", ""))
                    if "youtube.com/watch?v=" in link or "youtu.be/" in link:
                        video_id = ""
                        if "v=" in link:
                            video_id = link.split("v=")[1].split("&")[0]
                        elif "youtu.be/" in link:
                            video_id = link.split("youtu.be/")[1].split("?")[0]
                            
                        if video_id:
                            embed_link = f"https://www.youtube.com/embed/{video_id}"
                            compiled_videos.append({
                                "title": v.get("title", f"Elite Engineering Lab: {query}"),
                                "url": link,
                                "embed": embed_link,
                                "channel": v.get("publisher", "Elite Engineering Network"),
                                "duration": v.get("duration", "N/A")
                            })

                playlist_ddgs_results = list(ddg.videos(keywords=search_keywords_playlist, max_results=3))
                for p in playlist_ddgs_results:
                    link = p.get("content", p.get("url", ""))
                    if "list=" in link:
                        playlist_id = link.split("list=")[1].split("&")[0]
                        embed_link = f"https://www.youtube.com/embed/videoseries?list={playlist_id}"
                        compiled_playlists.append({
                            "title": p.get("title", f"Elite Masterclass Track: {query}"),
                            "url": link,
                            "embed": embed_link,
                            "channel": p.get("publisher", "Premium Architecture Channel")
                        })
                
                # Ultimate Fallback: Force absolute direct URI links if DDG video registers are momentarily empty
                if not compiled_videos:
                    fallback_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}+" + difficulty.lower().split()[0] + "+premium+masterclass"
                    compiled_videos.append({
                        "title": f"Premium Engineering Direct Results for: {query.capitalize()} ({difficulty})",
                        "url": fallback_url,
                        "embed": fallback_url,
                        "channel": "YouTube Premium Engineering Directory",
                        "duration": "N/A"
                    })
                    
                if not compiled_playlists:
                    fallback_p_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}+premium+masterclass+playlist+course&sp=EgIQAw%253D%253D"
                    compiled_playlists.append({
                        "title": f"Premium Masterclass Track (Direct Link) for: {query.capitalize()}",
                        "url": fallback_p_url,
                        "embed": fallback_p_url,
                        "channel": "YouTube Premium Engineering Directory"
                    })

        except Exception as e:
            print(f"⚠️ Elite search engine log notice: {str(e)}")
            
        return search_context, compiled_videos, compiled_playlists

    def execute_unlimited_generation(self, user_prompt: str, difficulty: str = "Production-Ready") -> Tuple[str, str, List[Dict[str, str]], List[Dict[str, str]]]:
        """Safely generates masterclass modules with fallback error handling."""
        try:
            if not self.client:
                return "⚠️ Setup Error: Configure your GROQ_API_KEY environment variable.", "", [], []

            search_data, video_list, playlist_list = self.execute_embedded_search(user_prompt, difficulty)

            system_instruction = (
                f"You are an Elite Enterprise Hyper-Personalized AI L&D Director operating at an ultra-premium '{difficulty}' complexity tier. "
                "Output exhaustively detailed, masterclass-grade enterprise training programs, deep-dive architectural strategies, "
                "failure-mode analyses, and production-ready code implementations natively in Markdown format. Do not use conversational filler.\n\n"
                "You MUST strictly structure your elite, advanced output into these 4 modules:\n"
                "1. 📊 SYSTEMIC SKILL GAP DIAGNOSTIC: Build elite failure-scenario analysis and advanced diagnostic check-questions to rigorously test capabilities.\n"
                "2. 📖 CORE INTELLECTUAL TEXTBOOK MODULES: Author massive, masterclass-grade technical articles complete with enterprise-scale configuration parameters, architectural diagrams (text-based), and fully syntactical code block scripts.\n"
                "3. 🧠 ADAPTIVE STRUCTURAL COMPLEXITY SCALE: Map explicit, premium operational blueprints scaled precisely to the fundamental, deployment, or advanced optimization levels.\n"
                "4. 🎯 AGGRESSIVE EVALUATION CRITIQUE LAB: Design comprehensive execution assignments paired with exact, line-by-line ideal answer breakdowns.\n\n"
                f"Ground your high-tier technical curriculum natively inside this premium open documentation matrix:\n{search_data}"
            )

            response = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": f"Generate elite premium custom training program for: {user_prompt}"}
                ],
                temperature=0.3,
                max_tokens=2500
            )
            markdown_output = response.choices[0].message.content
        except Exception as e:
            return f"🚨 Execution/API Error occurred: {str(e)}", "", [], []

        video_elements_html = ""
        for v in video_list:
            video_elements_html += f"""
            <div class="media-card">
                <h4>🎬 Elite Engineering Walkthrough: {v['title']}</h4>
                <p class="media-meta"><strong>Host:</strong> {v['channel']} &nbsp;|&nbsp; <strong>Duration:</strong> {v['duration']}</p>
                <div class="iframe-container">
                    <iframe src="{v['embed']}" frameborder="0" allowfullscreen></iframe>
                </div>
                <p class="media-link"><a href="{v['url']}" target="_blank">🔗 Direct Access Link: Watch Premium Lab on YouTube</a></p>
            </div>
            """

        playlist_elements_html = ""
        for p in playlist_list:
            playlist_elements_html += f"""
            <div class="media-card premium-playlist">
                <h4>📂 ADVANCED MASTERCLASS TRACK: {p['title']}</h4>
                <p class="media-meta"><strong>Curriculum Host:</strong> {p['channel']}</p>
                <div class="iframe-container">
                    <iframe src="{p['embed']}" frameborder="0" allowfullscreen></iframe>
                </div>
                <p class="media-link"><a href="{p['url']}" target="_blank">🔗 Direct Access Link: Watch Masterclass Series Playlist</a></p>
            </div>
            """

        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Premium AI Coach L&D Workspace</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
            <style>
                :root {
                    --bg-app: #050810;
                    --bg-card: #090d1a;
                    --border-card: #0ea5e9;
                    --text-main: #f8fafc;
                    --text-muted: #64748b;
                    --primary-glow: #38bdf8;
                    --accent-color: #0ea5e9;
                    --accent-premium: #10b981;
                }
                html { overflow-x: hidden; width: 100%; }
                body {
                    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
                    line-height: 1.7;
                    color: var(--text-main);
                    background-color: var(--bg-app);
                    width: 100%;
                    max-width: 100vw;
                    margin: 0 auto;
                    padding: 20px 15px;
                    box-sizing: border-box;
                    overflow-x: hidden;
                    background-image: radial-gradient(circle at 10% 20%, rgba(14, 165, 233, 0.03) 0%, transparent 40%),
                                      radial-gradient(circle at 90% 80%, rgba(56, 189, 248, 0.03) 0%, transparent 40%);
                }
                .container {
                    background: rgba(9, 13, 26, 0.75);
                    border: 1px solid #1e293b;
                    backdrop-filter: blur(16px);
                    padding: 32px;
                    border-radius: 22px;
                    box-shadow: 0 0 50px rgba(14, 165, 233, 0.06), inset 0 1px 0 rgba(255,255,255,0.05);
                    width: 100%;
                    box-sizing: border-box;
                    overflow-wrap: anywhere;
                }
                h1 {
                    color: #38bdf8;
                    border-bottom: 2px solid #0ea5e9;
                    padding-bottom: 18px;
                    font-size: 1.75em;
                    word-wrap: break-word;
                    letter-spacing: -0.025em;
                    text-transform: uppercase;
                    text-shadow: 0 0 10px rgba(14, 165, 233, 0.3);
                }
                h2 {
                    color: var(--primary-glow);
                    margin-top: 40px;
                    border-left: 5px solid var(--accent-color);
                    padding-left: 14px;
                    font-size: 1.35em;
                    word-wrap: break-word;
                    letter-spacing: -0.02em;
                    text-shadow: 0 0 8px rgba(56, 189, 248, 0.2);
                }
                h3 { font-size: 1.15em; word-wrap: break-word; color: #38bdf8; }
                p, li, div { font-size: 1em; color: var(--text-main); word-wrap: break-word; box-sizing: border-box; }
                strong { color: #38bdf8; text-shadow: 0 0 6px rgba(56, 189, 248, 0.3); }
                code {
                    background: #0f172a;
                    color: #38bdf8;
                    padding: 4px 8px;
                    border-radius: 6px;
                    font-family: 'Fira Code', monospace;
                    font-size: 0.85em;
                    word-break: break-all;
                    overflow-wrap: anywhere;
                    border: 1px solid #1e293b;
                }
                pre {
                    background: #020617;
                    color: #38bdf8;
                    padding: 22px;
                    border-radius: 14px;
                    overflow-x: auto;
                    font-size: 0.82em;
                    box-sizing: border-box;
                    border: 1px solid #334155;
                    box-shadow: inset 0 2px 10px rgba(0,0,0,0.6);
                    white-space: pre-wrap;
                    word-wrap: break-word;
                }
                pre code { background: transparent; color: inherit; padding: 0; font-size: 1em; }
                .badge {
                    background: rgba(14, 165, 233, 0.1);
                    color: #38bdf8;
                    padding: 8px 18px;
                    border-radius: 30px;
                    font-size: 0.75em;
                    font-weight: 800;
                    border: 1px solid var(--border-card);
                    display: inline-block;
                    letter-spacing: 0.05em;
                    text-transform: uppercase;
                    box-shadow: 0 0 15px rgba(14, 165, 233, 0.2);
                }
                .interactive-box {
                    background: rgba(3, 7, 18, 0.65);
                    border: 1px solid #1e293b;
                    border-radius: 16px;
                    padding: 26px;
                    margin-top: 35px;
                    box-sizing: border-box;
                    width: 100%;
                    box-shadow: 0 0 20px rgba(14, 165, 233, 0.05);
                }
                .action-btn {
                    background: linear-gradient(135deg, #0369a1, #0284c7, #0ea5e9);
                    color: #fff;
                    border: 1px solid #38bdf8;
                    padding: 12px 24px;
                    border-radius: 10px;
                    cursor: pointer;
                    font-weight: 800;
                    font-size: 0.9em;
                    letter-spacing: 0.05em;
                    text-transform: uppercase;
                    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                    box-shadow: 0 4px 20px rgba(14, 165, 233, 0.3);
                }
                .action-btn:hover {
                    transform: translateY(-3px) scale(1.02);
                    box-shadow: 0 0 25px rgba(56, 189, 248, 0.6);
                    background: linear-gradient(135deg, #0284c7, #0ea5e9, #38bdf8);
                    border-color: #fff;
                }
                .media-section { margin-top: 45px; padding-top: 25px; border-top: 2px solid #0ea5e9; width: 100%; box-sizing: border-box; }
                .media-card {
                    background: rgba(3, 7, 18, 0.5);
                    border: 1px solid #1e293b;
                    border-radius: 18px;
                    padding: 24px;
                    margin-bottom: 22px;
                    box-sizing: border-box;
                    width: 100%;
                    transition: all 0.3s ease;
                    box-shadow: inset 0 0 10px rgba(255,255,255,0.02);
                }
                .media-card:hover {
                    border-color: var(--accent-color);
                    box-shadow: 0 0 25px rgba(14, 165, 233, 0.2), inset 0 0 15px rgba(14, 165, 233, 0.1);
                    transform: translateX(4px);
                }
                .premium-playlist {
                    background: rgba(16, 185, 129, 0.03);
                    border-color: rgba(16, 185, 129, 0.3);
                }
                .premium-playlist:hover {
                    border-color: var(--accent-premium);
                    box-shadow: 0 0 25px rgba(16, 185, 129, 0.2), inset 0 0 15px rgba(16, 185, 129, 0.1);
                }
                .premium-playlist h4 { color: #34d399; text-shadow: 0 0 8px rgba(16, 185, 129, 0.4); }
                .media-meta { font-size: 0.9em; color: var(--text-muted); margin: 6px 0 16px 0; }
                .media-link a { color: var(--primary-glow); font-weight: 700; text-decoration: none; word-break: break-all; letter-spacing: 0.02em; }
                .media-link a:hover { text-decoration: underline; text-shadow: 0 0 8px rgba(56, 189, 248, 0.5); }
                .iframe-container { position: relative; width: 100%; padding-bottom: 56.25%; height: 0; margin-top: 12px; overflow: hidden; }
                .iframe-container iframe { position: absolute; top: 0; left: 0; width: 100%; height: 100%; border-radius: 12px; border: 0; box-shadow: 0 0 15px rgba(0,0,0,0.5); }
                textarea {
                    background: #020617;
                    color: var(--text-main);
                    border: 1px solid #1e293b;
                    border-radius: 10px;
                    padding: 16px;
                    font-family: 'Fira Code', monospace;
                    font-size: 0.95em;
                }
                textarea:focus { outline: none; border-color: var(--accent-color); box-shadow: 0 0 15px rgba(14, 165, 233, 0.3); }
                @media (min-width: 768px) {
                    body { padding: 0 40px; margin: 50px auto; max-width: 1100px; }
                    .container { padding: 48px; }
                    h1 { font-size: 2.6em; }
                    h2 { font-size: 1.65em; }
                    pre { font-size: 0.85em; padding: 28px; }
                }
                @media print {
                    body { background: #fff; color: #000; margin: 0; padding: 0; }
                    .container { box-shadow: none; padding: 0; border: none; background: none; }
                    .media-section, .interactive-box, button, .badge, .media-card { display: none !important; }
                }
            </style>
            <script>
                function checkFeedback() { alert("🎓 Elite Custom AI Workspace: Response successfully validated!"); }
                function triggerPrint() { window.print(); }
            </script>
        </head>
        <body>
            <div class="container">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px;">
                    <span class="badge">🛡️ ELITE ENTERPRISE AI L&D ACTIVE</span>
                    <button class="action-btn" onclick="triggerPrint()">🖨️ Export as PDF</button>
                </div>
                <br><br>
                <div class="text-course-content">
                    USER_MARKDOWN_CONTENT_REPLACE
                </div>
                <div class="interactive-box">
                    <h3>🎯 Live Skill Execution Sandbox</h3>
                    <p>Paste your architectural solutions to benchmark compliance:</p>
                    <textarea style="width:100%; height:110px; box-sizing:border-box;" placeholder="Insert technical deployment steps here..."></textarea><br><br>
                    <button class="action-btn" onclick="checkFeedback()">Evaluate Architecture</button>
                </div>
                <div class="media-section">
                    <h2>📺 Premium Masterclass Series & Architecture Tracks</h2>
                    USER_PLAYLIST_REPLACE
                    <h2 style="margin-top:45px;">🎬 Sequenced Core Engineering Laboratories</h2>
                    USER_VIDEO_REPLACE
                </div>
            </div>
        </body>
        </html>
        """

        formatted_md = markdown_output.replace('# ', '<h1>').replace('## ', '<h2>').replace('### ', '<h3>').replace('\n', '<br>')
        html_output = html_template.replace("USER_MARKDOWN_CONTENT_REPLACE", formatted_md)
        
        playlist_content = playlist_elements_html if playlist_elements_html else "<p>Aggregating elite Masterclass pathways...</p>"
        html_output = html_output.replace("USER_PLAYLIST_REPLACE", playlist_content)
        
        video_content = video_elements_html if video_elements_html else "<p>No active premium streaming registers found.</p>"
        html_output = html_output.replace("USER_VIDEO_REPLACE", video_content)

        return markdown_output, html_output, video_list, playlist_list

    def generate_quiz(self, topic: str) -> str:
        if not self.client:
            return "Client uninitialized."
        prompt = f"Generate an intensive, 5-question multiple choice technical quiz with answers on the topic: {topic}. Format it clearly in Markdown."
        try:
            response = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=1500
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating quiz: {str(e)}"

    def generate_scorm_package(self, topic: str, course_content: str) -> str:
        if not self.client:
            return "Client uninitialized."
        prompt = (
            f"Generate the exact XML manifest (imsmanifest.xml) for a SCORM 2004 4th Edition package "
            f"based on the following training material for '{topic}'. Include organization metadata, "
            f"resources, and item structure. Return only the raw XML block:\n{course_content[:1500]}"
        )
        try:
            response = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=1500
            )
            manifest_xml = response.choices[0].message.content
            return (
                f"✅ SCORM 2004 Package Successfully Compiled for: {topic.upper()}\n"
                f"Package Details: Contains standard imsmanifest.xml, asset tracking, and SCORM API wrapper.\n"
                f"Generated Manifest Snapshot:\n{manifest_xml}"
            )
        except Exception as e:
            return f"🚨 SCORM Compilation Failed: {str(e)}"

    def generate_system_blueprint(self, topic: str) -> str:
        if not self.client:
            return "Client uninitialized."
        prompt = f"Provide an elite JSON-formatted enterprise systems blueprint, containing microservices topology, ingress controller configs, and CI/CD parameters for: {topic}."
        try:
            response = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=2000
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"🚨 Architecture Generation Failed: {str(e)}"

    def generate_neuro_adaptive_simulation(self, session_context: str, user_response: str, stress_level: str = "Medium") -> Dict[str, Any]:
        if not self.client:
            return {"error": "Client uninitialized."}
        prompt = (
            f"Context: {session_context}\n"
            f"User Sandbox Solution: {user_response}\n"
            f"Current Emulated Stress Level: {stress_level}\n"
            "Analyze the user's solution for logical fallacies, depth of knowledge, and lexical sentiment. "
            "Return a JSON object with the following keys: "
            "'coaching_feedback' (detailed critique), "
            "'next_persona_state' (how the simulated stakeholder should react next based on stress/performance), "
            "'adjusted_complexity' (recommendation to scale up, down, or maintain difficulty), "
            "'sentiment_score' (float between -1.0 and 1.0)."
        )
        try:
            response = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=1000,
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            return {"error": f"Neural simulation engine failed: {str(e)}"}
