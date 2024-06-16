'use client';
import { useState, FormEvent } from 'react';
import axios from 'axios';
import './styles/page.css';

export default function Home() {
  const [text, setText] = useState<string>('');
  const [redactedText, setRedactedText] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await axios.post('http://127.0.0.1:5000/redact', { text });
      setRedactedText(response.data.redacted_text);
    } catch (error) {
      console.error('Error redacting text:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      {loading && <div className="loading-overlay"><div className="spinner"></div></div>}
      <h1 className="title">PHI Redaction System</h1>
      <form onSubmit={handleSubmit} className="form-container">
        <textarea
          className="textarea"
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Enter text to redact PHI"
        />
        <br />
        <button className="button" type="submit">Redact</button>
      </form>
      {redactedText && (
        <div className="redacted-text">
          <h2>Redacted Text</h2>
          <p>{redactedText}</p>
        </div>
      )}
    </div>
  );
}
