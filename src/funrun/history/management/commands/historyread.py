from datetime import date, datetime
from io import BytesIO
from pathlib import Path

from django.core.management.base import BaseCommand
from django.db import transaction
from django.core.files.base import ContentFile
from django.utils import timezone
from PIL import Image
import pytz
from ruamel import yaml

from ...models import Sheet, Match, Player, Participation, Place, RaisingRates


class Command(BaseCommand):
	help = 'Read history sheets'

	def add_arguments(self, parser):
		parser.add_argument('path', nargs='+', type=str)

	def handle(self, *args, **options):
		current_timezone = pytz.timezone('Asia/Novosibirsk')
		for path_string in options['path']:
			path = Path(path_string).resolve()
			with transaction.atomic(), path.open('rb') as source:
				sheet = Sheet()
				sheet.save()
				previous_date = date.min
				matches = 0
				for data in yaml.load(source):
					if 'sheet' in data:
						sheet.rows = data['sheet']['rows']
						sheet.columns = data['sheet']['columns']
						sheet.save()
					elif 'players' in data:
						for player_name in data['players']:
							Player.objects.get_or_create(name=player_name)
					elif {'date', 'victories', 'places'} <= data.keys():
						assert previous_date <= data['date'], 'Previous date %r is greater then present %r' % (previous_date, data['date'])
						previous_date = data['date']
						match = Match.objects.create(
							date=timezone.make_aware(datetime(*data['date'].timetuple()[:3], hour=12), current_timezone)
						)
						sheet.matches.add(match)
						matches += 1
						max_score = max(data['victories'].values())
						raisingrates = data.get('raised', {'by': None, 'from': -1})
						for player_name, count in data['victories'].items():
							player = Player.objects.get(name=player_name)
							participation = Participation.objects.create(match=match, player=player, victories=count)
							if player_name in data['places']:
								assert max_score == count, 'Player %r is medalist, but his victories number %r is less then max %r in data %r' % (player_name, count, max_score, data)
								Place.objects.create(participation=participation, number=data['places'].index(player_name)+1)
							if player_name == raisingrates['by']:
								RaisingRates.objects.create(participation=participation, count=raisingrates['from'])

					elif 'photo_fact' in data:
						format = Image.open(BytesIO(data['photo_fact'])).format
						sheet.photo.save(name='%d.%s'%(sheet.id, format.lower()), content=ContentFile(data['photo_fact']))
					else:
						raise ValueError('data "%r" is not supported.'%data)

				assert matches <= sheet.rows * sheet.columns, 'Matrix of sheet %dx%d can not fit %d matches' % (sheet.columns, sheet.rows, matches)
