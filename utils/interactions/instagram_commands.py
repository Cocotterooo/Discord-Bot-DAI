from supabase import Client
from utils.api.instagram.Instagram import InstagramAPI
import discord
from discord.ext import commands
from discord import app_commands
import io

from utils.db.get_post_info import get_post_info
from utils.db.Discord_instagram_messsage import Dc_insta_msg
from config import instagram_embed

def instagram_send_command(client: commands.Bot, supabase: Client, instagram: InstagramAPI, dc_insta_msg: Dc_insta_msg, instagram_dai_channel: int, admin_role_id: int):
    @client.tree.command(name='instagram', description='Envía una publicación de Instagram al canal de Instagram')
    @app_commands.describe(post_id='La ID de la publicación')
    async def instagram_send(interaction: discord.Interaction, post_id: str):
        await interaction.response.defer(thinking=True)  # Indica que se está procesando
        role_allowed = discord.utils.get(interaction.guild.roles, id=admin_role_id)

        if role_allowed not in interaction.user.roles:
            await interaction.response.send_message("<:no:1288631410558767156> No tienes permiso para usar este comando.", ephemeral=True)
            return
        try:
            # Asegúrate de que el post_id sea un entero
            post_id = int(post_id)
            data = await get_post_info(post_id, supabase)

            if data is None:
                await interaction.followup.send(f'<:no:1288631410558767156> Error: No se pudo encontrar la publicación.')
                return

            # Datos de la publicación
            channel = client.get_channel(instagram_dai_channel)
            type_post = data.get('media_type')
            permalink = data.get('permalink')
            caption = data.get('caption')
            likes = data.get('likes_count')
            comments = data.get('comments_count')
            date_published = data.get('date_published')
            media_url = data.get('media_url')

            embed = instagram_embed(
                permalink=permalink,
                caption=caption,
                likes=likes,
                comments=comments,
                post_id=post_id,
                date_published=date_published,
                media_url=media_url
            )

            # Envía el embed dependiendo del tipo de publicación
            if type_post == 'CAROUSEL_ALBUM':
                embed_message = await channel.send(content='-# <a:dinkdonk:1289157144436015174> <@&1288263963812958300>', embed=embed)
                message_id = embed_message.id
                image_files = []

                try:
                    items = instagram.get_items_carousel(post_id)
                    for item in items[1:]:  # Omitir la primera imagen
                        image_data = instagram.get_image_post(item['media_url'])
                        if image_data:
                            image_files.append(discord.File(fp=image_data, filename='image.png'))
                    
                    if image_files:
                        await channel.send(files=image_files)

                except Exception as e:
                    print(f"❌Error: al obtener las imágenes del carrusel: {e}")
                    await interaction.followup.send(f'<:no:1288631410558767156> Error al obtener las imágenes del carrusel.')
                    return

            elif type_post == 'VIDEO':
                try:
                    embed_message = await channel.send(content='-# <a:dinkdonk:1289157144436015174> <@&1288263963812958300>', embed=embed)
                    message_id = embed_message.id

                    video_file = await instagram.get_video_post(media_url)
                    video_file = io.BytesIO(video_file)
                    video_file.name = 'video.mp4'
                    await channel.send(file=discord.File(video_file, 'video.mp4'))

                except Exception as e:
                    print(f"❌Error: al obtener o enviar el video: {e}")
                    await interaction.followup.send(f'<:no:1288631410558767156> Error al obtener o enviar el video de la publicación.')
                    return

            else:  # Publicaciones de imagen
                try:
                    embed_message = await channel.send(content='-# <a:dinkdonk:1289157144436015174> <@&1288263963812958300>', embed=embed)
                    message_id = embed_message.id
                except Exception as e:
                    print(f"❌Error: al enviar el mensaje con embed: {e}")
                    await interaction.followup.send(f'<:no:1288631410558767156> Error al enviar el mensaje con el embed.')
                    return

            # Almacena el ID del mensaje en la base de datos
            try:
                await dc_insta_msg.save_message_id(message_id, post_id)
                print(f"✅ID del mensaje almacenado en la DB: {message_id}")
            except Exception as e:
                print(f"❌Error: al almacenar el ID del mensaje en la base de datos: {e}")
                await interaction.followup.send(f'<:no:1288631410558767156> Error al almacenar el ID del mensaje en la base de datos. (La publicación no se actualizará)')
                return

            await interaction.followup.send(f'<:correcto:1288631406452412428> Se ha enviado la publicación con id `{post_id}` a <#{instagram_dai_channel}>. ID del mensaje: `{message_id}`')

        except ValueError:
            await interaction.followup.send(f'<:no:1288631410558767156> Error: ID de publicación no válida.')
        except Exception as e:
            print(f"❌Error: al enviar la publicación: {e}")
            await interaction.followup.send(f'<:no:1288631410558767156> Error al enviar la publicación.')
