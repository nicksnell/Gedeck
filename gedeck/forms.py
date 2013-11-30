from django import forms
from django.utils.safestring import mark_safe

from gedeck.models import Preference

class MenuChoiceField(forms.ModelChoiceField):

	def label_from_instance(self, obj):
		return mark_safe(u'<span class="menu-option"><b>%s</b><br><p>%s</p></span>' % (obj.title, obj.description))


class MenuSelectForm(forms.Form):
	"""Skeleton for a menu selection"""

	guest = forms.CharField(widget=forms.HiddenInput())
	appetizer = MenuChoiceField(queryset=[], widget=forms.RadioSelect(), required=False, empty_label=None)
	entree = MenuChoiceField(queryset=[], widget=forms.RadioSelect(), empty_label=None)
	dessert = MenuChoiceField(queryset=[], widget=forms.RadioSelect(), required=False, empty_label=None)

	def __init__(self, *args, **kwargs):
		# Get our menu and add the choices for each course
		menu = kwargs.pop('menu')

		super(MenuSelectForm, self).__init__(*args, **kwargs)

		self.fields['appetizer'].queryset = menu.get_items_by_type('APPETIZER')
		self.fields['entree'].queryset = menu.get_items_by_type('ENTREE')
		self.fields['dessert'].queryset = menu.get_items_by_type('DESSERT')


class PreferenceSelectForm(forms.Form):

	preference = forms.CharField(label='Your preferences', widget=forms.Textarea)