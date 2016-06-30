from django.db import models
from django.shortcuts import render, get_object_or_404

from .models import Sheet

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
	sheet = get_object_or_404(Sheet, id=sheet_id)
	return render(request, 'history/sheet.html', context={'sheet': sheet})
