using System;
using System.Collections.Generic;
using System.Text;
using Discord.WebSocket;
using Discord;
using System.Linq;
using CirnoBot.Http;

namespace CirnoBot.Commands
{
    public class CommandCountGelbooru : CirnoCommand
    {
        #region Properties

        public override string Name => "countgelbooru";

        public override string Description => "Counts all posts with the specified tags on Gelbooru.";

        public override string Syntax => "countgelbooru <tags>";

        public override List<string> Aliases => new List<string> { "cgelbooru" };

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

            string tags = String.Join(' ', tagList.ToArray());

            var client = new GelbooruClient(ctx.DbContext);

            int count = await client.GetImageCountAsync(tags);

            await ctx.ReplyAsync($"Total amount of posts with the tags ``{tags}`` on Gelbooru: **{count}**");
        }
    }
}
