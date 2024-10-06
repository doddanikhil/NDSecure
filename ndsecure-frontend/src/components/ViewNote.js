import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Alert, Spinner, Form, Button } from 'react-bootstrap';
import axios from 'axios';
import { getCurrentUser } from '../services/auth';

function ViewNote() {
  const [note, setNote] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);
  const [password, setPassword] = useState('');
  const { id } = useParams();

  const fetchNote = async (notePassword = '') => {
    try {
      const user = getCurrentUser();
      const response = await axios.get(`http://localhost:8000/api/notes/${id}/`, {
        headers: { Authorization: `Token ${user.token}` },
        params: { password: notePassword }
      });
      setNote(response.data.content);
      setLoading(false);
      setError('');
    } catch (error) {
      setError(error.response?.data?.error || 'Failed to fetch note');
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchNote();
  }, [id]);

  const handlePasswordSubmit = (e) => {
    e.preventDefault();
    fetchNote(password);
  };

  if (loading) {
    return <Spinner animation="border" />;
  }

  if (error === 'Invalid password') {
    return (
      <div>
        <h1>Secure Note</h1>
        <Alert variant="warning">This note is password protected</Alert>
        <Form onSubmit={handlePasswordSubmit}>
          <Form.Group className="mb-3">
            <Form.Label>Password</Form.Label>
            <Form.Control
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter note password"
            />
          </Form.Group>
          <Button variant="primary" type="submit">
            Submit
          </Button>
        </Form>
      </div>
    );
  }

  return (
    <div>
      <h1>Secure Note</h1>
      {error ? (
        <Alert variant="danger">{error}</Alert>
      ) : (
        <>
          <Alert variant="info">
            <p>{note}</p>
          </Alert>
          <Alert variant="warning">
            This note will be destroyed after you close this page.
          </Alert>
        </>
      )}
    </div>
  );
}

export default ViewNote;