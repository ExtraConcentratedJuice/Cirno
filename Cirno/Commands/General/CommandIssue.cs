using System;
using System.Collections.Generic;
using System.Text;
using Discord.WebSocket;
using Discord;

namespace CirnoBot.Commands.General
{
    public class CommandIssue : CirnoCommand
    {
        #region Properties

        public override string Name => "issue";

        public override string Description => "Reports an issue to the bot's developer.";

        public override string Syntax => "issue <issue>";

        public override List<string> Aliases => new List<string> { "reportissue" };

        public override float Cooldown => 10F;

        #endregion

        public override async void Invoke(CommandContext ctx, string[] args)
        {
            if (args.Length < 1)
            {
                await ctx.ReplyAsync("Invalid parameters.\nUsage: " + ctx.Bot.Configuration.Prefix + Syntax);
                return;
            }

            EmbedBuilder embed = new EmbedBuilder
            {
                Title = ctx.Author.Username,
                Description = String.Join(' ', args)
            };

            embed.WithCurrentTimestamp();
            embed.AddField("Server", ctx.Guild?.Name ?? "Direct Message");
            embed.AddField("Channel", ctx.Channel.Id);

            await ((ITextChannel)ctx.Bot.Client.GetChannel(338421643879645186)).SendMessageAsync("", embed: embed.Build());
            await ((IUserMessage)ctx.Message).AddReactionAsync(new Emoji("👌"));
        }
    }
}
