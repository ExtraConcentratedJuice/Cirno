using CirnoBot.Entities;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Web;

namespace CirnoBot.Http
{
    public class DanbooruClient : BooruClient
    {
        public DanbooruClient(CirnoContext context) : base(context) { }
        
        protected override string BaseUrl() => 
            "https://danbooru.donmai.us";

        public async Task<int> GetImageCountAsync(string tags)
        {
            var cache = context.DanbooruCountCache.FirstOrDefault(x => x.Tags == tags);

            if (cache != null && (DateTime.Now - cache.LastChecked).TotalDays < 1)
                return cache.Count;

            var query = HttpUtility.ParseQueryString(String.Empty);

            query["tags"] = tags;

            string endp = $"{BaseUrl()}/counts/posts.json?{query.ToString()}";

            string data = await client.GetStringAsync(endp);

            dynamic json = JsonConvert.DeserializeObject(data);
            int count = json.counts.posts;

            if (count < 1)
                return count;

            if (cache != null)
            {
                cache.Count = count;
                cache.LastChecked = DateTime.Now;
            }
            else
                context.DanbooruCountCache.Add(new DanbooruCountCache(tags, count, DateTime.Now));

            await context.SaveChangesAsync();

            return count;
        }

        public async override Task<Dictionary<int, string>> GetPostsAsync(string tags, int page, int limit)
        {
            try
            {
                var query = HttpUtility.ParseQueryString(String.Empty);

                query["limit"] = limit.ToString();
                query["page"] = page.ToString();
                query["tags"] = tags;

                string endp = $"{BaseUrl()}/posts.json?{query.ToString()}";

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

            } catch(Exception e) { Console.WriteLine(e.ToString()); return new Dictionary<int, string>(); }
        }
    }
}
