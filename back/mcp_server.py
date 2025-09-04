# mcp_server.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_mail import Mail, Message
import pdfplumber
from docx import Document
import json
import re
from rapidfuzz import fuzz

app = Flask(__name__)
CORS(app)

# -------------------------
# Mailtrap configuration (safe sandbox)
# -------------------------
app.config['MAIL_SERVER'] = 'sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = '6bf33a822ff4f5'  # Mailtrap username
app.config['MAIL_PASSWORD'] = 'f6ab57b94695a3'  # Mailtrap password
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

# -------------------------
# CV parsing helpers
# -------------------------
section_map = {
    "experience": ["experience", "work history", "employment"],
    "skills": ["skills", "technologies", "expertise"]
}

def extract_text(file):
    if file.filename.endswith(".pdf"):
        text = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text
    elif file.filename.endswith(".docx"):
        doc = Document(file)
        return "\n".join([p.text for p in doc.paragraphs])
    else:
        return ""

def extract_name(text):
    """
    Extract the candidate's name from CV text.
    1. Look for line starting with 'Name:'
    2. If not found, use the first non-empty line
    """
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    
    # 1. Look for 'Name:' label
    for line in lines:
        if line.lower().startswith("name:"):
            return line.split(":", 1)[1].strip()
    
    # 2. Fallback: first non-empty line
    if lines:
        return lines[0]
    
    return "N/A"

def find_section(text, keywords):
    lines = text.split("\n")
    section_lines = []
    capture = False
    for line in lines:
        line_lower = line.lower()
        if any(k in line_lower for k in keywords):
            capture = True
            continue
        # Stop at next heading (all uppercase or title case)
        if capture and re.match(r'^[A-Z][A-Za-z ]{2,}$', line.strip()):
            break
        if capture:
            section_lines.append(line.strip())
    return "\n".join(section_lines)

def parse_skills(section_text):
    skills = re.split(r',|\n', section_text)
    return [s.strip() for s in skills if s.strip()]

def parse_experience(section_text):
    exp_list = []
    lines = section_text.split("\n")
    for line in lines:
        # Simple pattern: Role at Company (Years)
        match = re.match(r'(.+) at (.+) \((\d+)', line)
        if match:
            role, company, years = match.groups()
            exp_list.append({"role": role.strip(), "company": company.strip(), "years": int(years)})
    return exp_list

def parse_cv(text):
    cv_json = {
        "name": extract_name(text),
        "contact": {"email": "", "phone": ""},
        "last_position": "",
        "skills": [],
        "experience": []
    }

    # Skills
    skills_text = find_section(text, section_map["skills"])
    cv_json["skills"] = parse_skills(skills_text)

    # Experience
    exp_text = find_section(text, section_map["experience"])
    cv_json["experience"] = parse_experience(exp_text)

    if cv_json["experience"]:
        cv_json["last_position"] = cv_json["experience"][0]["role"]

    # Extract email/phone
    email_match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    phone_match = re.search(r'\+?\d[\d -]{7,}\d', text)
    cv_json["contact"]["email"] = email_match.group(0) if email_match else ""
    cv_json["contact"]["phone"] = phone_match.group(0) if phone_match else ""

    return cv_json

# -------------------------
# Endpoint: upload CV
# -------------------------
@app.route("/upload-cv", methods=["POST"])
def upload_cv():
    if "file" not in request.files:
        return jsonify({"status": "error", "message": "No file uploaded"}), 400
    file = request.files["file"]
    text = extract_text(file)
    if not text:
        return jsonify({"status": "error", "message": "Cannot extract text from file"}), 400

    cv_json = parse_cv(text)

    # Save CV JSON
    with open("cv.json", "w") as f:
        json.dump(cv_json, f, indent=2)

    return jsonify({"status": "success", "cv": cv_json})

# -------------------------
# Question-answer endpoint
# -------------------------
question_map = {
    "last_position": ["last job", "last position", "previous role", "recent job"],
    "skills": ["skills", "technologies", "expertise"],
    "email": ["email", "contact email"],
    "phone": ["phone", "contact number"]
}

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question", "").lower()
    answer = "Sorry, I don't know the answer."

    try:
        with open("cv.json") as f:
            cv = json.load(f)
    except FileNotFoundError:
        return jsonify({"answer": "No CV uploaded yet."})

    for key, phrases in question_map.items():
        for phrase in phrases:
            if fuzz.partial_ratio(question, phrase) > 60:  # lowered threshold for better matching
                answer = cv.get(key) if key != "skills" else cv.get(key, [])
                break

    return jsonify({"answer": answer})

# -------------------------
# Send email endpoint (Mailtrap)
# -------------------------
@app.route("/send-email", methods=["POST"])
def send_email():
    try:
        with open("cv.json") as f:
            cv = json.load(f)
    except FileNotFoundError:
        return jsonify({"status": "error", "message": "No CV uploaded yet"}), 400

    recipient = request.json.get("recipient") or app.config['MAIL_USERNAME']
    subject = request.json.get("subject") or "CV Summary from MCP Server"

    body = f"""
Name: {cv.get('name','N/A')}
Last Position: {cv.get('last_position','N/A')}
Skills: {', '.join(cv.get('skills', []))}
Email: {cv.get('contact', {}).get('email','N/A')}
Phone: {cv.get('contact', {}).get('phone','N/A')}
"""

    try:
        msg = Message(subject=subject,
                      sender=app.config['MAIL_USERNAME'],
                      recipients=[recipient],
                      body=body)
        mail.send(msg)
        return jsonify({"status": "success", "message": f"Email sent to {recipient}"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# -------------------------
# Run the server
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)
