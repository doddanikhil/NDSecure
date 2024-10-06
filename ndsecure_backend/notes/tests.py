from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Note
from django.utils import timezone
import datetime

class NoteAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.force_authenticate(user=self.user)

    def test_create_note(self):
        data = {'content': 'Test note content'}
        response = self.client.post('/api/notes/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Note.objects.count(), 1)
        note = Note.objects.get()
        self.assertEqual(note.created_by, self.user)

    def test_retrieve_note(self):
        note = Note.objects.create(content='Test note', created_by=self.user)
        response = self.client.get(f'/api/notes/{note.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('content', response.data)

    def test_list_notes(self):
        Note.objects.create(content='Test note 1', created_by=self.user)
        Note.objects.create(content='Test note 2', created_by=self.user)
        response = self.client.get('/api/notes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_note_expiration(self):
        expired_note = Note.objects.create(
            content='Expired note',
            created_by=self.user,
            expires_at=timezone.now() - datetime.timedelta(hours=1)
        )
        response = self.client.get(f'/api/notes/{expired_note.id}/')
        self.assertEqual(response.status_code, status.HTTP_410_GONE)

    def test_note_password_protection(self):
        note = Note.objects.create(content='Protected note', created_by=self.user, password='secret')
        response = self.client.get(f'/api/notes/{note.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        response = self.client.get(f'/api/notes/{note.id}/?password=secret')
        self.assertEqual(response.status_code, status.HTTP_200_OK)