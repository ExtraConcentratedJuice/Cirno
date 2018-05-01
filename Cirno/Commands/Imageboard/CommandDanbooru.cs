using System;
using System.Collections.Generic;
using System.Text;
using Discord.WebSocket;
using Discord;
using CirnoBot.Http;
using System.Linq;

namespace CirnoBot.Commands.Imageboard
{
    public class CommandDanbooru : CirnoCommand
    {
        #region Properties

        public override string Name => "danbooru";

        public override string Description => "Grabs a random post from the Danbooru imageboard with the specified tags.";

        public override string Syntax => "danbooru <tags>";

        public override List<string> Aliases => new List<string> { "dbooru" };

        public override int Cooldown => 0;

        #endregion

        public override async void Invoke(CommandContext ctx, string[] args)
        {
            if (args.Length < 1)
            {
                await ctx.ReplyAsync("Invalid parameters.\nUsage: " + ctx.Bot.Configuration.Prefix + Syntax);
                return;
            }

            List<string> tagList = args.Distinct().OrderBy(x => x).Select(x => x.Trim()).ToList();
            List<string> sortParams = args.Where(x => x.Contains(":")).Distinct().OrderBy(x => x).Select(x => x.Trim()).ToList();
            tagList.RemoveAll(x => x.Contains(":"));
            tagList.AddRange(sortParams);

            if (ctx.Channel is ITextChannel ch && !ch.IsNsfw)
            {
                tagList.RemoveAll(x => String.Equals("rating:explicit", x, StringComparison.OrdinalIgnoreCase) ||
                    String.Equals("rating:questionable", x, StringComparison.OrdinalIgnoreCase));

                tagList.Add("rating:safe");
            }

            string tags = String.Join(' ', tagList.ToArray());

            if (tagList.Count > 2)
            {
                await ctx.ReplyAsync($"You supplied too many tags. Danbooru has a limit of two tags per query. Your tags: ``{tags}``");
                return;
            }

            var client = new DanbooruClient(ctx.DbContext);

            int count = await client.GetImageCountAsync(tags);

            if (count < 1)
            {
                await ctx.ReplyAsync("No posts were found for that tag.");
                return;
            }

            Random r = new Random();

            int limit = 20;

            Dictionary<int, string> urls = await client.GetPostsAsync(tags, r.Next(count / limit > 1000 ? 1000 : count / limit), limit);

            if (urls.Count < 1)
            {
                await ctx.ReplyAsync("No posts were found for that tag.");
                return;
            }

            KeyValuePair<int, string> url = urls.ElementAt(r.Next(urls.Count));

            EmbedBuilder embed = new EmbedBuilder
            {
                Title = $"tags: {tags}",
                Url = $"https://danbooru.donmai.us/posts/{url.Key}",
                ImageUrl = url.Value,
                Color = Util.CyanColor
            };

            embed.WithFooter("https://danbooru.donmai.us", "http://i.imgur.com/4Wjm9rb.png");

            await ctx.ReplyAsync(embed.Build());
        }
    }
}
