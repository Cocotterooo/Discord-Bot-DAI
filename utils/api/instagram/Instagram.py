import requests
from supabase import Client


class InstagramAPI():
    def __init__(self, access_token):
        self.access_token = access_token
    @property
    def user_id_username(self):
        url = f"https://graph.instagram.com/me?fields=id,username&access_token={self.access_token}"
        response = requests.get(url)
        if response.status_code != 200:
            print('Error')
            exit()
        data = response.json()
        return data

    def get_all_posts(self):
        url = f"https://graph.instagram.com/{self.user_id_username['id']}/media?fields=id,caption,media_type,media_url,thumbnail_url,permalink,timestamp&access_token={self.access_token}"
        response = requests.get(url)
        if response.status_code == 200:
            media_data = response.json()
            return media_data
        else:
            return(f"Error: {response.status_code} - {response.text}")

    def get_num_likes_comments(self, post_id: int):
        url = f"https://graph.instagram.com/{post_id}?fields=like_count,comments_count&access_token={self.access_token}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return(f"Error: {response.status_code} - {response.text}")

    def save_all_posts(self, supabase: Client):
        try:
            # Iterar sobre todas las publicaciones
            for i in self.get_all_posts()['data']:
                print("bucle")
                # Verificar si el ID de la publicación ya existe en la base de datos
                try:
                    result = (supabase
                            .table('posts')
                            .select('id')
                            .eq('id', i['id'])
                            .execute())
                    # Acceder a los datos correctamente
                    data = result.data
                    if data:
                        print(f"El ID {i['id']} ya existe en la DB")
                    else:
                        # Inserción en la tabla 'posts'
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
            return exception  # Manejo de excepción externa

    def update_likes_comments(self, id_post: int, supabase:Client):
        try:
            # Obtener el número de likes y comentarios de la publicación
            likes_comments = self.get_num_likes_comments(id_post)
            # Actualizar la base de datos con los nuevos datos
            print(likes_comments)
            response = supabase.table("posts").update({
                "likes_count": likes_comments['like_count'],
                "comments_count": likes_comments['comments_count']
            }).eq('id', id_post).execute()
            print(f"Likes y comentarios actualizados para la publicación {id_post}")
        except Exception as e:
            print(f"Error al actualizar los likes y comentarios: {e}")


#instagram = InstagramAPI('')


#print(instagram.get_num_likes_comments('18032521846722078'))


