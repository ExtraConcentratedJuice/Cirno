using CirnoBot.Entities;
using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Security.Authentication;
using System.Text;
using System.Threading.Tasks;

namespace CirnoBot.Http
{
    public abstract class BooruClient : ApiClient
    {
        protected CirnoContext context;

        protected BooruClient(CirnoContext context)
        {
            this.context = context;
        }

        public abstract Task<int> GetImageCountAsync(string tags);
        public abstract Task<Dictionary<int, string>> GetPostsAsync(string tags, int page, int limit);
    }
}
