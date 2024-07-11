from django.contrib import admin
from .models import Settings, skillsSettings, socialSettings, numberSettings, experienceSettings, contactSettings, MenuSite
from .models import FormsHome

@admin.register(FormsHome)
class FormsHomeAdmin(admin.ModelAdmin):
    list_display = ['nameFormsHome', 'emailFormsHome', 'callFormsHome', 'time_create']
# Register your models here.


admin.site.register(Settings)
admin.site.register(MenuSite)
admin.site.register(skillsSettings)
admin.site.register(socialSettings)
admin.site.register(numberSettings)
admin.site.register(experienceSettings)
admin.site.register(contactSettings)