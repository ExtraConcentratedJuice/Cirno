using System;
using System.Collections.Generic;
using System.Text;
using Discord.WebSocket;
using Discord;
using System.Linq;
using System.Threading.Tasks;

namespace CirnoBot.Commands.General
{
    public class CommandHelp : CirnoCommand
    {
        #region Properties

        public override string Name => "help";

        public override string Description => "All commands in one list.";

        public override string Syntax => "help [group]";

        public override List<string> Aliases => new List<string> { "halp" };

        public override float Cooldown => 4F;

        #endregion

        public override async Task InvokeAsync(CommandContext ctx, string[] args)
        {
            var commands = ctx.Bot.Commands.Commands.GroupBy(x => x.GetType().Namespace.Split('.').Last().Trim(' ').Trim(','));

            if (args.Length < 1)
            {
                EmbedBuilder embed = new EmbedBuilder
                {
                    Color = Util.CyanColor,
                    Title = "⑨ Manual",
                    Description = "(Previously Robo-Fuhrer, Nitori.)\nW o r k I n P r o g r e s s\nThe official Cirno manual.\n\nDo ``/help [group]`` to get more information on a command group."
                };

                foreach (var c in commands)
                {
                    string name = c.Key;
                    string field = String.Join(", ", c.Where(x => !x.IsHidden).Select(x => $"``{x.Name}``").ToArray()).Trim(' ').Trim(',');
                    embed.AddField(name, field);
                }

                await ctx.ReplyAsync(embed.Build());
            }
            else
            {
                var group = commands.FirstOrDefault(x => String.Equals(x.Key, args[0], StringComparison.OrdinalIgnoreCase));

                if (group == null)
                {
                    await ctx.ReplyAsync($"No command group by that name was found. Existing groups:\n {String.Join(", ", commands.Select(x => x.Key)).Trim(' ').Trim(',')}");
                    return;
                }

                EmbedBuilder embed = new EmbedBuilder
                {
                    Color = Util.CyanColor,
                    Title = "⑨ Manual",
                    Description = $"Commands in the group '{group.Key}'"
                };

                foreach (CirnoCommand c in group)
                {
                    if (c.IsHidden)
                        continue;

                    string field = $"{c.Description}\n**Syntax**: ``{ctx.Bot.Configuration.Prefix}{c.Syntax}``";

                    if (c.Aliases.Count > 0)
                        field += $"\n**Aliases**: {String.Join(", ", c.Aliases.ToArray()).TrimEnd(' ').TrimEnd(',')}";

                    embed.AddField(ctx.Bot.Configuration.Prefix + c.Name, field);
                }

                await ctx.ReplyAsync(embed.Build());
            }
        }
    }
}
