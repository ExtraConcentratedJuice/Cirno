using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Text;

namespace CirnoBot.Entities
{
    public class TwistEntry
    {
        [Key]
        public int Id { get; set; }
        public string Title { get; set; }
        public string AltTitle { get; set; }
        public int? MalId { get; set; }
        public string Slug { get; set; }

        public string Url { get => $"https://twist.moe/a/{Slug}"; }
    }
}
