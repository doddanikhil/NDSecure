from django.urls import path
from .views import NoteListCreate, NoteRetrieveDestroy, RegisterView, CustomObtainAuthToken

urlpatterns = [
    path('notes/', NoteListCreate.as_view(), name='note-list-create'),
    path('notes/<uuid:pk>/', NoteRetrieveDestroy.as_view(), name='note-retrieve-destroy'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomObtainAuthToken.as_view(), name='login'),
]