from django.template import Library

register = Library()

@register.filter
def has_activity_rsvp(activity, guest):
	return guest.has_activity_rsvp(activity)

@register.filter
def has_menu_selection(guest, event):
	return guest.has_menu_options(event)

@register.filter
def has_preference_selection(guest, event):
	return guest.has_preference(event)