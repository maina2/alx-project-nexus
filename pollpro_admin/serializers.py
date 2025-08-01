# pollpro_backend/pollpro_admin/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from polls.models import Poll, Vote, Option
from polls.serializers import OptionSerializer, PollSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_staff', 'is_active', 'date_joined')

    def update(self, instance, validated_data):
        # Update user fields, ensuring password is not included
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.is_staff = validated_data.get('is_staff', instance.is_staff)
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