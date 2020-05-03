import asyncio
from enum import Enum
import logging
import os
import sys
import traceback

from discord.ext import commands
from .utils import checks
import discord

log = logging.getLogger(__name__)

SERVER_ID = int(os.getenv('GUILD_ID'))
NOOKAZON_CHANNEL = int(os.getenv('NOOKAZON_CHAN_ID'))


class MarketChan(Enum):
    ACCESSORIES_CHAN_ID = 1
    DIY_CHAN_ID = 2
    FLOORS_CHAN_ID = 3
    FLOWER_CHAN_ID = 4
    FOSSIL_CHAN_ID = 5
    HOUSEWARE_CHAN_ID = 6
    MATERIALS_CHAN_ID = 7
    SEASONAL_CHAN_ID = 8
    MISC_CHAN_ID = 9


class Market(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # Reactions are: 1️⃣, 2️⃣, 3️⃣
        self.reaction_emojis = (u"\u0031\uFE0F\u20E3", u"\u0032\uFE0F\u20E3",
                                u"\u0033\uFE0F\u20E3")
        self.thumbnail_url = 'https://i.imgur.com/xJOaRAP.png'

    async def cog_command_error(self, ctx, error):
        traceback.print_exception(type(error),
                                  error,
                                  error.__traceback__,
                                  file=sys.stderr)
        await ctx.author.send(
            f"There was an error, please restart the process by using `!market`: {error}"
        )

    @commands.group()
    @checks.is_dm()
    async def market(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.author.send(
                'Invalid market command passed. Please use a valid subcommand. Message with `!help '
                'market` for options.')

    @market.command()
    @checks.is_dm()
    async def nookazon(self, ctx: commands.Context):
        def msgcheck(m: discord.Message):
            return m.author == ctx.author and m.channel == ctx.channel

        em = discord.Embed(
            title="Turnip Stonks Bot",
            description=
            f"Hey <@{ctx.author.id}>!\n\nWhat is your Nookazon URL? (e.g., "
            f"https://nookazon.com/profile/2907772910/listings)",
            color=0xF4B400)
        em.set_thumbnail(url=self.thumbnail_url)
        await ctx.author.send(embed=em)

        try:
            nookazon_url = await self.bot.wait_for('message',
                                                   check=msgcheck,
                                                   timeout=60)
        except asyncio.TimeoutError:
            return await ctx.author.send('You took too long. Goodbye.')

        em = discord.Embed(
            title="Turnip Stonks Bot",
            description=f"Thanks! Any other info people should know?",
            color=0xF4B400)
        em.set_thumbnail(url=self.thumbnail_url)
        await ctx.author.send(embed=em)

        try:
            other_info = await self.bot.wait_for('message',
                                                 check=msgcheck,
                                                 timeout=60)
        except asyncio.TimeoutError:
            return await ctx.author.send('You took too long. Goodbye.')

        em = discord.Embed(title="Turnip Stonks Bot",
                           description="",
                           color=0xF4B400)
        em.set_thumbnail(url=self.thumbnail_url)
        em.add_field(name="Seller", value=f"<@{ctx.author.id}>")
        em.add_field(name="Nookazon URL",
                     value=nookazon_url.clean_content,
                     inline=False)
        em.add_field(name="More Information",
                     value=other_info.clean_content,
                     inline=False)

        await self.bot.get_channel(NOOKAZON_CHANNEL).send(embed=em)

        em = discord.Embed(
            title="Turnip Stonks Bot",
            description=
            "Your listing has been posted with the following details:",
            color=0xF4B400)
        em.set_thumbnail(url=self.thumbnail_url)
        em.add_field(name="Seller", value=f"{ctx.author}")
        em.add_field(name="Nookazon URL",
                     value=nookazon_url.clean_content,
                     inline=False)
        em.add_field(name="More Information",
                     value=other_info.clean_content,
                     inline=False)

        await ctx.author.send(embed=em)

    async def trading_dialogue(self, ctx, market_opt: MarketChan):
        def msgcheck(m):
            return m.author == ctx.author

        em = discord.Embed(title="Turnip Stonks Bot",
                           description="What are you looking for?",
                           color=0xF4B400)
        em.set_thumbnail(url=self.thumbnail_url)
        await ctx.author.send(embed=em)

        msg = await self.bot.wait_for('message', check=msgcheck, timeout=60)
        trade_item = msg.clean_content

        em = discord.Embed(title="Turnip Stonks Bot",
                           description="What are you offering for trade?",
                           color=0xF4B400)
        em.set_thumbnail(url=self.thumbnail_url)
        await ctx.author.send(embed=em)

        msg = await self.bot.wait_for('message', check=msgcheck, timeout=60)
        trade_offer = msg.clean_content

        em = discord.Embed(title="Turnip Stonks Bot",
                           description="Any other details?",
                           color=0xF4B400)
        em.set_thumbnail(url=self.thumbnail_url)
        await ctx.author.send(embed=em)

        msg = await self.bot.wait_for('message', check=msgcheck, timeout=60)
        other_info = msg.clean_content

        em = discord.Embed(title="Turnip Stonks Bot",
                           description="",
                           color=0xF4B400)
        em.set_thumbnail(url=self.thumbnail_url)
        em.add_field(name="Trader", value=f"<@{ctx.author.id}>")
        em.add_field(name="Looking For", value=trade_item, inline=False)
        em.add_field(name="Offering", value=trade_offer, inline=False)
        em.add_field(name="More Information", value=other_info, inline=False)

        channel = int(os.getenv(market_opt.name))
        await self.bot.get_channel(channel).send(embed=em)

        em = discord.Embed(
            title="Turnip Stonks Bot",
            description=
            f"Thanks! Check <#{channel}> for your listing. Here's the info you provided:",
            color=0xF4B400)
        em.set_thumbnail(url=self.thumbnail_url)
        em.add_field(name="Looking For", value=trade_item, inline=False)
        em.add_field(name="Offering", value=trade_offer, inline=False)
        em.add_field(name="More Information", value=other_info, inline=False)

        await ctx.author.send(embed=em)

    async def selling_dialogue(self, ctx, market_opt: MarketChan):
        def msgcheck(m):
            return m.author == ctx.author

        em = discord.Embed(title="Turnip Stonks Bot",
                           description="What are you selling?",
                           color=0xF4B400)
        em.set_thumbnail(url=self.thumbnail_url)
        await ctx.author.send(embed=em)

        msg = await self.bot.wait_for('message', check=msgcheck, timeout=60)
        sale_item = msg.clean_content

        em = discord.Embed(title="Turnip Stonks Bot",
                           description="What's the price?",
                           color=0xF4B400)
        em.set_thumbnail(url=self.thumbnail_url)
        await ctx.author.send(embed=em)

        # Clunky validation loop to ensure price is a number
        item_price = None
        for i in range(5):
            msg = await self.bot.wait_for('message',
                                          check=msgcheck,
                                          timeout=60)
            if msg.clean_content.isdigit():
                item_price = msg.clean_content
                break

            await ctx.author.send(
                f"Price can only be digits. {4 - i} tries remaining.")

        if not item_price:
            raise commands.CommandError(
                "Too many retries, please restart the process.")

        em = discord.Embed(title="Turnip Stonks Bot",
                           description="Any other details?",
                           color=0xF4B400)
        em.set_thumbnail(url=self.thumbnail_url)
        await ctx.author.send(embed=em)

        msg = await self.bot.wait_for('message', check=msgcheck, timeout=60)
        other_info = msg.clean_content

        em = discord.Embed(title="Turnip Stonks Bot",
                           description="",
                           color=0xF4B400)
        em.set_thumbnail(url=self.thumbnail_url)
        em.add_field(name="Seller", value=f"<@{ctx.author.id}>")
        em.add_field(name="Selling", value=sale_item, inline=False)
        em.add_field(name="Price", value=item_price, inline=False)
        em.add_field(name="More Information", value=other_info, inline=False)

        channel = int(os.getenv(market_opt.name))
        await self.bot.get_channel(channel).send(embed=em)

        em = discord.Embed(
            title="Turnip Stonks Bot",
            description=
            f"Thanks! Check <#{channel}> for your listing. Here's the info you provided:",
            color=0xF4B400)
        em.set_thumbnail(url=self.thumbnail_url)
        em.add_field(name="Selling", value=sale_item, inline=False)
        em.add_field(name="Price", value=item_price, inline=False)
        em.add_field(name="More Information", value=other_info, inline=False)

        await ctx.author.send(embed=em)

    async def buying_dialogue(self, ctx, market_opt: MarketChan):
        def msgcheck(m):
            return m.author == ctx.author

        em = discord.Embed(title="Turnip Stonks Bot",
                           description="What are you buying?",
                           color=0xF4B400)
        em.set_thumbnail(url=self.thumbnail_url)
        await ctx.author.send(embed=em)

        msg = await self.bot.wait_for('message', check=msgcheck, timeout=60)
        buy_item = msg.clean_content

        em = discord.Embed(title="Turnip Stonks Bot",
                           description="What's the offer price?",
                           color=0xF4B400)
        em.set_thumbnail(url=self.thumbnail_url)
        await ctx.author.send(embed=em)

        # Clunky validation loop to ensure price is a number
        item_price = None
        for i in range(5):
            msg = await self.bot.wait_for('message',
                                          check=msgcheck,
                                          timeout=60)
            if msg.clean_content.isdigit():
                item_price = msg.clean_content
                break

            await ctx.author.send(
                f"Price can only be digits. {4 - i} tries remaining.")

        if not item_price:
            raise commands.CommandError(
                "Too many retries, please restart the process.")

        em = discord.Embed(title="Turnip Stonks Bot",
                           description="Any other details?",
                           color=0xF4B400)
        em.set_thumbnail(url=self.thumbnail_url)
        await ctx.author.send(embed=em)

        msg = await self.bot.wait_for('message', check=msgcheck, timeout=60)
        other_info = msg.clean_content

        em = discord.Embed(title="Turnip Stonks Bot",
                           description="",
                           color=0xF4B400)
        em.set_thumbnail(url=self.thumbnail_url)
        em.add_field(name="Buyer", value=f"<@{ctx.author.id}>")
        em.add_field(name="Buying", value=buy_item, inline=False)
        em.add_field(name="Offer Price", value=item_price, inline=False)
        em.add_field(name="More Information", value=other_info, inline=False)

        channel = int(os.getenv(market_opt.name))
        await self.bot.get_channel(channel).send(embed=em)

        em = discord.Embed(
            title="Turnip Stonks Bot",
            description=
            f"Thanks! Check <#{channel}> for your listing. Here's the info you provided:",
            color=0xF4B400)
        em.set_thumbnail(url=self.thumbnail_url)
        em.add_field(name="Buying", value=buy_item, inline=False)
        em.add_field(name="Offer Price", value=item_price, inline=False)
        em.add_field(name="More Information", value=other_info, inline=False)

        await ctx.author.send(embed=em)

    @market.command()
    @checks.is_dm()
    async def list(self, ctx: commands.Context):
        def msgcheck(m: discord.Message):
            return m.author == ctx.author and m.channel == ctx.channel

        em_desc = (
            f"Hey <@{ctx.author.id}>!\n\n"
            f"Welcome to the marketplace! What are you listing? Please enter a number from below:\n\n"
            f"1. Accessories\n2. DIY recipes\n3. Floors / rugs / wallpapers\n"
            f"4. Flowers\n5. Fossils\n6. Housewares\n"
            f"7. Materials\n8. Seasonal (e.g., Bunny Day eggs)\n9. Miscellaneous"
        )
        em = discord.Embed(title="Turnip Stonks Bot",
                           description=em_desc,
                           color=0xF4B400)
        em.set_thumbnail(url=self.thumbnail_url)
        await ctx.author.send(embed=em)

        market_opt = 0
        for i in range(5):
            message = await self.bot.wait_for('message',
                                              check=msgcheck,
                                              timeout=60)
            if message.clean_content.isdigit() and 1 <= int(
                    message.clean_content) <= 9:
                market_opt = MarketChan(int(message.clean_content))
                break

            num_tries = 4 - i
            if num_tries == 0:
                raise commands.CommandError("Too many retries")
            await ctx.author.send(
                f"Option can only be a digit between 1 and 9. {num_tries} tries remaining."
            )

        em = discord.Embed(
            title="Turnip Stonks Bot",
            description=f"Ok! Are you trading, selling, or buying?"
            f"\n\n :one: - Trading!\n:two: - Selling!\n:three: - Buying!",
            color=0xF4B400)
        em.set_thumbnail(url=self.thumbnail_url)
        em_message = await ctx.author.send(embed=em)

        for emoji in self.reaction_emojis:
            await em_message.add_reaction(emoji)

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
                await self.trading_dialogue(ctx, market_opt)
            elif reaction == self.reaction_emojis[1]:
                await self.selling_dialogue(ctx, market_opt)
            elif reaction == self.reaction_emojis[2]:
                await self.buying_dialogue(ctx, market_opt)
            else:
                await ctx.author.send(
                    "Invalid reaction. Please restart the process by using `!market`"
                )
        except asyncio.TimeoutError as e:
            await ctx.author.send(
                "You took too long to respond! Please restart the process by using `!market`"
            )
            log.info(e)


def setup(bot):
    bot.add_cog(Market(bot))
