import { useState } from "react";
import axios from "axios";

function App() {
  const [file, setFile] = useState(null);
  const [cvData, setCvData] = useState(null);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [emailStatus, setEmailStatus] = useState("");

  const handleUpload = async () => {
    if (!file) return;
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post("http://127.0.0.1:5000/upload-cv", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setCvData(res.data.cv);
      setAnswer("");
      setEmailStatus("");
    } catch (err) {
      console.error(err);
      alert("Failed to upload CV");
    }
  };

  const handleAsk = async () => {
    if (!question) return;
    try {
      const res = await axios.post("http://127.0.0.1:5000/ask", { question });
      setAnswer(res.data.answer);
    } catch (err) {
      console.error(err);
      alert("Failed to ask question");
    }
  };

  const handleSendEmail = async () => {
    try {
      const res = await axios.post("http://127.0.0.1:5000/send-email", {});
      setEmailStatus(res.data.message);
    } catch (err) {
      console.error(err);
      setEmailStatus("Failed to send email");
    }
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial, sans-serif" }}>
      <h1>MCP CV Demo</h1>

      {/* Upload CV */}
      <div style={{ marginBottom: "2rem" }}>
        <h2>1. Upload CV (PDF or Word)</h2>
        <input type="file" onChange={(e) => setFile(e.target.files[0])} />
        <button onClick={handleUpload} style={{ marginLeft: "1rem" }}>Upload</button>
      </div>

      {/* Show parsed CV */}
      {cvData && (
        <div style={{ marginBottom: "2rem" }}>
          <h2>Parsed CV JSON</h2>
          <pre style={{ background: "#f0f0f0", padding: "1rem" }}>{JSON.stringify(cvData, null, 2)}</pre>
        </div>
      )}

      {/* Ask question */}
      {cvData && (
        <div style={{ marginBottom: "2rem" }}>
          <h2>2. Ask a Question</h2>
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Type your question..."
            style={{ width: "300px" }}
          />
          <button onClick={handleAsk} style={{ marginLeft: "1rem" }}>Ask</button>
          {answer && <div style={{ marginTop: "1rem" }}><strong>Answer:</strong> {JSON.stringify(answer)}</div>}
        </div>
      )}

      {/* Send email */}
      {cvData && (
        <div style={{ marginBottom: "2rem" }}>
          <h2>3. Send CV Summary Email (Mailtrap)</h2>
          <button onClick={handleSendEmail}>Send Email</button>
          {emailStatus && <div style={{ marginTop: "1rem" }}>{emailStatus}</div>}
        </div>
      )}
    </div>
  );
}

export default App;
