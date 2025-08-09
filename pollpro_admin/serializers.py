# pollpro_backend/pollpro_admin/serializers.py
from rest_framework import serializers
from users.models import CustomUser  # Updated from django.contrib.auth.models
from polls.models import Poll, Vote, Option
from polls.serializers import OptionSerializer, PollSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser  # Updated to CustomUser
        fields = ('id', 'username', 'email', 'roles', 'is_active', 'date_joined')  # Replaced is_staff with roles

    def update(self, instance, validated_data):
        # Update user fields, ensuring password is not included
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.roles = validated_data.get('roles', instance.roles)  # Updated to roles
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance

class AdminPollSerializer(PollSerializer):
    class Meta(PollSerializer.Meta):
        fields = ('id', 'question', 'creator', 'category', 'created_at', 'expiry_date', 'options')

class VoteSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    poll = serializers.StringRelatedField()
    option = serializers.StringRelatedField()

    class Meta:
        model = Vote
        fields = ('id', 'user', 'poll', 'option', 'created_at')
        ref_name = 'AdminVoteSerializer'  # Unique ref_name for admin app