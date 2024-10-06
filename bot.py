import discord
from discord import app_commands
from dotenv import load_dotenv
import os
import asyncio
import io

from utils.welcome_image import generate_welcome_image
from utils.api.instagram.Instagram import InstagramAPI 
from utils.db.authentication import supabase_autenticated
from utils.periodic_tasks.renew import renew_all_likes_comments_task, renew_media_url_task, check_new_post_task
from utils.db.get_post_info import get_post_info
from utils.db.Posts import Post
from utils.db.Discord_instagram_messsage import Dc_insta_msg

from utils.interactions.dai_roles import dai_roles_interaction, setup_commands


from config import SERVER_ID, LOG_CHANNEL, WELCOME_CHANNEL, INSTAGRAM_DAI_CHANNEL, instagram_embed

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
        setup_commands(self)
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
    channel = client.get_channel(LOG_CHANNEL) 
    await channel.send('Estado Bot: **Online** <a:online:1288631919352877097>')
    asyncio.create_task(renew_all_likes_comments_task(posts, 3600, client, supabase, INSTAGRAM_DAI_CHANNEL))
    asyncio.create_task(renew_media_url_task(posts, 86400))
    asyncio.create_task(check_new_post_task(instagram, posts, dc_insta_msg, 3600))


@client.event
async def on_interaction(interaction):
    await dai_roles_interaction(interaction)


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



@client.tree.command(name='instagram', description='Envía una publicación de Instagram al canal de Instagram')
@app_commands.describe(
    post_id='La ID de la publicación')
async def instagram_send(interaction: discord.Interaction, post_id: str):
    await interaction.response.defer(thinking=True)  # Indica que se está procesando
    message_id = None
    try:
        post_id = int(post_id)
        data = await get_post_info(post_id, supabase)
        
        if data is None:
            await interaction.followup.send(f'<:no:1288631410558767156> Error al enviar la publicación')
            return
        else:
            channel = client.get_channel(INSTAGRAM_DAI_CHANNEL)
            type_post = data['media_type']
            permalink = data['permalink']
            caption = data['caption']
            likes = data['likes_count']
            comments = data['comments_count']
            date_published = data['date_published']
            media_url = data['media_url']

            if type_post == 'CAROUSEL_ALBUM':
                embed = instagram_embed(permalink=permalink, 
                                        caption=caption, 
                                        likes=likes, 
                                        comments=comments, 
                                        post_id=post_id, 
                                        date_published=date_published, 
                                        media_url=media_url)
                # Envía el embed y almacena el mensaje
                embed_message = await channel.send(
                    content='-# <a:dinkdonk:1289157144436015174> <@&1288263963812958300>',
                    embed=embed)
                message_id = embed_message.id
                image_files = []
                try:
                    items =  instagram.get_items_carousel(post_id)
                    for item in items[1:]:  # Omitir la primera imagen
                        image_data =  instagram.get_image_post(item['media_url'])
                        if image_data:
                            image_files.append(discord.File(fp=image_data, filename='image.png'))
                except Exception as e:
                    print(f"❌Error: instagram_send() - al obtener las imágenes del carrusel: {e}")
                    await interaction.followup.send(f'<:no:1288631410558767156> Error al obtener las imágenes del carrusel')
                    return
                if image_files:
                    # Envía las imágenes adjuntas
                    await channel.send(files=image_files)
                # Respuesta con la ID del mensaje
            elif type_post == 'VIDEO':
                embed = instagram_embed(
                    permalink=permalink, 
                    caption=caption, 
                    likes=likes, 
                    comments=comments, 
                    post_id=post_id, 
                    date_published=date_published
                )
                # Envía el mensaje con el embed
                try:
                    embed_message = await channel.send(
                        content='-# <a:dinkdonk:1289157144436015174> <@&1288263963812958300>', 
                        embed=embed
                    )
                    message_id = embed_message.id
                except Exception as e:
                    print(f"❌Error: instagram_send() - al enviar el mensaje con embed: {e}")
                    await interaction.followup.send(f'<:no:1288631410558767156> Error al enviar el mensaje con el embed')
                    return
                # Intenta obtener y enviar el video después del embed
                try:
                    video_file = await instagram.get_video_post(media_url)
                    video_file = io.BytesIO(video_file)
                    video_file.name = 'video.mp4'  # Asigna un nombre al archivo
                    await channel.send(file=discord.File(video_file, 'video.mp4'))
                except Exception as e:
                    print(f"❌Error: instagram_send() - al obtener o enviar el video: {e}")
                    await interaction.followup.send(f'<:no:1288631410558767156> Error al obtener o enviar el video de la publicación')
            else:
                embed = instagram_embed(permalink=permalink, 
                                        caption=caption, 
                                        likes=likes, 
                                        comments=comments, 
                                        post_id=post_id, 
                                        date_published=date_published, 
                                        media_url=media_url)
                embed_message = await channel.send(
                    content='-# <a:dinkdonk:1289157144436015174> <@&1288263963812958300>',
                    embed=embed)
                message_id = embed_message.id
            try:
                await dc_insta_msg.save_message_id(message_id, post_id)
                print(f"✅ID del mensaje almacenado en la DB: {message_id}")
            except Exception as e:
                print(f"❌Error: instagram_send() - al almacenar el ID del mensaje en la base de datos: {e}")
                await interaction.followup.send(f'<:no:1288631410558767156> Error al almacenar el ID del mensaje en la base de datos (La publicación no se actualizará)')
            await interaction.followup.send(f'<:correcto:1288631406452412428> Se ha enviado la publicación con id `{post_id}` a <#{INSTAGRAM_DAI_CHANNEL}>. ID del mensaje: `{embed_message.id}`')
            
    except Exception as e:
        await interaction.followup.send(f'<:no:1288631410558767156> Error al enviar la publicación')
        print(f"❌Error: instagram_send() - al enviar la publicación: {e}")



client.run(TOKEN)