# pollpro_backend/polls/admin.py
from django.contrib import admin
from .models import Poll, Option, Vote

@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ('question', 'creator', 'category', 'created_at', 'expiry_date', 'is_active')
    list_filter = ('category', 'created_at', 'expiry_date')
    search_fields = ('question', 'creator__username')

@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('poll', 'text')
    list_filter = ('poll',)
    search_fields = ('text', 'poll__question')

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('poll', 'option', 'user', 'created_at')
    list_filter = ('poll', 'created_at')
    search_fields = ('user__username', 'option__text')