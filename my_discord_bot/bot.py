import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

# Cargar el archivo .env
load_dotenv()

# Obtener el token de Discord desde el archivo .env
TOKEN = os.getenv("DISCORD_TOKEN")

# Crear una instancia del bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Evento que se ejecuta cuando el bot está listo
@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")
    # Sincroniza los comandos slash
    try:
        await bot.tree.sync()
        print("Comandos sincronizados.")
    except Exception as e:
        print(f"Error al sincronizar comandos: {e}")

# Cargar commands
async def load_commands():
    await bot.load_extension("commands.general")

async def main():
    await load_commands()
    await bot.start(TOKEN)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
