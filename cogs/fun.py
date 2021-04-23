import discord, asyncio, random, json, requests
from discord.ext import commands
from utils.utils import SendMSGTyping
from jokeapi import Jokes

class FunCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.jokeapi = Jokes()
        self.bot = bot
        self.api_fail_messages = {
            "The API didn't return anything.",
            "***W h e e z e***"
        }

    @commands.command()
    async def insult(self, ctx: commands.Context):
        """
        Posts a insult from the EvilInsult API.
        """
        response = requests.get("https://evilinsult.com/generate_insult.php?lang=en&type=json")
        insult_json = json.loads(response.content)
        message = insult_json.get("insult", None)
        await self.SendWithErrorReport(ctx.channel, message)

    async def SendWithErrorReport(self, channel: discord.TextChannel, messages=None):
        """
        Sends the message(s) given to it as a string or a list of strings.
        """
        messages = messages or self.api_fail_messages

        if isinstance(messages, str):
            messages = [ messages ]

        for message in messages:
            await SendMSGTyping(channel, message)
            await asyncio.sleep(0.5)

    @commands.command()
    async def joke(self, ctx: commands.Context):
        response = self.jokeapi.get_joke(lang="en")
        if not response or response.get("error"):
            await self.SendWithErrorReport(ctx.channel)

        else:
            if response["type"] == "single":
                await self.SendWithErrorReport(ctx.channel, response["joke"])
            else:
                await self.SendWithErrorReport(ctx.channel, [ response["setup"], response["delivery"] ])

def setup(bot):
    bot.add_cog(FunCog(bot))