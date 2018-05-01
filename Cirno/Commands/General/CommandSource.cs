using System;
using System.Collections.Generic;
using System.Text;
using Discord.WebSocket;
using Discord;

namespace CirnoBot.Commands.General
{
    public class CommandSource : CirnoCommand
    {
        #region Properties

        public override string Name => "source";

        public override string Description => "Sends a link to the bot's source code.";

        public override string Syntax => "source";

        public override List<string> Aliases => new List<string> { "sauce" };

        public override int Cooldown => 0;

        #endregion

        public override async void Invoke(CommandContext ctx, string[] args) =>
            await ctx.ReplyAsync("https://github.com/extraconcentratedjuice/Cirno");
    }
}
