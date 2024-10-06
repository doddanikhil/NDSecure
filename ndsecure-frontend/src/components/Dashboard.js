import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Card, Button, Alert } from 'react-bootstrap';
import { getNotes } from '../services/note';

function Dashboard() {
  const [notes, setNotes] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchNotes();
  }, []);

  const fetchNotes = async () => {
    try {
      const response = await getNotes();
      setNotes(response.data);
    } catch (err) {
      setError('Failed to fetch notes');
    }
  };

  return (
    <div>
      <h2>Your Notes</h2>
      {error && <Alert variant="danger">{error}</Alert>}
      {notes.map(note => (
        <Card key={note.id} className="mb-3">
          <Card.Body>
            <Card.Title>Note {note.id}</Card.Title>
            <Card.Text>Created at: {new Date(note.created_at).toLocaleString()}</Card.Text>
            <Link to={`/view/${note.id}`}>
              <Button variant="primary">View Note</Button>
            </Link>
          </Card.Body>
        </Card>
      ))}
      <Link to="/create">
        <Button variant="success">Create New Note</Button>
      </Link>
    </div>
  );
}

export default Dashboard;