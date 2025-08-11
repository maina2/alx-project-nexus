from rest_framework import serializers
from users.models import CustomUser
from polls.models import Poll, Vote, Option
from polls.serializers import OptionSerializer, PollSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'roles', 'is_active', 'date_joined')
        ref_name = 'AdminUserSerializer' # Added to resolve naming conflict

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.roles = validated_data.get('roles', instance.roles)
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
        ref_name = 'AdminVoteSerializer'