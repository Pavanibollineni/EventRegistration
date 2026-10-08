using EventRegistration.api.Data;
using EventRegistration.api.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace EventRegistration.api.Controllers;

[ApiController]
[Route("api/[controller]")]
public class EventsController : ControllerBase
{
    private readonly AppDbContext _context;

    public EventsController(AppDbContext context)
    
    {
        _context = context;
    }

    [HttpGet]
    public async Task<IActionResult> GetEvents()
    {
        var events = await _context.Events
            .Include(e => e.Registrations)
            .ToListAsync();

        var result = events.Select(e => new
        {
            e.Id,
            e.Name,
            e.Date,
            e.Venue,
            e.TotalSeats,
            SeatsLeft = e.TotalSeats - e.Registrations.Count
        });

        return Ok(result);
    }

    [HttpPost]
    public async Task<IActionResult> CreateEvent(Event eventItem)
    {
        _context.Events.Add(eventItem);

        await _context.SaveChangesAsync();

        return CreatedAtAction(
            nameof(GetEvents),
            new { id = eventItem.Id },
            eventItem
        );
    }
}
 