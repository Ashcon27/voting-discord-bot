import os
from dotenv import load_dotenv
from matplotlib import pyplot as plt

import discord
from discord.ext import commands
from numpy.core.defchararray import lower
import asyncio

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

vote1 = 0
vote2 = 0

@bot.listen()
async def on_ready():
    print('Bot loaded and ready!')

@bot.command(name="hi", help="Says hello")
async def say_hello(ctx):
    await ctx.send(f"Hi {ctx.author.display_name}")

@bot.command(name="create", help="Give basic info such as title and options")
async def creator(ctx):
    await ctx.send(f"Hi {ctx.author.display_name}. Lets create the poll! Type !title for a title")

@bot.command(name="title", help="give a title to your poll")
async def titler(ctx):
    title = ctx.message.content[6:]
    with open("stats.txt", "a") as f:
        f.write(f"{str(title)}\n")
        f.close()
    await ctx.send(ctx.message.content[6:])

@bot.command(name="opt1", help="First Option")
async def option(ctx):
    opt1 = ctx.message.content[5:]
    with open("stats.txt", "a") as f:
        f.write(f"{str(opt1)}\n")
        f.close()
    await ctx.send(ctx.message.content[5:])


@bot.command(name="opt2", help="Second Option")
async def option(ctx):
    opt2 = ctx.message.content[5:]
    with open("stats.txt", "a") as f:
        f.write(f"{str(opt2)}\n")
        f.close()
    await ctx.send(ctx.message.content[5:])

@bot.command(name="vote1", help="Cast in your vote for the first option")
async def voter(ctx):
    global vote1
    f = open("stats.txt", "r")
    opt1 = f.readline(2)
    vote1 += 1
    await ctx.send(f"Your vote is in!")

@bot.command(name="vote2", help="Cast in your vote for the second option")
async def voter(ctx):
    global vote2
    f = open("stats.txt", "r")
    opt2 = f.readline(3)
    vote2 += 1
    await ctx.send(f"Your vote is in!")

@bot.command(name="results", help= "Gives the results of the voting")
async def result(ctx):
    f = open("results.txt", "r")
    results = f.read().split('\n')[1]
    await ctx.send(f"Option 1 -{results}- Option 2")

async def update_results():
    await bot.wait_until_ready()
    global vote1
    global vote2

    while not bot.is_closed():
        try:
            with open("results.txt", "a") as f:
                f.write(f"{vote1}, {vote2}\n")

            vote1 = 0
            vote2 = 0
            await asyncio.sleep(120)

        except Exception as e:
            print(e)
            await asyncio.sleep(120)
@bot.command(name="plot_directions", help="says the directions of how to use the plot function")
async def direct(ctx):
    await ctx.send("To use the plot function enter your values and names in the following format with spaces to separate the values: [number of people who chose option 1] [number of people who chose option 2] [option 1] [option 2] If a space is needed for a value use an underscore. Use ONLY numbers for the first two values. Use only this format (without the brackets) or the function will not return the desired results")

@bot.command(name= "plot", help = "makes a pie chart with the first two values given")
async def pplot(ctx, a, b, option1, option2):
    plt.style.use("fivethirtyeight")
    slices = [int(a), int(b)]
    labels = [f"{option1}", f"{option2}"]
    explode = [0.1, 0]
    colors= ["pink", "teal"]
    plt.pie(slices, labels =labels, colors = colors, wedgeprops = {"edgecolor":"black"}, explode =explode, shadow = True, autopct = "%1.1f%%")
    plt.title(f"{option1.upper()} OR {option2.upper()}???")
    plt.tight_layout()
    plt.savefig("online.png")
    file = discord.File("online.png", filename = "online.png")
    await ctx.send("online.png", file=file)
    plt.clf()


bot.loop.create_task(update_results())
bot.run(TOKEN)
