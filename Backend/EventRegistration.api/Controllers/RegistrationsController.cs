using EventRegistration.api.Data;
using EventRegistration.api.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace EventRegistration.api.Controllers;

[ApiController]
[Route("api/[controller]")]
public class RegistrationsController : ControllerBase
{
    private readonly AppDbContext _context;
    public RegistrationsController(AppDbContext context)
    {
        _context = context;
    }

    [HttpPost]
    public async Task<IActionResult> Register(Registration registration)
    {
        var eventItem = await _context.Events
            .Include(e => e.Registrations)
            .FirstOrDefaultAsync(e => e.Id == registration.EventId);

        if (eventItem == null)
        {
            return NotFound("Event not found.");
        }

        if (eventItem.Registrations.Count >= eventItem.TotalSeats)
        {
            return BadRequest("Event is full.");
        }

        registration.RegisteredAt = DateTime.UtcNow;

        _context.Registrations.Add(registration);

        await _context.SaveChangesAsync();

        return Ok(registration);
    }

    [HttpGet("event/{eventId}")]
    public async Task<IActionResult> GetAttendees(int eventId)
    {
        var attendees = await _context.Registrations
            .Where(r => r.EventId == eventId)
            .Select(r => new
            {
                r.Id,
                r.EmployeeName,
                r.EmployeeEmail,
                r.RegisteredAt
            })
            .ToListAsync();

        return Ok(new
        {
            TotalCount = attendees.Count,
            Attendees = attendees
        });
    }
}