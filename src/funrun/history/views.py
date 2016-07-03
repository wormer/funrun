from django.db import models
from django.shortcuts import render, get_object_or_404

from .models import Sheet, Player

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
	from django.utils.safestring import mark_safe
	sheet = get_object_or_404(Sheet, id=sheet_id)
	players = list(Player.objects.order_by('id'))

	header = [mark_safe('&nbsp;')] + list(range(sheet.columns))

	data = []
	for player in players:
		victories = [player.name] + [choice('-012345') for _ in range(sheet.columns)]
		data.append(victories)

	rows = [(header, data)] * sheet.rows

	return render(request, 'history/sheet.html', context={
		'sheet': sheet,
		'rows': rows,
		'column_width': str(100/(sheet.columns+1)),
		'width': sheet.photo.width,
		'height': sheet.photo.height,
	})
