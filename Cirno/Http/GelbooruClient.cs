using CirnoBot.Entities;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Web;
using System.Xml.Linq;

namespace CirnoBot.Http
{
    public class GelbooruClient : BooruClient
    {
        public GelbooruClient(CirnoContext context) : base(context) { }

        protected override string BaseUrl => "https://gelbooru.com";

        public override async Task<int> GetImageCountAsync(string tags)
        {
            var cache = context.GelbooruCountCache.FirstOrDefault(x => x.Tags == tags);

            if (cache != null && (DateTime.Now - cache.LastChecked).TotalDays < 1)
                return cache.Count;

            var query = HttpUtility.ParseQueryString(String.Empty);

            query["tags"] = tags;
            query["page"] = "dapi";
            query["s"] = "post";
            query["q"] = "index";
            query["limit"] = "0";

            string endp = $"{BaseUrl}/index.php?{query.ToString()}";

            XElement root = XElement.Parse(await client.GetStringAsync(endp));

            int count = int.TryParse(root.Attribute("count").Value, out int res) ? res : 0;

            if (cache != null)
            {
                cache.Count = count;
                cache.LastChecked = DateTime.Now;
            }
            else
                context.GelbooruCountCache.Add(new GelbooruCountCache(tags, count, DateTime.Now));

            if (count < 1)
                return count;

            await context.SaveChangesAsync();

            return count;
        }

        public async override Task<Dictionary<int, string>> GetPostsAsync(string tags, int page, int limit)
        {
            var query = HttpUtility.ParseQueryString(String.Empty);

            query["tags"] = tags;
            query["page"] = "dapi";
            query["s"] = "post";
            query["q"] = "index";
            query["pid"] = page.ToString();
            query["limit"] = limit.ToString();
            query["json"] = "1";

            string endp = $"{BaseUrl}/index.php?{query.ToString()}";

            string data = await client.GetStringAsync(endp);

            JArray json = (JArray)JsonConvert.DeserializeObject(data);

            Dictionary<int, string> urls = new Dictionary<int, string>();

            foreach (var x in json)
            {
                int id = x["id"].ToObject<int>();
                string u = x["file_url"]?.ToObject<string>();

                if (u != null && !u.EndsWith(".webm"))
                    urls[id] = u;
            }

            return urls;
        }
    }
}
