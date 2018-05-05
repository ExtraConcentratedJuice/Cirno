using System;
using System.Collections.Generic;
using System.Text;
using Discord.WebSocket;
using Discord;
using System.Threading.Tasks;

namespace CirnoBot.Commands.General
{
    public class CommandSource : CirnoCommand
    {
        #region Properties

        public override string Name => "source";

        public override string Description => "Sends a link to the bot's source code.";

        public override string Syntax => "source";

        public override List<string> Aliases => new List<string> { "sauce" };

        public override float Cooldown => 4F;

        #endregion

        public override async Task InvokeAsync(CommandContext ctx, string[] args) =>
            await ctx.ReplyAsync("https://github.com/extraconcentratedjuice/Cirno");
    }
}
