# MCP Server for CV

A full-stack application for parsing CVs, answering questions, and sending summaries via email. This project includes:

1. **Backend (Flask)**: A microservice to parse CVs (PDF/DOCX), extract details, answer questions, and send summaries via email using Mailtrap.
2. **Frontend (React)**: A web interface to upload CVs, view parsed data, ask questions, and send emails.

---

## 🚀 Features

* Upload CVs in PDF or DOCX format
* Extract candidate details: name, contact info, skills, experience
* Natural-language Q\&A over CV data
* Send CV summaries via email (Mailtrap sandbox)
* Web interface with React for easy interaction

---

## 📂 Project Structure

```
.
├── backend/
│   └── mcp_server.py       # Flask backend server
├── frontend/
│   └── src/
│       └── App.js          # React frontend
├── README.md
└── requirements.txt        # Python dependencies
```

---

## ⚙️ Setup

### Backend (Flask)

```bash
cd backend
pip install -r ../requirements.txt
python mcp_server.py
```

Runs at: `http://127.0.0.1:5000`

### Frontend (React)

```bash
cd frontend
npm install
npm start
```

Runs at: `http://localhost:3000`
Ensure the backend is running for full functionality.

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

Feel free to copy and paste this into your `README.md` file. If you need further customization or additional sections, let me know!
