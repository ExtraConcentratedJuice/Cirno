using System;
using System.Collections.Generic;
using System.Text;
using Discord.WebSocket;
using Discord;

namespace CirnoBot.Commands
{
    public class CommandHelp : CirnoCommand
    {
        #region Properties

        public override string Name => "help";

        public override string Description => "All commands in one list.";

        public override string Syntax => "help";

        public override List<string> Aliases => new List<string> { "halp" };

        public override int Cooldown => 0;

        #endregion

        public override async void Invoke(CommandContext ctx, string[] args)
        {
            EmbedBuilder embed = new EmbedBuilder
            {
                Title = "⑨ Manual",
                Description = "(Previously Robo-Fuhrer, Nitori.)\nThe official Cirno manual.\nW o r k I n P r o g r e s s"
            };

            foreach (CirnoCommand c in ctx.Bot.Commands.Commands)
            {
                string field = $"{c.Description}\n**Syntax**: ``{ctx.Bot.Configuration.Prefix}{c.Syntax}``";

                if (c.Aliases.Count > 0)
                    field += $"\n**Aliases**: {String.Join(", ", c.Aliases.ToArray()).TrimEnd(' ').TrimEnd(',')}";

                embed.AddField(ctx.Bot.Configuration.Prefix + c.Name, field);
            }

            await ctx.ReplyAsync(embed.Build());
        }
    }
}
