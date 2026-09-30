# Campus Event System

A Django web application for managing campus events. Organizers create events tied to a venue, and attendees can RSVP to multiple events.

## Features

- Organizers can create and manage multiple events
- Each event is assigned to one venue
- Attendees can RSVP to multiple events (Going / Maybe / Not going)
- Event status tracking (Draft / Published / Cancelled / Completed)
- Django admin panel for managing all data
- Public-facing pages to browse events and RSVP

## Tech stack

- Python
- Django
- SQLite (development database)

## Data model

- **Organizer** — linked to a User, can create many Events
- **Venue** — has a name, building, and capacity
- **Event** — belongs to one Organizer and one Venue, has a status
- **Attendee** — linked to a User, can RSVP to many Events
- **RSVP** — links an Attendee to an Event with a response (Going / Maybe / Not going)

## Setup

1. Clone the repository
2. Install dependencies
3. Run migrations
4. Create an admin user
5. Run the server
6. Visit `http://127.0.0.1:8000/events/` to view events, or `http://127.0.0.1:8000/admin/` for the admin panel.

## Author

Rosemond Oye Dartey — BSc Information Technology, KNUST
