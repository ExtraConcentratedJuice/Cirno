using System;
using System.Collections.Generic;
using System.Text;

namespace CirnoBot.Entities
{
    public class GelbooruCountCache : CountCache
    {
        public GelbooruCountCache(string tags, int count, DateTime lastChecked) : base(tags, count, lastChecked)
        {
        }
    }
}
