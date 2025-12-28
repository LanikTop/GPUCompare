import json
from pathlib import Path
from django.core.management.base import BaseCommand
from django.core import serializers
from core.models import Gpu, Game, PerformanceData


class Command(BaseCommand):
    help = 'Export database data to Django fixtures'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output',
            type=str,
            default='core/fixtures/initial_data.json',
            help='Output file path for fixtures'
        )

    def handle(self, *args, **options):
        output_path = Path(options['output'])

        output_path.parent.mkdir(parents=True, exist_ok=True)

        self.stdout.write("Exporting data to fixtures...")

        gpus = Gpu.objects.all()
        games = Game.objects.all()
        performance = PerformanceData.objects.all()
        data = []

        data.extend(json.loads(serializers.serialize('json', gpus)))
        data.extend(json.loads(serializers.serialize('json', games)))
        data.extend(json.loads(serializers.serialize('json', performance)))

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        self.stdout.write(f"EXPORTED {len(data)} objects:")
        self.stdout.write(f"    GPUs: {gpus.count()}")
        self.stdout.write(f"    Games: {games.count()}")
        self.stdout.write(f"    Performance datas: {performance.count()}")
        self.stdout.write(f"Saved to: {output_path}")
        file_size = output_path.stat().st_size
        self.stdout.write(f"    File size: {file_size / 1024:.1f} KB")
        self.stdout.write(f"WRITE: python manage.py loaddata {output_path}")
