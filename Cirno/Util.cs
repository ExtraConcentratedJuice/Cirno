using Discord;
using Discord.WebSocket;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace CirnoBot
{
    public static class Util
    {
        public static Color CyanColor { get => new Color(81, 172, 214); }

        public static string GenerateInvalidUsage(CirnoBot bot, CirnoCommand command) =>
            $"Invalid parameters.\nUsage: ``{bot.Configuration.Prefix}{command.Syntax}``";

        public static SocketTextChannel ParseChannel(string channel, DiscordSocketClient client)
        {
            if (ulong.TryParse(new String(channel.Where(x => Char.IsDigit(x)).ToArray()), out ulong cId))
            {
                return client.GetChannel(cId) as SocketTextChannel;
            }
            else
                return null;

        }


    }
}
