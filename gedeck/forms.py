from django import forms


class MenuSelectForm(forms.Form):
	"""Skeleton for a menu selection"""

	guest = forms.CharField(widget=forms.HiddenInput())
	appetizer = forms.ModelChoiceField(queryset=[], widget=forms.RadioSelect(), required=False, empty_label=None)
	entree = forms.ModelChoiceField(queryset=[], widget=forms.RadioSelect(), empty_label=None)
	dessert = forms.ModelChoiceField(queryset=[], widget=forms.RadioSelect(), required=False, empty_label=None)

	def __init__(self, *args, **kwargs):
		# Get our menu and add the choices for each course
		menu = kwargs.pop('menu')

		super(MenuSelectForm, self).__init__(*args, **kwargs)

		self.fields['appetizer'].queryset = menu.get_items_by_type('APPETIZER')
		self.fields['entree'].queryset = menu.get_items_by_type('ENTREE')
		self.fields['dessert'].queryset = menu.get_items_by_type('DESSERT')