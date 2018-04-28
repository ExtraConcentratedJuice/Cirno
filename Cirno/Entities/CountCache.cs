using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Text;

namespace CirnoBot.Entities
{
    public class CountCache
    {
        [Key]
        public string Tags { get; set; }
        public int Count { get; set; }
        public DateTime LastChecked { get; set; }

        public CountCache() { }

        public CountCache(string tags, int count, DateTime lastChecked)
        {
            Tags = tags;
            Count = count;
            LastChecked = lastChecked;
        }
    }
}
