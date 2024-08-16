import discord, random, os, requests
from discord.ext import commands

# Uprawnienia bota
intents = discord.Intents.default()

# Uprawnienia czytania wiadomości
intents.message_content = True

# Tworzenie bota w jakiejś zmiennej klijenta i dajwać mu uprawnienia :/
client = discord.Client(intents=intents)

bot = commands.Bot(command_prefix = "!", intents = intents)

sortowanie = {
    "butelka": "kosz żółty",
    "karton": "kosz niebieski",
    "trawa": "kosz BIO",
    "okno": "kosz zielony"
}

rozklad = {
    "plastik": "450 lat",
    "szklo": "1mil lat",
    "papier": "2-6 tyg",
    "jedzenie": "1-2 tyg"
}

WhatCanIDo = """Jestem bot Harpek:ballot_box_with_check:! A to co umiem zrobić:
    :pushpin:   !help
    :pushpin:   !dodaj           \*a (int, składniki)
    :pushpin:   !repeat          word (str), times (int)
    :pushpin:   !password        length (int)
    :pushpin:   !wybierz         \*choices (str, wyrazy)
    :pushpin:   !memes           CS2 / others
    :pushpin:   !sortuj          rzecz (str)
    :pushpin:   !rozkladanie     rzecz (str)
    :pushpin:   !add_task        zadanie (str)
    :pushpin:   !show_tasks_list"""

@bot.event
async def on_ready():
    print("Bot gotowy!")
    print(f"Zalogowano, {bot.user.name}")

@bot.command()
async def dodaj(ctx, *a: int):
    await ctx.send(f":nerd: Suma wszystkich cyfr jest :heavy_equals_sign: {sum(a)}")

@bot.command()
async def repeat(ctx, word: str, times: int):
    await ctx.send(f"{word} " * times)

@bot.command()
async def password(ctx, length: int):
    letters = "qwertyuiopasfghjkldzxcvbnm,./;'[]\=-1234567890?><:|}{+_)(*&^%$#@!)}"
    passWord = ""
    for i in range(length):
        passWord += random.choice(letters)
    await ctx.send(f":fire: Twoje wygenerowane hasło to :fire::\n       {passWord}")

@bot.command()
async def wybierz(ctx, *choices: str):
    await ctx.send(f":thinking: Wybieram:\n\n:fire: {random.choice(choices)} :fire:")

@bot.command()
async def HELP(ctx):
    await ctx.send(WhatCanIDo)

@bot.command()
async def img(ctx):
    img_name = random.choice(os.listdir('images'))
    with open(f"images/{img_name}", 'rb') as f:
        await ctx.send(file=discord.File(f))

def get_duck_image():
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']

@bot.command()
async def kaczka(ctx):
    image_url = get_duck_image()
    await ctx.send(image_url)

@bot.command()
async def memes(ctx, theme: str):
    if (theme == "CS2"):
        meme = random.choice(os.listdir('memes/CS'))
        with open(f"memes/CS/{meme}", 'rb') as f:
            await ctx.send(file=discord.File(f))
    else:
        meme = random.choice(os.listdir('memes/other'))
        with open(f"memes/other/{meme}", 'rb') as f:
            await ctx.send(file=discord.File(f))
# qwertyuiop[cvbnm,./]
@bot.command()
async def renkodzielo(ctx, mat):
    if (mat == "plastik"):
        idea = random.choice(os.listdir('pomysl/plastik'))
        with open(f"pomysl/plastik/{idea}", 'rb') as f:
            await ctx.send("zrób to!:")
            await ctx.send(file=discord.File(f))
    elif (mat == 'papier'):
        idea = random.choice(os.listdir('pomysl/papier'))
        with open(f"pomysl/papier/{idea}", 'rb') as f:
            await ctx.send("zrób to!:")
            await ctx.send(file=discord.File(f))
    else:
        ctx.send("podaj materiał (plastik/papier)")

@bot.command()
async def sortuj(ctx, thing):
    if thing in sortowanie:
        await ctx.send(f"Użyj {sortowanie[thing]}")
    else:
        await ctx.send("Nie wiem, wygoogluj")

@bot.command()
async def rozkladanie(ctx, thing):
    if thing in rozklad:
        await ctx.send(f"{thing} rozkłada się około {rozklad[thing]}")
    else:
        await ctx.send("Nie wiem, wygoogluj")

import json
TASKS_FILE = "tasks.json"
def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_tasks():
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=4)

tasks = load_tasks()

@bot.command()
async def add_task(ctx, *, task):
    user_tasks = tasks.get(ctx.author.id, [])
    user_tasks.append(task)
    tasks[ctx.author.id] = user_tasks
    save_tasks()
    await ctx.send(f"Dodano {task} do listy!")

@bot.command()
async def show_tasks_list(ctx):
    user_tasks = tasks.get(ctx.author.id, [])
    if user_tasks:
        await ctx.send(f'Twoje zadania: {", ".join(user_tasks)}')
    else:
        await ctx.send("Nie masz żadnych zadań!")

# TU MA BYĆ KONIEC !!!
bot.run("Miejsce na twój token tutaj!!!")
