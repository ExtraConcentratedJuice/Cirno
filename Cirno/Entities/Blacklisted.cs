using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Text;

namespace CirnoBot.Entities
{
    public class Blacklisted
    {
        [Key]
        public ulong Id { get; set; }

        public Blacklisted() { }
        public Blacklisted(ulong id) { Id = id; }
    }
}
