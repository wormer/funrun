from django.db import models


class Match(models.Model):
	date = models.DateTimeField()


class Player(models.Model):
	name = models.CharField(max_length=254, unique=True)


class Participation(models.Model):
	match = models.ForeignKey(Match)
	player = models.ForeignKey(Player)
	victories = models.PositiveSmallIntegerField()

	class Meta:
		unique_together = 'match', 'player'


class Place(models.Model):
	participation = models.ForeignKey(Participation, unique=True)
	number = models.PositiveSmallIntegerField()


class RaisingRates(models.Model):
	participation = models.ForeignKey(Participation, unique=True)
	count = models.PositiveSmallIntegerField()


class Sheet(models.Model):
	photo = models.ImageField(upload_to='history/facts/', null=True, blank=True)
	rows = models.PositiveSmallIntegerField(null=True, blank=True)
	columns = models.PositiveSmallIntegerField(null=True, blank=True)
	matches = models.ManyToManyField(Match)
