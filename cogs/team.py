import discord, asyncio, random, json
from discord.ext import commands
from utils.utils import TYPING_WPM, CalcTypingTime

"""
Team Cog:

To show Team stats and other misc. stuff related to the Team.

- A Chinese Government function for bulk deletes.

Some 'on_message' keyword hooks:
  - Kids in Sock's Basement.
  - Sock has Chlamydia.

Commands:
  - tquote: Out Of Context quotes from yours truly!
  - team: Sends an Embed with a list of the team members.
"""

class TeamCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        details_json = json.load(open("details.json"))
        self.cps = details_json.get("wpm", 55)
        self.last_quote = ""
        self.last_quoter = ""

        self.last_hook_msgs = {}

        self.bot = bot

        self.quotes = json.load(open("cogs/team_resources/quotes.json"))
        self.messages = json.load(open("cogs/team_resources/messages.json"))
        self.team_members = json.load(open("cogs/team_resources/team_members.json"))

        self.keyword_func_dict = {
            (("i", "like"), ): self.so_did_hitler,
            ("cry", "crying"): self.pussy,
            ("basement", "loli", "lolis"): self.lolis_say_hi,
            ("std", "aids", "chlamydia"): self.sock_has_chlamydia,
        }

    async def send_hook_messages(self, channel: discord.TextChannel, key: str):
        if key not in self.messages:
            return

        while True:
            if len(self.messages[key]) > 1:
                msgs = random.choice(self.messages[key])
                if self.last_hook_msgs.get(key, []) != msgs:
                    break
            else:
                msgs = self.messages[key][0]
                break

        for msg in msgs:
            with channel.typing():
                await asyncio.sleep(CalcTypingTime(msg))
                await channel.send(msg)

        self.last_hook_msgs[key] = msgs

    @commands.Cog.listener()
    async def on_bulk_message_delete(self, messages: list):
        channel = messages[0].channel
        if not channel:
            return

        await self.send_hook_messages(channel, "bulk_delete")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return

        channel = message.channel
        if not channel:
            return

        message_content = message.content.lower()

        for keywords, func in self.keyword_func_dict.items():
            if not isinstance(keywords, tuple):
                keywords = (keywords, )

            checks = []
            for item in keywords:
                if isinstance(item, str):
                    checks.append(item in message_content.lower().split())
                elif isinstance(item, tuple):
                    checks.append(all([word.lower() in message_content.lower().split() for word in item]))

            if any(checks) and random.randint(1, 2) == 1:
                await func(channel=channel, message=message)
                return

    @commands.command()
    async def team(self, ctx:commands.Context):
        embed: discord.Embed = discord.Embed(title="Meet The Team", color=0x61adff)
        embed.set_author(name="MooseBoard")

        for role, members in self.team_members.items():
            if not isinstance(members, (tuple, list)):
                members = [ members ]
            embed.add_field(name=role, value="\n".join(members), inline=False)

        embed.set_footer(text="© Team Icebreaker")
        await ctx.send(embed=embed)

    @commands.command()
    async def tquote(self, ctx:commands.Context):
        while True:
            quoter = random.choice(list(self.quotes.keys()))
            quote = random.choice(self.quotes[quoter])
            if (self.last_quote, self.last_quoter) != (quote, quoter):
                break

        self.last_quote, self.last_quoter = quote, quoter

        message = f"*{quote}*\n- *{quoter}*"

        with ctx.channel.typing():
            await asyncio.sleep(CalcTypingTime(message))
            await ctx.channel.send(message)

    async def lolis_say_hi(self, channel: discord.TextChannel, **kwargs):
        await self.send_hook_messages(channel, "lolis")

    async def sock_has_chlamydia(self, channel: discord.TextChannel, **kwargs):
        await self.send_hook_messages(channel, "std")

    async def so_did_hitler(self, channel: discord.TextChannel, message: discord.TextChannel,**kwargs):
        if len(message.content.lower().split()) > 2:
            await self.send_hook_messages(channel, "ilike")

    async def pussy(self, channel: discord.TextChannel, **kwargs):
        await self.send_hook_messages(channel, "pussy")

def setup(bot):
    bot.add_cog(TeamCog(bot))