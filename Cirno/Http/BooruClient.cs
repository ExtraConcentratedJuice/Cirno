using CirnoBot.Entities;
using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;

namespace CirnoBot.Http
{
    public abstract class BooruClient
    {
        protected BooruClient(CirnoContext context)
        {
            this.context = context;
        }

        protected CirnoContext context;

        protected abstract string BaseUrl();

        protected HttpClient client = new HttpClient();

        public abstract Task<Dictionary<int, string>> GetPostsAsync(string tags, int page, int limit);
    }
}
