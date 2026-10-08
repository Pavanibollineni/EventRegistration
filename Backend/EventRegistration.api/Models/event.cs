namespace EventRegistration.api.Models;

public class Event
{
    public int Id { get; set; }

    public string Name { get; set; } = string.Empty;

    public DateTime Date { get; set; }

    public string Venue { get; set; } = string.Empty;

    public int TotalSeats { get; set; }

    public ICollection<Registration> Registrations { get; set; }
        = new List<Registration>();

}


