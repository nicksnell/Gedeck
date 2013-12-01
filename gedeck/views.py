from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect

from gedeck.forms import MenuSelectForm, PreferenceSelectForm
from gedeck.models import Invitation, Activity, Guest, GuestSelection, \
	GuestActivityRsvp, GuestPreference


def invitation(request, invitation_ref=None):
	"""Landing view for the invitation"""

	invite = get_object_or_404(Invitation, ref=invitation_ref, active=True)

	# Check to see if the selection is complete
	all_done = True
	guests = invite.guests.all().order_by('name')

	for g in guests:
		if not g.has_completed(invite):
			all_done = False

	return render(request, 'gedeck/invite.html', {
		'invite': invite,
		'all_done': all_done,
		'guests': guests,
	})


def rsvp(request, invitation_ref=None, activity=None, guest=None):
	"""Toggle RSVP for a guest for an activity (part of an event) - events can have
	multiple activities, we need to ensure we RSVP for the correct activity within the event"""

	guest = get_object_or_404(Guest, id=guest)
	invite = get_object_or_404(Invitation, ref=invitation_ref, active=True, guests=guest)
	activity = get_object_or_404(Activity, id=activity)

	guest_rsvp, created = GuestActivityRsvp.objects.get_or_create(
		activity=activity,
		guest=guest
	)

	# If it hasn't be created now then remove
	# it (this toggles the rsvp)
	if not created:
		guest_rsvp.delete()

	return redirect('invitation', invitation_ref=invite.ref)


def menu_select(request, invitation_ref=None, guest=None):
	"""Select menu options and save the selected options"""

	invite = get_object_or_404(Invitation, ref=invitation_ref, active=True)

	# Must have a guest to continue
	if not guest:
		return redirect('invitation')

	elif guest is not None:
		# Check the guest is part of the invitation
		try:
			guest = invite.guests.get(id=guest)
		except Guest.DoesNotExist:
			# Wrong guest for the invitation, redirect to guest select
			return redirect('invitation', invitation_ref=invite.ref)

	guest_selection = None
	appetizer, entree, dessert = None, None, None

	if guest.has_menu_options(invite.event):
		guest_selection = guest.get_menu_options(invite.event)

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
				event=invite.event,
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

			return redirect('invitation', invitation_ref=invite.ref)

	else:
		form = MenuSelectForm(initial=initial_data, menu=invite.menu)

	return render(request, 'gedeck/menu.html', {
		'invite': invite,
		'guest': guest,
		'form': form,
	})


def preference_select(request, invitation_ref=None, guest=None):
	invite = get_object_or_404(Invitation, ref=invitation_ref, active=True)

	# Must have a guest to continue
	if not guest:
		return redirect('invitation')

	elif guest is not None:
		# Check the guest is part of the invitation
		try:
			guest = invite.guests.get(id=guest)
		except Guest.DoesNotExist:
			# Wrong guest for the invitation, redirect to guest select
			return redirect('invitation', invitation_ref=invite.ref)

	# Current preference
	current_preference = guest.get_preference(invite.event)

	initial = {
		'preference': current_preference.preference if current_preference is not None else ''
	}

	if request.method == 'POST':
		form = PreferenceSelectForm(request.POST, initial=initial)

		if form.is_valid():

			# Save the menu data and redirect to thank you
			preference, created = GuestPreference.objects.get_or_create(
				event=invite.event,
				guest=guest
			)

			preference.preference = form.cleaned_data['preference']
			preference.save()

			return redirect('invitation', invitation_ref=invite.ref)

	else:
		form = PreferenceSelectForm(initial=initial)

	return render(request, 'gedeck/preference.html', {
		'invite': invite,
		'guest': guest,
		'form': form,
	})

