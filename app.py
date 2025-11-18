import os
import time
import requests
import pdfplumber
import mammoth
import markdown
import json
import re
from flask import Flask, render_template, request, jsonify 
from dotenv import load_dotenv

# --- Configuration ---
load_dotenv()

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024 

# --- Helpers ---
def clean_json_text(text):
    """Removes markdown code blocks to prevent parsing errors."""
    try:
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]
        return text.strip()
    except Exception:
        return text

def call_gemini_api_json(user_query, system_prompt, retries=3, delay=3):
    """Calls Gemini with JSON enforcement."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key: raise EnvironmentError("GEMINI_API_KEY not set")
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    
    payload = {
        "contents": [{"parts": [{"text": user_query}]}],
        "systemInstruction": {"parts": [{"text": system_prompt}]},
        "generationConfig": {"response_mime_type": "application/json"}
    }
    return _make_api_request(api_url, payload, retries, delay)

def call_gemini_api_text(user_query, system_prompt, retries=3, delay=3):
    """Calls Gemini for standard text output."""
    api_key = os.environ.get("GEMINI_API_KEY")
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    
    payload = {
        "contents": [{"parts": [{"text": user_query}]}],
        "systemInstruction": {"parts": [{"text": system_prompt}]},
    }
    return _make_api_request(api_url, payload, retries, delay)

def _make_api_request(url, payload, retries, delay):
    for attempt in range(retries):
        try:
            response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
            if response.status_code == 200:
                result = response.json()
                if "candidates" in result and result["candidates"]:
                    return result["candidates"][0]["content"]["parts"][0]["text"]
            elif response.status_code == 503:
                print("Model overloaded, retrying...")
        except requests.RequestException as e:
            print(f"Request failed: {e}")
        
        if attempt < retries - 1:
            time.sleep(delay * (2 ** attempt))
    raise ConnectionError("Failed to get response from AI.")

# --- Text Extraction ---
def extract_text_from_pdf(filepath):
    text = ""
    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages: text += page.extract_text() or ""
    return text

def extract_text_from_docx(filepath):
    with open(filepath, "rb") as docx_file: return mammoth.extract_raw_text(docx_file).value

def extract_text_from_txt(filepath):
    with open(filepath, "r", encoding="utf-8") as txt_file: return txt_file.read()

# --- Routes ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    analysis_result_html = ""
    error_message = ""
    resume_text = "" 
    highlighted_text = ""
    missing_keywords = []
    match_score = 0
    job_description = request.form.get('job_description', '')
    
    if 'resume_file' not in request.files:
        error_message = "No resume file selected."
    else:
        file = request.files['resume_file']
        if file.filename == '':
            error_message = "No resume file selected."
        elif file:
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            try:
                file.save(filepath)
                if filename.endswith('.pdf'): resume_text = extract_text_from_pdf(filepath)
                elif filename.endswith('.docx'): resume_text = extract_text_from_docx(filepath)
                elif filename.endswith('.txt'): resume_text = extract_text_from_txt(filepath)
                else: error_message = "Unsupported file type."

                if resume_text:
                    system_prompt = "You are an expert ATS. Analyze the resume against the job description."
                    user_query = f"""
                        **JOB DESCRIPTION:** {job_description}
                        **RESUME:** {resume_text}
                        
                        Output a JSON object with these 4 keys:
                        1. "match_score": An integer (0-100) representing the match percentage.
                        2. "analysis_markdown": A structured summary with Key Strengths and Suggestions.
                        3. "matched_keywords": List of matching skills found in resume.
                        4. "missing_keywords": List of important keywords missing from resume.
                    """
                    
                    raw = call_gemini_api_json(user_query, system_prompt)
                    cleaned = clean_json_text(raw)
                    
                    try:
                        data = json.loads(cleaned)
                        match_score = data.get("match_score", 0)
                        analysis_result_html = markdown.markdown(data.get("analysis_markdown", ""))
                        matched_keywords = data.get("matched_keywords", [])
                        missing_keywords = data.get("missing_keywords", [])

                        # Highlighting
                        highlighted_text = resume_text
                        matched_keywords.sort(key=len, reverse=True)
                        for keyword in matched_keywords:
                            pattern = re.compile(f"({re.escape(keyword)})", re.IGNORECASE)
                            highlighted_text = pattern.sub(r'<span class="bg-green-200 text-green-800 font-semibold px-1 rounded">\1</span>', highlighted_text)
                        highlighted_text = highlighted_text.replace('\n', '<br>')
                        
                    except json.JSONDecodeError:
                        error_message = "AI response error."
            except Exception as e:
                error_message = f"Error: {e}"
            finally:
                if os.path.exists(filepath): os.remove(filepath)
    
    if error_message:
        analysis_result_html = f'<p class="text-red-500"><strong>Error:</strong> {error_message}</p>'

    return render_template('index.html', 
        analysis_result_html=analysis_result_html, 
        job_description=job_description, 
        resume_text=resume_text,
        highlighted_text=highlighted_text,
        missing_keywords=missing_keywords,
        match_score=match_score
    )

# --- Bonus Tools Routes ---

@app.route('/generate_questions', methods=['POST'])
def generate_questions():
    data = request.get_json()
    user_query = f"Job: {data.get('job_description')} Resume: {data.get('resume_text')} Output HTML: 5 Technical, 3 Behavioral Questions."
    try:
        res = call_gemini_api_text(user_query, "Technical Interviewer")
        return jsonify({"html": markdown.markdown(res)})
    except Exception as e: return jsonify({"error": str(e)}), 500

@app.route('/generate_cover_letter', methods=['POST'])
def generate_cover_letter():
    data = request.get_json()
    user_query = f"Write a cover letter for Job: {data.get('job_description')} using Resume: {data.get('resume_text')}. HTML output."
    try:
        res = call_gemini_api_text(user_query, "Career Coach")
        return jsonify({"html": markdown.markdown(res)})
    except Exception as e: return jsonify({"error": str(e)}), 500

@app.route('/rewrite_bullet', methods=['POST'])
def rewrite_bullet():
    data = request.get_json()
    bullet_text = data.get('bullet_text')
    if not bullet_text: return jsonify({"error": "No text provided"}), 400
    
    system_prompt = "You are a professional resume writer."
    user_query = f"""
        Rewrite this resume bullet point to be impactful, use action verbs, and include placeholder metrics.
        ORIGINAL: "{bullet_text}"
        Provide 3 variations (Conservative, Aggressive, Concise) as HTML bullets.
    """
    try:
        res = call_gemini_api_text(user_query, system_prompt)
        return jsonify({"html": markdown.markdown(res)})
    except Exception as e: return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True, port=5000)