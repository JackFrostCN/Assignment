# MCP Server  

A simple Flask-based microservice for **CV parsing, Q&A, and email sending**.  

## 🚀 Features
- Upload CVs (`.pdf` / `.docx`)  
- Extract **name, contact, skills, experience**  
- Ask natural questions (e.g., *“What is the last job?”*)  
- Send CV summary via **Mailtrap email**  

## ⚙️ Setup
```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
pip install -r requirements.txt
python mcp_server.py
````

Server runs at: `http://127.0.0.1:5000`

## 📡 Endpoints

* **POST /upload-cv** → upload and parse CV
* **POST /ask** → ask questions about CV
* **POST /send-email** → send summary via email
