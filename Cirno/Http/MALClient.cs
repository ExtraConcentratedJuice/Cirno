using CirnoBot.Entities;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Security.Authentication;
using System.Text;
using System.Threading.Tasks;
using System.Web;
using System.Xml.Linq;

namespace CirnoBot.Http
{
    public class MalClient : ApiClient
    {
        protected override string BaseUrl => "https://myanimelist.net/api";

        public MalClient(string username, string password)
        {
            client.DefaultRequestHeaders.Authorization = 
                new AuthenticationHeaderValue("Authorization", "Basic " + Convert.ToBase64String(Encoding.UTF8.GetBytes(username + ":" + password)));
        }

        public async Task<List<MALAnimeEntry>> SearchAnimeAsync(string search)
        {
            var query = HttpUtility.ParseQueryString(String.Empty);

            query["q"] = search;

            string endp = $"{BaseUrl}/anime/search.xml?{query.ToString()}";

            string resp = await client.GetStringAsync(endp);

            if (String.IsNullOrWhiteSpace(resp))
                return null;

            List<MALAnimeEntry> entries = new List<MALAnimeEntry>();

            XElement root = XElement.Parse(resp);

            foreach (XElement e in root.Elements())
            {
                entries.Add(new MALAnimeEntry
                {
                    Id = int.Parse(e.Element("id").Value),
                    Title = e.Element("title").Value,
                    EnglishTitle = e.Element("english").Value,
                    Synonyms = e.Element("synonyms").Value,
                    Episodes = int.Parse(e.Element("episodes").Value),
                    Score = float.Parse(e.Element("score").Value),
                    Type = e.Element("type").Value,
                    Status = e.Element("status").Value,
                    StartDate = e.Element("start_date").Value,
                    EndDate = e.Element("end_date").Value,
                    Synopsis = e.Element("synopsis").Value,
                    Image = e.Element("image").Value
                });
            }

            return entries;
        }

        public async Task<MALAnimeEntry> FirstAnimeAsync(string search)
        {
            var results = await SearchAnimeAsync(search);

            if (results == null)
                return null;

            MALAnimeEntry entry = results.FirstOrDefault(x =>
                String.Equals(search, x.Title, StringComparison.OrdinalIgnoreCase) ||
                String.Equals(search, x.EnglishTitle, StringComparison.OrdinalIgnoreCase));

            if (entry == null)
                entry = results.OrderBy(x => x.Title.Length)
                .FirstOrDefault(x => x.Title.IndexOf(search, StringComparison.OrdinalIgnoreCase) >= 0);

            if (entry == null)
                entry = results.OrderBy(x => x.EnglishTitle.Length)
                .FirstOrDefault(x => x.EnglishTitle.IndexOf(search, StringComparison.OrdinalIgnoreCase) >= 0);

            if (entry == null)
                entry = results.First();

            return entry;
        }
    }
}
