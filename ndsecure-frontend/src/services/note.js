import axios from 'axios';
import { authHeader } from './auth';

const API_URL = 'http://localhost:8000/api/notes/';

export const createNote = (content, expiresIn, password) => {
  return axios.post(API_URL, { content, expires_in: expiresIn, password }, { headers: authHeader() });
};

export const getNotes = () => {
  return axios.get(API_URL, { headers: authHeader() });
};

export const getNote = (id, password) => {
  return axios.get(`${API_URL}${id}/`, {
    headers: authHeader(),
    params: { password }
  });
};