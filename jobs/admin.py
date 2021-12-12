from django.contrib import admin

from jobs.models import PostcardJob, Address


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    pass


@admin.register(PostcardJob)
class PostcardJobAdmin(admin.ModelAdmin):
    pass
