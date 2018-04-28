using System;
using System.Collections.Generic;
using System.Text;

namespace CirnoBot
{
    class Program
    {
        public static void Main() => new CirnoBot().MainAsync().GetAwaiter().GetResult();
    }
}
