using System;
using System.Collections.Generic;
using System.Text;
using Discord.WebSocket;
using Discord;
using System.Linq;
using CirnoBot.Http;
using System.Threading.Tasks;
using System.Net.Http;

namespace CirnoBot.Commands.Imageboard
{
    public class CommandCountDanbooru : CirnoCommand
    {
        #region Properties

        public override string Name => "countdanbooru";

        public override string Description => "Counts all posts with the specified tags on Danbooru.";

        public override string Syntax => "countdanbooru <tags>";

        public override List<string> Aliases => new List<string> { "cdanbooru" };

        public override float Cooldown => 2.5F;

        #endregion

        public override async Task InvokeAsync(CommandContext ctx, string[] args)
        {
            if (args.Length < 1)
            {
                await ctx.ReplyAsync(Util.GenerateInvalidUsage(ctx.Bot, this));
                return;
            }

            List<string> tagList = args.Distinct().OrderBy(x => x).Select(x => x.Trim()).ToList();
            List<string> sortParams = args.Where(x => x.Contains(":")).Distinct().OrderBy(x => x).Select(x => x.Trim()).ToList();
            tagList.RemoveAll(x => x.Contains(":"));
            tagList.AddRange(sortParams);

            string tags = String.Join(" ", tagList.ToArray());

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
            

            await ctx.ReplyAsync($"Total amount of posts with the tags ``{tags}`` on Danbooru: **{count}**");
        }
    }
}
