import discord
import asyncio
import json
import datetime
import os
from datetime import timedelta
from discord import app_commands
from discord.ext import commands, tasks
from discord.utils import get
from dotenv import load_dotenv


intents = discord.Intents.default()
intents.message_content = True

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')

client = commands.Bot(command_prefix='!', intents=intents)

#define time zone
utc = datetime.timezone.utc

#set the time for the loop to run
time = datetime.time(hour=6, minute=0, tzinfo=utc)

@tasks.loop(time=time)
async def check_birthdays():
    #define channel where the bot will send the happy bday message
    channel = client.get_channel(int(CHANNEL_ID))
    
    # Define current date and use it in the birthdays_in() function
    today_date = datetime.datetime.now().strftime("%d/%m")
    today_bday = birthdays_in(today_date)

    #name formatting for days with multiple bdays
    def format_names(names):
        if len(names) > 1:
            return ', '.join(names[:-1]) + ' and ' + names[-1]
        elif names:
            return names[0]
        else:
            return ''

    #check if there is a match between the current date and any of the dates of birth in db.json
    if today_bday:
        await channel.send(content=f" @everyone Today is {format_names(today_bday)}'s birthday!", file=discord.File('jerma.gif'))
    
    else:
        print("no bdays today")


def json_to_list():
    f = open('db.json')  
    data = json.load(f)
    persons = []
    for person in data:
        persons.append(data[person])
    f.close()
    return persons 

persons = json_to_list()

def birthdays_in(date):
    date = date.split('/')
    today_birthday = []
    for person in persons:
        bday = person['bday'].split('/')
        if bday[0] == date[0] and bday[1] == date[1] :
            today_birthday.append(person['name'])
    return today_birthday

@client.command()
async def kill(ctx):
    await ctx.send("jerma is dead")
    await client.close()



@client.event
async def on_ready():
    print("birthbot has started")
    check_birthdays.start()




client.run(DISCORD_TOKEN)