import logging
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('DISCORD_API_TOKEN')
SERVER_ID = int(os.getenv('GUILD_ID'))
DAISY_CHAN = int(os.getenv('DAISY_SELL_CHAN_ID'))
NOOKS_CHAN = int(os.getenv('NOOKS_BUY_CHAN_ID'))
MKT_BUY_CHAN = int(os.getenv('MARKETPLACE_BUY_CHAN_ID'))
MKT_SELL_CHAN = int(os.getenv('MARKETPLACE_SELL_CHAN_ID'))
MKT_TRADE_CHAN = int(os.getenv('MARKETPLACE_TRADE_CHAN_ID'))

# Setup logging
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log',
                              encoding='utf-8',
                              mode='w')
formatter = logging.Formatter(
    "%(asctime)s %(name)s[%(lineno)d] - %(levelname)s: %(message)s",
    datefmt="%m/%d/%y %H:%M:%S")
handler.setFormatter(formatter)
logger.addHandler(handler)

# Set bot prefix
bot = commands.Bot(command_prefix="!")


@bot.event
async def on_ready():
    logger.info("{} running with the following credentials:".format(bot.user))
    logger.info("Username: {}".format(bot.user.name))
    logger.info("Password: {}".format(bot.user.id))
    await bot.change_presence(activity=discord.Game(
        name="Direct Message !hello"))


