using System;
using System.Collections.Generic;
using System.Text;

namespace CirnoBot.Entities
{
    public class Configuration
    {
        public string Token { get; set; }
        public string Prefix { get; set; }
        public string ConnectionString { get; set; }

        public Configuration() { }
    }
}
