import requests
from io import BytesIO
import aiohttp

class InstagramAPI():
    def __init__(self, access_token):
        self.access_token = access_token

    @property
    async def user_id_username(self):
        url = f"https://graph.instagram.com/me?fields=id,username&access_token={self.access_token}"
        response = requests.get(url)
        if response.status_code != 200:
            print(f'❌Error: user_id_username - al obtener el ID y el nombre de usuario: {response}')
        data = response.json()
        return data

    async def get_all_posts(self):
        user_info = await self.user_id_username
        url = f"https://graph.instagram.com/{user_info['id']}/media?fields=id,caption,media_type,media_url,thumbnail_url,permalink,timestamp&access_token={self.access_token}"
        response = requests.get(url)
        if response.status_code == 200:
            media_data = response.json()
            return media_data
        else:
            return(f"Error: {response.status_code} - {response.text}")

    async def get_num_likes_comments(self, post_id: int):
        url = f"https://graph.instagram.com/{post_id}?fields=like_count,comments_count&access_token={self.access_token}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return(f"Error: {response.status_code} - {response.text}")

    async def get_media_url(self, post_id: int):
        url = f"https://graph.instagram.com/{post_id}?fields=media_url&access_token={self.access_token}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    
    def get_items_carousel(self, media_id: int):
        url = f'https://graph.instagram.com/{media_id}?fields=children{{media_url}}&access_token={self.access_token}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data.get('children', {}).get('data', [])
        else:
            print(f"Error al obtener datos del carrusel: {response.status_code}")
            return []

    def get_image_post(self, media_url):
        try: # Obtiene la imagen
            image_response = requests.get(media_url)
            image_response.raise_for_status()  # Lanza un error si la solicitud falló
        except requests.RequestException as e:
            print(f"❌Error: get_image_post() - al obtener la imagen: {e}")
            return None

        # Guarda la imagen en un objeto BytesIO
        image_binary = BytesIO()
        try:
            image_binary.write(image_response.content)  # Guarda el contenido de la imagen en el BytesIO
            image_binary.seek(0)  # Reajusta el puntero al inicio
            return image_binary  # Devuelve el objeto BytesIO
        except Exception as e:
            print(f"❌Error: get_image_post() - al guardar la imagen: {e}")
            return None
    
    async def get_video_post(self, media_url):
        async with aiohttp.ClientSession() as session:
            async with session.get(media_url) as response:
                if response.status == 200:
                    return await response.read()  # Lee los datos como binarios
                else:
                    raise Exception(f"Error al descargar el video: {response.status}")
