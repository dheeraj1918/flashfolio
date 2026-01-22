from flask import Flask, request, jsonify
from flask_cors import CORS
from PyPDF2 import PdfReader
from google import genai
import requests
import base64
from flask import session
import random
import string
import os
from dotenv import load_dotenv
load_dotenv()



chars = string.ascii_letters + string.digits


app=Flask(__name__)
CORS(app,supports_credentials=True)
gemini_api_key=os.environ.get("GEMINI_API_KEY")
GITHUB_TOKEN=os.environ.get("GITHUB_TOKEN")
app.secret_key = "super-secret-key-change-this"
USERNAME="iamsai-pro"

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}
client = genai.Client(api_key=gemini_api_key)

@app.route("/upload",methods=["POST"])
def upload_pdf():
    if "pdf" not in request.files:
        return jsonify({"error":"No file provided"})
    file=request.files["pdf"]
    style=request.form.get("style")
    prompt=get_prompt(style)

    if file.filename=="":
        return jsonify({"error":"Empty file"})
    text_data=extract_text_from_pdf(file)
    REPO_NAME=''.join(random.choices(chars, k=10))
    response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=text_data+prompt
        )
    gemini_output=response.text
    
    if "```html" in gemini_output:
        html_part = gemini_output.split("```html")[1].split("```")[0]
    else:
         html_part = gemini_output

    if "```css" in gemini_output:
        css_part = gemini_output.split("```css")[1].split("```")[0]
    else:
        css_part = ""
    
    
    create_repo(REPO_NAME)
    pages_link = f"https://{USERNAME}.github.io/{REPO_NAME}/"
    upload_to_github(REPO_NAME,"index.html",html_part)
    upload_to_github(REPO_NAME,"style.css",css_part)
    
    return jsonify({"message":"File uploaded successfully","link":pages_link})

def create_repo(REPO_NAME):
    url = "https://api.github.com/user/repos"
    data = {
        "name": REPO_NAME,
        "public": True
    }

    r = requests.post(url, headers=headers, json=data)

    # 201 = created, 422 = already exists
    if r.status_code not in (201, 422):
        r.raise_for_status()


def upload_to_github(REPO_NAME,filename,content):
    url = f"https://api.github.com/repos/{USERNAME}/{REPO_NAME}/contents/{filename}"
    encoded = base64.b64encode(content.encode()).decode()

    data = {
        "message": f"Add {filename}",
        "content": encoded,
        "branch": "main"
    }

    r = requests.put(url, headers=headers, json=data)
    r.raise_for_status()
    requests.post(
    f"https://api.github.com/repos/{USERNAME}/{REPO_NAME}/pages",
    headers=headers,
    json={"source": {"branch": "main", "path": "/"}}
    )
    pages_link = f"https://{USERNAME}.github.io/{REPO_NAME}/"
    session["link"]=pages_link
    print("Website live at:", pages_link)
    return pages_link

@app.route("/getlink",methods=['GET'])
def getLink():
    link=session.get("link")
    return jsonify({
        "link": session.get("link")
    })



    

