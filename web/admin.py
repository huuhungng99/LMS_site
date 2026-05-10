from django.contrib import admin
from web.models import *

# Register your models here.
admin.site.register(Student) 
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Subject) 
admin.site.register(Lesson)
admin.site.register(Material)
admin.site.register(Result)