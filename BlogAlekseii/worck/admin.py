from django.contrib import admin
from .models import WorckSite, GalleryWorck, categoryWorck

# Register your models here.

admin.site.register(categoryWorck)

@admin.register(WorckSite)
class WorckSiteAdmin(admin.ModelAdmin):
    list_display = ['titleWorck', 'dateWorck', 'date_old_Worck']
    actions = ['duplicate_records']

    def duplicate_records(self, request, queryset):
        for obj in queryset:
            obj.pk = None  # Сбросить первичный ключ, чтобы создать новую запись
            obj.id = None  # Очистить id, если это поле не автоинкрементное
            obj.save()

    duplicate_records.short_description = "Дублировать записи"

@admin.register(GalleryWorck)
class GalleryWorckAdmin(admin.ModelAdmin):
    list_display = ['id', 'gallery_img_Worck']
