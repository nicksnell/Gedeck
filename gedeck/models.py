# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _

MENU_TYPE_CHOICES = (
	('APPETIZER', _(u'Appetizer')),
	('ENTREE', _(u'Entrée')),
	('DESSERT', _(u'Dessert')),
)

class Event(models.Model):

	active = models.BooleanField(default=True)
	name = models.CharField(max_length=200)

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


class Guest(models.Model):

	name = models.CharField(max_length=150)
	email = models.EmailField()
	rsvp = models.BooleanField(default=False)
	notify = models.BooleanField(default=True)

	def __unicode__(self):
		return u'%s' % self.name

	def get_menu_options(self):
		try:
			return GuestSelection.objects.get(guest=self)
		except GuestSelection.DoesNotExist:
			return None

	def has_menu_options(self):
		return True if self.get_menu_options() is not None else False

	def delete_menu_options(self):
		menu_option = self.get_menu_options()

		if menu_option is not None:
			menu_option.delete()


class Invitation(models.Model):

	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)
	active = models.BooleanField(default=True)
	ref = models.CharField(max_length=100)
	event = models.ForeignKey(Event, blank=True, null=True)
	menu = models.ForeignKey(Menu, blank=True, null=True)
	guests = models.ManyToManyField(Guest, blank=True)

	def __unicode__(self):
		return u'Invitation: #%s' % self.ref


class GuestSelection(models.Model):

	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)
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

