from django.contrib import admin
from meowoof import models
# 注册了已存在的数据库中的模型

admin.site.register(models.User)
admin.site.register(models.Pet)
admin.site.register(models.Comment)
admin.site.register(models.Tool)
admin.site.register(models.CollectTool)
admin.site.register(models.CollectPet)
admin.site.register(models.Suggestion)