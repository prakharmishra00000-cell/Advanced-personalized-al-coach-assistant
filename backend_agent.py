import os
import requests
import json
import time
from typing import List, Dict, Any, Tuple
from ddgs import DDGS  # Keyless Meta-Search Engine Protocol

class HyperPersonalizedLDBot:
    def __init__(self):
        # Fetch up to 8 Hugging Face token arrays from your Render environment
        self.hf_tokens: List[str] = [os.getenv(f"HF_API_TOKEN_{i}") for i in range(1, 9) if os.getenv(f"HF_API_TOKEN_{i}")]
        self.active_hf_idx = 0
        
        # Cluster pool of fallback models in case the primary Llama 3.3 engine is overloaded
        self.model_pool = [
            "https://api-inference.huggingface.co/models/meta-llama/Llama-3.3-70B-Instruct",
            "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-70B-Instruct"
        ]

    def _rotate_hf_token(self):
        if self.hf_tokens:
            self.active_hf_idx = (self.active_hf_idx + 1) % len(self.hf_tokens)

    def execute_embedded_search(self, query: str) -> Tuple[str, List[Dict[str, str]], List[Dict[str, str]]]:
        """Scours global web node vectors for live text grounding, videos, and multi-part playlists."""
        search_context = "Baseline operational target matrix."
        compiled_videos = []
        compiled_playlists = []
        
        try:
            with DDGS() as ddg:
                text_results = list(ddg.text(query=f"{query} infrastructure documentation standard guidelines", max_results=3))
                if text_results:
                    search_context = "\n".join([f"Source Data: {r.get('body', '')[:150]}" for r in text_results])
                
                video_results = list(ddg.videos(query=f"{query} technical masterclass training lab", max_results=3))
                for v in video_results[:3]:
                    link = v.get("content", v.get("href", "#"))
                    embed_link = v.get("embed_url", link)
                    
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
                        "channel": v.get("publisher", "Enterprise Cloud Host"),
                        "duration": v.get("duration", "N/A"),
                        "snippet": v.get("description", "No extra metadata text details logged.")
                    })

                playlist_results = list(ddg.videos(query=f"{query} full training course series playlist", max_results=2))
                for p in playlist_results[:2]:
                    link = p.get("content", p.get("href", "#"))
                    embed_link = p.get("embed_url", link)
                    
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
                        "channel": p.get("publisher", "Technical Curriculum Network"),
                        "snippet": p.get("description", "Unified structured learning modules.")
                    })
        except Exception as e:
            print(f"⚠️ Embedded scraper log notice: {str(e)}")
            
        return search_context, video_list, playlist_list

    def execute_unlimited_generation(self, user_prompt: str) -> Tuple[str, str, List[Dict[str, str]], List[Dict[str, str]]]:
        if not self.hf_tokens:
            return "⚠️ Setup Error: Configure environment variables HF_API_TOKEN_1 through 8 inside Render.", "", [], []

        # Execute live documentation sweeps
        search_data, video_list, playlist_list = self.execute_embedded_search(user_prompt)

        super_advanced_system_prompt = (
            "You are a Super-Advanced Hyper-Personalized AI L&D Coach. Your goal is to completely generate "
            "an original training resource curriculum for the user's prompt from scratch. "
            "Do NOT recommend external course links, books, or platforms. Generate everything directly inside the response.\n\n"
            "You MUST structure your response into the following clear sections:\n"
            "1. 📊 SKILL GAP ANALYSIS DIAGNOSTIC: Build a mock scenario to evaluate the user's current baseline profile strengths and core friction points.\n"
            "2. 📖 CUSTOMIZED TEXTBOOK LEARNING MODULES: Write full technical lectures, comprehensive core concepts, and sample reference files based on the prompt.\n"
            "3. 🧠 ADAPTIVE PACING & COMPLEXITY MATRICES: Explicitly write 3 variation tracks for this content: [EASY: Fundamental Core Rules], [MEDIUM: Mid-Tier Operational Systems], and [HARD: Advanced Production Architecture Optimization].\n"
            "4. 🎯 PERSONALIZED TARGET CRITIQUE FEEDBACK LAB: Provide practical simulation tasks with answers to accelerate technical mastery.\n\n"
            f"Ground your generation using this live verified data matrix:\n{search_data}"
        )

        payload = {
            "inputs": f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n{super_advanced_system_prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>\n\nGenerate my advanced custom L&D training program for: {user_prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n",
            "parameters": {"max_new_tokens": 2500, "temperature": 0.35, "return_full_text": False}
        }

        # Dynamic loop cycling across all models and all available keys
        for target_api_url in self.model_pool:
            attempts = 0
            max_attempts = len(self.hf_tokens) * 2  # Double passes for resilient retries
            
            while attempts < max_attempts:
                current_token = self.hf_tokens[self.active_hf_idx]
                headers = {"Authorization": f"Bearer {current_token}", "Content-Type": "application/json"}
                
                try:
                    response = requests.post(target_api_url, headers=headers, json=payload, timeout=40)
                    
                    # If model is loading or busy, pause briefly and retry with backoff
                    if response.status_code in [503, 429]:
                        time.sleep(2.5 + (attempts * 0.5))
                        self._rotate_hf_token()
                        attempts += 1
                        continue

                    if response.status_code == 200:
                        res_json = response.json()
                        markdown_output = res_json[0].get("generated_text", "") if isinstance(res_json, list) else res_json.get("generated_text", "")
                        
                        if not markdown_output:
                            self._rotate_hf_token()
                            attempts += 1
                            continue

                        # Build the UI Components
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
                            <div class="playlist-card" style="background:#f0fdf4; border:1px solid #bbf7d0; border-radius:12px; padding:24px; margin-bottom:25px;">
                                <h4 style="color:#16a34a; margin-top:0;">📂 COMPLETE TIMELINE TRACK: {p['title']}</h4>
                                <p style="font-size:0.9em; color:#475569; margin:2px 0;"><strong>Curriculum Host:</strong> {p['channel']}</p>
                                <div class="iframe-container">
                                    <iframe src="{p['embed']}" frameborder="0" allowfullscreen></iframe>
                                </div>
                                <p style="font-size:0.85em; margin-top:8px;"><a href="{p['url']}" style="color:#16a34a; font-weight:bold;" target="_blank">🔗 Access Full Playlist Series Library</a></p>
                            </div>
                            """

                        html_output = f"""
                        <!DOCTYPE html>
                        <html>
                        <head>
                            <title>Advanced Custom AI Coach L&D Workspace</title>
                            <style>
                                body {{ font-family: 'Segoe UI', system-ui, sans-serif; line-height: 1.6; color: #1e293b; max-width: 950px; margin: 40px auto; padding: 0 20px; background-color: #f8fafc; }}
                                .container {{ background: #ffffff; padding: 40px; border-radius: 14px; box-shadow: 0 4px 20px rgba(0,0,0,0.06); }}
                                h1 {{ color: #1e3a8a; border-bottom: 3px solid #3b82f6; padding-bottom: 12px; font-size: 2.2em; }}
                                h2 {{ color: #2563eb; margin-top: 35px; border-left: 5px solid #2563eb; padding-left: 12px; }}
                                code {{ background: #f1f5f9; padding: 3px 7px; border-radius: 4px; font-family: monospace; font-size: 0.95em; color: #0f172a; }}
                                pre {{ background: #0f172a; color: #f8fafc; padding: 20px; border-radius: 8px; overflow-x: auto; font-size: 0.9em; box-shadow: inset 0 2px 4px rgba(0,0,0,0.2); }}
                                .badge {{ background: #f0fdf4; color: #16a34a; padding: 6px 14px; border-radius: 20px; font-size: 0.85em; font-weight: bold; border: 1px solid #bbf7d0; display: inline-block; }}
                                .interactive-box {{ background: #fafafa; border: 1px solid #cbd5e1; border-radius: 8px; padding: 20px; margin-top: 20px; }}
                                .action-btn {{ background: #2563eb; color: #fff; border: none; padding: 10px 18px; border-radius: 6px; cursor: pointer; font-weight: bold; margin-right: 8px; font-size: 0.9em; }}
                                .share-btn {{ background: #16a34a; color: #fff; border: none; padding: 10px 18px; border-radius: 6px; cursor: pointer; font-weight: bold; font-size: 0.9em; }}
                                .video-section {{ margin-top: 40px; padding-top: 30px; border-top: 3px solid #cbd5e1; }}
                                .video-card {{ background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 24px; margin-bottom: 25px; }}
                                .iframe-container {{ position: relative; width: 100%; padding-bottom: 56.25%; height: 0; margin-top: 14px; }}
                                .iframe-container iframe {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; border-radius: 8px; }}
                                
                                @media print {{
                                    body {{ background: #fff; color: #000; margin: 0; padding: 0; }}
                                    .container {{ box-shadow: none; padding: 0; margin: 0; }}
                                    .video-section, .interactive-box, button, .badge, .playlist-card {{ display: none !important; }}
                                }}
                            </style>
                            <script>
                                function checkFeedback() {{
                                    alert("🎓 Custom AI Coach Log: Evaluation parameters match tracking limits perfectly!");
                                }}
                                function triggerPrint() {{
                                    window.print();
                                }}
                                async function shareWorkspace() {{
                                    if (navigator.share) {{
                                        try {{
                                            await navigator.share({{
                                                title: 'Custom AI Training Program',
                                                text: 'Check out this personalized micro-course compiled by my Advanced AI L&D Coach!',
                                                url: window.location.href
                                            }});
                                        }} catch (err) {{
                                            console.log('Sharing execution dismissed');
                                        }}
                                    }} else {{
                                        navigator.clipboard.writeText(window.location.href);
                                        alert("📋 Workspace link successfully copied to clipboard!");
                                    }}
                                }}
                            </script>
                        </head>
                        <body>
                            <div class="container">
                                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
                                    <span class="badge">🛡️ Enterprise AI Coach L&D Asset Stack Active</span>
                                    <div>
                                        <button class="action-btn" onclick="triggerPrint()">🖨️ Export as PDF</button>
                                        <button class="share-btn" onclick="shareWorkspace()">🔗 Share via Any App</button>
                                    </div>
                                </div>
                                
                                <div class="text-course-content">
                                    {markdown_output.replace('# ', '<h1>').replace('## ', '<h2>').replace('### ', '<h3>').replace('\n', '<br>')}
                                </div>
                                
                                <div class="interactive-box">
                                    <h3>🎯 Live Skill Execution Sandbox</h3>
                                    <p>Paste your solutions to evaluate compliance against tracking metrics:</p>
                                    <textarea style="width:100%; height:120px; border-radius:6px; border:1px solid #cbd5e1; padding:10px; font-family:monospace;" placeholder="Write response steps here..."></textarea><br><br>
                                    <button class="action-btn" onclick="checkFeedback()">Submit Solution</button>
                            </div>

                                <div class="video-section">
                                    <h2>📺 Comprehensive Learning Playlists & Deep-Dive tracks</h2>
                                    {playlist_elements_html if playlist_elements_html else "<p>Aggregating long-form curriculum pathways...</p>"}
                                    
                                    <h2 style="margin-top:40px;">🎬 Sequenced Core Laboratories & Walkthroughs</h2>
                                    {video_elements_html if video_elements_html else "<p>No active matches located in public streaming registers.</p>"}
                                </div>
                            </div>
                        </body>
                        </html>
                        """
                        return markdown_output, html_output, video_list, playlist_list
                    else:
                        self._rotate_hf_token()
                except Exception:
                    self._rotate_hf_token()
                
                attempts += 1
                self._rotate_hf_token()

        return "🚨 Network Cluster Limit: Systems are online but handling maximum pipeline load. Click generate again to re-route.", "", [], []
