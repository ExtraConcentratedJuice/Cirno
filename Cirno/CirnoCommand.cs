using CirnoBot.Entities;
using Discord.WebSocket;
using System;
using System.Collections.Generic;
using System.Text;
using System.Threading.Tasks;

namespace CirnoBot
{
    public abstract class CirnoCommand
    {
        public abstract string Name { get; }
        public abstract string Description { get; }
        public abstract string Syntax { get; }
        public abstract List<string> Aliases { get; }
        public abstract float Cooldown { get; }
        public virtual bool IsHidden { get => false; }
        public Dictionary<ulong, DateTime> CooldownTable { get; } = new Dictionary<ulong, DateTime>();

        public abstract Task Invoke(CommandContext ctx, string[] args);
    }
}
