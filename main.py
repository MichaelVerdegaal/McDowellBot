import random
import discord
import requests
import validators
from discord.ext import commands

from Reactions import ReactUtils as Ru
from Game import GameUtils as Gu
from dbconn import *

version = '2.42'
bot = commands.Bot(command_prefix=".", description="A silly bot for people with a low IQ.")
twitch_url = "https://www.twitch.tv/ninjatuna6"
status_playing = "Playing with Tuna"


@bot.event
async def on_ready():
    bot.load_extension('SimpleCommands')
    bot.load_extension('Reactions')
    bot.load_extension('Game')
    print("I am the Great Archdemon Satanichia, Queen of all Hell!\n")
    print("SATANIA Version: {}".format(version))
    print(
        "Bot id: {} | Bot name {} | Bot discriminator: #{}".format(bot.user.id, bot.user.name, bot.user.discriminator))
    print("Bot status: '{}' | Stream url: {}".format(status_playing, twitch_url))
    if conn.status:
        print("Database connection: True\n")
    else:
        print("Database connection: False, check ASAP.\n")
    await bot.change_presence(activity=discord.Streaming(name=status_playing, url=twitch_url))


@bot.event
async def on_message(message):
    msg = message.content
    did = message.author.id
    dname = message.author.name
    random_number = int(random.uniform(1, 100))
    message_chance = 25
    gif_chance = 10

    if not message.author.bot:
        if random_number <= message_chance:
            if not Gu.user_exists(did):
                Gu.user_create(did, dname)
            # chain to take care of bot reactions
            reactions = Ru.get_reacts(msg)
            if reactions:
                if random_number <= gif_chance:
                    Gu.increment_score(did, 1)
                    # iterate over reactions to keep only those without urls
                    for idx, item in enumerate(reactions):
                        if not validators.url(item[1]):
                            reactions.pop(idx)
                else:
                    # iterate over reactions to keep only those with urls
                    for idx, item in enumerate(reactions):
                        if validators.url(item[1]):
                            reactions.pop(idx)
                # send a random response from the remaining reactions
                if reactions:
                    r = random.choice(reactions)
                    await message.channel.send(r[1])
                    Gu.increment_rcounter(did, 1)
                    Gu.increment_score(did, 1)
                else:
                    return
        # if bot is mentioned in a message
        elif "@386627978618077184" in msg:
            endpoint = 'http://api.adviceslip.com/advice'
            response = requests.get(url=endpoint)
            data = response.json()
            advice = data['slip']['advice']
            await message.channel.send("Somebody asked for my assistance? Fine then, "
                                       "i'll bless you with my glorious knowledge: *{}*".format(advice))
    await bot.process_commands(message)


bot.run(os.getenv('TOKEN'))
