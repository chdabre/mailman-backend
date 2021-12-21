from django.contrib import admin

from postcards.models import PostcardCreatorCredentials


@admin.register(PostcardCreatorCredentials)
class PostcardCreatorCredentialsAdmin(admin.ModelAdmin):
    pass
