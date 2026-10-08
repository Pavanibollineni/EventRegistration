namespace EventRegistration.api.Models;

public class Registration
{
    public int Id { get; set; }

    public string EmployeeName { get; set; } = string.Empty;

    public string EmployeeEmail { get; set; } = string.Empty;

    public int EventId { get; set; }

    public Event? Event { get; set; }

    public DateTime RegisteredAt { get; set; } = DateTime.UtcNow;
}