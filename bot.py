import discord
from discord import app_commands
from dotenv import load_dotenv
import os

from functions.welcome_image import generate_welcome_image


# Cargar el archivo .env
load_dotenv()

# Obtener el token de Discord desde el archivo .env
TOKEN = os.getenv("DISCORD_TOKEN")
SERVER_ID = 1288206483091361885

#* Crear una instancia del bot
# Define el objeto MY_GUILD con el ID del servidor de Discord en el que se van a sincronizar los comandos.
MY_GUILD = discord.Object(id=SERVER_ID)

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    # Aquí sincronizamos los comandos de aplicación con el servidor especificado (MY_GUILD).
    async def setup_hook(self):
        # Copiamos los comandos globales a nuestro servidor específico (MY_GUILD)
        # Esto evita tener que esperar la propagación global de hasta una hora.
        self.tree.copy_global_to(guild=MY_GUILD)
        
        # Sincronizamos los comandos en el árbol para asegurarnos de que estén listos en el servidor.
        await self.tree.sync(guild=MY_GUILD)

# Creamos un conjunto de intenciones (intents) predeterminado. 
# Estas intenciones definen los eventos a los que el bot estará atento, como mensajes, miembros, etc.
intents = discord.Intents.default()
client = MyClient(intents=intents)


@client.event
async def on_ready():
    print(f"Bot conectado como {client.user}")

# Evento cuando un miembro se une al servidor
@client.event
async def on_member_join(member):
    # Obtener el avatar y el nombre del miembro
    avatar_url = member.avatar.url
    nombre_usuario = member.name
    image_binary = generate_welcome_image(nombre_usuario, avatar_url)
    # Envia la imagen
    channel = client.get_channel(1288283913181200446) 
    image_binary = generate_welcome_image(nombre_usuario, avatar_url, 'assets/tema_claro_recortado.png')
    if image_binary is None:
        await print(f"Ocurrió un error al generar la imagen de Bienvenida de {nombre_usuario}")
    else:
        await channel.send(file=discord.File(fp=image_binary, filename='tema_claro_recortado.png'))
        await channel.send(f"<:entrar:1288631392070012960> {member.mention} ¡Bienvenid@ a la **Comunidad Oficial** de la **EEI**! 🎉\n-#       **Delegación de Alumnos** EEI - Uvigo")

@client.tree.command(name='bienvenida', description='Imagen de Bienvenida')
async def ip(interaction: discord.Interaction):
    avatar_url = interaction.user.avatar.url
    nombre_usuario = interaction.user.name
    image_binary = generate_welcome_image(nombre_usuario, avatar_url, 'assets/tema_claro_recortado.png')
    # Envia la imagen
    channel = client.get_channel(1288283913181200446) 
    image_binary = generate_welcome_image(nombre_usuario, avatar_url, 'assets/tema_claro_recortado.png')
    if image_binary is None:
        await print(f"Ocurrió un error al generar la imagen de Bienvenida de {nombre_usuario}")
    else:
        await channel.send(file=discord.File(fp=image_binary, filename='tema_claro_recortado.png'))
        await channel.send(f"<:entrar:1288631392070012960>  ¡Bienvenid@ a la **Comunidad Oficial** de la **EEI**! 🎉\n-#       **Delegación de Alumnos** EEI - Uvigo")




@client.tree.command(name='hola', description='Sabrás la IP del servidor')
async def ip(interaction: discord.Interaction):
    await interaction.response.send_message(f"{interaction.user.mention} ¡La ip es **analand.net**!", ephemeral = True)


client.run(TOKEN)