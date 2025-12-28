import json
import re
from pathlib import Path

from django.core.management.base import BaseCommand
from django.utils.text import slugify

from core.models import Gpu, Game, PerformanceData


class Command(BaseCommand):
    help = 'Import GPU performance data from JSON file to database'

    def add_arguments(self, parser):
        parser.add_argument(
            'json_file',
            type=str,
            help='Path to JSON file with GPU data(Kaggle)')
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before import')

    def handle(self, *args, **options):
        json_path = Path(options['json_file'])
        if not json_path.exists():
            self.stderr.write(f"File {json_path} not found!")
            return
        if options['clear']:
            self.stdout.write("Clearing existing data...")
            PerformanceData.objects.all().delete()
            Game.objects.all().delete()
            Gpu.objects.all().delete()
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        stats = {
            'gpus_created': 0,
            'games_created': 0,
            'performance_created': 0,
            'gpus_updated': 0,
            'games_updated': 0,
        }
        self.stdout.write(f"Processing GPUs")
        for row in data:
            gpu_name = row['Series']['Value'].strip()
            gpu_manufacturer = self.get_manufacturer(gpu_name)
            # TODO rubbles
            gpu_price = row['Price']['Value']
            gpu_year = row['Year']['Value']
            gpu_memory = ''.join(filter(str.isdigit, row['Memory']['Value']))
            gpu_memory = gpu_memory if gpu_memory else '0'
            self.stdout.write(f"Processing row: {gpu_name}")

            new_gpu = Gpu.objects.create(name=gpu_name,
                               manufacturer=gpu_manufacturer,
                               release_year=gpu_year,
                               memory_gb=gpu_memory,
                               price_rub=re.findall(r'\d+\.?\d*', gpu_price)[0],
                               slug=slugify(gpu_name))
            stats['gpus_created'] += 1

            for settings in row['Settings'].values():
                for resolution in settings['Resolution'].values():
                    for game in resolution['Games']:
                        game_name = game['Game_Name']
                        release_year = game['Release_Date']
                        avg_fps = game['Avg_FPS'].replace(',', '')

                        new_game, created = Game.objects.get_or_create(title=game_name,
                                              release_year=release_year,
                                              slug=slugify(game_name))
                        if created:
                            self.stdout.write(f"Created game: {game_name}")
                            stats['games_created'] += 1

                        PerformanceData.objects.create(gpu=new_gpu,
                                                         game=new_game,
                                                         resolution=resolution,
                                                         graphics_settings=settings,
                                                         avg_fps=avg_fps)
                        stats['performance_created'] += 1


        self.stdout.write(stats.__str__())

    @staticmethod
    def get_manufacturer(gpu_name):
        gpu_name_lower = gpu_name.lower()
        if 'nvidia' in gpu_name_lower or 'geforce' in gpu_name_lower or 'rtx' in gpu_name_lower or 'gtx' in gpu_name_lower:
            return 'NVIDIA'
        elif 'amd' in gpu_name_lower or 'radeon' in gpu_name_lower or 'rx' in gpu_name_lower:
            return 'AMD'
        elif 'intel' in gpu_name_lower or 'arc' in gpu_name_lower:
            return 'Intel'
        else:
            return 'NVIDIA'
