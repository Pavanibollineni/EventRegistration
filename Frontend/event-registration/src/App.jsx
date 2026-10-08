import Events from "./components/Events";
import Register from "./components/Register";
import Attendees from "./components/Attendees";
 function App() {
  return (
    <div>
      <h1>Event Registration System</h1>

      <Events />

      <hr />

      <Register />

      <hr />

      <Attendees />
    </div>
  );
}

export default App;