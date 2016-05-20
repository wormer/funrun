from django import forms
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.core.paginator import InvalidPage, EmptyPage, Paginator
from django.utils import timezone

from .models import Match


def paginate_list(request, queryset, per_page):
	try:
		page = int(request.GET.get('page', 1))
	except ValueError:
		page = 1
	paginator = Paginator(queryset, per_page)
	try:
		return paginator.page(page)
	except (EmptyPage, InvalidPage):
		return paginator.page(paginator.num_pages)


def index(request):
	matches = Match.objects.all()
	matches_page = paginate_list(request, matches, settings.MATCHES_PER_PAGE)
	return render(request, "match/index.html", {
		'page': matches_page,
	})


def start_match(request):
	match = Match.objects.create()
	return redirect(match)


class PlayersForm(forms.ModelForm):
	class Meta:
		model = Match
		fields = 'players',


def match(request, match_id):
	match = get_object_or_404(Match, id=match_id)
	players_form = None
	if match.end_time is None:
		players_form = PlayersForm(instance=match, data=request.POST or None)
		if request.method == 'POST':
			finish = request.POST.get('finish')
			update = request.POST.get('update')
			leave = request.POST.get('leave')
			if update and players_form.is_valid():
				players_form.save()
			if leave:
				player = match.players.get(id=leave)
				stats = match.get_stats(exclude_winners=True)
				max_wins = 0
				player_wins = 0
				for record in stats:
					if record[0] == player.id:
						player_wins = record[2]
					if record[2] > max_wins:
						max_wins = record[2]
				if player_wins == max_wins:
					place = match.leave_set.exclude(place=0).count() + 1
				else:
					place = 0
				match.leave_set.create(player=player, place=place)
				if len(match.get_stats(exclude_winners=True)) == 0:
					finish = True
			if finish:
				if match.players.count() < 2:
					match.delete()
					return redirect(index)
				else:
					match.end_time = timezone.now()
					match.save()
			return redirect(match)
	return render(request, "match/match.html", {
		'match': match,
		'players_form': players_form,
	})


def round(request, match_id):
	match = get_object_or_404(Match, id=match_id)
	if request.method == 'POST':
		round = request.POST.get('round')
		winner = request.POST.get('winner')
		current_round = match.round_set.first()
		if round == 'new':
			new_round = match.round_set.create()
			if match.round_set.filter(winner=None).count() > 1:
				match.round_set.filter(winner=None).exclude(id=new_round.id).delete()
		elif round == 'cancel':
			current_round.winner = None
			current_round.save()
		elif round == 'delete':
			current_round.delete()
		if winner:
			current_round.winner_id = winner
			current_round.end_time = timezone.now()
			current_round.save()
	return redirect(match)
