from django.contrib import admin

from .models import *

admin.site.register(Activity)
admin.site.register(Event)

admin.site.register(Menu)
admin.site.register(MenuItem)

admin.site.register(Preference)

admin.site.register(Guest)
admin.site.register(GuestActivityRsvp)
admin.site.register(GuestSelection)
admin.site.register(GuestPreference)


class InvitationAdmin(admin.ModelAdmin):
	list_display = ['ref', 'event', 'total_guests', 'active']

admin.site.register(Invitation, InvitationAdmin)

