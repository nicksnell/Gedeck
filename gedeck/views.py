from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect

from gedeck.forms import MenuSelectForm
from gedeck.models import Invitation, Guest, GuestSelection


def rsvp_guest(request, invitation_ref=None, guest=None):
	"""RSVP a guest for an event"""

	guest = get_object_or_404(Guest, id=guest)
	invite = get_object_or_404(Invitation, ref=invitation_ref, active=True, guests=guest)

	if guest.rsvp and guest.has_menu_options():
		# If we are toggling the RSVP, remove any menu selections
		guest.delete_menu_options()

	# RSVP the guest
	guest.rsvp = not guest.rsvp
	guest.save()

	return redirect('menu_select', invitation_ref=invite.ref)


def menu_select(request, invitation_ref=None, guest=None):
	"""Main view to select menu options and to save the posted form"""

	invite = get_object_or_404(Invitation, ref=invitation_ref, active=True)

	# Check if the invite has multiple guests and we haven't selected one
	if invite.guests.count() > 1 and not guest:
		return render(request, 'gedeck/rsvp.html', {
			'invite': invite,
			'guests': invite.guests.all(),
		})

	elif guest is not None:
		# Check the guest is part of the invitation
		try:
			guest = invite.guests.get(id=guest)
		except Guest.DoesNotExist:
			# Wrong guest for the invitation, redirect to guest select
			return redirect('menu_select', invitation_ref=invite.ref)

	else:
		guest = invite.guests.all()[0]

	guest_selection = None
	appetizer, entree, dessert = None, None, None

	if guest.has_menu_options():
		guest_selection = guest.get_menu_options()

		appetizer = guest_selection.get_appetizer()
		entree = guest_selection.get_entree()
		dessert = guest_selection.get_dessert()

	# Build the form data
	initial_data = {
		'guest': guest.id,
		'appetizer': appetizer,
		'entree': entree,
		'dessert': dessert,
	}

	if request.method == 'POST':
		form = MenuSelectForm(request.POST, initial=initial_data, menu=invite.menu)

		if form.is_valid():

			# Save the menu data and redirect to thank you
			selection, created = GuestSelection.objects.get_or_create(
				guest=guest
			)

			if not created:
				# Kill current selections
				selection.items.clear()

			# Set the appetizer/entree/dessert
			selection.items.add(form.cleaned_data['appetizer'])
			selection.items.add(form.cleaned_data['entree'])
			selection.items.add(form.cleaned_data['dessert'])

			selection.save()

			return redirect('menu_select', invitation_ref=invite.ref)

	else:
		form = MenuSelectForm(initial=initial_data, menu=invite.menu)

	return render(request, 'gedeck/select.html', {
		'invite': invite,
		'guest': guest,
		'form': form,
	})
