from django.contrib import admin

from .models import Player, Match, Round, Leave


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
	list_display = 'name',


class RoundInline(admin.TabularInline):
	model = Round


class LeaveInline(admin.TabularInline):
	model = Leave


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
	list_display = '__str__', 'start_time'
	inlines = RoundInline, LeaveInline
