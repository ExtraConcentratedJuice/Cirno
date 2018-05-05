using System;
using System.Collections.Generic;
using System.Text;
using Discord.WebSocket;
using Discord;
using CirnoBot.Http;
using System.Linq;
using System.Threading.Tasks;
using System.Net.Http;

namespace CirnoBot.Commands.Imageboard
{
    public class CommandHentaiBomb : CirnoCommand
    {
        #region Properties

        public override string Name => "hentaibomb";

        public override string Description => "Please no";

        public override string Syntax => "hentaibomb <tags>";

        public override List<string> Aliases => new List<string>();

        public override float Cooldown => 10F;

        public override bool IsHidden { get => true; }

        #endregion

        public override async Task InvokeAsync(CommandContext ctx, string[] args)
        {
            if (args.Length < 1)
            {
                await ctx.ReplyAsync(Util.GenerateInvalidUsage(ctx.Bot, this));
                return;
            }

            if (ctx.Channel is ITextChannel ch && !ch.IsNsfw)
            {
                await ctx.ReplyAsync("gtfo homo nsfw or nothing");
                return;
            }

            args[0] = args[0] + " -rating:safe";
            List<string> tagList = args.Distinct().OrderBy(x => x).Select(x => x.Trim()).ToList();
            List<string> sortParams = args.Where(x => x.Contains(":")).Distinct().OrderBy(x => x).Select(x => x.Trim()).ToList();
            tagList.RemoveAll(x => x.Contains(":"));
            tagList.AddRange(sortParams);

            string tags = String.Join(' ', tagList.ToArray());

            if (tagList.Count > 2)
            {
                await ctx.ReplyAsync($"You supplied too many tags. Danbooru has a limit of two tags per query. Your tags: ``{tags}``");
                return;
            }

            var client = new DanbooruClient(ctx.DbContext);

            int count;
            try { count = await client.GetImageCountAsync(tags); }
            catch (HttpRequestException e)
            {
                Console.WriteLine(e.ToString());
                await ctx.ReplyAsync("The request to the API failed. Looks like the service might be down, try again later.");
                return;
            }

            if (count < 1)
            {
                await ctx.ReplyAsync("No posts were found for that tag.");
                return;
            }

            Random r = new Random();

            int limit = 20;

            Dictionary<int, string> urls;
            try { urls = await client.GetPostsAsync(tags, r.Next(count / limit > 1000 ? 1000 : count / limit), limit); }
            catch (HttpRequestException e)
            {
                Console.WriteLine(e.ToString());
                await ctx.ReplyAsync("The request to the API failed. Looks like the service might be down, try again later.");
                return;
            }

            if (urls.Count < 1)
            {
                await ctx.ReplyAsync("No posts were found for that tag.");
                return;
            }

            var urlList = urls.OrderBy(x => r.Next()).Take(r.Next(2, 5));

            foreach (var url in urlList)
            {
                EmbedBuilder e = new EmbedBuilder
                {
                    Title = $"tags: {tags}",
                    Url = $"https://danbooru.donmai.us/posts/{url.Key}",
                    ImageUrl = url.Value,
                    Color = Util.CyanColor
                };
                e.WithFooter("https://danbooru.donmai.us", "http://i.imgur.com/4Wjm9rb.png");

                try { await ctx.Author.SendMessageAsync("", embed: e.Build()); }
                catch (Exception) { await ctx.ReplyAsync("Something went wrong. Do you have your DMs disabled?"); break; }
            }

            await ((IUserMessage)ctx.Message).AddReactionAsync(new Emoji("👌"));
        }
    }
}
