from django.contrib import admin

from jobs.models import PostcardJob


@admin.register(PostcardJob)
class PostcardJobAdmin(admin.ModelAdmin):
    pass