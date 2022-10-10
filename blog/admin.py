# blog/admin.py

from django.contrib import admin
from . import models

class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'created',
        'updated',
    )

    search_fields = (
        'title',
        'author__username',
        'author__first_name',
        'author__last_name',
    )

    list_filter = (
        'status',
    )

    prepopulated_fields = {'slug': ('title',)}
    pass

# Register the `Post` model
admin.site.register(models.Post, PostAdmin)
