from django.shortcuts import render


def sheets(request):
	return render(request, 'history/sheets.html')
