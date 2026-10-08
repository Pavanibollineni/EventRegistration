using EventRegistration.api.Models;
using Microsoft.EntityFrameworkCore;

namespace EventRegistration.api.Data;

public class AppDbContext : DbContext
{
    public AppDbContext(DbContextOptions<AppDbContext> options)
        : base(options)
    {
    }

    public DbSet<Event> Events { get; set; }

    public DbSet<Registration> Registrations { get; set; }


}