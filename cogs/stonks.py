import asyncio
import logging
import os

from discord.ext import commands
from .utils import checks
import discord

log = logging.getLogger(__name__)

SERVER_ID = int(os.getenv('GUILD_ID'))
DAISY_CHAN = int(os.getenv('DAISY_SELL_CHAN_ID'))
NOOKS_CHAN = int(os.getenv('NOOKS_BUY_CHAN_ID'))


class Stonks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reaction_emojis = (u"\u0031\uFE0F\u20E3", u"\u0032\uFE0F\u20E3")
        self.thumbnail_url = 'https://i.imgur.com/xJOaRAP.png'

    async def cog_command_error(self, ctx, error):
        await ctx.author.send(
            "There was an error, please restart the process by using `!stonks`"
        )

    async def dialogue(self, ctx, buy=True):
        def msgcheck(m):
            return m.author == ctx.author

        if buy:
            text = "Timmy and Tommy's buy price?"
        else:
            text = "Daisy Mae's sell price?"

        em = discord.Embed(title="Turnip Stonks Bot",
                           description="What is {}".format(text),
                           color=0xF4B400)
        em.set_thumbnail(url=self.thumbnail_url)
        await ctx.author.send(embed=em)

        # Clunky validation loop to ensure price is a number
        turnip_price = None
        for i in range(5):
            message = await self.bot.wait_for('message',
                                              check=msgcheck,
                                              timeout=60)
            if message.cleant_content.isdigit():
                turnip_price = message.clean_content
                break

            await ctx.author.send(
                f"Price can only be digits. {4 - i} tries remaining.")

        if not turnip_price:
            raise commands.CommandError(
                "Too many retries, please restart the process.")

        em = discord.Embed(
            title="Turnip Stonks Bot",
            description=
            "Please copy and paste your Turnip Exchange URL. (If you do not how know to create a Turnip "
            "Exchange URL click [here]("
            "https://discordapp.com/channels/{}/696847359514116156))".format(
                SERVER_ID),
            color=0xF4B400)
        em.set_thumbnail(url=self.thumbnail_url)
        await ctx.author.send(embed=em)
        message = await self.bot.wait_for('message',
                                          check=msgcheck,
                                          timeout=60)
        turnip_url = message.clean_content

        em = discord.Embed(
            title="Turnip Stonks Bot",
            description=
            "Would you like to add any more information: (Ex. Directions to Daisy Mae/Nooks, entry fee, etc)",
            color=0xF4B400)
        em.set_thumbnail(url=self.thumbnail_url)
        await ctx.author.send(embed=em)
        message = await self.bot.wait_for('message',
                                          check=msgcheck,
                                          timeout=60)
        turnip_more_info = message.clean_content

        em = discord.Embed(title="Turnip Stonks Bot",
                           description="",
                           color=0xF4B400)
        em.set_thumbnail(url=self.thumbnail_url)
        em.add_field(name="Stonk Broker", value=f"<@{ctx.author.id}>")
        em.add_field(name="Price", value=turnip_price, inline=False)
        em.add_field(name="Turnip Exchange URL",
                     value=turnip_url,
                     inline=False)
        em.add_field(name="More Information",
                     value=turnip_more_info,
                     inline=False)

        if buy:
            await self.bot.get_channel(NOOKS_CHAN).send(embed=em)
        else:
            await self.bot.get_channel(DAISY_CHAN).send(embed=em)

        em = discord.Embed(
            title="Turnip Stonks Bot",
            description=
            "Your listing has been posted with the following details:",
            color=0xF4B400)
        em.set_thumbnail(url=self.thumbnail_url)
        em.add_field(name="Price", value=turnip_price, inline=False)
        em.add_field(name="Turnip Exchange URL",
                     value=turnip_url,
                     inline=False)
        em.add_field(name="More Information",
                     value=turnip_more_info,
                     inline=False)

        await ctx.author.send(embed=em)

    @commands.command()
    @checks.is_dm()
    async def stonks(self, ctx):
        """Let users list turnips for sale/purchase"""
        em = discord.Embed(
            title="Turnip Stonks Bot",
            description=
            f"Hey <@{ctx.author.id}>!\n\nLet's get you some bells! Is Daisy Mae selling or are Timmy and Tommy buying?"
            f"\n\n :one: - Daisy Mae is selling!\n:two: - Timmy and Tommy are buying!",
            color=0xF4B400)
        em.set_thumbnail(url=self.thumbnail_url)
        first_message = await ctx.author.send(embed=em)

        for emoji in self.reaction_emojis:
            await first_message.add_reaction(emoji)

        def react_check(payload):
            if payload.user_id != ctx.author.id:
                return False

            to_check = str(payload.emoji)
            for emoji in self.reaction_emojis:
                if to_check == emoji:
                    return True
            return False

        try:
            payload = await self.bot.wait_for('raw_reaction_add',
                                              check=react_check,
                                              timeout=60)
            reaction = str(payload.emoji)
            if reaction == self.reaction_emojis[0]:
                await self.dialogue(ctx, buy=False)
            elif reaction == self.reaction_emojis[1]:
                await self.dialogue(ctx, buy=True)
            else:
                await ctx.author.send(
                    "Invalid reaction. Please restart the process by using `!stonks`"
                )
        except asyncio.TimeoutError as e:
            await ctx.author.send(
                "You took too long to respond! Please restart the process by using `!stonks`"
            )
            log.info(e)


def setup(bot):
    bot.add_cog(Stonks(bot))
