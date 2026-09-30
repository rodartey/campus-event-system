from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Event, Attendee, RSVP
from .forms import RSVPForm


def event_list(request):
    events = Event.objects.all()
    return render(request, 'events/event_list.html', {'events': events})


@login_required
def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    attendee, created = Attendee.objects.get_or_create(user=request.user)
    existing_rsvp = RSVP.objects.filter(event=event, attendee=attendee).first()

    if request.method == 'POST':
        form = RSVPForm(request.POST, instance=existing_rsvp)
        rsvp = form.save(commit=False)
        rsvp.event = event
        rsvp.attendee = attendee
        rsvp.save()
        return redirect('event_detail', event_id=event.id)
    else:
        form = RSVPForm(instance=existing_rsvp)

    return render(request, 'events/event_detail.html', {
        'event': event,
        'form': form,
        'existing_rsvp': existing_rsvp,
    })