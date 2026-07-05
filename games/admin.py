from django.contrib import admin
from .models import Game, Review

class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'year_of_release', 'poster_preview')  # 👈 ЭТА СТРОКА ВКЛЮЧАЕТ ТАБЛИЦУ
    ordering = ['title']
    def poster_preview(self, obj):
        if obj.poster_url:
            return f'<img src="{obj.poster_url}" width="50" height="75" />'
        return 'Нет постера'
    poster_preview.allow_tags = True
    poster_preview.short_description = 'Постер'

admin.site.register(Game, GameAdmin)
admin.site.register(Review)