from django.contrib import admin

from .models import Event, Menu, MenuItem, Guest, Preference, \
	GuestSelection, GuestPreference, Invitation

class EventAdmin(admin.ModelAdmin):
	pass

admin.site.register(Event, EventAdmin)


class MenuAdmin(admin.ModelAdmin):
	pass

admin.site.register(Menu, MenuAdmin)


class MenuItemAdmin(admin.ModelAdmin):
	pass

admin.site.register(MenuItem, MenuItemAdmin)


class PreferenceAdmin(admin.ModelAdmin):
	pass

admin.site.register(Preference, PreferenceAdmin)


class GuestAdmin(admin.ModelAdmin):
	pass

admin.site.register(Guest, GuestAdmin)


class GuestSelectionAdmin(admin.ModelAdmin):
	pass

admin.site.register(GuestSelection, GuestSelectionAdmin)


class GuestPreferenceAdmin(admin.ModelAdmin):
	pass

admin.site.register(GuestPreference, GuestPreferenceAdmin)


class InvitationAdmin(admin.ModelAdmin):
	list_display = ['ref', 'event', 'total_guests', 'active']

admin.site.register(Invitation, InvitationAdmin)