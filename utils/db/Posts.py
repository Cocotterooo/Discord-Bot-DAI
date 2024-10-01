from supabase import Client
from utils.api.instagram.Instagram import InstagramAPI
import requests
import asyncio

class Post():
    def __init__(self, supabase: Client, instagram: InstagramAPI) -> None:
        self.supabase = supabase
        self.instagram = instagram

    async def update_media_url(self, id_post: int):
        try:
            media_url = self.instagram.get_media_url(id_post)
            # Actualizar la base de datos con la nueva URL
            await self.supabase.table("posts").update({
                "media_url": media_url['media_url']
            }).eq('id', id_post).execute()
            print(f"URL de la publicación {id_post} actualizada")
            return
        except Exception as e:
            print(f"Error al actualizar la URL de la publicación: {e}")
            return e

    def renew_videos_media_url_db(self, interval):
        while interval > 0:
            asyncio.sleep(interval)
            print("🔃Actualizando media_url de los posts tipo videos")
            posts = self.instagram.get_all_posts()
            for i in posts['data']:
                if i['media_type'] == 'VIDEO':
                    try:
                        self.update_media_url(i['id'])
                    except Exception as e:
                        print(f"Error - ID{i['id']}: {e}")
            print(f"💚URL de los videos actualizados en la Base de Datos")

    async def update_likes_comments(self, id_post: int, likes_count: int, comments_count: int):
        try:
            # Actualizar la base de datos con los nuevos datos
            print(likes_count, comments_count)
            response = self.supabase.table("posts").update({
                "likes_count": likes_count,
                "comments_count": comments_count
            }).eq('id', id_post).execute()
            print(f"Likes y comentarios actualizados para la publicación {id_post}")
        except Exception:
            print(f"❌ Error al actualizar los likes y comentarios: {response}")

    async def renew_all_likes_comments_db(self, interval):
        while interval > 0:
            await asyncio.sleep(interval)
            print("🔃Actualizando likes y comentarios")
            posts = self.instagram.get_all_posts()
            for i in posts['data']:
                try:
                    self.update_likes_comments(i['id'], i['likes_count'], i['comments_count'])
                except Exception as e:
                    print(f"❌Error: renew_all_likes_comments_db() - Al intentar actualizar ID: {i['id']} ({i['likes_count']}, {i['comments_count']}): {e}")
            print(f"💚Likes y comentarios actualizados en la Base de Datos")


    def save_all_posts(self, all_posts, supabase: Client):
        try:
            for i in self.get_all_posts()['data']: # Itera las publicaciones
                print("bucle")
                # Verificar si el ID de la publicación ya existe en la base de datos
                try:
                    result = (supabase
                            .table('posts')
                            .select('id')
                            .eq('id', i['id'])
                            .execute())
                    data = result.data
                    if data:
                        print(f"El ID {i['id']} ya existe en la DB")
                    else:
                        supabase.table("posts").insert([{
                            "id": i['id'],
                            "date_published": i["timestamp"],
                            "media_type": i["media_type"],
                            "caption": i["caption"],
                            "media_url": i["media_url"],
                            "permalink": i["permalink"]
                        }]).execute()
                        print(f"Publicación {i['id']} guardada en la DB")
                except Exception as e:
                    print(f"Error al realizar la consulta o guardar la publicación: {e}")
        except Exception as exception:
            return exception  