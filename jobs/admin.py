from django.contrib import admin

from jobs.models import PostcardJob, Address


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'user', 'is_primary', 'num_used', 'display_status']


@admin.register(PostcardJob)
class PostcardJobAdmin(admin.ModelAdmin):
    list_display = ['user', 'status', 'sender', 'recipient', 'send_on', 'time_sent']