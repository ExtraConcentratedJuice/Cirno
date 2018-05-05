using CirnoBot.Entities;
using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Security.Authentication;
using System.Text;
using System.Threading.Tasks;

namespace CirnoBot.Http
{
    public abstract class BooruClient
    {
        protected BooruClient(CirnoContext context)
        {
            var handler = new HttpClientHandler
            {
                SslProtocols = SslProtocols.Tls12 | SslProtocols.Tls11 | SslProtocols.Tls,
                ServerCertificateCustomValidationCallback = (message, cert, chain, errors) => true
            };

            client = new HttpClient(handler);

            this.context = context;
        }

        protected CirnoContext context;

        protected abstract string BaseUrl();

        protected HttpClient client;

        public abstract Task<Dictionary<int, string>> GetPostsAsync(string tags, int page, int limit);
    }
}
