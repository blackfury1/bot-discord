import discord
from discord import app_commands
from discord.ui import View, Select, Modal, TextInput
import os
import datetime

# Configuração do bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} está online!')

@bot.command(name='oi')
async def oi(ctx):
    await ctx.send('Olá! Eu sou seu bot Discord!')

@bot.command(name='ping')
async def ping(ctx):
    await ctx.send('Pong!')

# Token do bot (use variável de ambiente)
bot.run(os.getenv("1c72237c305b18e844aae633b9f7f6b10b0b82010d351220cde8f5a8ac3bf288"))
