import asyncio
from utils.api.instagram.Instagram import InstagramAPI
from supabase import Client

async def update_likes_comments_db(instagram: InstagramAPI, supabase: Client, seconds: int):
    while seconds > 0:
        await asyncio.sleep(seconds)
        print("🔃Actualizando likes y comentarios")
        posts = instagram.get_all_posts()
        for i in posts['data']:
            try:
                instagram.update_likes_comments(i['id'], supabase)
            except Exception as e:
                print(f"Error - ID{i['id']}: {e}")
        print(f"💚Likes y comentarios actualizados en la Base de Datos")

