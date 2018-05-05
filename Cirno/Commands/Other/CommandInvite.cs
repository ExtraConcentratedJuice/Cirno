using System;
using System.Collections.Generic;
using System.Text;
using Discord.WebSocket;
using Discord;
using System.Threading.Tasks;

namespace CirnoBot.Commands.Other
{
    public class CommandInvite : CirnoCommand
    {
        #region Properties

        public override string Name => "invite";

        public override string Description => "Sends an invite that can be used to add Cirno to servers.";

        public override string Syntax => "invite";

        public override List<string> Aliases => new List<string>();

        public override float Cooldown => 5F;

        #endregion

        public override async Task Invoke(CommandContext ctx, string[] args) =>
            await ctx.ReplyAsync("https://discordapp.com/oauth2/authorize?client_id=338414455291510785&scope=bot&permissions=201850055");
    }
}
