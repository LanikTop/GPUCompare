from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

MANUFACTURER_CHOICES = [
    ('NVIDIA', 'NVIDIA'),
    ('AMD', 'AMD'),
    ('Intel', 'Intel'),
]

RESOLUTION_CHOICES = [
    ('1920x1080', '1920x1080 (Full HD)'),
    ('2560x1440', '2560x1440 (2K/QHD)'),
    ('3440x1440', '3440x1440 (UltraWide2K/UWQHD)'),
    ('3840x2160', '3840x2160 (4K/UHD)'),
]

SETTINGS_CHOICES = [
    ('low', 'Низкие/low'),
    ('medium', 'Средние/medium'),
    ('high', 'Высокие/high'),
    ('ultra', 'Ультра/ultra'),
]


class Gpu(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название модели")
    manufacturer = models.CharField(
        max_length=10,
        choices=MANUFACTURER_CHOICES,
        verbose_name="Производитель")
    release_year = models.IntegerField(
        verbose_name="Год выпуска",
        validators=[MinValueValidator(2007), MaxValueValidator(2025)])
    memory_gb = models.IntegerField(verbose_name="Объем памяти (ГБ)")
    memory_type = models.CharField(max_length=10, verbose_name="Тип памяти", default='GDDR6')
    # TODO Тепловыделение (TDP) tdp_w
    price_rub = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Средняя цена (руб)")
    image_url = models.URLField(blank=True, verbose_name="Ссылка на изображение")
    slug = models.SlugField(max_length=200, verbose_name="URL")

    # TODO fps/rub; fps/w; methods
    def fps_per_ruble(self, avg_fps):
        if self.price_rub and avg_fps:
            return round((avg_fps / float(str(self.price_rub)) * 100) * 1000, 2)
        return 0

    class Meta:
        db_table = "Gpu"
        ordering = ['-release_year', '-name']
        verbose_name = "Видеокарта"
        verbose_name_plural = "Видеокарты"
        indexes = [models.Index(fields=['price_rub']),
                   models.Index(fields=['name']), ]


class Game(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    release_year = models.IntegerField(
        verbose_name="Год выхода",
        validators=[MinValueValidator(1990), MaxValueValidator(2024)])
    slug = models.SlugField(max_length=200, unique=True, verbose_name="URL")

    def __str__(self):
        return f"{self.title} ({self.release_year})"

    class Meta:
        db_table = "Game"
        verbose_name = "Игра"
        verbose_name_plural = "Игры"
        ordering = ['title']
        indexes = [models.Index(fields=['title']), ]


class PerformanceData(models.Model):
    gpu = models.ForeignKey(
        Gpu,
        on_delete=models.CASCADE,
        related_name='performance_data',
        verbose_name="Видеокарта")
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name='performance_data',
        verbose_name="Игра")
    resolution = models.CharField(
        max_length=20,
        choices=RESOLUTION_CHOICES,
        default='1920x1080',
        verbose_name="Разрешение")
    graphics_settings = models.CharField(
        max_length=20,
        choices=SETTINGS_CHOICES,
        default='medium',
        verbose_name="Настройки графики")
    avg_fps = models.FloatField(
        verbose_name="Средний FPS",
        validators=[MinValueValidator(0)])

    # TODO methods

    class Meta:
        db_table = "PerformanceData"
        verbose_name = "Тест производительности"
        verbose_name_plural = "Тесты производительности"
        ordering = ['-avg_fps']
        unique_together = ['gpu', 'game', 'resolution', 'graphics_settings']
        indexes = [
            models.Index(fields=['gpu', 'game']),
            models.Index(fields=['resolution', 'graphics_settings'])]
