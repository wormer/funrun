from django.db import models
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .models import Sheet, Player, Match, Participation

def sheets(request):
	processed = (Sheet.objects
		.filter(matches__isnull=False)
		.annotate(
			from_date=models.Min('matches__date'),
			to_date=models.Max('matches__date')
		)
		.order_by('from_date')
	)
	raw = (Sheet.objects
		.filter(matches__isnull=True)
		.order_by('id')
	)
	return render(request, 'history/sheets.html', context={'processed': processed, 'raw': raw})


def sheet(request, sheet_id):
	from random import choice
	sheet = get_object_or_404(Sheet, id=sheet_id)
	players = list(Player.objects.order_by('id'))
	matches = Match.objects.filter(sheet=sheet).order_by('id')

	rows = []
	for start in range(0, sheet.columns*sheet.rows, sheet.columns):
		row_matches = matches[start:start+sheet.columns]
		header = ['']
		header.extend(timezone.make_naive(match.date).strftime('%d.%m') for match in row_matches)

		data = []
		for player in players:
			victories = [player.name]
			for match in row_matches:
				participation = Participation.objects.filter(player__name=player.name, match=match)
				value = '-'
				if participation.exists():
					v = participation.get().victories
					value = v and '+' * v
				victories.append(value)
			data.append(victories)

		rows.append((header, data))

	return render(request, 'history/sheet.html', context={
		'sheet': sheet,
		'rows': rows,
		'column_width': str(100/(sheet.columns+1)),
		'width': sheet.photo.width,
		'height': sheet.photo.height,
	})
