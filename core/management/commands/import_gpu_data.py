import json
import re
from pathlib import Path

from django.core.management.base import BaseCommand
from django.utils.text import slugify

from core.models import Gpu, Game, PerformanceData

DOLLAR_TO_RUBLE = 78.23

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
        }
        self.stdout.write(f"Processing GPUs")
        performance_list = []
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
                                         price_rub=self.extract_price_regex(gpu_price) * DOLLAR_TO_RUBLE,
                                         slug=slugify(gpu_name))
            stats['gpus_created'] += 1
            for settings, resolutions in row['Settings'].items():
                for resolution, games in resolutions['Resolution'].items():
                    for game in games['Games']:
                        game_name = game['Game_Name']
                        release_year = game['Release_Date']
                        avg_fps = game['Avg_FPS'].replace(',', '')

                        new_game, created = Game.objects.get_or_create(title=game_name,
                                                                       release_year=release_year,
                                                                       slug=slugify(game_name))
                        if created:
                            self.stdout.write(f"Created game: {game_name}")
                            stats['games_created'] += 1
                        performance_list.append(PerformanceData(gpu=new_gpu,
                                                                game=new_game,
                                                                resolution=resolution,
                                                                graphics_settings=settings,
                                                                avg_fps=avg_fps))
                        stats['performance_created'] += 1

        PerformanceData.objects.bulk_create(performance_list, batch_size=1000)
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

    @staticmethod
    def extract_price_regex(price_str):
        cleaned = re.sub(r'[^\d.,]', '', price_str)
        if ',' in cleaned and '.' in cleaned:
            cleaned = cleaned.replace(',', '')
        elif ',' in cleaned and cleaned.count(',') == 1:
            comma_pos = cleaned.find(',')
            if len(cleaned) - comma_pos <= 3:
                cleaned = cleaned.replace(',', '.')
            else:
                cleaned = cleaned.replace(',', '')
        try:
            return float(cleaned)
        except ValueError:
            return 0
