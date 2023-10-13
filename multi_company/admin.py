from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(FormSettings)
admin.site.register(Doisser)
admin.site.register(Formation)
admin.site.register(JotFormSubmission)