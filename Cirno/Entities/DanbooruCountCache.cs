using System;
using System.Collections.Generic;
using System.Text;

namespace CirnoBot.Entities
{
    public class DanbooruCountCache : CountCache
    {
        public DanbooruCountCache(string tags, int count, DateTime lastChecked) : base(tags, count, lastChecked)
        {
        }
    }
}
