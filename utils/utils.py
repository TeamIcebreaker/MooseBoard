import discord, re, json, asyncio
from discord.ext import commands

'''
Misc. functions and values.
'''

global TYPING_WPM, BOT_TOKEN

details_json = json.load(open("details.json"))

BOT_TOKEN = details_json.get("token")
TYPING_WPM = details_json.get("wpm", 50)

def FilterLinks(message: discord.Message):
    """
    Used to remove all embeds and urls for retrieving
    filtered message used for flagging and events. 
    """

    urls = [embed.url for embed in message.embeds]
    url_regex = re.compile('|'.join(map(re.escape, urls)))
    message_text = url_regex.sub("", message.content)
    return message_text

def CalcTypingTime(message_content: str):
    """
    Calculate the time for typing.
    """

    word_count = len(message_content.split())
    delay = (word_count / TYPING_WPM) * 60
    return delay

async def SendMSGTyping(channel: discord.TextChannel, message):
    """
    Send message after a calculated delay in the typing state.
    """

    message = str(message)
    with channel.typing():
        await asyncio.sleep(CalcTypingTime(message))
        await channel.send(message)
