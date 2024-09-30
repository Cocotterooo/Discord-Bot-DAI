import discord
from discord import app_commands
from dotenv import load_dotenv
import os

from utils.welcome_image import generate_welcome_image
from utils.api.instagram.Instagram import InstagramAPI 
from utils.db.authentication import supabase_autenticated
from utils.periodic_tasks.update_likes_comments import update_likes_comments_db
from utils.db.get_post_info import get_post_info

from config import SERVER_ID, LOG_CHANNEL, WELCOME_CHANNEL, INSTAGRAM_DAI_CHANNEL, instagram_message_format

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

class Bot(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    #* Aquí sincronizamos los comandos de aplicación con el servidor especificado (MY_GUILD).
    async def setup_hook(self):
        # Copiamos los comandos globales a nuestro servidor 
        # Esto evita tener que esperar la propagación global de hasta una hora.
        self.tree.copy_global_to(guild=MY_GUILD)
        # Sincronizamos los comandos en el árbol para asegurarnos de que estén listos en el servidor.
        await self.tree.sync(guild=MY_GUILD)

# Las intenciones definen los eventos a los que el bot estará atento, como mensajes, miembros, etc.
intents = discord.Intents.default()
intents.members = True  # Habilita la intención de recibir eventos relacionados con miembros
intents.messages = True  # Habilita la intención de recibir eventos relacionados con mensajes
intents.guilds = True  # Habilita la intención de recibir eventos relacionados con servidores
client = Bot(intents=intents)



@client.event
async def on_ready():
    print(f'Bot conectado como {client.user}')
    channel = client.get_channel(LOG_CHANNEL) 
    await channel.send('Estado Bot: **Online** <a:online:1288631919352877097>')
    await update_likes_comments_db(instagram, supabase, 1800)


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
async def ip(interaction: discord.Interaction):
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



@client.tree.command(name='instagram', description='Envía una publicación de Instagram al canal de Instagram')
@app_commands.describe(
    post_id='La ID de la publicación')
async def instagram_send(interaction: discord.Interaction, post_id:str):
    try:
        post_id = int(post_id)
        data = await get_post_info(post_id, supabase)
        if data is None:
            await interaction.response.send_message(f'<:no:1288631410558767156> Error al enviar la publicación', ephemeral = True)
            return
        else:
            channel = client.get_channel(INSTAGRAM_DAI_CHANNEL)
            permalink = data['permalink']
            caption = data['caption']
            likes = data['likes_count']
            comments = data['comments_count']
            date_published = data['date_published']
            media_url = data['media_url']
            await channel.send(instagram_message_format(permalink, caption, likes, comments, post_id, date_published, media_url))
            await interaction.response.send_message(f'<:correcto:1288631406452412428> Se ha enviado la publicación con id `{post_id}` a <#{INSTAGRAM_DAI_CHANNEL}>', ephemeral = True)
    except Exception as e:
        await interaction.response.send_message(f'<:no:1288631410558767156> Error al enviar la publicación', ephemeral = True)
        print(f"❌Error: instagram_send() - al enviar la publicación: {e}")
        return

instagram = InstagramAPI(INSTAGRAM_API_KEY)




client.run(TOKEN)


#print(instagram.get_all_posts())
#instagram.save_all_posts(supabase)
#instagram.update_likes_comments('18032521846722078', supabase)