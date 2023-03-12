import openai
import discord
import config
import requests
import image_recognition

client = discord.Client()

openai.api_key = config.OPENAI_API_KEY

#!weather
async def get_weather(city):
    api_key = config.OPENWEATHERMAPS_API_KEY
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(url)
    data = response.json()
    temperature = data["main"]["temp"]
    return f"The temperature in {city} is {temperature} degrees."

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

#!shakespeare
async def make_shakespeare(text):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Make this sound like Shakespeare: {text}"
    )
    return response.choices[0].text

#!image
async def generate_image(message):
    image = await image_recognition.generate_image(message)
    return image


#functions –– !help, !weather, !math, !opinion. !code, !translate, !concise, !shakespeare
@client.event
async def on_message(message):
    try:
        #!help
        if message.content == "!help":
            help_message = "Available commands: !math, !opinion, !code <language> <prompt>, !translate <text> <from_language> <to_language>, !concise <text>, !weather <city>, !help"
            await message.channel.send(help_message)


        #!weather
        elif message.content.startswith("!weather"):
            city = message.content[8:]
            weather = await get_weather(city)
            await message.channel.send(weather)

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

        #!shakespeare
        elif message.content.startswith("!shakespeare"):
            command, text = message.content.split(" ", 1)
            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=f"Make this sound like Shakespeare: {text}"
            )
            shakespeare = response.choices[0].text
            await message.channel.send(shakespeare)
        
        #!image
        elif message.content.startswith("!image"):
            command, prompt = message.content.split(" ", 1)
            image = await generate_image(prompt)
            await message.channel.send(file=image)

    except Exception as e:
        await message.channel.send("Sorry, something went wrong. Please try again later.")
        print(e)



client.run(config.DISCORD_TOKEN)