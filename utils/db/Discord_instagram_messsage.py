from supabase import Client
from utils.api.instagram.Instagram import InstagramAPI
import discord
import io

from config import instagram_embed
from utils.api.instagram.Instagram import InstagramAPI

class Dc_insta_msg():
    def __init__(self, supabase: Client, client: discord.Client, instagram:InstagramAPI) -> None:
        self.supabase = supabase
        self.client = client
        self.instagram = instagram

    async def save_message_id(self, message_id:int, post_id:int):
        try:
            response = self.supabase.table('instagram_post_discord').insert(
                                [{'id': post_id,
                                'message_id': message_id}]
                            ).execute()
            print(f'response: {response}')
            return
        except Exception as e:
            try:
                response = self.supabase.table('instagram_post_discord').update(
                                {'message_id': message_id}
                            ).eq('id', post_id).execute()
            except Exception as e:
                print(f'❌Error: Dc_insta_msg.save_message_id() - Al subir un post a la DB: {e}')


    async def remove_msg(self, message_id:int):
        try:
            response = self.supabase.table('instagram_post_discord').delete().eq('message_id', message_id).execute()
            return response
        except Exception as e:
            print(f'❌Error: Dc_insta_msg.remove_msg() - Al eliminar un post a la DB: {e}')


    async def check_is_sended(self, post_id:int) -> bool:
        try:
            response = self.supabase.table('instagram_post_discord').select('message_id').eq('id', post_id).execute()
            return response
        except Exception as e:
            print(f'❌Error: Dc_insta_msg.post_is_sended() - Al verificar si un post ya fue enviado: {e}')


    async def send_new_post(self, post_data:dict = None, channel_id:int = None):
        try:
            if post_data is None or channel_id is None:
                return
            else:
                try:
                    channel = self.client.get_channel(channel_id)
                    type_post = post_data['media_type']
                    permalink = post_data['permalink']
                    caption = post_data['caption']
                    likes = post_data['like_count']
                    comments = post_data['comments_count']
                    date_published = post_data['timestamp']
                    media_url = post_data['media_url']
                    post_id = post_data['id']
                except Exception as e:
                    print(f"❌Error: send_new_post() - al obtener los datos de la publicación: {e}")
                    return
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
                        embed=embed
                        )
                    message_id = embed_message.id
                    image_files = []
                    try:
                        items =  self.instagram.get_items_carousel(post_id)
                        for item in items[1:]:  # Omitir la primera imagen
                            image_data =  self.instagram.get_image_post(item['media_url'])
                            if image_data:
                                image_files.append(discord.File(fp=image_data, filename='image.png'))
                    except Exception as e:
                        print(f"❌Error: send_new_post() - al obtener las imágenes del carrusel: {e}")
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
                        print(f"❌Error: send_new_post() - al enviar el mensaje con embed: {e}")
                        return
                    # Intenta obtener y enviar el video después del embed
                    try:
                        video_file = await self.instagram.get_video_post(media_url)
                        video_file = io.BytesIO(video_file)
                        video_file.name = 'video.mp4'  # Asigna un nombre al archivo
                        await channel.send(file=discord.File(video_file, 'video.mp4'))
                    except Exception as e:
                        print(f"❌Error: send_new_post() - al obtener o enviar el video: {e}")
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
                    await self.save_message_id(message_id, post_id)
                    print(f"✅ID del mensaje almacenado en la DB: {message_id}")
                except Exception as e:
                    print(f"❌Error: send_new_post() - al almacenar el ID del mensaje en la base de datos: {e}")    
        except Exception as e:
            print(f"❌Error: send_new_post() - al enviar la publicación: {e}")
