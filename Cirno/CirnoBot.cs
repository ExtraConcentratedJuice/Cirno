using CirnoBot.Entities;
using Discord;
using Discord.WebSocket;
using Newtonsoft.Json;
using System;
using System.IO;
using System.Runtime.InteropServices;
using System.Threading.Tasks;

namespace CirnoBot
{
    public class CirnoBot
    {
        public Configuration Configuration { get; private set; }
        public DiscordSocketClient Client { get; private set; }
        public CommandHandler Commands { get; private set; }

        public async Task MainAsync()
        {
            Configuration = JsonConvert.DeserializeObject<Configuration>(File.ReadAllText("config.json"));

            Client = new DiscordSocketClient(new DiscordSocketConfig()
            {
                LogLevel = LogSeverity.Info,
                WebSocketProvider = Discord.Net.Providers.WS4Net.WS4NetProvider.Instance
            });

            Commands = new CommandHandler(this);

            Client.Log += async x => Console.WriteLine($"[{x.Severity.ToString()}] {x.Message}");
            Client.Ready += () => Client.SetGameAsync("c/help | cirYES", "https://twitch.tv/courierfive", ActivityType.Streaming);
            Client.MessageReceived += Commands.OnMessage;

            await Client.LoginAsync(TokenType.Bot, Configuration.Token);
            await Client.StartAsync();

            await Task.Delay(-1);
        }
    }
}
