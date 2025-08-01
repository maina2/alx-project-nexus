# pollpro_backend/polls/serializers.py
from rest_framework import serializers
from .models import Poll, Option, Vote
from django.utils import timezone

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ('id', 'text')

class PollSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)
    creator = serializers.StringRelatedField()
    category = serializers.ChoiceField(choices=Poll.CATEGORY_CHOICES, read_only=True)
    user_vote = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Poll
        fields = ('id', 'question', 'creator', 'category', 'created_at', 'expiry_date', 'options', 'user_vote')

    def get_user_vote(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            try:
                vote = obj.votes.get(user=user)
                return OptionSerializer(vote.option).data
            except Vote.DoesNotExist:
                return None
        return None

class PollCreateSerializer(serializers.ModelSerializer):
    options = serializers.ListField(child=serializers.CharField(), write_only=True)
    category = serializers.ChoiceField(choices=Poll.CATEGORY_CHOICES, write_only=True)

    class Meta:
        model = Poll
        fields = ('question', 'category', 'expiry_date', 'options')

    def create(self, validated_data):
        options_data = validated_data.pop('options')
        poll = Poll.objects.create(creator=self.context['request'].user, **validated_data)
        for option_text in options_data:
            Option.objects.create(poll=poll, text=option_text)
        return poll

    def validate_options(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Poll must have at least 2 options.")
        return value

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ('option',)
        ref_name = 'PollsVoteSerializer'  # Unique ref_name for polls app

    def validate_option(self, value):
        if value.poll != self.context['poll']:
            raise serializers.ValidationError("Option does not belong to this poll.")
        if not value.poll.is_active():
            raise serializers.ValidationError("Poll is expired.")
        return value

class PollResultSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()

    class Meta:
        model = Poll
        fields = ('id', 'question', 'options')

    def get_options(self, obj):
        total_votes = obj.votes.count()
        options = obj.options.all()
        return [
            {
                'id': option.id,
                'text': option.text,
                'votes': option.votes.count(),
                'percentage': (option.votes.count() / total_votes * 100) if total_votes > 0 else 0
            } for option in options
        ]