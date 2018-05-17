using System;
using System.Collections.Generic;
using System.Text;
using Discord.WebSocket;
using Discord;
using System.Threading.Tasks;
using Microsoft.CodeAnalysis.CSharp.Scripting;
using Microsoft.CodeAnalysis.Scripting;
using System.Linq;

namespace CirnoBot.Commands.General
{
    public class CommandEval : CirnoCommand
    {
        #region Properties

        public override string Name => "eval";

        public override string Description => "Evaluates a segment of C# code.";

        public override string Syntax => "eval <code>";

        public override List<string> Aliases => new List<string>();

        public override float Cooldown => 1F;

        public override bool IsOwner => true;

        public override bool IsHidden => true;

        #endregion

        public override async Task InvokeAsync(CommandContext ctx, string[] args)
        {
            try
            {
                object output = (await CSharpScript.EvaluateAsync(
                    String.Join(' ', args),
                    ScriptOptions.Default
                        .WithReferences(AppDomain.CurrentDomain.GetAssemblies().Where(x => !x.IsDynamic && !String.IsNullOrWhiteSpace(x.Location)))
                    ,
                    globals: new Globals(ctx)));

                if (output != null)
                    await ctx.ReplyAsync("``" + output.ToString() + "``");
            }
            catch (Exception e) { await ctx.ReplyAsync($"Exception: ``{e.GetType().Name}: {e.Message}``"); Console.WriteLine(e.ToString()); }
        }
            

        public class Globals
        {
            public Globals(CommandContext ctx)
            {
                Context = ctx;
            }

            public CommandContext Context { get; }
        }
    }
}
