using Discord.WebSocket;
using System;
using Discord;
using System.Collections.Generic;
using System.Text;
using CirnoBot;
using CirnoBot.Entities;
using System.Threading.Tasks;

namespace CirnoBot
{
    public class CommandContext
    {
        public SocketMessage Message { get; }
        public SocketUser Author { get => Message.Author; }
        public ISocketMessageChannel Channel { get => Message.Channel; }
        public string Content { get => Message.Content; }
        public IGuild Guild { get => Channel is SocketGuildChannel x ? x.Guild : null; }
        public CirnoContext DbContext { get; }
        public CirnoBot Bot { get; }

        public CommandContext(SocketMessage msg, CirnoBot bot, CirnoContext db)
        {
            Bot = bot;
            Message = msg;
            DbContext = db;
        }

        public async Task ReplyAsync(string msg)
            => await Channel.SendMessageAsync(msg);

        public async Task ReplyAsync(Embed msg)
            => await Channel.SendMessageAsync("", embed: msg);
    }
}
