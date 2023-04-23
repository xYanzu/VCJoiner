import discord
import asyncio
import colorama
from colorama import Fore, Style
import os

colorama.init(autoreset=True)
os.system('cls' if os.name == 'nt' else 'clear')

BANNER = """
 ██▒   █▓ ▄████▄   ▄▄▄██▀▀▀▒█████   ██▓ ███▄    █ ▓█████  ██▀███  
▓██░   █▒▒██▀ ▀█     ▒██  ▒██▒  ██▒▓██▒ ██ ▀█   █ ▓█   ▀ ▓██ ▒ ██▒
 ▓██  █▒░▒▓█    ▄    ░██  ▒██░  ██▒▒██▒▓██  ▀█ ██▒▒███   ▓██ ░▄█ ▒
  ▒██ █░░▒▓▓▄ ▄██▒▓██▄██▓ ▒██   ██░░██░▓██▒  ▐▌██▒▒▓█  ▄ ▒██▀▀█▄  
   ▒▀█░  ▒ ▓███▀ ░ ▓███▒  ░ ████▓▒░░██░▒██░   ▓██░░▒████▒░██▓ ▒██▒
   ░ ▐░  ░ ░▒ ▒  ░ ▒▓▒▒░  ░ ▒░▒░▒░ ░▓  ░ ▒░   ▒ ▒ ░░ ▒░ ░░ ▒▓ ░▒▓░
   ░ ░░    ░  ▒    ▒ ░▒░    ░ ▒ ▒░  ▒ ░░ ░░   ░ ▒░ ░ ░  ░  ░▒ ░ ▒░
     ░░  ░         ░ ░ ░  ░ ░ ░ ▒   ▒ ░   ░   ░ ░    ░     ░░   ░ 
      ░  ░ ░       ░   ░      ░ ░   ░           ░    ░  ░   ░     
     ░   ░                                                        
                         By Yanzu
"""
print(Fore.MAGENTA + BANNER)

async def run_bot():
    await asyncio.sleep(5)

    print(Fore.YELLOW + "> - Please choose an option:")
    print(Fore.GREEN + "1 [+] Connect to VC Token")
    print(Fore.GREEN + "2 [+] Disconnect from VC Token")
    print(Fore.RED + "3 [+] Exit")
    choice = input()

    if choice in ["1", "2"]:
        channel_id = input(Fore.YELLOW + "> - Enter the ID of the voice channel to join: ")
    else:
        exit()

    async def join_voice(token):
        client = discord.Client()

        @client.event
        async def on_ready():
            print(Fore.GREEN + f'> - Logged in as {client.user}')
            channel = client.get_channel(int(channel_id))
            if channel and channel.type == discord.ChannelType.voice:
                try:
                    vc = await channel.connect()
                except discord.errors.ClientException:
                    print(Fore.RED + "> - Already connected to a voice channel.")
            else:
                print(Fore.RED + "> - Invalid voice channel ID.")

        await client.start(token)

    async def disconnect_voice(token):
        client = discord.Client()

        @client.event
        async def on_ready():
            print(Fore.GREEN + f'> - Disconnected as {client.user}')
            channel = client.get_channel(int(channel_id))
            if channel and channel.type == discord.ChannelType.voice:
                try:
                    vc = await channel.connect()
                    await vc.disconnect()
                except discord.errors.ClientException:
                    print(Fore.RED + "> - Already connected to a voice channel.")
            else:
                print(Fore.RED + "> - Invalid voice channel ID.")

        try:
            await client.start(token)
        except discord.LoginFailure:
            print(Fore.RED + f"> - Invalid token: {token}")

    with open("tokens.txt") as f:
        tokens = f.read().splitlines()

    if choice == "1":
        tasks = [asyncio.create_task(join_voice(token)) for token in tokens]
        print(Fore.YELLOW + f"> - Connecting {len(tokens)} tokens to voice channel...")
    elif choice == "2":
        tasks = [asyncio.create_task(disconnect_voice(token)) for token in tokens]
        print(Fore.YELLOW + f"> - Disconnecting {len(tokens)} tokens from voice channel...")
    else:
        print(Fore.RED + "> - Invalid choice. Please type 1 or 2.")
        tasks = []

    await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(run_bot())
