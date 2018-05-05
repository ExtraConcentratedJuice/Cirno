using System;
using System.Collections.Generic;
using System.Text;
using Discord.WebSocket;
using Discord;
using System.Threading.Tasks;

namespace CirnoBot.Commands.Other
{
    public class CommandInfo : CirnoCommand
    {
        #region Properties

        public override string Name => "info";

        public override string Description => "Gives some information regarding Cirno.";

        public override string Syntax => "info";

        public override List<string> Aliases => new List<string>();

        public override float Cooldown => 5F;

        #endregion

        public override async Task InvokeAsync(CommandContext ctx, string[] args) =>
            await ctx.ReplyAsync(new EmbedBuilder
            {
                Color = Util.CyanColor,
                Title = "Information",
                Description = "Some brief details regarding Cirno.",
                ThumbnailUrl = ctx.Bot.Client.CurrentUser.GetAvatarUrl(),
                Author = new EmbedAuthorBuilder
                {
                    Name = ctx.Bot.Client.CurrentUser.Username,
                    IconUrl = ctx.Bot.Client.CurrentUser.GetAvatarUrl()
                },
                Fields = new List<EmbedFieldBuilder>
                {
                    new EmbedFieldBuilder
                    {
                        Name = "Library",
                        Value = $"discord.net ({typeof(DiscordSocketClient).Assembly.GetName().Version})",
                        IsInline = false
                    },
                    new EmbedFieldBuilder
                    {
                        Name = "Author",
                        Value = $"{(await ctx.Bot.Client.GetApplicationInfoAsync()).Owner.ToString()}",
                        IsInline = false
                    },
                    new EmbedFieldBuilder
                    {
                        Name = "Guild Count",
                        Value = Util.GuildCount(ctx.Bot),
                        IsInline = false
                    },
                    new EmbedFieldBuilder
                    {
                        Name = "Latency",
                        Value = ctx.Bot.Client.Latency + "ms",
                        IsInline = false
                    }
                }
            }.Build());
    }
}
