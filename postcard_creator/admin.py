from django.contrib import admin

from postcard_creator.models import PostcardCreatorCredentials


@admin.register(PostcardCreatorCredentials)
class PostcardCreatorCredentialsAdmin(admin.ModelAdmin):
    pass