@bot.command()
async def hello(ctx):
    em = discord.Embed(
        title="Turnip Stonks Bot",
        description=
        f"Hello <@{ctx.author.id}>, \n\nPlease complete the following questionnaire by using reactions and text. "
        f"\n\n:one: — Host \n:two: — Buy, Sell or Trade",
        color=0xF4B400)

    first_message = await ctx.author.send(embed=em)

    await first_message.add_reaction("1️⃣")
    await first_message.add_reaction("2️⃣")

    try:

        def check(reaction, user):
            return user == ctx.author

        def msgcheck(message):
            return message.author == ctx.author

        reaction, user = await bot.wait_for('reaction_add',
                                            check=check,
                                            timeout=60)

        reaction = reaction.emoji

        if reaction == "1️⃣":
            em = discord.Embed(
                title="Turnip Stonks Bot",
                description=
                "Is Daisy Mae selling turnips or are Timmy and Tommy buying turnips? \n\n:one: — Daisy Mae is selling "
                "turnips \n:two: —  Timmy and Tommy are buying turnips",
                color=0xF4B400)
            secondmessage = await ctx.author.send(embed=em)

            await secondmessage.add_reaction("1️⃣")
            await secondmessage.add_reaction("2️⃣")

            reaction, user = await bot.wait_for('reaction_add',
                                                check=check,
                                                timeout=60)

            reaction = reaction.emoji

            if reaction == "1️⃣":
                em = discord.Embed(
                    title="Turnip Stonks Bot",
                    description=
                    "What is the current price Daisy Mae is selling turnips for?",
                    color=0xF4B400)
                await ctx.author.send(embed=em)

                message = await bot.wait_for('message',
                                             check=msgcheck,
                                             timeout=60)

                turnipprice = message.content

                em = discord.Embed(
                    title="Turnip Stonks Bot",
                    description=
                    "Please copy and paste your Turnip Exchange URL. (If you do not how know to create a Turnip "
                    "Exchange URL click [here]("
                    "https://discordapp.com/channels/{}/696847359514116156))".
                    format(SERVER_ID),
                    color=0xF4B400)
                await ctx.author.send(embed=em)
                message = await bot.wait_for('message',
                                             check=msgcheck,
                                             timeout=60)
                turnip_url = message.content

                em = discord.Embed(
                    title="Turnip Stonks Bot",
                    description=
                    "Would you like to add any more information: (Ex. Directions to Daisy Mae, Entry Fee, etc)",
                    color=0xF4B400)
                await ctx.author.send(embed=em)
                message = await bot.wait_for('message',
                                             check=msgcheck,
                                             timeout=60)
                turnipmoreinfo = message.content

                em = discord.Embed(title="Turnip Stonks Bot",
                                   description="",
                                   color=0xF4B400)
                em.add_field(name="Stonk Broker", value=f"{ctx.author}")
                em.add_field(name="Price", value=turnipprice, inline=False)
                em.add_field(name="Turnip Exchange URL",
                             value=turnip_url,
                             inline=False)
                em.add_field(name="More Information",
                             value=turnipmoreinfo,
                             inline=False)

                await bot.get_channel(DAISY_CHAN).send(embed=em)

                em = discord.Embed(
                    title="Turnip Stonks Bot",
                    description=
                    "Your listing has been posted with the following details:",
                    color=0xF4B400)
                em.add_field(name="Price", value=turnipprice, inline=False)
                em.add_field(name="Turnip Exchange URL",
                             value=turnip_url,
                             inline=False)
                em.add_field(name="More Information",
                             value=turnipmoreinfo,
                             inline=False)

                await ctx.author.send(embed=em)

            elif reaction == "2️⃣":
                em = discord.Embed(
                    title="Turnip Stonks Bot",
                    description=
                    "What is the current price Timmy and Tommy are buying turnips for?",
                    color=0xF4B400)
                await ctx.author.send(embed=em)

                message = await bot.wait_for('message',
                                             check=msgcheck,
                                             timeout=60)

                turnipprice = message.content

                em = discord.Embed(
                    title="Turnip Stonks Bot",
                    description=
                    "Please copy and paste your Turnip Exchange URL. (If you do not how know to create a Turnip "
                    "Exchange URL click [here]("
                    "https://discordapp.com/channels/{}/696847359514116156))".
                    format(SERVER_ID),
                    color=0xF4B400)
                await ctx.author.send(embed=em)
                message = await bot.wait_for('message',
                                             check=msgcheck,
                                             timeout=60)
                turnip_url = message.content

                em = discord.Embed(
                    title="Turnip Stonks Bot",
                    description=
                    "Would you like to add any more information: (Ex. Directions to Timmy and Tommy, Entry Fee, etc)",
                    color=0xF4B400)
                await ctx.author.send(embed=em)
                message = await bot.wait_for('message',
                                             check=msgcheck,
                                             timeout=60)
                turnipmoreinfo = message.content

                em = discord.Embed(title="Turnip Stonks Bot",
                                   description="",
                                   color=0xF4B400)
                em.add_field(name="Stonk Broker", value=f"{ctx.author}")
                em.add_field(name="Price", value=turnipprice, inline=False)
                em.add_field(name="Turnip Exchange URL",
                             value=turnip_url,
                             inline=False)
                em.add_field(name="More Information",
                             value=turnipmoreinfo,
                             inline=False)

                await bot.get_channel(NOOKS_CHAN).send(embed=em)

                em = discord.Embed(
                    title="Turnip Stonks Bot",
                    description=
                    "Your listing has been posted with the following details:",
                    color=0xF4B400)
                em.add_field(name="Price", value=turnipprice, inline=False)
                em.add_field(name="Turnip Exchange URL",
                             value=turnip_url,
                             inline=False)
                em.add_field(name="More Information",
                             value=turnipmoreinfo,
                             inline=False)

                await ctx.author.send(embed=em)

            else:
                await ctx.author.send(
                    "Invalid reaction. Please restart the process by using `!hello`"
                )

        elif reaction == "2️⃣":
            em = discord.Embed(
                title="Turnip Stonks Bot",
                description=
                "Would you like to Buy, Sell, or Trade? \n:one: — Buy \n:two: —  Sell \n:three: —  Trade",
                color=0xF4B400)
            secondmessage = await ctx.author.send(embed=em)

            await secondmessage.add_reaction("1️⃣")
            await secondmessage.add_reaction("2️⃣")
            await secondmessage.add_reaction("3️⃣")

            reaction, user = await bot.wait_for('reaction_add',
                                                check=check,
                                                timeout=60)

            reaction = reaction.emoji

            if reaction == "1️⃣":
                em = discord.Embed(
                    title="Turnip Stonks Bot",
                    description="What is the name of the item you are buying?",
                    color=0xF4B400)
                await ctx.author.send(embed=em)

                message = await bot.wait_for('message',
                                             check=msgcheck,
                                             timeout=60)

                itemname = message.content

                em = discord.Embed(
                    title="Turnip Stonks Bot",
                    description="What is the price of the item you are buying?",
                    color=0xF4B400)
                await ctx.author.send(embed=em)

                message = await bot.wait_for('message',
                                             check=msgcheck,
                                             timeout=60)

                itemprice = message.content

                em = discord.Embed(
                    title="Turnip Stonks Bot",
                    description="Would you like to add any more information:",
                    color=0xF4B400)
                await ctx.author.send(embed=em)

                message = await bot.wait_for('message',
                                             check=msgcheck,
                                             timeout=60)

                itemmoreinfo = message.content

                em = discord.Embed(title="Turnip Stonks Bot",
                                   description="",
                                   color=0xF4B400)
                em.add_field(name="Stonk Broker", value=f"{ctx.author}")
                em.add_field(name="Buying", value=itemname, inline=False)
                em.add_field(name="Price", value=itemprice, inline=False)
                em.add_field(name="More Information",
                             value=itemmoreinfo,
                             inline=False)

                await bot.get_channel(MKT_BUY_CHAN).send(embed=em)

                em = discord.Embed(
                    title="Turnip Stonks Bot",
                    description=
                    "Your listing has been posted with the following details:",
                    color=0xF4B400)
                em.add_field(name="Buying", value=itemname, inline=False)
                em.add_field(name="Price", value=itemprice, inline=False)
                em.add_field(name="More Information",
                             value=itemmoreinfo,
                             inline=False)

                await ctx.author.send(embed=em)

            elif reaction == "2️⃣":
                em = discord.Embed(
                    title="Turnip Stonks Bot",
                    description="What is the name of the item you are selling?",
                    color=0xF4B400)
                await ctx.author.send(embed=em)

                message = await bot.wait_for('message',
                                             check=msgcheck,
                                             timeout=60)

                itemname = message.content

                em = discord.Embed(
                    title="Turnip Stonks Bot",
                    description=
                    "What is the price of the item you are selling?",
                    color=0xF4B400)
                await ctx.author.send(embed=em)

                message = await bot.wait_for('message',
                                             check=msgcheck,
                                             timeout=60)

                itemprice = message.content

                em = discord.Embed(
                    title="Turnip Stonks Bot",
                    description="Would you like to add any more information:",
                    color=0xF4B400)
                await ctx.author.send(embed=em)

                message = await bot.wait_for('message',
                                             check=msgcheck,
                                             timeout=60)

                itemmoreinfo = message.content

                em = discord.Embed(title="Turnip Stonks Bot",
                                   description="",
                                   color=0xF4B400)
                em.add_field(name="Stonk Broker", value=f"{ctx.author}")
                em.add_field(name="Selling", value=itemname, inline=False)
                em.add_field(name="Price", value=itemprice, inline=False)
                em.add_field(name="More Information",
                             value=itemmoreinfo,
                             inline=False)

                await bot.get_channel(MKT_SELL_CHAN).send(embed=em)

                em = discord.Embed(
                    title="Turnip Stonks Bot",
                    description=
                    "Your listing has been posted with the following details:",
                    color=0xF4B400)
                em.add_field(name="Selling", value=itemname, inline=False)
                em.add_field(name="Price", value=itemprice, inline=False)
                em.add_field(name="More Information",
                             value=itemmoreinfo,
                             inline=False)

                await ctx.author.send(embed=em)

            elif reaction == "3️⃣":
                em = discord.Embed(
                    title="Turnip Stonks Bot",
                    description="What is the name of the item you are trading?",
                    color=0xF4B400)
                await ctx.author.send(embed=em)

                message = await bot.wait_for('message',
                                             check=msgcheck,
                                             timeout=60)

                itemname = message.content

                em = discord.Embed(
                    title="Turnip Stonks Bot",
                    description=
                    "What is the price of the item you are trading?",
                    color=0xF4B400)
                await ctx.author.send(embed=em)

                message = await bot.wait_for('message',
                                             check=msgcheck,
                                             timeout=60)

                itemprice = message.content

                em = discord.Embed(
                    title="Turnip Stonks Bot",
                    description="Would you like to add any more information:",
                    color=0xF4B400)
                await ctx.author.send(embed=em)

                message = await bot.wait_for('message',
                                             check=msgcheck,
                                             timeout=60)

                itemmoreinfo = message.content

                em = discord.Embed(title="Turnip Stonks Bot",
                                   description="",
                                   color=0xF4B400)
                em.add_field(name="Stonk Broker", value=f"{ctx.author}")
                em.add_field(name="Trading", value=itemname, inline=False)
                em.add_field(name="Price", value=itemprice, inline=False)
                em.add_field(name="More Information",
                             value=itemmoreinfo,
                             inline=False)

                await bot.get_channel(MKT_TRADE_CHAN).send(embed=em)

                em = discord.Embed(
                    title="Turnip Stonks Bot",
                    description=
                    "Your listing has been posted with the following details:",
                    color=0xF4B400)
                em.add_field(name="Trading", value=itemname, inline=False)
                em.add_field(name="Price", value=itemprice, inline=False)
                em.add_field(name="More Information",
                             value=itemmoreinfo,
                             inline=False)
                await ctx.author.send(embed=em)

            else:
                await ctx.author.send(
                    "Invalid reaction. Please restart the process by using `!hello`"
                )

        else:
            await ctx.author.send(
                "Invalid reaction. Please restart the process by using `!hello`"
            )

    except Exception as e:
        await ctx.author.send(
            "You took too long to respond! Please restart the process by using `!hello`"
        )
        logger.info(e)


bot.run(BOT_TOKEN)
