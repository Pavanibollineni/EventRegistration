import { useEffect, useState } from "react";

const EVENTS_API = "http://localhost:5198/api/Events";
const REGISTRATION_API =
  "http://localhost:5198/api/Registrations";

function Register() {
  const [events, setEvents] = useState([]);

  const [form, setForm] = useState({
    employeeName: "",
    employeeEmail: "",
    eventId: ""
  });

  useEffect(() => {
    loadEvents();
  }, []);

  async function loadEvents() {
    const response = await fetch(EVENTS_API);
    const data = await response.json();

    setEvents(data);
  }

  async function handleSubmit(e) {
    e.preventDefault();

    const response = await fetch(REGISTRATION_API, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        employeeName: form.employeeName,
        employeeEmail: form.employeeEmail,
        eventId: Number(form.eventId)
      })
    });

    const data = await response.text();

    if (response.ok) {
      alert("Registration successful!");

      setForm({
        employeeName: "",
        employeeEmail: "",
        eventId: ""
      });
    } else {
      alert(data);
    }
  }

  return (
    <div>
      <h2>Register</h2>

      <form onSubmit={handleSubmit}>
        <input
          placeholder="Employee Name"
          value={form.employeeName}
          onChange={(e) =>
            setForm({
              ...form,
              employeeName: e.target.value
            })
          }
        />

        <input
          type="email"
          placeholder="Employee Email"
          value={form.employeeEmail}
          onChange={(e) =>
            setForm({
              ...form,
              employeeEmail: e.target.value
            })
          }
        />

        <select
          value={form.eventId}
          onChange={(e) =>
            setForm({
              ...form,
              eventId: e.target.value
            })
          }
        >
          <option value="">Select Event</option>

          {events.map((event) => (
            <option key={event.id} value={event.id}>
              {event.name} - {event.seatsLeft} seats left
            </option>
          ))}
        </select>

        <button type="submit">
          Register
        </button>
      </form>
    </div>
  );
}

export default Register;