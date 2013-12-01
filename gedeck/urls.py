from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
	url(r'^$', TemplateView.as_view(template_name='gedeck/index.html'), name='home'),
	url(r'^rsvp/(?P<invitation_ref>[-\w]+)/(?P<activity>[-\d]+)/(?P<guest>[-\d]+)/$', 'gedeck.views.rsvp', name='rsvp'),
	url(r'^preference/(?P<invitation_ref>[-\w]+)/(?P<guest>[-\d]+)/$', 'gedeck.views.preference_select', name='preference_select_for_guest'),
	url(r'^menu/(?P<invitation_ref>[-\w]+)/(?P<guest>[-\d]+)/$', 'gedeck.views.menu_select', name='menu_select_for_guest'),
	url(r'^invite/(?P<invitation_ref>[-\w]+)/$', 'gedeck.views.invitation', name='invitation'),
)
