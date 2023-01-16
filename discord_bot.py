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

async def generate_code(language, message):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Code this in {language}: {message}"
    )
    return response.choices[0].text

@client.event
async def on_message(message):
    try:
        if message.content == "!help":
            help_message = "Available commands: !opinion, !code <language> <prompt>, !help"
            await message.channel.send(help_message)
        elif message.content.startswith("!opinion"):
            opinion = await generate_opinion(message.content[8:])
            await message.channel.send(opinion)
        elif message.content.startswith("!code"):
            command, language, prompt = message.content.split(" ", 2)
            code = await generate_code(language, prompt)
            await message.channel.send(code)
    except Exception as e:
        await message.channel.send("Sorry, something went wrong. Please try again later.")
        print(e)


client.run(config.DISCORD_TOKEN)
