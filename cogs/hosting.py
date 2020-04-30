import asyncio
import logging
import os

from discord.ext import commands
from .utils import checks
import discord

log = logging.getLogger(__name__)

SERVER_ID = int(os.getenv('GUILD_ID'))
CELESTE_CHAN = int(os.getenv('CELESTE_HOST_CHAN_ID'))
REDD_CHAN = int(os.getenv('REDD_HOST_CHAN_ID'))

npc_dict = {
    'celeste': CELESTE_CHAN,
    'redd': REDD_CHAN
}


class Hosting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reaction_emojis = (u"\u0031\uFE0F\u20E3", u"\u0032\uFE0F\u20E3")
        self.thumbnail_url = 'https://i.imgur.com/xJOaRAP.png'

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.author.send(
                "There was an error, please restart the process by using `!hosting [celeste/redd]`"
            )

    async def dialogue(self, ctx, npc):
        def msgcheck(m):
            return m.author == ctx.author

        em = discord.Embed(
            title="Turnip Stonks Bot",
            description="Awesome! How long are you planning on hosting for?",
            color=0xF4B400)
        em.set_thumbnail(url=self.thumbnail_url)
        await ctx.author.send(embed=em)
        message = await self.bot.wait_for('message',
                                          check=msgcheck,
                                          timeout=60)
        host_time = message.content

        em = discord.Embed(
            title="Turnip Stonks Bot",
            description=f"Ok! Any more info (e.g., {npc.capitalize()} location)?",
            color=0xF4B400)
        em.set_thumbnail(url=self.thumbnail_url)
        await ctx.author.send(embed=em)
        message = await self.bot.wait_for('message',
                                          check=msgcheck,
                                          timeout=60)
        npc_location = message.content

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
        message = await self.bot.wait_for('message',
                                          check=msgcheck,
                                          timeout=60)
        turnip_url = message.content

        em = discord.Embed(title="Turnip Stonks Bot",
                           description="",
                           color=0xF4B400)
        em.set_thumbnail(url=self.thumbnail_url)
        em.add_field(name="Host", value=f"{ctx.author}")
        em.add_field(name="Duration:", value=host_time, inline=False)
        em.add_field(name="Turnip Exchange URL",
                     value=turnip_url,
                     inline=False)
        em.add_field(name="More information:",
                     value=npc_location,
                     inline=False)

        await self.bot.get_channel(npc_dict[npc]).send(embed=em)

        em = discord.Embed(
            title="Turnip Stonks Bot",
            description=
            "Thank you for hosting! Your listing has been posted with the following details:",
            color=0xF4B400)
        em.set_thumbnail(url=self.thumbnail_url)
        em.add_field(name="Host", value=f"{ctx.author}")
        em.add_field(name="Duration:", value=host_time, inline=False)
        em.add_field(name="Turnip Exchange URL",
                     value=turnip_url,
                     inline=False)
        em.add_field(name="More information:",
                     value=npc_location,
                     inline=False)

        await ctx.author.send(embed=em)

    @commands.group()
    @checks.is_dm()
    async def hosting(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.author.send('Invalid hosting command passed...')

    @hosting.command()
    @checks.is_dm()
    async def celeste(self, ctx):
        """Let users host for Celeste"""
        em = discord.Embed(
            title="Turnip Stonks Bot",
            description=
            f"Hey <@{ctx.author.id}>!\n\nWant to invite some friends to see a meteor shower?"
            f"\n\n :one: - Yes! Let's go!\n:two: - On the other hand...maybe not.",
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
                await self.dialogue(ctx, 'celeste')
            elif reaction == self.reaction_emojis[1]:
                await ctx.author.send("Ok! Maybe another time!")
            else:
                await ctx.author.send(
                    "Invalid reaction. Please restart the process by using `!hosting celeste`"
                )
        except asyncio.TimeoutError as e:
            await ctx.author.send(
                "You took too long to respond! Please restart the process by using `!hosting celeste`"
            )
            log.info(e)


def setup(bot):
    bot.add_cog(Hosting(bot))
