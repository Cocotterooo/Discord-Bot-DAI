import requests
from supabase import Client
import instaloader

class InstagramAPI():
    def __init__(self, access_token):
        self.access_token = access_token

    @property
    def user_id_username(self):
        url = f"https://graph.instagram.com/me?fields=id,username&access_token={self.access_token}"
        response = requests.get(url)
        if response.status_code != 200:
            print(f'❌Error: user_id_username - al obtener el ID y el nombre de usuario: {response}')
        data = response.json()
        return data

    def get_all_posts(self):
        url = f"https://graph.instagram.com/{self.user_id_username['id']}/media?fields=id,caption,media_type,media_url,thumbnail_url,permalink,timestamp&access_token={self.access_token}"
        response = requests.get(url)
        print(response)
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

    def get_media_url(self, post_id: int):
        url = f"https://graph.instagram.com/{post_id}?fields=media_url&access_token={self.access_token}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    # BASES DE DATOS
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

    

