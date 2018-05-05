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

        public abstract Task InvokeAsync(CommandContext ctx, string[] args);

        internal async Task InvokeInternalAsync(CommandContext ctx, string[] args)
        {
            if (CooldownTable.ContainsKey(ctx.Author.Id) && (DateTime.Now - CooldownTable[ctx.Author.Id]).TotalSeconds < Cooldown)
            {
                await ctx.Channel.SendMessageAsync($"You are on cooldown for this command. Seconds remaining: {(int)(Cooldown - (DateTime.Now - CooldownTable[ctx.Author.Id]).TotalSeconds)}");
                return;
            }

            try { await InvokeAsync(ctx, args); }
            catch (Exception e) { throw new CommandException(ctx, e, this); }
            finally
            {
                if (Cooldown > 0)
                    CooldownTable[ctx.Author.Id] = DateTime.Now;
            }
        }
    }

    public class CommandException : Exception
    {
        public CommandContext Context { get; set; }
        public Exception Exception { get; set; }
        public CirnoCommand Command { get; set; }

        public CommandException(CommandContext context, Exception exception, CirnoCommand command)
        {
            Context = context;
            Exception = exception;
            Command = command;
        }
    }
}
