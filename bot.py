import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
import subprocess
import functools
import typing
import math
import uuid
import yt_dlp
import shutil
import asyncio



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




    if message.content.lower().startswith("!download "):
        splitCommand = message.content.split(" ")
        link = splitCommand[1]


        if "youtube.com/watch?v=" in link:
            splitId = link.split("youtube.com/watch?v=")
            tempId = splitId[1]
            splitId = tempId.split("&")
            tempId = splitId[0]
            splitId = tempId.split("?")
            tempId = splitId[0]
            splitId = tempId.split("#")
            id = splitId[0]
        elif "youtube.com/shorts/" in link:
            splitId = link.split("youtube.com/shorts/")
            tempId = splitId[1]
            splitId = tempId.split("&")
            tempId = splitId[0]
            splitId = tempId.split("?")
            tempId = splitId[0]
            splitId = tempId.split("#")
            id = splitId[0]
        elif "youtu.be" in link:
            splitId = link.split("youtu.be/")
            tempId = splitId[1]
            splitId = tempId.split("&")
            tempId = splitId[0]
            splitId = tempId.split("?")
            tempId = splitId[0]
            splitId = tempId.split("#")
            id = splitId[0]
        else:
            await message.channel.send("Invalid URL")
            return

        await message.channel.send("Beginning download")
        os.system("yt-dlp " + link)




        for files in os.walk('.', topdown=True):
            for i in files:
                for j in i:
                    if id in j:
                        filename = j
                        splitFilename = j.split(".")
                        fileExtension = splitFilename[-1]
                        extensionLength = len(fileExtension) + 1



        getLength = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", filename], stdout=subprocess.PIPE, stderr=subprocess.STDOUT) # Getting the total video length

        videoLength = (getLength.stdout.decode('utf-8').strip("b\'\\rn")) # Converting it to a string and removing unwanted characters

        #audioBitrate = 64000
        totalBitrate = 64000000 / float(videoLength) # Calculating the bitrate needed for an 8MB
        audioBitrate = (totalBitrate / 8)
        videoBitrate = (totalBitrate / 8)
        print(videoBitrate)
        await message.channel.send(videoBitrate)
        await message.channel.send(audioBitrate)
        print(audioBitrate)

        

        #videoBitrate = str(tempBitrate).split(".")[0] / 2
        #print(videoBitrate)
        print(videoLength)
        print(str(videoLength)[:-5])
        print(len(videoLength))
        print(extensionLength)
        #print('ffmpeg -i "' + filename + '" -c:v h264 -b:v ' + str(videoBitrate) + ' "' + filename[:-extensionLength] + '.mp4"')

        #os.system('ffmpeg -i "' + filename + '" -c:v h264 -b:v ' + str(videoBitrate) + ' -maxrate:v ' + str(videoBitrate) + ' -bufsize:v 3200000 -b:a ' + str(audioBitrate) + ' "' + filename[:-extensionLength] + ' .mp4"') # Running an ffmpeg command to convert the video to an mp4 with a bitrate totalling 8MB (max discord free file size)

        #os.system('ffmpeg -y -i "' + filename + '" -c:v h264 -b:v ' + str(videoBitrate) + ' -b:a ' + str(audioBitrate) + ' -pass 1 -an -f null nul && ^') # add audio
        print('test')
        await message.channel.send('test')
        await message.channel.send('ffmpeg -y -i "' + filename + '" -c:v h264 -b:v ' + str(videoBitrate) + ' -minrate:v ' + str(videoBitrate) + 'k -pass 2 -c:a aac -b:a ' + str(audioBitrate) + 'k "' + filename[:-extensionLength] + ' .mp4"')
        os.system('ffmpeg -y -i "' + filename + '" -c:v libx264 -b:v ' + str(videoBitrate) + ' -c:a aac -strict -2 -ac 2 -ar 44100 -b:a ' + str(audioBitrate) + ' "' + filename[:-extensionLength] + ' .mp4"')

        #os.system('ffmpeg -y -i 1.mp4 -c:v libx264 -b:v 555k -pass 1 -an -f null nul && ^ffmpeg -y -i 1.mp4 -c:v libx264 -b:v 555k -pass 2 -c:a aac -b:a 128k output.mp4')


        # Removing the video files
        newFilename = filename[:-extensionLength] + " .mp4"
        await message.reply(file=discord.File(newFilename))

        #os.remove(filename)
        os.remove(filename[:-extensionLength] + " .mp4")


client.run(TOKEN)