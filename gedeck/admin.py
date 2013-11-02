from django.contrib import admin

from .models import Menu, MenuItem, Guest, GuestSelection, Invitation


class MenuAdmin(admin.ModelAdmin):
	pass

admin.site.register(Menu, MenuAdmin)


class MenuItemAdmin(admin.ModelAdmin):
	pass

admin.site.register(MenuItem, MenuItemAdmin)


class GuestAdmin(admin.ModelAdmin):
	pass

admin.site.register(Guest, GuestAdmin)


class GuestSelectionAdmin(admin.ModelAdmin):
	pass

admin.site.register(GuestSelection, GuestSelectionAdmin)


class InvitationAdmin(admin.ModelAdmin):
	pass

admin.site.register(Invitation, InvitationAdmin)