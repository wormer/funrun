from django.core.urlresolvers import reverse
from django.db import models, connection


class Player(models.Model):
	name = models.CharField('Имя', max_length=255)

	class Meta:
		verbose_name = 'Игрок'
		verbose_name_plural = 'Игроки'
		ordering = 'name',

	def __str__(self):
		return self.name

	def get_place1_number(self):
		return self.leave_set.filter(place=1).count()

	def get_place2_number(self):
		return self.leave_set.filter(place=2).count()

	def get_place3_number(self):
		return self.leave_set.filter(place=3).count()


class Match(models.Model):
	players = models.ManyToManyField(Player, verbose_name='Игроки')
	start_time = models.DateTimeField('Время начала', auto_now_add=True)
	end_time = models.DateTimeField('Время окончания', null=True, blank=True)

	class Meta:
		verbose_name = 'Матч'
		verbose_name_plural = 'Матчи'
		ordering = '-start_time',

	def __str__(self):
		return 'Матч %d' % self.pk

	def get_absolute_url(self):
		return reverse('funrun.match.views.match', args=[self.pk])

	def get_stats(self, exclude_winners=False):
		sql = 'SELECT p.id, p.name, (SELECT count(*) FROM match_round r WHERE r.match_id=m.match_id AND r.winner_id=p.id) AS wins, l.place FROM match_player p JOIN match_match_players m ON m.player_id=p.id AND m.match_id=%s LEFT JOIN match_leave l ON l.match_id=m.match_id AND l.player_id=p.id'
		if exclude_winners:
			sql += ' WHERE l.id IS NULL'
		sql += ' ORDER BY p.name'
		cursor = connection.cursor()
		cursor.execute(sql, [self.id])
		return cursor.fetchall()

class Round(models.Model):
	match = models.ForeignKey(Match, verbose_name='Матч')
	start_time = models.DateTimeField('Время начала', auto_now_add=True)
	end_time = models.DateTimeField('Время окончания', null=True, blank=True)
	winner = models.ForeignKey(Player, verbose_name='Победитель', null=True, blank=True)

	class Meta:
		verbose_name = 'Раунд'
		verbose_name_plural = 'Раунды'
		ordering = '-start_time',

	def __str__(self):
		return 'Матч %d раунд %d' % (self.match_id, self.get_number())

	def get_number(self):
		return self.match.round_set.filter(start_time__lt=self.start_time).count() + 1


class Leave(models.Model):
	time = models.DateTimeField('Время', auto_now_add=True)
	match = models.ForeignKey(Match, verbose_name='Матч')
	player = models.ForeignKey(Player, verbose_name='Игрок')
	place = models.PositiveSmallIntegerField(u'Место')

	class Meta:
		verbose_name = 'Выход'
		verbose_name_plural = 'Выходы'
		ordering = 'place',

	def __str__(self):
		if self.place > 0:
			return '%s получил %d место в матче %d' % (self.player, self.place, self.match_id)
		else:
			return '%s вышел из матча %d' % (self.player, self.match_id)
