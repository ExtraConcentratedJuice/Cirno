using CirnoBot.Entities;
using CirnoBot.Exceptions;
using Discord.WebSocket;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
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

        private async Task HandleExceptionAsync(CommandException e)
        {
            if (e == null)
                return;

            if (e.Exception is Discord.Net.HttpException ex && ex.HttpCode == HttpStatusCode.Forbidden)
            {
                await e.Context.ReplyAsync("Error! I didn't have permissions to do something. It's probably embeds, can you give me permission to embed links in this channel?");
                return;
            }

            Console.WriteLine(e.Exception.ToString());
            await e.Context.ReplyAsync($"An exception occurred while attempting to execute this command. Report this issue with ``{bot.Configuration.Prefix}issue <issue>``.");
        }

        public async Task OnMessageAsync(SocketMessage message)
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
                Task task = Task.Run(async () =>
                    await command.InvokeInternalAsync(new CommandContext(message, bot, new CirnoContext(bot.Configuration.ConnectionString)), args.ToArray()));

                task.ContinueWith(async t => await HandleExceptionAsync(t.Exception.Flatten().InnerException as CommandException), TaskContinuationOptions.OnlyOnFaulted);
            }
        }
    }
}
