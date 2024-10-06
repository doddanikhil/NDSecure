from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings
from .models import Note, AuditLog
from .serializers import NoteSerializer, UserSerializer
from cryptography.fernet import Fernet, InvalidToken
import os

# Initialize Fernet
fernet = Fernet(settings.ENCRYPTION_KEY.encode())

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer
    throttle_classes = [AnonRateThrottle]

    def perform_create(self, serializer):
        user = serializer.save()
        Token.objects.create(user=user)

class CustomObtainAuthToken(ObtainAuthToken):
    throttle_classes = [AnonRateThrottle]

    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'user_id': token.user_id})

class NoteListCreate(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get_queryset(self):
        return Note.objects.filter(created_by=self.request.user, expires_at__gt=timezone.now())

    def perform_create(self, serializer):
        content = self.request.data.get('content')
        password = self.request.data.get('password')
        expires_in = self.request.data.get('expires_in')
        
        encrypted_content = fernet.encrypt(content.encode()).decode()
        
        if password:
            hashed_password = make_password(password)
        else:
            hashed_password = None

        expires_at = None
        if expires_in:
            expires_at = timezone.now() + timezone.timedelta(hours=int(expires_in))
        
        note = serializer.save(
            content=encrypted_content,
            created_by=self.request.user,
            password=hashed_password,
            expires_at=expires_at
        )
        
        AuditLog.objects.create(
            action='create_note',
            note=note,
            user=self.request.user,
            ip_address=self.get_client_ip(self.request)
        )

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

class NoteRetrieveDestroy(generics.RetrieveDestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def retrieve(self, request, *args, **kwargs):
        try:
            note = self.get_object()
            
            if note.is_expired():
                return Response({"error": "Note has expired"}, status=status.HTTP_410_GONE)
            
            if note.has_been_read:
                return Response({"error": "Note has already been read"}, status=status.HTTP_410_GONE)
            
            if note.password:
                provided_password = request.query_params.get('password')
                if not provided_password or not check_password(provided_password, note.password):
                    return Response({"error": "Invalid password"}, status=status.HTTP_403_FORBIDDEN)
            
            decrypted_content = fernet.decrypt(note.content.encode()).decode()
            note.has_been_read = True
            note.save()

            AuditLog.objects.create(
                action='read_note',
                note=note,
                user=request.user,
                ip_address=self.get_client_ip(request)
            )

            return Response({"content": decrypted_content})
        except ObjectDoesNotExist:
            return Response({"error": "Note not found"}, status=status.HTTP_404_NOT_FOUND)
        except InvalidToken:
            return Response({"error": "Unable to decrypt note"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        note = self.get_object()
        if note.created_by != request.user:
            return Response({"error": "You don't have permission to delete this note"}, status=status.HTTP_403_FORBIDDEN)
        
        AuditLog.objects.create(
            action='delete_note',
            note=note,
            user=request.user,
            ip_address=self.get_client_ip(request)
        )
        
        return super().destroy(request, *args, **kwargs)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip