import discord
from discord.ext import commands

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Comando slash /hola
    @commands.Cog.listener()
    async def on_ready(self):
        print("Cog General listo")

    @commands.command(name="hola", description="Te saludo")
    async def hola(self, ctx):
        await ctx.send("Hola, ¿qué tal?")

# Función para añadir el cog
async def setup(bot):
    await bot.add_cog(General(bot))
