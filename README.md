# MCP CV System  

A full-stack project for **CV parsing, Q&A, and email sending**.  
It consists of:  

1. **MCP Server (Backend)** – A Flask microservice to parse CVs (PDF/DOCX), extract details, answer questions, and send CV summaries via email using Mailtrap.  
2. **MCP CV Frontend (React)** – A web interface to upload CVs, view parsed data, ask questions, and send emails.  

---

## 🚀 Features

- Upload CVs in PDF or DOCX format  
- Extract candidate details: name, contact info, skills, experience  
- Natural-language Q&A over CV data  
- Send CV summaries via email (Mailtrap sandbox)  
- Web interface with React for easy interaction  

---

## 📂 Project Structure

```

.
├── backend/
│   └── mcp\_server.py       # Flask backend server
├── frontend/
│   └── src/
│       └── App.js          # React frontend
├── README.md
└── requirements.txt        # Python dependencies

````

---

## ⚙️ Setup

### Backend (Flask)

```bash
cd backend
pip install -r ../requirements.txt
python mcp_server.py
````

Runs at: `http://127.0.0.1:5000`

### Frontend (React)

```bash
cd frontend
npm install
npm start
```

Runs at: `http://localhost:3000`
Make sure the backend is running for full functionality.

---

## 📡 API Endpoints

* **POST /upload-cv** – Upload and parse CV
* **POST /ask** – Ask a question about the CV
* **POST /send-email** – Send CV summary via email

---

## 📧 Mailtrap Setup

Update credentials in `backend/mcp_server.py`:

```python
app.config['MAIL_SERVER'] = 'sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = '<your-username>'
app.config['MAIL_PASSWORD'] = '<your-password>'
```

---

## 🛠️ Technologies Used

* **Backend:** Python, Flask, Flask-Mail, Flask-CORS, pdfplumber, python-docx, RapidFuzz
* **Frontend:** React, JavaScript, Axios, HTML, CSS

---

## 📜 License

MIT License

---

**GitHub Repo:** [https://github.com/JackFrostCN/Assignment](https://github.com/JackFrostCN/Assignment.git)

``` 

Do you want me to do that next?
```
