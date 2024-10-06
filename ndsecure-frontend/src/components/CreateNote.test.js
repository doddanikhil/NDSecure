import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import CreateNote from './CreateNote';
import { createNote } from '../services/note';

jest.mock('../services/note');

describe('CreateNote Component', () => {
  test('renders CreateNote component', () => {
    render(<CreateNote />);
    expect(screen.getByText('Create a Secure Note')).toBeInTheDocument();
  });

  test('submits form with note content', async () => {
    createNote.mockResolvedValue({ data: { id: '123' } });

    render(<CreateNote />);
    
    fireEvent.change(screen.getByPlaceholderText('Enter your secure note'), {
      target: { value: 'Test note content' },
    });
    
    fireEvent.click(screen.getByText('Create Note'));

    await waitFor(() => {
      expect(createNote).toHaveBeenCalledWith('Test note content', null, null);
      expect(screen.getByText('Note Created Successfully!')).toBeInTheDocument();
    });
  });
});