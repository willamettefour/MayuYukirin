import aiohttp
import discord
import random
import re

from colour import Color as col
from colour import rgb2hex
from redbot.core import commands

class Random(commands.Cog):
    """Commands that randomly generate/send things."""

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()
        self.catapi = "https://shibe.online/api/cats"
        self.dogapi = "https://dog.ceo/api/breeds/image/random"
        self.foxapi = "http://wohlsoft.ru/images/foxybot/randomfox.php"
        self.error_message = "An API error occured. Probably just a hiccup.\nIf this error persists for several days, please report it."
        
    def rgb_to_decimal(self, rgb):
        return (rgb[0] << 16) + (rgb[1] << 8) + rgb[2]

    def decimal_to_rgb(self, d):
        return ((d >> 16) & 255, (d >> 8) & 255, d & 255)

    async def build_embed(self, co):
        if isinstance(co, int):
            rgb = self.decimal_to_rgb(co)
            r, g, b = rgb[0] / 255, rgb[1] / 255, rgb[2] / 255
            co = col(rgb=(r, g, b))
        else:
            rgb = tuple([int(c * 255) for c in co.rgb])
        hexa = rgb2hex(co.rgb, force_long=True)
        extended = ", ".join([f"{(part*255):.0f}" for part in co.rgb])
        return extended
        
    @commands.group()
    async def random(self, ctx):
        """Commands that randomly generate/send things."""
        
    @random.command()
    async def color(self, ctx):
        """Generates a random color"""
        color = random.randint(0, 0xFFFFFF)
        color2 = "%06x" % color
        color3 = f"#{color2}"
        match = re.match(r"(?i)^(?:0x|#|)((?:[a-fA-F0-9]{3}){1,2})$", color3)
        c = col("#" + match.group(1))
        extended = await self.build_embed(c)
        embed = discord.Embed(title="", description=f"rgb: {extended}", color=color)
        embed.set_author(name=f"random color — {color3}")
        embed.set_image(url=f"https://fakeimg.pl/600x200/{color2}/?text=%20")
        await ctx.send(embed=embed)

    @random.command()
    async def cat(self, ctx):
        """Sends a random cat"""
        try:
            async with self.session.get(self.catapi) as r:
                result = await r.json()
            await ctx.send(result[0])
        except:
            await ctx.send(self.error_message)

    @random.command()
    async def dog(self, ctx):
        """Sends a random dog"""
        api = self.dogapi
        try:
            async with self.session.get(api) as r:
                result = await r.json()
            await ctx.send(result['message'])
        except Exception:
            await ctx.send(self.error_message)
                
    @random.command()
    async def fox(self, ctx):
        """Sends a random fox"""
        try:
            async with self.session.get(self.foxapi) as r:
                result = await r.json()
            await ctx.send(result['file'])
        except:
            await ctx.send(self.error_message)
         
    def cog_unload(self):
        self.bot.loop.create_task(self.session.close())