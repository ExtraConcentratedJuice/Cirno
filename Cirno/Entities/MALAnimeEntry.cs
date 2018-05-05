using System;
using System.Collections.Generic;
using System.Text;

namespace CirnoBot.Entities
{
    public class MALAnimeEntry
    {
        public int Id { get; set; }
        public string Title { get; set; }
        public string EnglishTitle { get; set; }
        public string Synonyms { get; set; }
        public int Episodes { get; set; }
        public float Score { get; set; }
        public string Type { get; set; }
        public string Status { get; set; }
        public string StartDate { get; set; }
        public string EndDate { get; set; }
        public string Synopsis { get; set; }
        public string Image { get; set; }
    }
}
