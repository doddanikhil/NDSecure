from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Note
from django.utils import timezone

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user

class NoteSerializer(serializers.ModelSerializer):
    expires_in = serializers.IntegerField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)
    is_expired = serializers.SerializerMethodField()

    class Meta:
        model = Note
        fields = ['id', 'content', 'created_at', 'expires_at', 'has_been_read', 'expires_in', 'password', 'is_expired']
        read_only_fields = ['id', 'created_at', 'has_been_read', 'expires_at', 'is_expired']

    def get_is_expired(self, obj):
        return obj.is_expired()

    def create(self, validated_data):
        expires_in = validated_data.pop('expires_in', None)
        if expires_in:
            validated_data['expires_at'] = timezone.now() + timezone.timedelta(hours=expires_in)
        
        password = validated_data.pop('password', None)
        if password:
            # The actual password hashing will be done in the view
            validated_data['password'] = password
        
        return super().create(validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Remove content from the representation if the note has been read or is expired
        if instance.has_been_read or instance.is_expired():
            representation.pop('content', None)
        return representation