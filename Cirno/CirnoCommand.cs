using CirnoBot.Entities;
using Discord.WebSocket;
using System;
using System.Collections.Generic;
using System.Text;

namespace CirnoBot
{
    public abstract class CirnoCommand
    {
        public abstract string Name { get; }
        public abstract string Description { get; }
        public abstract string Syntax { get; }
        public abstract List<string> Aliases { get; }
        public abstract int Cooldown { get; }

        public abstract void Invoke(CommandContext ctx, string[] args);
    }
}
