from django.shortcuts import render
from django.shortcuts import render
from .models import Gpu, Game, PerformanceData
from .forms import ComparisonForm
from django.db.models import F, FloatField, ExpressionWrapper
from .utils.plotting_graphs import create_top5_best_graph, create_top5_optimal_graph

def index_page(request):
    return render(request, 'index.html')

def compare(request):
    if request.method == 'POST':
        form = ComparisonForm(request.POST)
        if form.is_valid():
            game = form.cleaned_data['game']
            resolution = form.cleaned_data['resolution']
            settings = form.cleaned_data['settings']
            min_fps = 30

            filter_gpus = PerformanceData.objects.filter(
                game=game,
                resolution=resolution,
                graphics_settings=settings,
                avg_fps__gte=min_fps
            ).select_related('gpu')

            top5fps = filter_gpus.order_by('-avg_fps')[:5]
            best_gpu = filter_gpus.order_by('-avg_fps')[0]
            top5best_graph = create_top5_best_graph(top5fps, game, resolution, settings)
            best_gpu_data = {
                'perf': best_gpu,
                'fps_per_ruble': best_gpu.gpu.fps_per_ruble(best_gpu.avg_fps)
            }

            budget_gpu = filter_gpus.order_by('gpu__price_rub').first()
            budget_gpu_data = {
                'perf': budget_gpu,
                'fps_per_ruble': budget_gpu.gpu.fps_per_ruble(budget_gpu.avg_fps)
            }

            optimal_gpus = filter_gpus.annotate(
                efficiency=ExpressionWrapper(
                    F('avg_fps') / F('gpu__price_rub'), output_field=FloatField())).order_by('-efficiency')[:5]


            optimal_gpu = optimal_gpus[0]
            top5optimal_graph = create_top5_optimal_graph(optimal_gpus, game, resolution, settings)
            optimal_gpu_data = {
                'perf': optimal_gpu,
                'fps_per_ruble': optimal_gpu.gpu.fps_per_ruble(optimal_gpu.avg_fps)
            }

            return render(request, 'comparison_result.html', {
                'best_gpu': best_gpu_data,
                'optimal_gpu': optimal_gpu_data,
                'budget_gpu': budget_gpu_data,
                'game': game,
                'resolution': resolution,
                'settings': settings,
                'top5fps_graph': top5best_graph,
                'top5optimal_graph': top5optimal_graph,
            })
    else:
        form = ComparisonForm()
    stats = {
        'total_gpus': Gpu.objects.count(),
        'total_games': Game.objects.count(),
        'total_tests': PerformanceData.objects.count(),
    }
    return render(request, 'compare.html', {'stats': stats, 'form': form})