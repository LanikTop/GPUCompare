from django.contrib import admin

from core.models import Gpu, Game, PerformanceData


@admin.register(Gpu)
class GpuAdmin(admin.ModelAdmin):
    list_display = ('name', 'manufacturer', 'release_year', 'price_rub', 'memory_gb')
    list_filter = ('price_rub',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_year')
    list_filter = ('title',)
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(PerformanceData)
class PerformanceDataAdmin(admin.ModelAdmin):
    list_display = ('gpu', 'game', 'resolution', 'graphics_settings', 'avg_fps')
    list_filter = ('resolution', 'graphics_settings')
    search_fields = ('gpu__name', 'game__title')
