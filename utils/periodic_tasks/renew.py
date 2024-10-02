import asyncio
from utils.db.Posts import Post
from supabase import Client

async def renew_all_likes_comments_task(posts: Post, interval: int):
    while interval > 0:
        await posts.renew_all_likes_comments_db()  # Esto se ejecutará cada 1 hora
        await asyncio.sleep(interval)
    print("🔃 Actualizando likes y comentarios ❌ Deshabilitado")

async def renew_media_url_task(posts: Post, interval: int):
    while interval > 0:
        await posts.renew_media_url_db()  # Esto se ejecutará cada 10 segundos
        await asyncio.sleep(interval)
    print("🔃 Actualizando media_url de los posts ❌ Deshabilitado")

