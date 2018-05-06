using CirnoBot.Entities;
using CirnoBot.Exceptions;
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
        public virtual bool IsOwner { get => false; }
        public Dictionary<ulong, DateTime> CooldownTable { get; } = new Dictionary<ulong, DateTime>();

        public abstract Task InvokeAsync(CommandContext ctx, string[] args);

        internal async Task InvokeInternalAsync(CommandContext ctx, string[] args)
        {
            if (IsOwner && !ctx.Bot.Configuration.OwnerIds.Contains(ctx.Author.Id))
                return;

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
}
