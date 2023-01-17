import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
import subprocess



load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
help_command = commands.DefaultHelpCommand(no_category='Commands')
bot = commands.Bot(command_prefix="!", intents=intents, help_command=help_command)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return


    if message.author.id == 418084307257786369:
        if "say something" in message.content.lower():
            await message.channel.send("Hello")



    if message.author.id == 618018877573431297 or message.author.id == 189758961984077824:
        if "say something" in message.content.lower():
            await message.channel.send("Hi")

            


    if "send a file" in message.content.lower():
        await message.channel.send("here's a video", file=discord.File('files\Logo.png'))

    
    if str(bot.user.id) in message.content:
        await message.channel.send("Do you need me?")


    await bot.process_commands(message)
    
    
    
@bot.command(brief="View supported download sites", help="Syntax: !sites")
async def sites(ctx):
    if ctx.author == bot.user:
        return


    await ctx.reply("""**Audio:**
YouTube
SoundCloud
    
**Video:**
YouTube""")
    return




@bot.command(brief="Downloads the audio from a link and adds it to the library", help="""Syntax: !audio [File link]
Only downlaods the first video in a playlist. use !sites to view supported sites""")
async def download(ctx):
    if ctx.author == bot.user:
        return
    splitCommand = ctx.content.split(" ")
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
        await ctx.channel.send("Invalid URL")
        return

    await ctx.channel.send("Beginning download")
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
    await ctx.channel.send(videoBitrate)
    await ctx.channel.send(audioBitrate)
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
    await ctx.channel.send('ffmpeg -y -i "' + filename + '" -c:v h264 -b:v ' + str(videoBitrate) + ' -minrate:v ' + str(videoBitrate) + 'k -pass 2 -c:a aac -b:a ' + str(audioBitrate) + 'k "' + filename[:-extensionLength] + ' .mp4"')
    os.system('ffmpeg -y -i "' + filename + '" -c:v libx264 -b:v ' + str(videoBitrate) + ' -c:a aac -strict -2 -ac 2 -ar 44100 -b:a ' + str(audioBitrate) + ' "' + filename[:-extensionLength] + ' .mp4"')

    #os.system('ffmpeg -y -i 1.mp4 -c:v libx264 -b:v 555k -pass 1 -an -f null nul && ^ffmpeg -y -i 1.mp4 -c:v libx264 -b:v 555k -pass 2 -c:a aac -b:a 128k output.mp4')


    # Removing the video files
    newFilename = filename[:-extensionLength] + " .mp4"
    await ctx.reply(file=discord.File(newFilename))

    #os.remove(filename)
    os.remove(filename[:-extensionLength] + " .mp4")


bot.run(DISCORD_TOKEN)