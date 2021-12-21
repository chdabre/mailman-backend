from django.contrib import admin

from jobs.models import PostcardJob, Address


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    pass


@admin.register(PostcardJob)
class PostcardJobAdmin(admin.ModelAdmin):
    list_display = ['user', 'status', 'sender', 'recipient', 'send_on', 'time_sent']