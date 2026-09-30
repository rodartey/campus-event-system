from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Organizer(models.Model):
    """Someone who can create and manage events."""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="organizer_profile"
    )
    department = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.get_username()


class Attendee(models.Model):
    """A student or staff member who can RSVP to events."""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="attendee_profile"
    )
    student_id = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.get_username()


class Venue(models.Model):
    name = models.CharField(max_length=150)
    building = models.CharField(max_length=150, blank=True)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} ({self.building})" if self.building else self.name


class Event(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"
        CANCELLED = "cancelled", "Cancelled"
        COMPLETED = "completed", "Completed"

    # One organizer -> many events
    organizer = models.ForeignKey(
        Organizer, on_delete=models.CASCADE, related_name="events"
    )
    # Each event has exactly one venue; a venue can host many events over time
    venue = models.ForeignKey(
        Venue, on_delete=models.PROTECT, related_name="events"
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.DRAFT
    )
    # Many attendees <-> many events, via the RSVP model below
    attendees = models.ManyToManyField(
        Attendee, through="RSVP", related_name="events_rsvped"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["start_time"]

    def clean(self):
        if self.end_time and self.start_time and self.end_time <= self.start_time:
            raise ValidationError("End time must be after start time.")

    def __str__(self):
        return self.title


class RSVP(models.Model):
    class Response(models.TextChoices):
        GOING = "going", "Going"
        MAYBE = "maybe", "Maybe"
        NOT_GOING = "not_going", "Not going"

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="rsvps")
    attendee = models.ForeignKey(Attendee, on_delete=models.CASCADE, related_name="rsvps")
    response = models.CharField(
        max_length=10, choices=Response.choices, default=Response.GOING
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # An attendee can RSVP to an event only once
        constraints = [
            models.UniqueConstraint(fields=["event", "attendee"], name="unique_rsvp")
        ]

    def __str__(self):
        return f"{self.attendee} -> {self.event} ({self.get_response_display()})"