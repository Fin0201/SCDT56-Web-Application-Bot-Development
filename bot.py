# bot.py
import os
import discord
from dotenv import load_dotenv



load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return


    if message.author.id == 418084307257786369:
        if "say something" in message.content.lower():
            await message.channel.send("Hello")



    if message.author.id == 618018877573431297 or message.author.id == 189758961984077824:
        if "say something" in message.content.lower():
            await message.channel.send("Hi")

            


    if "send a file" in message.content.lower():
        await message.channel.send("here's a video", file=discord.File('files\Logo.png'))

    
    if client.user.mention in message.content:
        await message.channel.send("Do you need me?")


client.run(TOKEN)