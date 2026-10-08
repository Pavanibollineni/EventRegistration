import { useEffect, useState } from "react";

const API_URL = "http://localhost:5198/api/Events";

function Events() {
  const [events, setEvents] = useState([]);

  const [form, setForm] = useState({
    name: "",
    date: "",
    venue: "",
    totalSeats: ""
  });

  async function loadEvents() {
    const response = await fetch(API_URL);
    const data = await response.json();

    setEvents(data);
  }

  useEffect(() => {
    loadEvents();
  }, []);

  async function handleSubmit(e) {
    e.preventDefault();

    const response = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        name: form.name,
        date: form.date,
        venue: form.venue,
        totalSeats: Number(form.totalSeats)
      })
    });

    if (response.ok) {
      setForm({
        name: "",
        date: "",
        venue: "",
        totalSeats: ""
      });

      loadEvents();
    }
  }

  return (
    <div>
      <h2>Events</h2>

      <form onSubmit={handleSubmit}>
        <input
          placeholder="Event Name"
          value={form.name}
          onChange={(e) =>
            setForm({ ...form, name: e.target.value })
          }
        />

        <input
          type="datetime-local"
          value={form.date}
          onChange={(e) =>
            setForm({ ...form, date: e.target.value })
          }
        />

        <input
          placeholder="Venue"
          value={form.venue}
          onChange={(e) =>
            setForm({ ...form, venue: e.target.value })
          }
        />

        <input
          type="number"
          placeholder="Total Seats"
          value={form.totalSeats}
          onChange={(e) =>
            setForm({ ...form, totalSeats: e.target.value })
          }
        />

        <button type="submit">
          Add Event
        </button>
      </form>

      <h3>Available Events</h3>

      {events.map((event) => (
        <div key={event.id}>
          <h3>{event.name}</h3>

          <p>Date: {event.date}</p>

          <p>Venue: {event.venue}</p>

          <p>
            Seats Left: {event.seatsLeft}
          </p>
        </div>
      ))}
    </div>
  );
}

export default Events;