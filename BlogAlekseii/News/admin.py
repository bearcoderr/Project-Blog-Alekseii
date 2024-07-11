from django.contrib import admin
from .models import News, newsTag, newsCategory, FormsNews, galleryNews

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('titleNews', 'slugNews', 'dataNews')  # Замените 'status' на правильное имя поля

@admin.register(newsTag)
class NewsTagAdmin(admin.ModelAdmin):
    pass

@admin.register(newsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(galleryNews)
class galleryNewsAdmin(admin.ModelAdmin):
    pass

@admin.register(FormsNews)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('nameComm', 'emailComm', 'textComm', 'time_create')

