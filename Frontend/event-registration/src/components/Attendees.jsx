import { useEffect, useState } from "react";

const EVENTS_API = "http://localhost:5198/api/Events";
const ATTENDEES_API =
  "http://localhost:5198/api/Registrations/event/";

function Attendees() {
  const [events, setEvents] = useState([]);
  const [selectedEvent, setSelectedEvent] = useState("");
  const [attendees, setAttendees] = useState([]);
  const [totalCount, setTotalCount] = useState(0);

  useEffect(() => {
    loadEvents();
  }, []);

  async function loadEvents() {
    const response = await fetch(EVENTS_API);
    const data = await response.json();

    setEvents(data);
  }

  async function handleEventChange(eventId) {
    setSelectedEvent(eventId);

    if (!eventId) {
      setAttendees([]);
      setTotalCount(0);
      return;
    }

    const response = await fetch(
      ATTENDEES_API + eventId
    );

    const data = await response.json();

    setAttendees(data.attendees);
    setTotalCount(data.totalCount);
  }

  return (
    <div>
      <h2>Attendees</h2>

      <select
        value={selectedEvent}
        onChange={(e) =>
          handleEventChange(e.target.value)
        }
      >
        <option value="">Select Event</option>

        {events.map((event) => (
          <option key={event.id} value={event.id}>
            {event.name}
          </option>
        ))}
      </select>

      <h3>Total Attendees: {totalCount}</h3>

      {attendees.map((person) => (
        <div key={person.id}>
          <p>
            {person.employeeName}
          </p>

          <p>
            {person.employeeEmail}
          </p>
        </div>
      ))}
    </div>
  );
}

export default Attendees;