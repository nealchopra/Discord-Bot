import openai
import discord
import config

client = discord.Client()

openai.api_key = config.OPENAI_API_KEY

#!math
async def calculate_math(message):
    response = openai.Completion.create(
        engine="davinci",
        prompt=f"Calculate: {message}"
    )
    return response.choices[0].text

#!opinion
async def generate_opinion(message):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"What is your opinion on {message}?"
    )
    return response.choices[0].text

#!code
async def generate_code(language, message):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Code this in {language}: {message}"
    )
    return response.choices[0].text

#!translate
async def translate_text(text, from_language, to_language):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Translate this from {from_language} to {to_language}: {text}"
    )
    return response.choices[0].text

#!concise
async def make_concise(text):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Make this concise: {text}"
    )
    return response.choices[0].text

@client.event
async def on_message(message):
    try:
        #!help
        if message.content == "!help":
            help_message = "Available commands: !opinion, !code <language> <prompt>, !translate <text> <from_language> <to_language> ,!help"
            await message.channel.send(help_message)
        
        #!math
        elif message.content.startswith("!math"):
            command, prompt = message.content.split(" ", 1)
            response = openai.Completion.create(
                engine="davinci",
                prompt=f"Calculate: {prompt}"
            )
            answer = response.choices[0].text
            await message.channel.send(answer)

        #!opinion
        elif message.content.startswith("!opinion"):
            opinion = await generate_opinion(message.content[8:])
            await message.channel.send(opinion)

        #!code
        elif message.content.startswith("!code"):
            command, language, prompt = message.content.split(" ", 2)
            code = await generate_code(language, prompt)
            await message.channel.send(code)

        #!translate
        elif message.content.startswith("!translate"):
            command, text, from_language, to_language = message.content.split(" ", 3)
            translation = await translate_text(text, from_language, to_language)
            await message.channel.send(translation)
        
        #!concise
        elif message.content.startswith("!concise"):
            command, text = message.content.split(" ", 1)
            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=f"Make this concise: {text}"
            )
            concise = response.choices[0].text
            await message.channel.send(concise)

    except Exception as e:
        await message.channel.send("Sorry, something went wrong. Please try again later.")
        print(e)



client.run(config.DISCORD_TOKEN)
