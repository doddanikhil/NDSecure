import React, { useState } from 'react';
import { Form, Button, Alert, Spinner } from 'react-bootstrap';
import { createNote } from '../services/note';
import '../styles/HackerTheme.css';

function CreateNote() {
  const [content, setContent] = useState('');
  const [expiresIn, setExpiresIn] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      await createNote(content, expiresIn, password);
      setSuccess(true);
      setContent('');
      setExpiresIn('');
      setPassword('');
    } catch (err) {
      setError('Failed to create note. Please try again.');
    }
    setLoading(false);
  };

  return (
    <div className="hacker-container">
      <h2 className="hacker-text">Create a Secure Note</h2>
      {error && <Alert variant="danger" className="hacker-alert">{error}</Alert>}
      {success && <Alert variant="success" className="hacker-alert">Note created successfully!</Alert>}
      <Form onSubmit={handleSubmit} className="hacker-form">
        <Form.Group>
          <Form.Label className="hacker-label">Note Content</Form.Label>
          <Form.Control 
            as="textarea" 
            rows={3} 
            value={content}
            onChange={(e) => setContent(e.target.value)}
            required
            className="hacker-input"
          />
        </Form.Group>
        <Form.Group>
          <Form.Label className="hacker-label">Expires In (hours)</Form.Label>
          <Form.Control 
            type="number" 
            value={expiresIn}
            onChange={(e) => setExpiresIn(e.target.value)}
            className="hacker-input"
          />
        </Form.Group>
        <Form.Group>
          <Form.Label className="hacker-label">Password (optional)</Form.Label>
          <Form.Control 
            type="password" 
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="hacker-input"
          />
        </Form.Group>
        <Button type="submit" disabled={loading} className="hacker-button">
          {loading ? <Spinner animation="border" size="sm" /> : 'Encrypt & Send'}
        </Button>
      </Form>
    </div>
  );
}

export default CreateNote;