def get_prompt(style):
    if style=="Classic":
        prompt="""You are an expert web designer and senior front-end developer.

Your task is to generate a **classic-style personal portfolio website**
using **HTML, CSS, and minimal JavaScript**.

────────────────────────────────
### 🎨 Design & Appearance (Classic Style)

• Timeless, elegant, professional aesthetic  
• Neutral color palette (white, ivory, gray, navy, black)  
• Serif or classic sans-serif typography  
• Balanced spacing and symmetrical layout  
• Minimal or no animations  
• Clean, formal visual hierarchy  

────────────────────────────────
### ⚙️ Technical Requirements

• Use semantic HTML5 elements  
• Clean, readable, well-commented code  
• Fully responsive (desktop, tablet, mobile)  
• No heavy frameworks (pure HTML, CSS, JS only)  
• Easy to customize and extend  

────────────────────────────────
### 📜 STRICT CONTENT RULES (VERY IMPORTANT)

• **ALL displayed content must come ONLY from the provided JSON**
• ❌ Do NOT invent, guess, summarize, or rewrite content
• ❌ Do NOT show labels, headings, or placeholders without real data
• ❌ Do NOT render empty UI like:
  - “Name:”
  - “Email:”
  - “Skills:”
  - “Projects:”
  when values are missing

✅ **If a field is empty (`""`, `[]`, or missing), completely hide it**
✅ **If an entire section has no valid data, DO NOT render that section at all**
✅ The page must never show “empty” or “template-like” content

────────────────────────────────
### 🧠 REQUIRED RENDERING LOGIC (MANDATORY)

When generating HTML:

• Render a field ONLY if its value exists and is non-empty  
• Render a section ONLY if it contains at least one valid field  
• If `basics.fullName` is empty → hide header name  
• If `contact.email` is empty → do NOT show email label  
• If an array is empty → do NOT render its section  

❗The final website must look like a **real finished portfolio**, not a template.

────────────────────────────────
### 👤 User Data (JSON)

The JSON below is the **single source of truth**.
Use it exactly as provided.

```json
{
  "basics": {
    "fullName": "",
    "title": "",
    "summary": "",
    "location": {
      "city": "",
      "country": ""
    },
    "contact": {
      "email": "",
      "phone": "",
      "website": "",
      "linkedin": "",
      "github": ""
    }
  },

  "skills": [
    {
      "category": "",
      "items": []
    }
  ],

  "experience": [
    {
      "jobTitle": "",
      "company": "",
      "location": "",
      "startDate": "",
      "endDate": "",
      "description": ""
    }
  ],

  "projects": [
    {
      "name": "",
      "description": "",
      "technologies": [],
      "link": ""
    }
  ],

  "education": [
    {
      "degree": "",
      "institution": "",
      "location": "",
      "startYear": "",
      "endYear": ""
    }
  ],

  "certifications": [
    {
      "name": "",
      "issuer": "",
      "year": ""
    }
  ],

  "languages": [
    {
      "language": "",
      "proficiency": ""
    }
  ],

  "achievements": [""],
  "interests": []
}
"""
    if style=="Complex UI":
        prompt="""You are a senior UI/UX designer and expert front-end engineer.

The text ABOVE this instruction is extracted from a resume PDF.
You MUST use ONLY that text as the source of information.

Your task:
Generate a COMPLETE, WORKING, modern **COMPLEX UI personal portfolio website**
using **HTML and CSS**.

────────────────────────────────
### 🚫 ABSOLUTE RULES (NON-NEGOTIABLE)

• DO NOT explain anything
• DO NOT ask questions
• DO NOT request JSON or more input
• DO NOT include analysis or commentary
• DO NOT include markdown outside code blocks
• DO NOT include placeholder text
• DO NOT invent or guess missing details
• If information is missing → HIDE that section completely
• BOTH HTML AND CSS ARE MANDATORY — empty CSS is INVALID

────────────────────────────────
### 🎨 DESIGN STYLE — COMPLEX UI

• Modern, dashboard-style interface  
• Sidebar or panel-based navigation  
• Cards, grids, and structured layouts  
• Smooth hover effects and transitions  
• Professional, tech-focused aesthetic  
• Fully responsive layout  

────────────────────────────────
### 🧱 TECHNICAL REQUIREMENTS

• Semantic HTML5  
• Modular, clean CSS  
• No frameworks (pure HTML + CSS only)  
• No inline styles (ALL styles must be in CSS)  
• Accessible and responsive  

────────────────────────────────
### 📂 REQUIRED SECTIONS  
(Include ONLY if data exists in resume text)

• Header / Hero  
• About  
• Skills  
• Projects  
• Experience  
• Education  
• Contact  
• Footer  

────────────────────────────────
### 📤 OUTPUT FORMAT (STRICT — MUST FOLLOW EXACTLY)

Return ONLY the following TWO code blocks — NOTHING ELSE.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Portfolio</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <!-- FULL HTML CONTENT -->
</body>
</html>

"""    
    if style=="Hacker UI":
        prompt="""You are a senior UI/UX designer and front-end engineer specializing in
**HACKER-STYLE / TERMINAL-INSPIRED USER INTERFACES**.

The text ABOVE this instruction is extracted from a resume PDF.
You MUST use ONLY that text as the source of information.

Your task:
Generate a COMPLETE, WORKING **HACKER UI personal portfolio website**
using **HTML and CSS**.

────────────────────────────────
### 🚫 ABSOLUTE RULES (NON-NEGOTIABLE)

• DO NOT explain anything  
• DO NOT ask questions  
• DO NOT request JSON or more input  
• DO NOT include analysis or commentary  
• DO NOT include markdown outside code blocks  
• DO NOT include placeholder text  
• DO NOT invent or guess missing details  
• If information is missing → HIDE that section completely  
• BOTH HTML AND CSS ARE MANDATORY — empty CSS is INVALID  

────────────────────────────────
### 🧠 DESIGN STYLE — HACKER UI

• Terminal-inspired interface  
• Dark background (black / very dark gray)  
• Neon green, cyan, or red monospace text  
• Hacker-style panels, borders, and separators  
• Command-line aesthetics (prompts, blinking cursor feel)  
• Matrix / cyberpunk / security-console vibe  
• ASCII-style separators or borders (visual only, not text junk)  
• Subtle glitch or scanline effects using CSS (lightweight)  

────────────────────────────────
### 🧱 TECHNICAL REQUIREMENTS

• Semantic HTML5  
• Clean, modular CSS  
• Monospace fonts only (system or Google Fonts)  
• No frameworks (pure HTML + CSS only)  
• No inline styles (ALL styling in CSS)  
• Fully responsive (desktop + mobile)  
• High contrast for readability  

────────────────────────────────
### 📂 REQUIRED SECTIONS  
(Include ONLY if data exists in resume text)

• Boot / Intro screen  
• About (displayed like system info)  
• Skills (displayed like command output or logs)  
• Projects (displayed like executed commands)  
• Experience (timeline or log-style output)  
• Education  
• Contact (terminal-style links)  
• Footer (system status / signature)

────────────────────────────────
### 📤 OUTPUT FORMAT (STRICT — MUST FOLLOW EXACTLY)

Return ONLY the following TWO code blocks — NOTHING ELSE.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Hacker Portfolio</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <!-- FULL HTML CONTENT -->
</body>
</html>
"""
    if style=="Windows 95":
        prompt=""" You are a senior UI/UX designer and front-end engineer specializing in
AUTHENTIC WINDOWS 95–STYLE DESKTOP INTERFACES.

The text ABOVE this instruction is extracted from a resume PDF.
You MUST use ONLY that text as the source of information.

Your task:
Generate a COMPLETE, WORKING **Windows 95–style personal portfolio website**
using **HTML, CSS, and JavaScript**.

────────────────────────────────
### 🚫 ABSOLUTE RULES (NON-NEGOTIABLE)

• DO NOT explain anything
• DO NOT ask questions
• DO NOT request JSON or more input
• DO NOT include analysis or commentary
• DO NOT include markdown outside code blocks
• DO NOT include placeholder text
• DO NOT invent or guess missing details
• If information is missing → HIDE that section completely
• HTML + CSS are MANDATORY
• JavaScript is REQUIRED for window movement
• ALL JavaScript MUST be inside the HTML file (inside <script> tag)
• CSS MUST be in a separate CSS file
• Output MUST include ```html``` and ```css``` blocks

────────────────────────────────
### 🪟 WINDOWS 95 BEHAVIOR (CRITICAL)

The UI MUST behave like a real Windows 95 desktop:

• Each section must be inside a draggable window
• Windows MUST be movable by dragging the title bar
• Clicking a window brings it to the front (z-index change)
• Windows start at different screen positions
• Close (❌) button hides the window
• Minimize (_) button collapses window content
• Title bar drag is smooth and natural

FAILURE TO IMPLEMENT DRAGGING = INVALID OUTPUT

────────────────────────────────
### 🎨 DESIGN STYLE — WINDOWS 95

• Classic gray background (#c0c0c0)
• Teal desktop background
• Blue title bars
• Beveled borders (inset / outset)
• Pixel/system fonts (MS Sans Serif / Tahoma style)
• Sharp edges, NO rounded corners
• NO modern effects (no blur, no gradients)

────────────────────────────────
### 🧱 TECHNICAL REQUIREMENTS

• Semantic HTML5
• Modular CSS (Windows 95–style buttons, windows)
• No frameworks
• No external JS files
• JavaScript ONLY inside <script> in HTML
• Fully responsive (windows stack vertically on mobile)

────────────────────────────────
### 📂 REQUIRED WINDOWS  
(Include ONLY if data exists in resume text)

• About Me (window)
• Skills (window)
• Projects (window)
• Experience (window)
• Education (window)
• Certifications (window)
• Contact (window)

────────────────────────────────
### 📤 OUTPUT FORMAT (STRICT — MUST FOLLOW EXACTLY)

Return ONLY the following TWO code blocks — NOTHING ELSE.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Windows 95 Portfolio</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>

  <!-- DESKTOP AND WINDOWS HERE -->

  <script>
    /* DRAGGABLE WINDOWS JAVASCRIPT */
    /* z-index management */
    /* close & minimize logic */
  </script>

</body>
</html>

 """
    if style=="Mac OS":
        prompt="""You are a senior UI/UX designer and front-end engineer specializing in
AUTHENTIC CLASSIC MAC OS (Mac OS 8 / Mac OS 9) USER INTERFACES.

The text ABOVE this instruction is extracted from a resume PDF.
You MUST use ONLY that text as the source of information.

Your task:
Generate a COMPLETE, WORKING **Classic Mac OS–style personal portfolio website**
using **HTML, CSS, and JavaScript**.

────────────────────────────────
### 🚫 ABSOLUTE RULES (NON-NEGOTIABLE)

• DO NOT explain anything  
• DO NOT ask questions  
• DO NOT request JSON or more input  
• DO NOT include analysis or commentary  
• DO NOT include markdown outside code blocks  
• DO NOT include placeholder text  
• DO NOT invent or guess missing details  
• If information is missing → HIDE that section completely  
• HTML + CSS are MANDATORY  
• JavaScript is REQUIRED  
• ALL JavaScript MUST be inside the HTML file (inside `<script>` tag)  
• CSS MUST be in a separate CSS file  
• Output MUST include ```html``` and ```css``` blocks  

────────────────────────────────
### 🍎 CLASSIC MAC OS BEHAVIOR (CRITICAL)

The UI MUST behave like real **old Mac OS (8/9)**:

• Each section appears inside a draggable Mac-style window  
• Windows MUST be draggable by the title bar  
• Clicking a window brings it to the front (z-index focus)  
• Close button (●) closes the window  
• No maximize button (classic Mac behavior)  
• Title bars have centered titles  
• Windows start at different desktop positions  
• Smooth, natural dragging behavior  

FAILURE TO IMPLEMENT DRAGGING = INVALID OUTPUT

────────────────────────────────
### 🎨 DESIGN STYLE — CLASSIC MAC OS

• Light gray desktop background  
• Platinum-style window UI  
• Rounded window corners (subtle)  
• Soft shadows under windows  
• Title bar with **single left circular button (●)**  
• Chicago / Geneva / system-style fonts  
• Simple icons and separators  
• No modern effects (no blur, no glass, no gradients)  
• Friendly, clean, nostalgic Apple aesthetic  

────────────────────────────────
### 🧱 TECHNICAL REQUIREMENTS

• Semantic HTML5  
• Modular, clean CSS  
• No frameworks  
• No external JS files  
• JavaScript ONLY inside `<script>` in HTML  
• Fully responsive (windows stack vertically on mobile)  

────────────────────────────────
### 📂 REQUIRED WINDOWS  
(Include ONLY if data exists in resume text)

• Welcome / About  
• Skills  
• Projects  
• Experience  
• Education  
• Certifications  
• Contact  
• Footer (desktop info / copyright)

────────────────────────────────
### 📤 OUTPUT FORMAT (STRICT — MUST FOLLOW EXACTLY)

Return ONLY the following TWO code blocks — NOTHING ELSE.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Classic Mac OS Portfolio</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>

  <!-- DESKTOP AND MAC WINDOWS HERE -->

  <script>
    /* DRAGGABLE MAC WINDOWS JAVASCRIPT */
    /* z-index focus handling */
    /* close button logic */
  </script>

</body>
</html>
"""
    if style=="VS Code":
        prompt="""You are a senior UI/UX designer and front-end engineer specializing in
AUTHENTIC VS CODE / IDE-STYLE USER INTERFACES.

The text ABOVE this instruction is extracted from a resume PDF.
You MUST use ONLY that text as the source of information.

Your task:
Generate a COMPLETE, WORKING **VS Code–style personal portfolio website**
using **HTML, CSS, and JavaScript**.

────────────────────────────────
### 🚫 ABSOLUTE RULES (NON-NEGOTIABLE)

• DO NOT explain anything  
• DO NOT ask questions  
• DO NOT request JSON or more input  
• DO NOT include analysis or commentary  
• DO NOT include markdown outside code blocks  
• DO NOT include placeholder text  
• DO NOT invent or guess missing details  
• If information is missing → HIDE that section completely  
• HTML + CSS are MANDATORY  
• JavaScript is REQUIRED  
• ALL JavaScript MUST be inside the HTML file (inside `<script>` tag)  
• CSS MUST be in a separate CSS file  
• Output MUST include ```html``` and ```css``` blocks  

────────────────────────────────
### 🧠 VS CODE UI BEHAVIOR (CRITICAL)

The UI MUST behave like a real IDE:

• Left sidebar with file explorer  
• Explorer items represent portfolio sections (About, Skills, Projects, etc.)  
• Clicking a file opens content in the editor area  
• Tabs appear at the top for opened files  
• Clicking tabs switches content  
• Active tab is highlighted  
• Sidebar can be collapsed (JS toggle)  
• No page reloads — single-page behavior  

FAILURE TO IMPLEMENT FILE → TAB → EDITOR FLOW = INVALID OUTPUT

────────────────────────────────
### 🎨 DESIGN STYLE — VS CODE

• Dark theme inspired by VS Code  
• Dark sidebar, slightly lighter editor background  
• Monospace fonts (Fira Code / system monospace)  
• Subtle borders and separators  
• Minimal icons (CSS-based or simple text icons)  
• No flashy animations — clean developer aesthetic  
• Professional, realistic IDE look  

────────────────────────────────
### 🧱 TECHNICAL REQUIREMENTS

• Semantic HTML5  
• Modular, readable CSS  
• No frameworks  
• No external JS files  
• JavaScript ONLY inside `<script>` in HTML  
• Fully responsive (sidebar stacks on mobile)  

────────────────────────────────
### 📂 REQUIRED FILES (SECTIONS)
(Include ONLY if data exists in resume text)

• about.md  
• skills.json  
• projects.js  
• experience.txt  
• education.md  
• certifications.txt  
• contact.md  

(These are UI labels only — content comes from resume text.)

────────────────────────────────
### 📤 OUTPUT FORMAT (STRICT — MUST FOLLOW EXACTLY)

Return ONLY the following TWO code blocks — NOTHING ELSE.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>VS Code Portfolio</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>

  <!-- VS CODE LAYOUT: SIDEBAR, TABS, EDITOR -->

  <script>
    /* FILE EXPLORER CLICK HANDLING */
    /* TAB MANAGEMENT */
    /* ACTIVE FILE STATE */
    /* SIDEBAR TOGGLE */
  </script>

</body>
</html>
"""
    if style=="Terminal":
        prompt="""You are a senior UI/UX designer and front-end engineer specializing in
AUTHENTIC TERMINAL / COMMAND-LINE USER INTERFACES.

The text ABOVE this instruction is extracted from a resume PDF.
You MUST use ONLY that text as the source of information.

Your task:
Generate a COMPLETE, WORKING **Terminal-style personal portfolio website**
using **HTML, CSS, and JavaScript**.

────────────────────────────────
### 🚫 ABSOLUTE RULES (NON-NEGOTIABLE)

• DO NOT explain anything  
• DO NOT ask questions  
• DO NOT request JSON or more input  
• DO NOT include analysis or commentary  
• DO NOT include markdown outside code blocks  
• DO NOT include placeholder text  
• DO NOT invent or guess missing details  
• If information is missing → HIDE that section completely  
• HTML + CSS are MANDATORY  
• JavaScript is REQUIRED  
• ALL JavaScript MUST be inside the HTML file (inside `<script>` tag)  
• CSS MUST be in a separate CSS file  
• Output MUST include ```html``` and ```css``` blocks  

────────────────────────────────
### 🖥️ TERMINAL UI BEHAVIOR (CRITICAL)

The UI MUST behave like a real terminal:

• Black or very dark background  
• Monospace font  
• Blinking cursor effect  
• Command prompt (e.g. `user@portfolio:~$`)  
• Commands typed automatically or via buttons  
• Each command prints output below it  
• Portfolio sections appear as command outputs  
• No page reloads — single-page terminal session  

FAILURE TO IMPLEMENT COMMAND → OUTPUT FLOW = INVALID OUTPUT

────────────────────────────────
### 🎨 DESIGN STYLE — TERMINAL

• Pure terminal aesthetics  
• High contrast text (green / white / cyan)  
• No cards, no panels, no modern UI  
• Clean, hacker-friendly CLI look  
• Minimal colors  
• Optional scanline or CRT effect (CSS only, subtle)  

────────────────────────────────
### 🧱 TECHNICAL REQUIREMENTS

• Semantic HTML5  
• Clean, modular CSS  
• No frameworks  
• No external JS files  
• JavaScript ONLY inside `<script>`  
• Fully responsive (terminal resizes on mobile)  

────────────────────────────────
### 📂 REQUIRED COMMANDS  
(Include ONLY if data exists in resume text)

• `whoami` → name + title  
• `about` → summary  
• `skills` → skills list  
• `projects` → projects output  
• `experience` → experience logs  
• `education` → education details  
• `certifications` → certifications  
• `contact` → contact info  

Commands are UI labels only — content comes from resume text.

────────────────────────────────
### 📤 OUTPUT FORMAT (STRICT — MUST FOLLOW EXACTLY)

Return ONLY the following TWO code blocks — NOTHING ELSE.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Terminal Portfolio</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>

  <!-- TERMINAL WINDOW -->

  <script>
    /* TERMINAL COMMAND HANDLING */
    /* OUTPUT RENDERING */
    /* BLINKING CURSOR LOGIC */
    /* COMMAND SIMULATION */
  </script>

</body>
</html>
"""
    if style=="Cyberpunk UI":
        prompt="""You are a senior UI/UX designer and front-end engineer specializing in
FUTURISTIC **CYBERPUNK USER INTERFACES**.

The text ABOVE this instruction is extracted from a resume PDF.
You MUST use ONLY that text as the source of information.

Your task:
Generate a COMPLETE, WORKING **Cyberpunk-style personal portfolio website**
using **HTML, CSS, and JavaScript**.

────────────────────────────────
### 🚫 ABSOLUTE RULES (NON-NEGOTIABLE)

• DO NOT explain anything  
• DO NOT ask questions  
• DO NOT request JSON or more input  
• DO NOT include analysis or commentary  
• DO NOT include markdown outside code blocks  
• DO NOT include placeholder text  
• DO NOT invent or guess missing details  
• If information is missing → HIDE that section completely  
• HTML + CSS are MANDATORY  
• JavaScript is REQUIRED  
• ALL JavaScript MUST be inside the HTML file (inside `<script>` tag)  
• CSS MUST be in a separate CSS file  
• Output MUST include ```html``` and ```css``` blocks  

────────────────────────────────
### 🌃 CYBERPUNK UI BEHAVIOR (CRITICAL)

The interface MUST feel futuristic and interactive:

• Floating neon panels  
• Clickable sections with animated transitions  
• Panels open/close using JavaScript  
• Active panel highlighted with glow  
• Smooth state transitions (no page reloads)  
• Layered depth using z-index  

FAILURE TO IMPLEMENT INTERACTIVE PANELS = INVALID OUTPUT

────────────────────────────────
### 🎨 DESIGN STYLE — CYBERPUNK

• Dark background (near black / deep purple)  
• Neon accent colors (cyan, magenta, electric blue)  
• Glowing borders and text (CSS glow)  
• Futuristic monospace or techno fonts  
• Grid or HUD-style layout  
• Subtle glitch, scanline, or flicker effects (CSS only)  
• High contrast, readable text  

────────────────────────────────
### 🧱 TECHNICAL REQUIREMENTS

• Semantic HTML5  
• Modular, clean CSS  
• No frameworks  
• No external JS files  
• JavaScript ONLY inside `<script>`  
• Fully responsive (panels stack on mobile)  

────────────────────────────────
### 📂 REQUIRED PANELS  
(Include ONLY if data exists in resume text)

• Identity / About  
• Skills  
• Projects  
• Experience  
• Education  
• Certifications  
• Contact  
• Footer (system status / credits)

────────────────────────────────
### 📤 OUTPUT FORMAT (STRICT — MUST FOLLOW EXACTLY)

Return ONLY the following TWO code blocks — NOTHING ELSE.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Cyberpunk Portfolio</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>

  <!-- CYBERPUNK PANELS & HUD -->

  <script>
    /* PANEL OPEN / CLOSE LOGIC */
    /* ACTIVE STATE MANAGEMENT */
    /* OPTIONAL GLITCH EFFECTS */
  </script>

</body>
</html>
"""

    return prompt


def extract_text_from_pdf(file):
    reader=PdfReader(file)
    text=""
    for page in reader.pages:
        text+=page.extract_text()+"\n"
    
    return text


if __name__=="__main__":
    app.run(debug=True,port=8080)