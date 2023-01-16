import openai
import discord
import config

client = discord.Client()

openai.api_key = config.OPENAI_API_KEY


async def generate_opinion(message):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"What is your opinion on {message}?"
    )
    return response.choices[0].text

@client.event
async def on_message(message):
    if message.content.startswith("!opinion"):
        opinion = await generate_opinion(message.content[8:])
        await message.channel.send(opinion)

client.run(config.DISCORD_TOKEN)
