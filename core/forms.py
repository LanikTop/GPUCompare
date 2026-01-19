# core/forms.py
from django import forms
from .models import Game

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

class ComparisonForm(forms.Form):
    game = forms.ModelChoiceField(
        queryset=Game.objects.all().order_by('title'),
        label="Игра",
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Выберите игру",
        to_field_name='slug'
    )
    resolution = forms.ChoiceField(
        choices=RESOLUTION_CHOICES,
        label="Разрешение",
        initial='1920x1080',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    settings = forms.ChoiceField(
        choices=SETTINGS_CHOICES,
        label="Настройки графики",
        initial='medium',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    min_fps = forms.IntegerField(
        label="Минимальный FPS",
        initial=30,
        min_value=1,
        max_value=1000,
    )