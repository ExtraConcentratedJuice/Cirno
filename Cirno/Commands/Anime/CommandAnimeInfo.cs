﻿using System;
using System.Collections.Generic;
using System.Text;
using Discord.WebSocket;
using Discord;
using CirnoBot.Http;
using CirnoBot.Entities;
using System.Linq;
using System.Text.RegularExpressions;
using System.Web;
using System.Threading.Tasks;
using System.Net.Http;

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

        public override async Task InvokeAsync(CommandContext ctx, string[] args)
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

            var client = new MalClient(ctx.Bot.Configuration.MALUsername, ctx.Bot.Configuration.MALPassword);

            MALAnimeEntry entry;
            try { entry = await client.FirstAnimeAsync(animeName); }
            catch (HttpRequestException e)
            {
                Console.WriteLine(e.ToString());
                await ctx.ReplyAsync("The request to the API failed. Looks like the service might be down, try again later.");
                return;
            }

            if (entry == null)
            {
                await ctx.ReplyAsync("No results were found for your query.");
                return;
            }

            string desc = Util.BBCodeToMarkdown(HttpUtility.HtmlDecode(Regex.Replace(entry.Synopsis, @"<(?:[^>=]|='[^']*'|=""[^""]*""|=[^'""][^\s>]*)*>", "")));

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
