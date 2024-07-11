from django.contrib import admin
from .models import GallerySite, Photo

class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 3  # Количество дополнительных полей для загрузки фотографий

@admin.register(GallerySite)
class GallerySiteAdmin(admin.ModelAdmin):
    inlines = [PhotoInline]

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    pass