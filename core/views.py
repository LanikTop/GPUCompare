from django.shortcuts import render
from django.shortcuts import render
from .models import Gpu, Game, PerformanceData
from .forms import ComparisonForm

def index_page(request):
    return render(request, 'index.html')

def compare(request):
    if request.method == 'POST':
        form = ComparisonForm(request.POST)
        if form.is_valid():
            # Обработка формы сравнения
            game = form.cleaned_data['game']
            resolution = form.cleaned_data['resolution']
            settings = form.cleaned_data['settings']

            # Получаем данные для сравнения
            comparisons = PerformanceData.objects.filter(
                game=game,
                resolution=resolution,
                graphics_settings=settings
            ).select_related('gpu').order_by('-avg_fps')[:10]

            # Расчет метрик
            for comp in comparisons:
                comp.fps_per_ruble = comp.gpu.fps_per_ruble(comp.avg_fps)
                comp.fps_per_watt = comp.gpu.fps_per_watt(comp.avg_fps)

            return render(request, 'core/comparison_result.html', {
                'comparisons': comparisons,
                'game': game,
                'resolution': resolution,
                'settings': settings,
            })
    else:
        form = ComparisonForm()
    stats = {
        'total_gpus': Gpu.objects.count(),
        'total_games': Game.objects.count(),
        'total_tests': PerformanceData.objects.count(),
    }
    return render(request, 'compare.html', {'stats': stats, 'form': form})