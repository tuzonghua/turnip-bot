import os

from discord.ext import commands
from .utils import checks
import discord

DAISY_CHAN = int(os.getenv('DAISY_SELL_CHAN_ID'))
NOOKS_CHAN = int(os.getenv('NOOKS_BUY_CHAN_ID'))


class Stonks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @checks.is_dm()
    async def stonks(self, ctx):
        """Let users list turnips for sale/purchase"""
        em = discord.Embed(title="Turnip Stonks Bot",
                           description="",
                           color=0xF4B400)
        em.add_field(name="Stonk Broker", value="test")
        em.add_field(name="Price", value="2", inline=False)
        em.add_field(name="Turnip Exchange URL", value="3", inline=False)
        em.add_field(name="More Information",
                     value="turnipmoreinfo",
                     inline=False)

        await self.bot.get_channel(DAISY_CHAN).send(embed=em)


def setup(bot):
    bot.add_cog(Stonks(bot))
