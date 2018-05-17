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
using System.Threading.Tasks;
using System.Net.Http;
using System.Net;

namespace CirnoBot.Commands.Anime
{
    public class CommandAnimeStream : CirnoCommand
    {
        #region Properties

        public override string Name => "animestream";

        public override string Description => "Grabs a specified anime's stream from https://twist.moe";

        public override string Syntax => "animestream <name>";

        public override List<string> Aliases => new List<string>();

        public override float Cooldown => 8F;

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

            MalClient m = new MalClient(ctx.Bot.Configuration.MALUsername, ctx.Bot.Configuration.MALPassword);

            MALAnimeEntry anime = await m.FirstAnimeAsync(animeName);

            if (anime == null)
            {
                await ctx.ReplyAsync("We couldn't find that anime in the MAL database. Try an alternate name.");
                return;
            }

            var client = new TwistClient(ctx.DbContext);

            TwistEntry entry = await client.GetEntryAsync(anime.Id) ?? await client.GetEntryAsync(anime.Title);

            EmbedBuilder embed; 
            if (entry == null)
            {
                embed = new EmbedBuilder
                {
                    Title = "Anime Not Found",
                    Color = Util.CyanColor,
                    ThumbnailUrl = anime.Image,
                    Description = $"*{anime.Title}* wasn't found on twist.moe. Some possible alternate sources are listed below for your convenience."
                };

                embed.AddField("Alternate Sources", $"[Nyaa](https://nyaa.pantsu.cat/search?c=_&userID=0&q={WebUtility.UrlEncode(anime.Title)})\n[KissAnime](http://kissanime.ru/Search/Anime?keyword={WebUtility.UrlEncode(anime.Title)})");

                await ctx.ReplyAsync(embed.Build());
                return;
            }

            string desc = Util.BBCodeToMarkdown(HttpUtility.HtmlDecode(Regex.Replace(anime.Synopsis, @"<(?:[^>=]|='[^']*'|=""[^""]*""|=[^'""][^\s>]*)*>", "")));

            embed = new EmbedBuilder
            {
                Title = entry.Url,
                Url = entry.Url,
                ThumbnailUrl = anime.Image,
                Color = Util.CyanColor,
                Description = $"A stream was located for *{anime.Title}* on twist.moe. Click the link above to continue.\n\n[MAL Entry](https://myanimelist.net/anime/{anime.Id}/)"
            };
            embed.AddField("Description", desc.Length > 1024 ? desc.Substring(0, 1021) + "..." : desc);
            embed.WithFooter("https://twist.moe", "https://twist.moe/public/icons/fav_x16.png");

            await ctx.ReplyAsync(embed.Build());
        }
    }
}
