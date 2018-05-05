using CirnoBot.Entities;
using Discord.WebSocket;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using System.Text;
using System.Threading.Tasks;

namespace CirnoBot
{
    public class CommandHandler
    {
        private readonly CirnoBot bot;
        public List<CirnoCommand> Commands { get; }

        public CommandHandler(CirnoBot bot)
        {
            this.bot = bot;
            Commands = new List<CirnoCommand>();

            var cmds = Assembly.GetExecutingAssembly().GetTypes()
              .Where(x => x.IsSubclassOf(typeof(CirnoCommand)));

            foreach (Type x in cmds)
                Commands.Add((CirnoCommand)Activator.CreateInstance(x));

            Commands = Commands.OrderBy(x => x.Name).ToList();
        }

        public async Task OnMessage(SocketMessage message)
        {
            string content = message.Content;
            SocketUser user = message.Author;

            if (!content.StartsWith(bot.Configuration.Prefix))
                return;

            List<string> args = content.Trim().Split(" ").ToList();

            string cmd = args[0];
            args.RemoveAt(0);

            CirnoCommand command = Commands.FirstOrDefault(x => 
                String.Equals(x.Name, cmd.Substring(bot.Configuration.Prefix.Length), StringComparison.OrdinalIgnoreCase) ||
                x.Aliases.Any(z => String.Equals(z, cmd.Substring(bot.Configuration.Prefix.Length))));

            if (command != null)
            {
                if (command.CooldownTable.ContainsKey(user.Id) && (DateTime.Now - command.CooldownTable[user.Id]).TotalSeconds < command.Cooldown)
                {
                    await message.Channel.SendMessageAsync($"You are on cooldown for this command. Seconds remaining: {(int)(command.Cooldown - (DateTime.Now - command.CooldownTable[user.Id]).TotalSeconds)}");
                    return;
                }

                try { command.Invoke(new CommandContext(message, bot, new CirnoContext(bot.Configuration.ConnectionString)), args.ToArray()); }
                catch (Exception e)
                {
                    Console.WriteLine(e.ToString());
                    await message.Channel.SendMessageAsync($"An exception occurred while attempting to execute this command. Report this issue with the {bot.Configuration.Prefix}issue command.");
                }
                finally
                {
                    if (command.Cooldown > 0)
                        command.CooldownTable[user.Id] = DateTime.Now;
                }
            }
        }
    }
}
