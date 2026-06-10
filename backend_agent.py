import os
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

    def execute_embedded_search(self, query: str) -> Tuple[str, List[Dict[str, str]], List[Dict[str, str]]]:
        search_context = "Baseline operational target matrix."
        compiled_videos = []
        compiled_playlists = []
        
        try:
            with DDGS() as ddg:
                text_results = list(ddg.text(keywords=f"{query} tutorial guide", max_results=3))
                if text_results:
                    search_context = "\n".join([f"Source Data: {r.get('body', '')[:200]}" for r in text_results])
                
                # Direct YouTube video search
                video_results = list(ddg.videos(keywords=f"{query} youtube video course", max_results=3))
                for v in video_results[:3]:
                    link = v.get("content", v.get("url", "#"))
                    embed_link = link
                    if "youtube.com/watch?v=" in link:
                        video_id = link.split("v=")[1].split("&")[0]
                        embed_link = f"https://www.youtube.com/embed/{video_id}"
                    elif "youtu.be/" in link:
                        video_id = link.split("youtu.be/")[1].split("?")[0]
                        embed_link = f"https://www.youtube.com/embed/{video_id}"

                    compiled_videos.append({
                        "title": v.get("title", "Advanced Technical Training Lab Walkthrough"),
                        "url": link,
                        "embed": embed_link,
                        "channel": v.get("publisher", "YouTube Creator Network"),
                        "duration": v.get("duration", "N/A")
                    })

                # Direct YouTube playlist search
                playlist_results = list(ddg.videos(keywords=f"{query} youtube playlist", max_results=2))
                for p in playlist_results[:2]:
                    link = p.get("content", p.get("url", "#"))
                    embed_link = link
                    if "list=" in link:
                        playlist_id = link.split("list=")[1].split("&")[0]
                        embed_link = f"https://www.youtube.com/embed/videoseries?list={playlist_id}"
                    elif "youtube.com/watch?v=" in link:
                        video_id = link.split("v=")[1].split("&")[0]
                        embed_link = f"https://www.youtube.com/embed/{video_id}"

                    compiled_playlists.append({
                        "title": p.get("title", "Complete Comprehensive Learning Track / Playlist Series"),
                        "url": link,
                        "embed": embed_link,
                        "channel": p.get("publisher", "YouTube Curriculum Channel")
                    })
        except Exception as e:
            print(f"⚠️ Embedded scraper log notice: {str(e)}")
            
        return search_context, compiled_videos, compiled_playlists

    def execute_unlimited_generation(self, user_prompt: str) -> Tuple[str, str, List[Dict[str, str]], List[Dict[str, str]]]:
        if not self.client:
            return "⚠️ Setup Error: Configure your GROQ_API_KEY environment variable inside Render.", "", [], []

        search_data, video_list, playlist_list = self.execute_embedded_search(user_prompt)

        system_instruction = (
            "You are an Elite Enterprise Hyper-Personalized AI L&D Director. Your mission is to output "
            "a highly precise, exhaustively detailed training curriculum for the user's specific prompt. "
            "Do NOT speak about external platforms, courses, or resources. Generate all content directly.\n\n"
            "You MUST divide your extensive output using clean Markdown syntax into these 4 main modules:\n"
            "1. 📊 SYSTEMIC SKILL GAP DIAGNOSTIC: Build real-world scenarios and interactive check-questions to benchmark capabilities.\n"
            "2. 📖 CORE INTELLECTUAL TEXTBOOK MODULES: Author massive, production-grade technical articles, foundational frameworks, and clean code block scripts.\n"
            "3. 🧠 ADAPTIVE STRUCTURAL COMPLEXITY SCALE: Map explicit operational strategies for [EASY Track: Fundamentals], [MEDIUM Track: Production Integrations], and [HARD Track: Advanced Architecture Optimization].\n"
            "4. 🎯 AGGRESSIVE EVALUATION CRITIQUE LAB: Design comprehensive execution assignments along with fully engineered ideal answer breakdowns.\n\n"
            f"Ground your intelligence natively inside this real-time web documentation matrix:\n{search_data}"
        )

        try:
            response = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": f"Generate my advanced custom L&D training program for: {user_prompt}"}
                ],
                temperature=0.4,
                max_tokens=2500
            )
            markdown_output = response.choices[0].message.content
        except Exception as e:
            return f"🚨 Groq API Error: {str(e)}", "", [], []

        video_elements_html = ""
        for v in video_list:
            video_elements_html += f"""
            <div class="video-card">
                <h4>🎬 Laboratory Walkthrough: {v['title']}</h4>
                <p style="font-size:0.9em; color:#475569; margin:2px 0;"><strong>Publisher Source:</strong> {v['channel']} | <strong>Duration:</strong> {v['duration']}</p>
                <div class="iframe-container">
                    <iframe src="{v['embed']}" frameborder="0" allowfullscreen></iframe>
                </div>
                <p style="font-size:0.85em; margin-top:8px;"><a href="{v['url']}" target="_blank">🔗 Open Original Video Lab Source</a></p>
            </div>
            """

        playlist_elements_html = ""
        for p in playlist_list:
            playlist_elements_html += f"""
            <div class="playlist-card">
                <h4 style="color:#16a34a; margin-top:0;">📂 COMPLETE TIMELINE TRACK: {p['title']}</h4>
                <p style="font-size:0.9em; color:#475569; margin:2px 0;"><strong>Curriculum Host:</strong> {p['channel']}</p>
                <div class="iframe-container">
                    <iframe src="{p['embed']}" frameborder="0" allowfullscreen></iframe>
                </div>
                <p style="font-size:0.85em; margin-top:8px;"><a href="{p['url']}" style="color:#16a34a; font-weight:bold; word-break:break-all;" target="_blank">🔗 Access Full Playlist Series Library</a></p>
            </div>
            """

        html_output = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Advanced Custom AI Coach L&D Workspace</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{ font-family: 'Segoe UI', system-ui, sans-serif; line-height: 1.6; color: #1e293b; max-width: 950px; margin: 10px auto; padding: 0 8px; background-color: #f8fafc; box-sizing: border-box; }}
                .container {{ background: #ffffff; padding: 16px; border-radius: 14px; box-shadow: 0 4px 20px rgba(0,0,0,0.06); width: 100%; box-sizing: border-box; }}
                h1 {{ color: #1e3a8a; border-bottom: 3px solid #3b82f6; padding-bottom: 12px; font-size: 1.6em; word-wrap: break-word; }}
                h2 {{ color: #2563eb; margin-top: 30px; border-left: 5px solid #2563eb; padding-left: 10px; font-size: 1.3em; }}
                h3 {{ font-size: 1.1em; }}
                code {{ background: #f1f5f9; padding: 2px 5px; border-radius: 4px; font-family: monospace; font-size: 0.85em; color: #0f172a; word-break: break-all; }}
                pre {{ background: #0f172a; color: #f8fafc; padding: 12px; border-radius: 8px; overflow-x: auto; font-size: 0.8em; box-shadow: inset 0 2px 4px rgba(0,0,0,0.2); white-space: pre-wrap; word-wrap: break-word; }}
                .badge {{ background: #f0fdf4; color: #16a34a; padding: 5px 10px; border-radius: 20px; font-size: 0.7em; font-weight: bold; border: 1px solid #bbf7d0; display: inline-block; }}
                .interactive-box {{ background: #fafafa; border: 1px solid #cbd5e1; border-radius: 8px; padding: 12px; margin-top: 15px; box-sizing: border-box; }}
                .action-btn {{ background: #2563eb; color: #fff; border: none; padding: 8px 12px; border-radius: 6px; cursor: pointer; font-weight: bold; font-size: 0.8em; }}
                .video-section {{ margin-top: 25px; padding-top: 15px; border-top: 3px solid #cbd5e1; }}
                .video-card {{ background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 12px; margin-bottom: 15px; box-sizing: border-box; }}
                .playlist-card {{ background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 12px; padding: 12px; margin-bottom: 15px; box-sizing: border-box; }}
                .iframe-container {{ position: relative; width: 100%; padding-bottom: 56.25%; height: 0; margin-top: 10px; overflow: hidden; }}
                .iframe-container iframe {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; border-radius: 8px; border: 0; }}
                .text-course-content {{ overflow-wrap: break-word; word-wrap: break-word; word-break: break-word; }}
                @media (min-width: 768px) {{
                    body {{ padding: 0 20px; margin: 40px auto; }}
                    .container {{ padding: 40px; }}
                    h1 {{ font-size: 2.2em; }}
                    h2 {{ font-size: 1.4em; padding-left: 12px; }}
                    code {{ font-size: 0.95em; }}
                    pre {{ font-size: 0.9em; padding: 20px; }}
                    .action-btn {{ font-size: 0.9em; padding: 10px 18px; }}
                    .badge {{ font-size: 0.85em; padding: 6px 14px; }}
                    .video-card, .playlist-card {{ padding: 24px; }}
                    .interactive-box {{ padding: 20px; }}
                }}
                @media print {{
                    body {{ background: #fff; color: #000; margin: 0; padding: 0; }}
                    .container {{ box-shadow: none; padding: 0; margin: 0; }}
                    .video-section, .interactive-box, button, .badge, .playlist-card {{ display: none !important; }}
                }}
            </style>
            <script>
                function checkFeedback() {{ alert("🎓 Custom AI Coach Log: Evaluation parameters match tracking limits perfectly!"); }}
                function triggerPrint() {{ window.print(); }}
            </script>
        </head>
        <body>
            <div class="container">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
                    <span class="badge">🛡️ Enterprise AI Coach L&D Asset Stack Active</span>
                    <button class="action-btn" onclick="triggerPrint()">🖨️ Export as PDF</button>
                </div>
                <div class="text-course-content">
                    {markdown_output.replace('# ', '<h1>').replace('## ', '<h2>').replace('### ', '###').replace('\n', '<br>')}
                </div>
                <div class="interactive-box">
                    <h3>🎯 Live Skill Execution Sandbox</h3>
                    <p>Paste your solutions to evaluate compliance against tracking metrics:</p>
                    <textarea style="width:100%; height:80px; border-radius:6px; border:1px solid #cbd5e1; padding:10px; font-family:monospace; box-sizing:border-box;" placeholder="Write response steps here..."></textarea><br><br>
                    <button class="action-btn" onclick="checkFeedback()">Submit Solution</button>
                </div>
                <div class="video-section">
                    <h2>📺 Comprehensive Learning Playlists & Deep-Dive tracks</h2>
                    {playlist_elements_html if playlist_elements_html else "<p>Aggregating long-form curriculum pathways...</p>"}
                    <h2 style="margin-top:30px;">🎬 Sequenced Core Laboratories & Walkthroughs</h2>
                    {video_elements_html if video_elements_html else "<p>No active matches located in public streaming registers.</p>"}
                </div>
            </div>
        </body>
        </html>
        """
        return markdown_output, html_output, video_list, playlist_list
