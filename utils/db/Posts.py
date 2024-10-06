from supabase import Client
import discord
from utils.api.instagram.Instagram import InstagramAPI

class Post():
    def __init__(self, supabase: Client, instagram: InstagramAPI) -> None:
        self.supabase = supabase
        self.instagram = instagram

    async def update_media_url(self, id_post: int):
        try:
            media_url = await self.instagram.get_media_url(id_post)
            # Actualizar la base de datos con la nueva URL
            self.supabase.table("posts").update({
                "media_url": media_url['media_url']
            }).eq('id', id_post).execute()
            return None
        except Exception as e:
            print(f"❌Error: update_media_url() - al actualizar media_url de {id_post}: {e}")
            return e

    async def renew_media_url_db(self, ):
        print("🔃Actualizando media_url de los posts en la DB")
        posts = await self.instagram.get_all_posts()
        for i in posts['data']:
            try:
                await self.update_media_url(i['id'])
            except Exception as e:
                print(f"❌Error renew_media_url_db() - ID{i['id']}: {e}")
        print(f"💚media_url de las publicaciones actualizadas")

    async def update_likes_comments(self, id_post: int, likes_count: int, comments_count: int):
        try:
            #print(id_post, likes_count, comments_count)
            response = self.supabase.table("posts").update({
                "likes_count": likes_count,
                "comments_count": comments_count
            }).eq('id', id_post).execute()
        except Exception:
            print(f"❌Error: update_likes_comments() - Actualizar los likes y comentarios: {response}")

    async def renew_all_likes_comments_db(self) -> list:
        print("🔃Actualizando likes y comentarios en la DB")
        posts = await self.instagram.get_all_posts()
        error = False
        data = []
        for i in posts['data']:
            #print (f'{i}\n\n')
            try:
                likes_comments_count = await self.instagram.get_num_likes_comments(i['id'])
                await self.update_likes_comments(i['id'], likes_comments_count['like_count'], likes_comments_count['comments_count'])
                print(f"💚Likes y comentarios actualizados en la Base de Datos para la id ({i['id']})")
                data.append({'id': i['id'], 
                            'likes_count': likes_comments_count['like_count'], 
                            'comments_count': likes_comments_count['comments_count'], 
                            'caption': i['caption'], 
                            'permalink': i['permalink'], 
                            'media_url': i['media_url'], 
                            'date_published': i['timestamp']}
                            )
            except Exception as e:
                print(f"❌Error: renew_all_likes_comments_db() - Al intentar actualizar ID: {i['id']}: {e}")
                error = True
        if not error:
            print(f"💚Likes y comentarios actualizados en la Base de Datos")
            return data
        else:
            print(f"❌ERROR al actualizar los likes y comentarios")
            return None


    async def save_all_posts(self, supabase: Client):
        try:
            posts = await self.get_all_posts()['data']
            for i in posts: # Itera las publicaciones
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


    def check_post_exists(self, post_id):
        response = self.supabase.table("posts").select("*").eq("id", post_id).execute()
        return len(response.data) > 0


    async def save_new_post(self, post_id: int):
        try:
            post = await self.instagram.get_post(post_id)
            print(post)
            response = (self.supabase.table("posts").insert([{
                "id": post['id'],
                "date_published": post["timestamp"],
                "media_type": post["media_type"],
                "caption": post["caption"],
                "media_url": post["media_url"],
                "permalink": post["permalink"]
            }]).execute())
            print(response)
            print(f"💚Publicación {post_id} guardada en la DB")  # Cambié esta línea
            return post
        except Exception as e:
            print(f"❌Error al guardar el post en la DB: {e}")
            return None