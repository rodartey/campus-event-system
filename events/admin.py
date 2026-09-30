from django.contrib import admin
from .models import Organizer, Attendee, Venue, Event, RSVP

admin.site.register(Organizer)
admin.site.register(Attendee)
admin.site.register(Venue)
admin.site.register(Event)
admin.site.register(RSVP)