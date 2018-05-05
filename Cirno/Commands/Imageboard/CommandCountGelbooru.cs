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
    public class CommandCountGelbooru : CirnoCommand
    {
        #region Properties

        public override string Name => "countgelbooru";

        public override string Description => "Counts all posts with the specified tags on Gelbooru.";

        public override string Syntax => "countgelbooru <tags>";

        public override List<string> Aliases => new List<string> { "cgelbooru" };

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

            string tags = String.Join(' ', tagList.ToArray());

            var client = new GelbooruClient(ctx.DbContext);

            int count;
            try { count = await client.GetImageCountAsync(tags); }
            catch (HttpRequestException e)
            {
                Console.WriteLine(e.ToString());
                await ctx.ReplyAsync("The request to the API failed. Looks like the service might be down, try again later.");
                return;
            }

            await ctx.ReplyAsync($"Total amount of posts with the tags ``{tags}`` on Gelbooru: **{count}**");
        }
    }
}
