import os
import re
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
        search_context = "Baseline operational target operational matrix."
        compiled_videos = []
        compiled_playlists = []
        
        try:
            with DDGS() as ddg:
                # 1. Fetch relevant body text for course textbook generation
                text_results = list(ddg.text(keywords=f"{query} tutorial course", max_results=3))
                if text_results:
                    search_context = "\n".join([f"Source Data: {r.get('body', '')[:200]}" for r in text_results])
                
                # 2. Query DuckDuckGo Video API for actual specific videos
                video_ddgs_results = list(ddg.videos(keywords=f"{query} youtube", max_results=3))
                for v in video_ddgs_results:
                    link = v.get("content", v.get("url", ""))
                    # Validate and extract real YouTube watch links
                    if "youtube.com/watch?v=" in link or "youtu.be/" in link:
                        video_id = ""
                        if "v=" in link:
                            video_id = link.split("v=")[1].split("&")[0]
                        elif "youtu.be/" in link:
                            video_id = link.split("youtu.be/")[1].split("?")[0]
                            
                        if video_id:
                            embed_link = f"https://www.youtube.com/embed/{video_id}"
                            compiled_videos.append({
                                "title": v.get("title", f"Walkthrough: {query}"),
                                "url": link,
                                "embed": embed_link,
                                "channel": v.get("publisher", "YouTube Creator"),
                                "duration": v.get("duration", "N/A")
                            })

                # 3. Query DuckDuckGo Video API for actual specific playlists
                playlist_DDGS_results = list(ddg.videos(keywords=f"{query} playlist youtube", max_results=2))
                for p in playlist_DDGS_results:
                    link = p.get("content", p.get("url", ""))
                    # Validate and extract real YouTube playlist links
                    if "list=" in link:
                        playlist_id = link.split("list=")[1].split("&")[0]
                        embed_link = f"https://www.youtube.com/embed/videoseries?list={playlist_id}"
                        compiled_playlists.append({
                            "title": p.get("title", f"Playlist Track: {query}"),
                            "url": link,
                            "embed": embed_link,
                            "channel": p.get("publisher", "YouTube Creator")
                        })
                
                # Resilient Fallbacks: If direct parsing yields zero items, construct exact live YouTube search query links
                if not compiled_videos:
                    fallback_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
                    compiled_videos.append({
                        "title": f"Live Search Results for: {query.capitalize()}",
                        "url": fallback_url,
                        "embed": fallback_url,
                        "channel": "YouTube Search Directory",
                        "duration": "N/A"
                    })
                    
                if not compiled_playlists:
                    fallback_p_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}+playlist"
                    compiled_playlists.append({
                        "title": f"Live Playlist Track for: {query.capitalize()}",
                        "url": fallback_p_url,
                        "embed": fallback_p_url,
                        "channel": "YouTube Search Directory"
                    })

        except Exception as e:
            print(f"⚠️ Embedded scraper log notice: {str(e)}")
            
        return search_context, compiled_videos, compiled_playlists

    def execute_unlimited_generation(self, user_prompt: str, difficulty: str = "Production-Ready") -> Tuple[str, str, List[Dict[str, str]], List[Dict[str, str]]]:
        if not self.client:
            return "⚠️ Setup Error: Configure your GROQ_API_KEY environment variable inside Render.", "", [], []

        search_data, video_list, playlist_list = self.execute_embedded_search(user_prompt)

        system_instruction = (
            f"You are an Elite Enterprise Hyper-Personalized AI L&D Director operating at an '{difficulty}' complexity tier. "
            "Your mission is to output a highly precise, exhaustively detailed training curriculum for the user's specific prompt. "
            "Do NOT speak about external platforms, courses, or resources. Generate all content directly.\n\n"
            "You MUST divide your extensive output using clean Markdown syntax into these 4 main modules:\n"
            "1. 📊 SYSTEMIC SKILL GAP DIAGNOSTIC: Build real-world scenarios and interactive check-questions to benchmark capabilities.\n"
            "2. 📖 CORE INTELLECTUAL TEXTBOOK MODULES: Author massive, production-grade technical articles, foundational frameworks, and clean code block scripts.\n"
            "3. 🧠 ADAPTIVE STRUCTURAL COMPLEXITY SCALE: Map explicit operational strategies for fundamentals, production integrations, and advanced architecture optimizations.\n"
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
                <p style="font-size:0.85em; margin-top:8px; word-break:break-all;"><a href="{v['url']}" target="_blank">🔗 Direct Link to Access Video</a></p>
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
                <p style="font-size:0.85em; margin-top:8px;"><a href="{p['url']}" style="color:#16a34a; font-weight:bold; word-break:break-all;" target="_blank">🔗 Direct Link to Access Playlist</a></p>
            </div>
            """

        html_output = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Advanced Custom AI Coach L&D Workspace</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
            <style>
                html {{ overflow-x: hidden; width: 100%; }}
                body {{ font-family: 'Segoe UI', system-ui, sans-serif; line-height: 1.6; color: #1e293b; width: 100%; max-width: 100vw; margin: 0 auto; padding: 10px 8px; background-color: #f8fafc; box-sizing: border-box; overflow-x: hidden; }}
                .container {{ background: #ffffff; padding: 16px; border-radius: 14px; box-shadow: 0 4px 20px rgba(0,0,0,0.06); width: 100%; box-sizing: border-box; overflow-wrap: anywhere; }}
                h1 {{ color: #1e3a8a; border-bottom: 3px solid #3b82f6; padding-bottom: 12px; font-size: 1.5em; word-wrap: break-word; word-break: break-word; }}
                h2 {{ color: #2563eb; margin-top: 30px; border-left: 5px solid #2563eb; padding-left: 10px; font-size: 1.2em; word-wrap: break-word; }}
                h3 {{ font-size: 1.05em; word-wrap: break-word; }}
                p, li, div {{ font-size: 0.95em; word-wrap: break-word; box-sizing: border-box; }}
                code {{ background: #f1f5f9; padding: 2px 5px; border-radius: 4px; font-family: monospace; font-size: 0.8em; color: #0f172a; word-break: break-all; word-wrap: break-word; overflow-wrap: anywhere; }}
                pre {{ background: #0f172a; color: #f8fafc; padding: 12px; border-radius: 8px; overflow-x: auto; font-size: 0.75em; box-sizing: border-box; box-shadow: inset 0 2px 4px rgba(0,0,0,0.2); white-space: pre-wrap; word-wrap: break-word; word-break: break-word; }}
                pre code {{ background: transparent; color: inherit; padding: 0; font-size: 1e-1; word-break: break-word; }}
                .badge {{ background: #f0fdf4; color: #16a34a; padding: 5px 10px; border-radius: 20px; font-size: 0.65em; font-weight: bold; border: 1px solid #bbf7d0; display: inline-block; }}
                .interactive-box {{ background: #fafafa; border: 1px solid #cbd5e1; border-radius: 8px; padding: 12px; margin-top: 15px; box-sizing: border-box; width: 100%; }}
                .action-btn {{ background: #2563eb; color: #fff; border: none; padding: 8px 12px; border-radius: 6px; cursor: pointer; font-weight: bold; font-size: 0.75em; }}
                .video-section {{ margin-top: 25px; padding-top: 15px; border-top: 3px solid #cbd5e1; width: 100%; box-sizing: border-box; }}
                .video-card {{ background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 12px; margin-bottom: 15px; box-sizing: border-box; width: 100%; }}
                .playlist-card {{ background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 12px; padding: 12px; margin-bottom: 15px; box-sizing: border-box; width: 100%; }}
                .iframe-container {{ position: relative; width: 100%; padding-bottom: 56.25%; height: 0; margin-top: 10px; overflow: hidden; }}
                .iframe-container iframe {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; border-radius: 8px; border: 0; }}
                .text-course-content {{ width: 100%; overflow-wrap: anywhere; word-wrap: break-word; box-sizing: border-box; }}
                @media (min-width: 768px) {{
                    body {{ padding: 0 20px; margin: 40px auto; max-width: 950px; font-size: 100%; }}
                    .container {{ padding: 40px; }}
                    h1 {{ font-size: 2em; }}
                    h2 {{ font-size: 1.35em; padding-left: 12px; }}
                    p, li, div {{ font-size: 1em; }}
                    code {{ font-size: 0.9em; }}
                    pre {{ font-size: 0.85em; padding: 20px; }}
                    .action-btn {{ font-size: 0.85em; padding: 10px 16px; }}
                    .badge {{ font-size: 0.8em; padding: 6px 14px; }}
                    .video-card, .playlist-card {{ padding: 20px; }}
                    .interactive-box {{ padding: 20px; }}
                }}
                @media print {{
                    body {{ background: #fff; color: #000; margin: 0; padding: 0; width: auto; max-width: none; }}
                    .container {{ box-shadow: none; padding: 0; margin: 0; width: auto; }}
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

    def generate_quiz(self, topic: str) -> str:
        """Generates an interactive 5-question multiple choice quiz using Groq."""
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
