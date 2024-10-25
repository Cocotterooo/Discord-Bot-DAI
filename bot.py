import discord
from discord import app_commands
from dotenv import load_dotenv
import os
import asyncio
import io

# Mensajes de Instagram:
from utils.welcome_image import generate_welcome_image
from utils.api.instagram.Instagram import InstagramAPI 
from utils.db.authentication import supabase_autenticated
from utils.periodic_tasks.renew import renew_all_likes_comments_task, renew_media_url_task, check_new_post_task
from utils.db.Posts import Post
from utils.db.Discord_instagram_messsage import Dc_insta_msg
from utils.interactions.instagram_commands import instagram_send_command

# Selector de Roles de la DAI:
from utils.interactions.dai_roles import dai_roles_interaction, dai_roles

# Creador de canales de voz:
from utils.interactions.interactive_voice_channel import voice_channel_creator, create_or_update_channel, monitor_channel_activity, resume_channel_monitoring
from config import voice_channel_creator_embed

# Constantes
from config import SERVER_ID, LOG_CHANNEL, WELCOME_CHANNEL, INSTAGRAM_DAI_CHANNEL, ADMIN_ROLE, linktree_embed

# Cargar el archivo .env
load_dotenv()

#! Crear una instancia del bot
TOKEN = os.getenv('DISCORD_TOKEN')
MY_GUILD = discord.Object(id=SERVER_ID)

#! Crear una instancia de Supabase
DB_URL: str = os.environ.get("DB_URL")
DB_API_KEY: str = os.environ.get("DB_API_KEY")
DB_EMAIL: str = os.environ.get("DB_EMAIL")
DB_EMAIL_PASSWORD: str = os.environ.get("DB_EMAIL_PASSWORD")
supabase = supabase_autenticated(DB_URL, DB_API_KEY, DB_EMAIL, DB_EMAIL_PASSWORD)

#! Crear una instancia de Instagram
INSTAGRAM_API_KEY = os.getenv('INSTAGRAM_API_KEY')
instagram = InstagramAPI(INSTAGRAM_API_KEY)
posts = Post(supabase, instagram)


class Bot(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    #* Aquí sincronizamos los comandos de aplicación con el servidor especificado (MY_GUILD).
    async def setup_hook(self):
        dai_roles(self)
        instagram_send_command(self, supabase, instagram, dc_insta_msg, INSTAGRAM_DAI_CHANNEL, ADMIN_ROLE)
        voice_channel_creator(self, ADMIN_ROLE, voice_channel_creator_embed())
        # Copiamos los comandos globales a nuestro servidor 
        # Esto evita tener que esperar la propagación global de hasta una hora.
        self.tree.copy_global_to(guild=MY_GUILD)
        # Sincronizamos los comandos en el árbol para asegurarnos de que estén listos en el servidor.
        await self.tree.sync(guild=MY_GUILD)

# Las intenciones definen los eventos a los que el bot estará atento, como mensajes, miembros, etc.
intents = discord.Intents.default()
# Habilita la intención de recibir eventos relacionados con miembros, mensajes y servidores.
intents.members = True  
intents.messages = True  
intents.guilds = True  
client = Bot(intents=intents)


#! Crear una instancia de Discord_instagram_messsage
dc_insta_msg = Dc_insta_msg(supabase, client, instagram)


@client.event
async def on_ready():
    print(f'Bot conectado como {client.user}')
    #log_channel = client.get_channel(LOG_CHANNEL) 
    #await log_channel.send('Estado Bot: **Online** <a:online:1288631919352877097>')
    await resume_channel_monitoring(client, supabase)
    asyncio.create_task(renew_all_likes_comments_task(posts, 3600, client, supabase, INSTAGRAM_DAI_CHANNEL))
    asyncio.create_task(renew_media_url_task(posts, 86400))
    asyncio.create_task(check_new_post_task(instagram, posts, dc_insta_msg, 3600))


@client.event
async def on_interaction(interaction):
    await dai_roles_interaction(interaction)
    if interaction.data and interaction.data.get("custom_id"):
        await create_or_update_channel(client, supabase, interaction)


# Evento cuando un miembro se une al servidor
@client.event
async def on_member_join(member):
    print(f'{member} se ha unido al servidor')
    # Obtener el avatar y el nombre del miembro
    avatar_url = member.avatar.url if member.avatar else member.default_avatar.url
    nombre_usuario = member.name
    # Envia la imagen
    channel = client.get_channel(WELCOME_CHANNEL) 
    image_binary = generate_welcome_image(nombre_usuario, avatar_url, 'assets/tema_claro_recortado.png')
    if image_binary is None:
        await print(f'Ocurrió un error al generar la imagen de Bienvenida de {nombre_usuario}')
    else:
        await channel.send(file=discord.File(fp=image_binary, filename='bienvenida.png'))
        await channel.send(f'<:entrar:1288631392070012960> {member.mention} ¡Bienvenid@ a la **Comunidad Oficial** de la **EEI**! 🎉\n-#       **Delegación de Alumnos** EEI - Uvigo')


@client.tree.command(name='bienvenida', description='Imagen de Bienvenida')
async def welcome(interaction: discord.Interaction):
    avatar_url = interaction.user.avatar.url
    nombre_usuario = interaction.user.name
    image_binary = generate_welcome_image(nombre_usuario, avatar_url, 'assets/tema_claro_recortado.png')
    # Envia la imagen
    channel = client.get_channel(WELCOME_CHANNEL) 
    image_binary = generate_welcome_image(nombre_usuario, avatar_url, 'assets/tema_claro_recortado.png')
    if image_binary is None:
        await print(f'Ocurrió un error al generar la imagen de Bienvenida de {nombre_usuario}')
    else:
        await channel.send(file=discord.File(fp=image_binary, filename='bienvenida.png'))
        await channel.send(f'<:entrar:1288631392070012960>  ¡Bienvenid@ a la **Comunidad Oficial** de la **EEI**! 🎉\n-#       **Delegación de Alumnos** EEI - Uvigo')


@client.tree.command(name='rss', description='Muestra las redes sociales y la web de la Delegación de Alumnos de Industriales')
async def web(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True)  # Indica que se está procesando
    await interaction.followup.send(embed=linktree_embed(), ephemeral=False)
    return


client.run(TOKEN)


