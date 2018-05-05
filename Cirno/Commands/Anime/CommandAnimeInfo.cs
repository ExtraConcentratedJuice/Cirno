using System;
using System.Collections.Generic;
using System.Text;
using Discord.WebSocket;
using Discord;
using CirnoBot.Http;
using CirnoBot.Entities;
using System.Linq;
using System.Text.RegularExpressions;
using System.Web;

namespace CirnoBot.Commands.Anime
{
    public class CommandAnimeInfo : CirnoCommand
    {
        #region Properties

        public override string Name => "animeinfo";

        public override string Description => "Grabs an anime's information from MAL.";

        public override string Syntax => "animeinfo <name>";

        public override List<string> Aliases => new List<string>();

        public override float Cooldown => 6F;

        #endregion

        public override async void Invoke(CommandContext ctx, string[] args)
        {
            if (args.Length < 1)
            {
                await ctx.ReplyAsync(Util.GenerateInvalidUsage(ctx.Bot, this));
                return;
            }

            string animeName = String.Join(' ', args);

            if (animeName.Length < 4)
            {
                await ctx.ReplyAsync("Please have your search query be more than four characters long.");
                return;
            }

            var client = new MALClient(ctx.Bot.Configuration.MALUsername, ctx.Bot.Configuration.MALPassword);

            List<MALAnimeEntry> results = await client.SearchAnimeAsync(animeName);

            if (results == null)
            {
                await ctx.ReplyAsync("No results were found for your query.");
                return;
            }

            MALAnimeEntry entry = await client.FirstAnimeAsync(animeName);

            string desc = HttpUtility.HtmlDecode(Regex.Replace(entry.Synopsis, @"<(?:[^>=]|='[^']*'|=""[^""]*""|=[^'""][^\s>]*)*>", ""));

            EmbedBuilder embed = new EmbedBuilder
            {
                Color = Util.CyanColor,
                Title = entry.Title,
                Description = desc.Length > 2000 ? desc.Substring(0, 1996) + "..." : desc,
                ThumbnailUrl = entry.Image
            };

            embed.AddField("Rating", entry.Score);
            embed.AddField("Episodes", entry.Episodes == 0 ? "Unknown" : entry.Episodes.ToString());
            embed.AddField("Type", entry.Type);
            embed.AddField("Status", entry.Status);
            embed.AddField("Started Airing", entry.StartDate == "0000-00-00" ? "N/A" : entry.StartDate);
            embed.AddField("Ended Airing", entry.EndDate == "0000-00-00" ? "N/A" : entry.EndDate);
            embed.WithFooter("https://myanimelist.net", "https://i.imgur.com/DcMFqr6.jpg");

            await ctx.ReplyAsync(embed.Build());
        }
    }
}
