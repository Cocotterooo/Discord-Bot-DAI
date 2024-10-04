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


async def renew_likes_comments_sended_messages(supabase: Client, interval: int):
    while interval > 0:
        discrepancies = await update_sended_messages(supabase, "instagram_post_discord", "posts")
        if discrepancies:
            for i in discrepancies:
                pass
        await asyncio.sleep(interval)
    print("🔃 Actualizando likes y comentarios de los mensajes enviados ❌ Deshabilitado")


async def update_sended_messages(supabase: Client, table1: str, table2:str):
    # Consulta SQL para verificar discrepancias
    query = """ QUERY SQL
    SELECT ipd.message_id, p.id , p.likes_count, p.comments_count, p.caption, p.permalink, p.media_url
    FROM instagram_post_discord ipd
    JOIN posts p ON ipd.id = p.id
    WHERE ipd.likes_count != p.likes_count
        OR ipd.comments_count != p.comments_count;
    """
    response = supabase.query(query).execute()
    #response = supabase.rpc('execute_sql', {'query': query}).execute()
    print(response)
    # Verificar y devolver resultados
    if response.status_code == 200:
        discrepancies = response.json()
        print(discrepancies)
        if discrepancies:
            return discrepancies
        else:
            return []  # No hay discrepancias
    else:
        raise Exception(f"Error en la consulta: {response.text}")
