import asyncio
from enum import Enum
import logging
import os

from discord.ext import commands
from .utils import checks
import discord

log = logging.getLogger(__name__)

SERVER_ID = int(os.getenv('GUILD_ID'))
NOOKAZON_CHANNEL = int(os.getenv('NOOKAZON_CHAN_ID'))
CATALOG_CHANNEL = int(os.getenv('CATALOGING_CHAN_ID'))
CRAFTING_CHANNEL = int(os.getenv('CRAFTING_CHAN_ID'))
RESIDENT_CHANNEL = int(os.getenv('RESIDENT_CHAN_ID'))


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
        em = discord.Embed(
            title="Turnip Stonks Bot",
            description=
            "There was an error! Please restart the process by using `!market`",
            color=0xF4B400)
        em.set_thumbnail(url=self.thumbnail_url)
        return await ctx.author.send(embed=em)

    @commands.group()
    @checks.is_dm()
    async def market(self, ctx: commands.Context):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)

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
            em = discord.Embed(
                title="Turnip Stonks Bot",
                description="Too many retries, please restart the process.",
                color=0xF4B400)
            em.set_thumbnail(url=self.thumbnail_url)
            return await ctx.author.send(embed=em)

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
            em = discord.Embed(
                title="Turnip Stonks Bot",
                description="Too many retries, please restart the process.",
                color=0xF4B400)
            em.set_thumbnail(url=self.thumbnail_url)
            return await ctx.author.send(embed=em)

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
                em = discord.Embed(
                    title="Turnip Stonks Bot",
                    description="Too many retries, please restart the process.",
                    color=0xF4B400)
                em.set_thumbnail(url=self.thumbnail_url)
                return await ctx.author.send(embed=em)
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
                em = discord.Embed(
                    title="Turnip Stonks Bot",
                    description=
                    "Invalid reaction. Please restart the process by using `!market`",
                    color=0xF4B400)
                em.set_thumbnail(url=self.thumbnail_url)
                return await ctx.author.send(embed=em)
        except asyncio.TimeoutError:
            em = discord.Embed(
                title="Turnip Stonks Bot",
                description=
                "You took too long to respond! Please restart the process by using `!market`",
                color=0xF4B400)
            em.set_thumbnail(url=self.thumbnail_url)
            return await ctx.author.send(embed=em)

    async def catalog_offer(self, ctx: commands.Context):
        def msgcheck(m: discord.Message):
            return m.author == ctx.author and m.channel == ctx.channel

        em = discord.Embed(title="Turnip Stonks Bot",
                           description="Ok! What are you offering to catalog?",
                           color=0xF4B400)
        em.set_thumbnail(url=self.thumbnail_url)
        await ctx.author.send(embed=em)

        msg = await self.bot.wait_for('message', check=msgcheck, timeout=60)
        catalog_item = msg.clean_content

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
        msg = await self.bot.wait_for('message', check=msgcheck, timeout=60)
        turnip_url = msg.clean_content

        em = discord.Embed(title="Turnip Stonks Bot",
                           description="Ok! Any other information?",
                           color=0xF4B400)
        em.set_thumbnail(url=self.thumbnail_url)
        await ctx.author.send(embed=em)

        msg = await self.bot.wait_for('message', check=msgcheck, timeout=60)
        other_info = msg.clean_content

        em = discord.Embed(title="Turnip Stonks Bot",
                           description="",
                           color=0xF4B400)
        em.set_thumbnail(url=self.thumbnail_url)
        em.add_field(name="User", value=f"<@{ctx.author.id}>")
        em.add_field(name="Cataloging", value=catalog_item, inline=False)
        em.add_field(name="Turnip Exchange URL",
                     value=turnip_url,
                     inline=False)
        em.add_field(name="More Information", value=other_info, inline=False)

        await self.bot.get_channel(CATALOG_CHANNEL).send(embed=em)

        em = discord.Embed(
            title="Turnip Stonks Bot",
            description=
            f"Thanks! Check <#{CATALOG_CHANNEL}> for your listing. Here's the info you provided:",
            color=0xF4B400)
        em.set_thumbnail(url=self.thumbnail_url)
        em.add_field(name="Cataloging", value=catalog_item, inline=False)
        em.add_field(name="Turnip Exchange URL",
                     value=turnip_url,
                     inline=False)
        em.add_field(name="More Information", value=other_info, inline=False)

        await ctx.author.send(embed=em)

    async def catalog_looking(self, ctx: commands.Context):
        def msgcheck(m: discord.Message):
            return m.author == ctx.author and m.channel == ctx.channel

        em = discord.Embed(title="Turnip Stonks Bot",
                           description="Ok! What are you looking to catalog?",
                           color=0xF4B400)
        em.set_thumbnail(url=self.thumbnail_url)
        await ctx.author.send(embed=em)

        msg = await self.bot.wait_for('message', check=msgcheck, timeout=60)
        catalog_item = msg.clean_content

        em = discord.Embed(title="Turnip Stonks Bot",
                           description="Ok! Any other information?",
                           color=0xF4B400)
        em.set_thumbnail(url=self.thumbnail_url)
        await ctx.author.send(embed=em)

        msg = await self.bot.wait_for('message', check=msgcheck, timeout=60)
        other_info = msg.clean_content

        em = discord.Embed(title="Turnip Stonks Bot",
                           description="",
                           color=0xF4B400)
        em.set_thumbnail(url=self.thumbnail_url)
        em.add_field(name="User", value=f"<@{ctx.author.id}>")
        em.add_field(name="Looking to catalog",
                     value=catalog_item,
                     inline=False)
        em.add_field(name="More Information", value=other_info, inline=False)

        await self.bot.get_channel(CATALOG_CHANNEL).send(embed=em)

        em = discord.Embed(
            title="Turnip Stonks Bot",
            description=
            f"Thanks! Check <#{CATALOG_CHANNEL}> for your listing. Here's the info you provided:",
            color=0xF4B400)
        em.set_thumbnail(url=self.thumbnail_url)
        em.add_field(name="Looking to catalog",
                     value=catalog_item,
                     inline=False)
        em.add_field(name="More Information", value=other_info, inline=False)

        await ctx.author.send(embed=em)

    @market.command()
    @checks.is_dm()
    async def catalog(self, ctx: commands.Context):
        em = discord.Embed(
            title="Turnip Stonks Bot",
            description=
            f"Hey <@{ctx.author.id}>! Are you offering to catalog or looking to "
            f"catalog an item?\n\n:one: - Offering!\n:two: - Looking!",
            color=0xF4B400)
        em.set_thumbnail(url=self.thumbnail_url)
        em_message = await ctx.author.send(embed=em)

        for emoji in self.reaction_emojis[:2]:
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
                await self.catalog_offer(ctx)
            elif reaction == self.reaction_emojis[1]:
                await self.catalog_looking(ctx)
            else:
                em = discord.Embed(
                    title="Turnip Stonks Bot",
                    description=
                    "Invalid reaction! Please restart the process by using `!market`",
                    color=0xF4B400)
                em.set_thumbnail(url=self.thumbnail_url)
                return await ctx.author.send(embed=em)
        except asyncio.TimeoutError:
            em = discord.Embed(
                title="Turnip Stonks Bot",
                description=
                "You took too long to respond! Please restart the process by using `!market`",
                color=0xF4B400)
            em.set_thumbnail(url=self.thumbnail_url)
            return await ctx.author.send(embed=em)

    async def crafting_offer(self, ctx: commands.Context):
        def msgcheck(m: discord.Message):
            return m.author == ctx.author and m.channel == ctx.channel

        em = discord.Embed(title="Turnip Stonks Bot",
                           description="Awesome! What are you crafting?",
                           color=0xF4B400)
        em.set_thumbnail(url=self.thumbnail_url)
        await ctx.author.send(embed=em)

        msg = await self.bot.wait_for('message', check=msgcheck, timeout=60)
        crafting_item = msg.clean_content

        em = discord.Embed(
            title="Turnip Stonks Bot",
            description=f"Ok! Do you need people to provide materials?\n\n"
            f":one: - Yes\n:two: - No",
            color=0xF4B400)
        em.set_thumbnail(url=self.thumbnail_url)
        em_message = await ctx.author.send(embed=em)

        for emoji in self.reaction_emojis[:2]:
            await em_message.add_reaction(emoji)

        def react_check(payload):
            if payload.user_id != ctx.author.id:
                return False

            to_check = str(payload.emoji)
            for emoji in self.reaction_emojis:
                if to_check == emoji:
                    return True
            return False

        payload = await self.bot.wait_for('raw_reaction_add',
                                          check=react_check,
                                          timeout=60)
        reaction = str(payload.emoji)

        mats_req = "No"
        if reaction == self.reaction_emojis[0]:
            mats_req = "Yes"
        else:
            em = discord.Embed(
                title="Turnip Stonks Bot",
                description=
                "Invalid reaction! Please restart the process by using `!market`",
                color=0xF4B400)
            em.set_thumbnail(url=self.thumbnail_url)
            return await ctx.author.send(embed=em)

        em = discord.Embed(title="Turnip Stonks Bot",
                           description="Ok! Any other information?",
                           color=0xF4B400)
        em.set_thumbnail(url=self.thumbnail_url)
        await ctx.author.send(embed=em)

        msg = await self.bot.wait_for('message', check=msgcheck, timeout=60)
        other_info = msg.clean_content

        em = discord.Embed(title="Turnip Stonks Bot",
                           description="",
                           color=0xF4B400)
        em.set_thumbnail(url=self.thumbnail_url)
        em.add_field(name="User", value=f"<@{ctx.author.id}>")
        em.add_field(name="Offering to craft",
                     value=crafting_item,
                     inline=False)
        em.add_field(name="Materials required?", value=mats_req, inline=False)
        em.add_field(name="More Information", value=other_info, inline=False)

        await self.bot.get_channel(CRAFTING_CHANNEL).send(embed=em)

        em = discord.Embed(
            title="Turnip Stonks Bot",
            description=
            f"Thanks! Check <#{CRAFTING_CHANNEL}> for your listing. Here's the info you provided:",
            color=0xF4B400)
        em.set_thumbnail(url=self.thumbnail_url)
        em.add_field(name="Offering to craft",
                     value=crafting_item,
                     inline=False)
        em.add_field(name="Materials required?", value=mats_req, inline=False)
        em.add_field(name="More Information", value=other_info, inline=False)

        await ctx.author.send(embed=em)

    async def crafting_looking(self, ctx: commands.Context):
        def msgcheck(m: discord.Message):
            return m.author == ctx.author and m.channel == ctx.channel

        em = discord.Embed(title="Turnip Stonks Bot",
                           description="Ok! What are you looking to craft?",
                           color=0xF4B400)
        em.set_thumbnail(url=self.thumbnail_url)
        await ctx.author.send(embed=em)

        msg = await self.bot.wait_for('message', check=msgcheck, timeout=60)
        crafting_item = msg.clean_content

        em = discord.Embed(title="Turnip Stonks Bot",
                           description=f"Ok! Can you provide materials?\n\n"
                           f":one: - Yes\n:two: - No",
                           color=0xF4B400)
        em.set_thumbnail(url=self.thumbnail_url)
        em_message = await ctx.author.send(embed=em)

        for emoji in self.reaction_emojis[:2]:
            await em_message.add_reaction(emoji)

        def react_check(payload):
            if payload.user_id != ctx.author.id:
                return False

            to_check = str(payload.emoji)
            for emoji in self.reaction_emojis:
                if to_check == emoji:
                    return True
            return False

        payload = await self.bot.wait_for('raw_reaction_add',
                                          check=react_check,
                                          timeout=60)
        reaction = str(payload.emoji)

        mats_req = "No"
        if reaction == self.reaction_emojis[0]:
            mats_req = "Yes"
        elif reaction == self.reaction_emojis[1]:
            pass
        else:
            em = discord.Embed(
                title="Turnip Stonks Bot",
                description=
                "Invalid reaction! Please restart the process by using `!market`",
                color=0xF4B400)
            em.set_thumbnail(url=self.thumbnail_url)
            return await ctx.author.send(embed=em)

        em = discord.Embed(title="Turnip Stonks Bot",
                           description="Ok! Any other information?",
                           color=0xF4B400)
        em.set_thumbnail(url=self.thumbnail_url)
        await ctx.author.send(embed=em)

        msg = await self.bot.wait_for('message', check=msgcheck, timeout=60)
        other_info = msg.clean_content

        em = discord.Embed(title="Turnip Stonks Bot",
                           description="",
                           color=0xF4B400)
        em.set_thumbnail(url=self.thumbnail_url)
        em.add_field(name="User", value=f"<@{ctx.author.id}>")
        em.add_field(name="Looking to craft",
                     value=crafting_item,
                     inline=False)
        em.add_field(name="Materials provided?", value=mats_req, inline=False)
        em.add_field(name="More Information", value=other_info, inline=False)

        await self.bot.get_channel(CRAFTING_CHANNEL).send(embed=em)

        em = discord.Embed(
            title="Turnip Stonks Bot",
            description=
            f"Thanks! Check <#{CRAFTING_CHANNEL}> for your listing. Here's the info you provided:",
            color=0xF4B400)
        em.set_thumbnail(url=self.thumbnail_url)
        em.add_field(name="Looking to craft",
                     value=crafting_item,
                     inline=False)
        em.add_field(name="Materials provided?", value=mats_req, inline=False)
        em.add_field(name="More Information", value=other_info, inline=False)

        await ctx.author.send(embed=em)

    @market.command()
    @checks.is_dm()
    async def crafting(self, ctx: commands.Context):
        em = discord.Embed(
            title="Turnip Stonks Bot",
            description=
            f"Hey <@{ctx.author.id}>! Are you offering to craft or do you need "
            f"something crafts?\n\n:one: - Offering!\n:two: - Looking!",
            color=0xF4B400)
        em.set_thumbnail(url=self.thumbnail_url)
        em_message = await ctx.author.send(embed=em)

        for emoji in self.reaction_emojis[:2]:
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
                await self.crafting_offer(ctx)
            elif reaction == self.reaction_emojis[1]:
                await self.crafting_looking(ctx)
            else:
                em = discord.Embed(
                    title="Turnip Stonks Bot",
                    description=
                    "Invalid reaction! Please restart the process by using `!market`",
                    color=0xF4B400)
                em.set_thumbnail(url=self.thumbnail_url)
                return await ctx.author.send(embed=em)
        except asyncio.TimeoutError:
            em = discord.Embed(
                title="Turnip Stonks Bot",
                description=
                "You took too long to respond! Please restart the process by using `!market`",
                color=0xF4B400)
            em.set_thumbnail(url=self.thumbnail_url)
            return await ctx.author.send(embed=em)

    async def resident_offer(self, ctx: commands.Context):
        def msgcheck(m: discord.Message):
            return m.author == ctx.author and m.channel == ctx.channel

        em = discord.Embed(title="Turnip Stonks Bot",
                           description="Ok! Who are you offering?",
                           color=0xF4B400)
        em.set_thumbnail(url=self.thumbnail_url)
        await ctx.author.send(embed=em)

        msg = await self.bot.wait_for('message', check=msgcheck, timeout=60)
        resident = msg.clean_content

        em = discord.Embed(title="Turnip Stonks Bot",
                           description=f"Ok! Are they in boxes?\n\n"
                           f":one: - Yes\n:two: - No",
                           color=0xF4B400)
        em.set_thumbnail(url=self.thumbnail_url)
        em_message = await ctx.author.send(embed=em)

        for emoji in self.reaction_emojis[:2]:
            await em_message.add_reaction(emoji)

        def react_check(payload):
            if payload.user_id != ctx.author.id:
                return False

            to_check = str(payload.emoji)
            for emoji in self.reaction_emojis:
                if to_check == emoji:
                    return True
            return False

        payload = await self.bot.wait_for('raw_reaction_add',
                                          check=react_check,
                                          timeout=60)
        reaction = str(payload.emoji)
        asking_for = None
        other_info = None
        if reaction == self.reaction_emojis[0]:
            em = discord.Embed(
                title="Turnip Stonks Bot",
                description=f"Ok! Are you asking for anything in return?\n\n"
                f":one: - Yes\n:two: - No",
                color=0xF4B400)
            em.set_thumbnail(url=self.thumbnail_url)
            em_message = await ctx.author.send(embed=em)

            for emoji in self.reaction_emojis[:2]:
                await em_message.add_reaction(emoji)

            payload = await self.bot.wait_for('raw_reaction_add',
                                              check=react_check,
                                              timeout=60)
            ret_reaction = str(payload.emoji)

            if ret_reaction == self.reaction_emojis[0]:
                em = discord.Embed(title="Turnip Stonks Bot",
                                   description="Ok! What are you asking for?",
                                   color=0xF4B400)
                em.set_thumbnail(url=self.thumbnail_url)
                await ctx.author.send(embed=em)

                msg = await self.bot.wait_for('message',
                                              check=msgcheck,
                                              timeout=60)
                asking_for = msg.clean_content

                em = discord.Embed(title="Turnip Stonks Bot",
                                   description="Ok! Any other information?",
                                   color=0xF4B400)
                em.set_thumbnail(url=self.thumbnail_url)
                await ctx.author.send(embed=em)

                msg = await self.bot.wait_for('message',
                                              check=msgcheck,
                                              timeout=60)
                other_info = msg.clean_content
            elif ret_reaction == self.reaction_emojis[1]:
                em = discord.Embed(title="Turnip Stonks Bot",
                                   description="Ok! Any other information?",
                                   color=0xF4B400)
                em.set_thumbnail(url=self.thumbnail_url)
                await ctx.author.send(embed=em)

                msg = await self.bot.wait_for('message',
                                              check=msgcheck,
                                              timeout=60)
                other_info = msg.clean_content
            else:
                em = discord.Embed(
                    title="Turnip Stonks Bot",
                    description=
                    "Invalid reaction! Please restart the process by using `!market`",
                    color=0xF4B400)
                em.set_thumbnail(url=self.thumbnail_url)
                return await ctx.author.send(embed=em)
        elif reaction == self.reaction_emojis[1]:
            em = discord.Embed(
                title="Turnip Stonks Bot",
                description=
                "Sorry! Residents must be in boxes first before listing!",
                color=0xF4B400)
            em.set_thumbnail(url=self.thumbnail_url)
            return await ctx.author.send(embed=em)
        else:
            em = discord.Embed(
                title="Turnip Stonks Bot",
                description=
                "Invalid reaction. Please restart the process by using `!market`",
                color=0xF4B400)
            em.set_thumbnail(url=self.thumbnail_url)
            return await ctx.author.send(embed=em)

        em = discord.Embed(title="Turnip Stonks Bot",
                           description="",
                           color=0xF4B400)
        em.set_thumbnail(url=self.thumbnail_url)
        em.add_field(name="User", value=f"<@{ctx.author.id}>")
        em.add_field(name="Offering resident", value=resident, inline=False)
        if asking_for:
            em.add_field(name="Asking for", value=asking_for, inline=False)
        if other_info:
            em.add_field(name="More Information",
                         value=other_info,
                         inline=False)

        await self.bot.get_channel(RESIDENT_CHANNEL).send(embed=em)

        em = discord.Embed(
            title="Turnip Stonks Bot",
            description=
            f"Thanks! Check <#{RESIDENT_CHANNEL}> for your listing. Here's the info you provided:",
            color=0xF4B400)
        em.set_thumbnail(url=self.thumbnail_url)
        em.add_field(name="Offering resident", value=resident, inline=False)
        if asking_for:
            em.add_field(name="Asking for", value=asking_for, inline=False)
        if other_info:
            em.add_field(name="More Information",
                         value=other_info,
                         inline=False)

        await ctx.author.send(embed=em)

    async def resident_looking(self, ctx: commands.Context):
        def msgcheck(m: discord.Message):
            return m.author == ctx.author and m.channel == ctx.channel

        em = discord.Embed(title="Turnip Stonks Bot",
                           description=f"Ok! Who are you looking for?",
                           color=0xF4B400)
        em.set_thumbnail(url=self.thumbnail_url)
        await ctx.author.send(embed=em)

        msg = await self.bot.wait_for('message', check=msgcheck, timeout=60)
        resident = msg.clean_content

        em = discord.Embed(title="Turnip Stonks Bot",
                           description="Ok! Offering anything in return?",
                           color=0xF4B400)
        em.set_thumbnail(url=self.thumbnail_url)
        await ctx.author.send(embed=em)

        msg = await self.bot.wait_for('message', check=msgcheck, timeout=60)
        trade = msg.clean_content

        em = discord.Embed(title="Turnip Stonks Bot",
                           description="Ok! Any other information?",
                           color=0xF4B400)
        em.set_thumbnail(url=self.thumbnail_url)
        await ctx.author.send(embed=em)

        msg = await self.bot.wait_for('message', check=msgcheck, timeout=60)
        other_info = msg.clean_content

        em = discord.Embed(title="Turnip Stonks Bot",
                           description="",
                           color=0xF4B400)
        em.set_thumbnail(url=self.thumbnail_url)
        em.add_field(name="User", value=f"<@{ctx.author.id}>")
        em.add_field(name="In search of resident",
                     value=resident,
                     inline=False)
        em.add_field(name="Trades?", value=trade, inline=False)
        em.add_field(name="More Information", value=other_info, inline=False)

        await self.bot.get_channel(RESIDENT_CHANNEL).send(embed=em)

        em = discord.Embed(
            title="Turnip Stonks Bot",
            description=
            f"Thanks! Check <#{RESIDENT_CHANNEL}> for your listing. Here's the info you provided:",
            color=0xF4B400)
        em.set_thumbnail(url=self.thumbnail_url)
        em.add_field(name="In search of resident",
                     value=resident,
                     inline=False)
        em.add_field(name="Trades?", value=trade, inline=False)
        em.add_field(name="More Information", value=other_info, inline=False)

        await ctx.author.send(embed=em)

    @market.command()
    @checks.is_dm()
    async def residents(self, ctx: commands.Context):
        em = discord.Embed(
            title="Turnip Stonks Bot",
            description=
            f"Hey <@{ctx.author.id}>! Are you offering a resident or "
            f"looking for a resident?\n\n:one: - Offering!\n:two: - Looking!",
            color=0xF4B400)
        em.set_thumbnail(url=self.thumbnail_url)
        em_message = await ctx.author.send(embed=em)

        for emoji in self.reaction_emojis[:2]:
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
                await self.resident_offer(ctx)
            elif reaction == self.reaction_emojis[1]:
                await self.resident_looking(ctx)
            else:
                em = discord.Embed(
                    title="Turnip Stonks Bot",
                    description=
                    "Invalid reaction! Please restart the process by using `!market`",
                    color=0xF4B400)
                em.set_thumbnail(url=self.thumbnail_url)
                return await ctx.author.send(embed=em)
        except asyncio.TimeoutError:
            em = discord.Embed(
                title="Turnip Stonks Bot",
                description=
                "You took too long to respond! Please restart the process by using `!market`",
                color=0xF4B400)
            em.set_thumbnail(url=self.thumbnail_url)
            return await ctx.author.send(embed=em)


def setup(bot):
    bot.add_cog(Market(bot))
