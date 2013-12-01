# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _


MENU_TYPE_CHOICES = (
	('APPETIZER', _(u'Appetizer')),
	('ENTREE', _(u'Entrée')),
	('DESSERT', _(u'Dessert')),
)


class Activity(models.Model):

	name = models.CharField(max_length=200)
	required = models.BooleanField(default=True)

	def __unicode__(self):
		return u'%s (%s)' % (self.name, u'Required' if self.required else 'Optional')

	class Meta:
		verbose_name_plural = 'Activities'

class Event(models.Model):

	active = models.BooleanField(default=True)
	name = models.CharField(max_length=200)
	activities = models.ManyToManyField(Activity)

	def __unicode__(self):
		return u'Event: %s' % self.name


class Menu(models.Model):

	name = models.CharField(max_length=150)

	def __unicode__(self):
		return u'Menu: %s' % self.name

	def get_items_by_type(self, menu_type):
		return MenuItem.objects.filter(menu=self, active=True, type=menu_type).order_by('order')


class MenuItem(models.Model):

	active = models.BooleanField(default=True)
	type = models.CharField(max_length=10, choices=MENU_TYPE_CHOICES)
	title = models.CharField(max_length=200)
	description = models.TextField(blank=True)
	order = models.IntegerField(default=0)
	menu = models.ForeignKey(Menu)

	def __unicode__(self):
		return u'Menu item: %s (%s)' % (self.title, self.get_type_display())


class Preference(models.Model):

	active = models.BooleanField(default=True)
	title = models.CharField(max_length=200)
	description = models.TextField(blank=True)
	required = models.BooleanField(default=True)

	def __unicode__(self):
		return u'Preference: %s' % self.title


class Guest(models.Model):

	name = models.CharField(max_length=150)
	email = models.EmailField()
	rsvp = models.BooleanField(default=False)
	notify = models.BooleanField(default=True)

	def __unicode__(self):
		return u'%s' % self.name

	def has_completed(self, invite):
		"""Check if the user has completed all of the required
		details for the invite"""

		# RSVP details
		for activity in invite.event.activities.all():
			if activity.required:
				if not self.has_activity_rsvp(activity):
					return False

		# Menu options
		if invite.menu and not self.has_menu_options(invite.event):
			return False

		# Preferences
		if invite.preference and invite.preference.required and not self.has_preference(invite.event):
			return False

		return True

	def has_activity_rsvp(self, activity):
		"""Check if the guest has an rsvp for a specific activity"""

		try:
			GuestActivityRsvp.objects.get(
				guest=self,
				activity=activity
			)
		except GuestActivityRsvp.DoesNotExist:
			return False

		return True

	def get_menu_options(self, event):
		try:
			return GuestSelection.objects.get(
				event=event,
				guest=self
			)
		except GuestSelection.DoesNotExist:
			return None

	def has_menu_options(self, event):
		return True if self.get_menu_options(event) is not None else False

	def delete_menu_options(self, event):
		menu_option = self.get_menu_options(event)

		if menu_option is not None:
			menu_option.delete()

	def get_preference(self, event):
		try:
			return GuestPreference.objects.get(
				event=event,
				guest=self
			)
		except GuestPreference.DoesNotExist:
			return None

	def has_preference(self, event):
		return True if self.get_preference(event) is not None else False


class GuestActivityRsvp(models.Model):

	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)
	guest = models.ForeignKey(Guest)
	activity = models.ForeignKey(Activity)

	def __unicode__(self):
		return u'%s - %s' % (self.guest.name, self.activity.name)


class GuestSelection(models.Model):

	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)
	event = models.ForeignKey(Event)
	guest = models.ForeignKey(Guest)
	items = models.ManyToManyField(MenuItem, blank=True)

	def __unicode__(self):
		return u'Selection @ %s by %s' % (self.created, self.guest.name)

	def get_appetizer(self):
		return self.items.filter(type='APPETIZER')

	def get_entree(self):
		return self.items.filter(type='ENTREE')

	def get_dessert(self):
		return self.items.filter(type='DESSERT')


class GuestPreference(models.Model):

	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)
	event = models.ForeignKey(Event)
	guest = models.ForeignKey(Guest)
	preference = models.TextField()

	def __unicode__(self):
		return u'Preference @ %s by %s' % (self.created, self.guest.name)


class Invitation(models.Model):

	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)
	active = models.BooleanField(default=True)
	ref = models.CharField(max_length=100)
	lead = models.TextField(blank=True, null=True)
	lead_on_complete = models.TextField(blank=True, null=True)
	event = models.ForeignKey(Event)
	menu = models.ForeignKey(Menu, blank=True, null=True)
	preference = models.ForeignKey(Preference, blank=True, null=True)
	guests = models.ManyToManyField(Guest, blank=True)

	def __unicode__(self):
		return u'Invitation: #%s' % self.ref

	@property
	def total_guests(self):
		return self.guests.all().count()

