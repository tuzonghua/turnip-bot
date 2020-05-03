import asyncio
from enum import Enum
import logging
import os

from discord.ext import commands
from .utils import checks
import discord

log = logging.getLogger(__name__)

SERVER_ID = int(os.getenv('GUILD_ID'))
CELESTE_CHAN = int(os.getenv('CELESTE_HOST_CHAN_ID'))
REDD_CHAN = int(os.getenv('REDD_HOST_CHAN_ID'))


class HostingChan(Enum):
    CELESTE_HOST_CHAN_ID = 1
    REDD_HOST_CHAN_ID = 2
    SAHARAH_HOST_CHAN_ID = 3
    LEIF_HOST_CHAN_ID = 4


class Hosting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.thumbnail_url = 'https://i.imgur.com/xJOaRAP.png'

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.author.send(
                "There was an error, please restart the process by using `!hosting`"
            )

    @commands.command()
    @checks.is_dm()
    async def hosting(self, ctx: commands.Context):
        def msgcheck(m: discord.Message):
            return m.author == ctx.author and m.channel == ctx.channel

        em_desc = (
            f"Hey <@{ctx.author.id}>!\n\n"
            f"Who are you hosting? Please enter a number from below:\n\n"
            f"1. Celeste\n2. Redd\n"
            f"3. Saharah\n4. Leif")
        em = discord.Embed(title="Turnip Stonks Bot",
                           description=em_desc,
                           color=0xF4B400)
        em.set_thumbnail(url=self.thumbnail_url)
        await ctx.author.send(embed=em)

        hosting_opt = 0
        npc = None
        for i in range(5):
            try:
                msg = await self.bot.wait_for('message',
                                              check=msgcheck,
                                              timeout=60)
            except asyncio.TimeoutError as e:
                await ctx.author.send(
                    "You took too long to respond! Please restart the process by using `!market`"
                )
                log.info(e)
            if msg.clean_content.isdigit() and 1 <= int(
                    msg.clean_content) <= 4:
                hosting_opt = HostingChan(int(msg.clean_content))
                npc = hosting_opt.name.split("_")[0].capitalize()
                break

            num_tries = 4 - i
            if num_tries == 0:
                raise commands.CommandError("Too many retries")
            await ctx.author.send(
                f"Option can only be a digit between 1 and 4. {num_tries} tries remaining."
            )

        em = discord.Embed(
            title="Turnip Stonks Bot",
            description="Awesome! How long are you planning on hosting for?",
            color=0xF4B400)
        em.set_thumbnail(url=self.thumbnail_url)
        await ctx.author.send(embed=em)
        try:
            msg = await self.bot.wait_for('message',
                                          check=msgcheck,
                                          timeout=60)
        except asyncio.TimeoutError as e:
            await ctx.author.send(
                "You took too long to respond! Please restart the process by using `!market`"
            )
            log.info(e)
        host_time = msg.clean_content

        em = discord.Embed(
            title="Turnip Stonks Bot",
            description=f"Ok! Any more info (e.g., {npc} location)?",
            color=0xF4B400)
        em.set_thumbnail(url=self.thumbnail_url)
        await ctx.author.send(embed=em)
        try:
            msg = await self.bot.wait_for('message',
                                          check=msgcheck,
                                          timeout=60)
        except asyncio.TimeoutError as e:
            await ctx.author.send(
                "You took too long to respond! Please restart the process by using `!market`"
            )
            log.info(e)
        npc_location = msg.clean_content

        em = discord.Embed(
            title="Turnip Stonks Bot",
            description=
            "Please copy and paste your Turnip Exchange URL so people can queue. (If you do not how know to create a "
            "Turnip Exchange URL click [here]("
            "https://discordapp.com/channels/{}/696847359514116156))".format(
                SERVER_ID),
            color=0xF4B400)
        em.set_thumbnail(url=self.thumbnail_url)
        await ctx.author.send(embed=em)
        try:
            msg = await self.bot.wait_for('message',
                                          check=msgcheck,
                                          timeout=60)
        except asyncio.TimeoutError as e:
            await ctx.author.send(
                "You took too long to respond! Please restart the process by using `!market`"
            )
            log.info(e)
        turnip_url = msg.clean_content

        em = discord.Embed(title="Turnip Stonks Bot",
                           description="",
                           color=0xF4B400)
        em.set_thumbnail(url=self.thumbnail_url)
        em.add_field(name="Host", value=f"<@{ctx.author.id}>")
        em.add_field(name="Duration:", value=host_time, inline=False)
        em.add_field(name="Turnip Exchange URL",
                     value=turnip_url,
                     inline=False)
        em.add_field(name="More information:",
                     value=npc_location,
                     inline=False)

        channel = int(os.getenv(hosting_opt.name))
        await self.bot.get_channel(channel).send(embed=em)

        em = discord.Embed(
            title="Turnip Stonks Bot",
            description=
            f"Thanks! Check <#{channel}> for your listing. Here's the info you provided:",
            color=0xF4B400)
        em.set_thumbnail(url=self.thumbnail_url)
        em.add_field(name="Host", value=f"<@{ctx.author.id}>")
        em.add_field(name="Duration:", value=host_time, inline=False)
        em.add_field(name="Turnip Exchange URL",
                     value=turnip_url,
                     inline=False)
        em.add_field(name="More information:",
                     value=npc_location,
                     inline=False)

        await ctx.author.send(embed=em)


def setup(bot):
    bot.add_cog(Hosting(bot))
