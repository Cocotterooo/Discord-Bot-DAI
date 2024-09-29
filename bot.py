import discord
from discord import app_commands
from dotenv import load_dotenv
from supabase import create_client, Client
import os

from utils.welcome_image import generate_welcome_image
from utils.api.instagram.Instagram import InstagramAPI 
from utils.db.authentication import supabase_autenticated

# Cargar el archivo .env
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
SERVER_ID = 1288206483091361885

#! Crear una instancia de Supabase
DB_URL: str = os.environ.get("DB_URL")
DB_API_KEY: str = os.environ.get("DB_API_KEY")
DB_EMAIL: str = os.environ.get("DB_EMAIL")
DB_EMAIL_PASSWORD: str = os.environ.get("DB_EMAIL_PASSWORD")
supabase = supabase_autenticated(DB_URL, DB_API_KEY, DB_EMAIL, DB_EMAIL_PASSWORD)

#! Crear una instancia del bot
# Define el objeto MY_GUILD con el ID del servidor de Discord en el que se van a sincronizar los comandos.
MY_GUILD = discord.Object(id=SERVER_ID)

class Bot(discord.Client):
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
intents.members = True  # Habilita la intención de recibir eventos relacionados con miembros
client = Bot(intents=intents)



@client.event
async def on_ready():
    print(f'Bot conectado como {client.user}')
    channel = client.get_channel(1288285231652274207) 
    await channel.send('Estado Bot: **Online** <:online:1288631919352877097>')

# Evento cuando un miembro se une al servidor
@client.event
async def on_member_join(member):
    print(f'{member} se ha unido al servidor')
    # Obtener el avatar y el nombre del miembro
    avatar_url = member.avatar.url if member.avatar else member.default_avatar.url
    nombre_usuario = member.name
    # Envia la imagen
    channel = client.get_channel(1288283913181200446) 
    image_binary = generate_welcome_image(nombre_usuario, avatar_url, 'assets/tema_claro_recortado.png')
    if image_binary is None:
        await print(f'Ocurrió un error al generar la imagen de Bienvenida de {nombre_usuario}')
    else:
        await channel.send(file=discord.File(fp=image_binary, filename='bienvenida.png'))
        await channel.send(f'<:entrar:1288631392070012960> {member.mention} ¡Bienvenid@ a la **Comunidad Oficial** de la **EEI**! 🎉\n-#       **Delegación de Alumnos** EEI - Uvigo')


@client.tree.command(name='bienvenida', description='Imagen de Bienvenida')
async def ip(interaction: discord.Interaction):
    avatar_url = interaction.user.avatar.url
    nombre_usuario = interaction.user.name
    image_binary = generate_welcome_image(nombre_usuario, avatar_url, 'assets/tema_claro_recortado.png')
    # Envia la imagen
    channel = client.get_channel(1288283913181200446) 
    image_binary = generate_welcome_image(nombre_usuario, avatar_url, 'assets/tema_claro_recortado.png')
    if image_binary is None:
        await print(f'Ocurrió un error al generar la imagen de Bienvenida de {nombre_usuario}')
    else:
        await channel.send(file=discord.File(fp=image_binary, filename='bienvenida.png'))
        await channel.send(f'<:entrar:1288631392070012960>  ¡Bienvenid@ a la **Comunidad Oficial** de la **EEI**! 🎉\n-#       **Delegación de Alumnos** EEI - Uvigo')




@client.tree.command(name='hola', description='Sabrás la IP del servidor')
async def ip(interaction: discord.Interaction):
    await interaction.response.send_message(f'{interaction.user.mention} ¡La ip es **analand.net**!', ephemeral = True)


#client.run(TOKEN)

instagram = InstagramAPI('IGQWROX2t1bkU0U1NsTmFFc1ZAvUUd0bHlZAemZA6TmJYVTJhSEZAReWFJa3FnakdzcVMwRUk0Mm9jMzdwT1BzY2hpLUJ0TDJIVU40Ym5ZAbG94RDA0YTZA4X2NjTzl4UEliWTBidVFxb0J1M1RNYVI4cGVNNlhHZATFMUzAZD')
#print(instagram.get_all_posts())
#instagram.save_all_posts(supabase)
instagram.update_likes_comments('18032521846722078', supabase)