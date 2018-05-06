using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Security.Authentication;
using System.Text;

namespace CirnoBot.Http
{
    public abstract class ApiClient
    {
        protected abstract string BaseUrl { get; }
        protected HttpClient client;

        protected ApiClient()
        {
            var handler = new HttpClientHandler
            {
                SslProtocols = SslProtocols.Tls12 | SslProtocols.Tls11 | SslProtocols.Tls,
                ServerCertificateCustomValidationCallback = (message, cert, chain, errors) => true
            };

            client = new HttpClient(handler);
        }
    }
}
