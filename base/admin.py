from django.contrib import admin
from .models import Question,Topic,Answer,User

# Register your models here.
admin.site.register(User)
admin.site.register(Topic)
admin.site.register(Question)
admin.site.register(Answer)
