from django.contrib import admin
from django.db import models
from django.template.defaultfilters import date

from .models import Sheet, Match, Player, Participation, Place, RaisingRates


@admin.register(Sheet)
class SheetAdmin(admin.ModelAdmin):
	list_display = 'id', 'from_date', 'to_date',

	def get_queryset(self, request):
		queryset = super().get_queryset(request)
		return queryset.annotate(
			from_date=models.Min('matches__date'),
			to_date=models.Max('matches__date')
		)

	def from_date(self, obj):
		return date(obj.from_date)

	def to_date(self, obj):
		return date(obj.to_date)


class ParticipationInline(admin.TabularInline):
	model = Participation


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
	list_display = 'id', 'date',
	inlines = ParticipationInline,


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
	list_display = 'name',
