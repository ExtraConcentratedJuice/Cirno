using System;
using System.Collections.Generic;
using System.Text;
using Discord.WebSocket;
using Discord;
using System.Linq;
using System.Threading.Tasks;

namespace CirnoBot.Commands.General
{
    public class CommandTopWords : CirnoCommand
    {
        #region Properties

        public override string Name => "topwords";

        public override string Description => "Gets 30 of the top words within a channel.";

        public override string Syntax => "topwords <#channel>";

        public override List<string> Aliases => new List<string>();

        public override float Cooldown => 10F;

        #endregion

        public override async Task InvokeAsync(CommandContext ctx, string[] args)
        {
            if (args.Length < 1)
            {
                await ctx.ReplyAsync(Util.GenerateInvalidUsage(ctx.Bot, this));
                return;
            }

            SocketTextChannel channel = Util.ParseTextChannel(args[0], ctx.Bot.Client);

            if (channel == null)
            {
                await ctx.ReplyAsync("Invalid channel provided.");
                return;
            }

            var messages = channel.GetMessagesAsync(10000).Flatten().GetEnumerator();

            Dictionary<string, int> words = new Dictionary<string, int>();

            using (ctx.Channel.EnterTypingState())
            {
                while (await messages.MoveNext())
                {
                    if (messages.Current.Author.IsBot)
                        continue;

                    if ((DateTime.Now - messages.Current.Timestamp).TotalDays > 7)
                        break;

                    string[] content = messages.Current.Content.Split(' ').Where(x => x.Length > 3 && x.Length < 25).ToArray();

                    foreach (string s in content)
                    {
                        string word = s.Trim('`').Trim(' ');

                        if (word.StartsWith("http") || word.Length <= 3)
                            continue;

                        if (words.ContainsKey(s))
                            words[word]++;
                        else
                            words[word] = 1;
                    }
                }
            }

            await ctx.ReplyAsync($"```Top 30 words in #{channel.Name} in the past 7 days:\n{String.Join('\n', words.OrderByDescending(x => x.Value).Take(30).Select(x => $"\"{x.Key}\", {x.Value} times").ToArray())}```");
        }
    }
}
