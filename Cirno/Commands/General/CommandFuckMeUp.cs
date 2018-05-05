using System;
using System.Collections.Generic;
using System.Text;
using Discord.WebSocket;
using Discord;

namespace CirnoBot.Commands.General
{
    public class CommandFuckMeUp : CirnoCommand
    {
        #region Properties

        public override string Name => "fuckmeup";

        public override string Description => "Fucks up some text.";

        public override string Syntax => "fuckmeup <text>";

        public override List<string> Aliases => new List<string>();

        public override float Cooldown => 2.5F;

        private readonly Dictionary<char, char> letterMappings = new Dictionary<char, char>
        {
            {'a', 'ɐ'},
            {'b', 'q'},
            {'c', 'ɔ'},
            {'d', 'p'},
            {'e', 'ǝ'},
            {'f', 'ɟ'},
            {'g', 'ƃ'},
            {'h', 'ɥ'},
            {'i', 'ᴉ'},
            {'j', 'ɾ'},
            {'k', 'ʞ'},
            {'l', 'l'},
            {'m', 'ɯ'},
            {'n', 'u'},
            {'o', 'o'},
            {'p', 'd'},
            {'q', 'b'},
            {'r', 'ɹ'},
            {'s', 's'},
            {'t', 'ʇ'},
            {'u', 'n'},
            {'v', 'ʌ'},
            {'w', 'ʍ'},
            {'y', 'ʎ'},
            {'x', 'x'},
            {'z', 'z'}
        };

        #endregion

        public override async void Invoke(CommandContext ctx, string[] args)
        {
            if (args.Length < 1)
            {
                await ctx.ReplyAsync(Util.GenerateInvalidUsage(ctx.Bot, this));
                return;
            }

            List<char> letters = new List<char>();
            string message = String.Join(' ', args);

            for (int i = 0; i < message.Length; i++)
            {
                char c = message[i];
                letters.Insert(0, letterMappings.TryGetValue(c, out char ch) ? ch : c);
            }

            await ctx.ReplyAsync(new string(letters.ToArray()));
        }
    }
}
