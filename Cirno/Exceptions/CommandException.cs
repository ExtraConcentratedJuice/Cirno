using CirnoBot;
using System;

namespace CirnoBot.Exceptions
{
    public class CommandException : Exception
    {
        public CirnoCommand Command { get; set; }
        public CommandContext Context { get; set; }
        public Exception Exception { get; set; }

        public CommandException(CommandContext context, Exception exception, CirnoCommand command)
        {
            Context = context;
            Exception = exception;
            Command = command;
        }
    }
}