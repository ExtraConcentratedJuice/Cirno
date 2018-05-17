using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.Text;

namespace CirnoBot.Entities
{
    public class CirnoContext : DbContext
    {
        private readonly string connectionString;

        public CirnoContext(string connectionString)
        {
            this.connectionString = connectionString;
        }

        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        {
            optionsBuilder.UseSqlite(connectionString);
        }

        public DbSet<Blacklisted> Blacklisted { get; set; }
        public DbSet<GelbooruCountCache> GelbooruCountCache { get; set; }
        public DbSet<DanbooruCountCache> DanbooruCountCache { get; set; }
        public DbSet<TwistEntry> TwistEntries { get; set; }
    }
}
