using CirnoBot.Entities;
using HtmlAgilityPack;
using Microsoft.EntityFrameworkCore;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Xml.Linq;

namespace CirnoBot.Http
{
    public class TwistClient : ApiClient
    {
        private readonly CirnoContext context;

        protected override string BaseUrl => "https://twist.moe";

        public TwistClient(CirnoContext context)
        {
            this.context = context;
        }

        public async Task<TwistEntry> GetEntryAsync(string name)
        {
            if ((DateTime.Now - CirnoBot.Data.TwistLastUpdated).TotalDays > 1)
            {
                await UpdateDatabaseAsync();
                CirnoBot.Data.TwistLastUpdated = DateTime.Now;
                File.WriteAllText("data.json", JsonConvert.SerializeObject(CirnoBot.Data));
            }

            TwistEntry entry = context.TwistEntries.FirstOrDefault(x => String.Equals(x.Title, name, StringComparison.OrdinalIgnoreCase) ||
                String.Equals(x.AltTitle, name, StringComparison.OrdinalIgnoreCase));

            if (entry == null)
                entry = context.TwistEntries.FirstOrDefault(x => String.Equals(x.Title, name, StringComparison.OrdinalIgnoreCase) ||
                String.Equals(x.AltTitle, name, StringComparison.OrdinalIgnoreCase));

            return entry;
        }

        public async Task<TwistEntry> GetEntryAsync(int malid)
        {
            if ((DateTime.Now - CirnoBot.Data.TwistLastUpdated).TotalDays > 1)
            {
                await UpdateDatabaseAsync();
                CirnoBot.Data.TwistLastUpdated = DateTime.Now;
                File.WriteAllText("data.json", JsonConvert.SerializeObject(CirnoBot.Data));
            }

            return context.TwistEntries.FirstOrDefault(x => x.MalId.HasValue && x.MalId.Value == malid);
        }

        private async Task UpdateDatabaseAsync()
        {
            context.Database.ExecuteSqlCommand("DELETE FROM TwistEntries");
            await context.TwistEntries.AddRangeAsync(await GetAnimeDataAsync());
            await context.SaveChangesAsync();
        }

        public async Task<List<TwistEntry>> GetAnimeDataAsync()
        {
            HtmlDocument page = new HtmlDocument();
            page.LoadHtml(await client.GetStringAsync(BaseUrl));
            HtmlNode node = page.DocumentNode.Descendants().First(x => x.InnerText.StartsWith("window.__NUXT__="));
            string json = node.InnerText.Replace("window.__NUXT__=", "").Trim(';');
            JObject data = (JObject)JsonConvert.DeserializeObject(json);
            JArray anime = (JArray)data["state"]["anime"]["all"];

            List<TwistEntry> entries = new List<TwistEntry>();

            foreach (JObject x in anime)
            {
                entries.Add(new TwistEntry
                {
                    Id = (int)x["id"],
                    Title = (string)x["title"],
                    AltTitle = (string)x["alt_title"],
                    MalId = String.IsNullOrWhiteSpace(x["mal_id"].ToString()) ? (int?)null : (int)x["mal_id"],
                    Slug = (string)x["slug"]["slug"]
                });
            }

            return entries;
        }
    }
}
