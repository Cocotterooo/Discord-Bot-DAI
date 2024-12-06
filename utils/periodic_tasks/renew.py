import asyncio
from supabase import Client
import discord

from utils.db.Posts import Post
from utils.api.instagram.Instagram import InstagramAPI
from utils.db.Discord_instagram_messsage import Dc_insta_msg
from config import instagram_embed, INSTAGRAM_DAI_CHANNEL


async def renew_all_likes_comments_task(posts: Post, interval: int, discord_client, supabase: Client, chanel_id: int):
    while interval > 0:
        try:
            await posts.renew_all_likes_comments_db()  # Esto renovará los mensajes de la DB
            # Obtiene la data de las publicaciones que cambiaron sus likes o comentarios
            response = supabase.rpc('get_discrepancies').execute()
            print('🔃Actualizando likes y comentarios en Discord')
            await update_sended_messages(discord_client=discord_client, data=response.data, channel_id=chanel_id)
            # Actualiza los datos de la Base de Datos
            supabase.rpc('update_discrepancies').execute() 
            print('💚Likes y comentarios actualizados en la DB de control')
        except Exception as e:
            print(f"❌Error: renew_all_likes_comments_task() - Al actualizar los mensajes de discord: {e}")
        await asyncio.sleep(interval)
    print("🔃 Actualizando likes y comentarios ❌ Deshabilitado")


async def renew_media_url_task(posts: Post, interval: int):
    while interval > 0:
        await posts.renew_media_url_db()
        await asyncio.sleep(interval)
    print("🔃 Actualizando media_url de los posts ❌ Deshabilitado")


async def renew_likes_comments_sended_messages(supabase: Client, discord_client: discord.Client, channel_id:int, interval:int):
    while interval > 0:
        response = supabase.rpc('check_discrepancies').execute()
        await update_sended_messages(discord_client=discord_client, data=response.data, channel_id=channel_id)
        await asyncio.sleep(interval)
        '''DROP FUNCTION IF EXISTS public.check_discrepancies;

        CREATE OR REPLACE FUNCTION public.check_discrepancies()
        RETURNS TABLE (
            message_id BIGINT,
            post_id BIGINT,
            likes_count INTEGER,
            comments_count INTEGER,
            caption TEXT,
            permalink TEXT,
            media_url TEXT,
            date_published TIMESTAMPTZ
        ) AS $$
        BEGIN
            -- Actualizar las columnas likes_count y comments_count en instagram_post_discord
            UPDATE instagram_post_discord ipd
            SET 
                likes_count = p.likes_count,
                comments_count = p.comments_count
            FROM posts p
            WHERE ipd.id = p.id
            AND (ipd.likes_count != p.likes_count OR ipd.comments_count != p.comments_count);

            -- Devolver los registros donde hubo discrepancias
            RETURN QUERY
            SELECT ipd.message_id, p.id, p.likes_count, p.comments_count, p.caption, 
                p.permalink, p.media_url, p.date_published
            FROM instagram_post_discord ipd
            JOIN posts p ON ipd.id = p.id
            WHERE ipd.likes_count != p.likes_count
            OR ipd.comments_count != p.comments_count;

        END;
        $$ LANGUAGE plpgsql;
        
        
    print("🔃 Actualizando likes y comentarios de los mensajes enviados ❌ Deshabilitado")'''

async def update_sended_messages(discord_client, data: list, channel_id: int):
    # Consulta SQL para verificar discrepancias
    print("🔃Actualizando mensajes enviados")
    for i in data:
        try:
            channel = discord_client.get_channel(channel_id)
            message = await channel.fetch_message(i['message_id'])
            new_embed = instagram_embed(permalink=i['permalink'], 
                                        likes=i['likes_count'], 
                                        comments=i['comments_count'], 
                                        post_id=i['id'], 
                                        caption=i['caption'], 
                                        media_url=i['media_url'],
                                        date_published=i['date_published'])
            await message.edit(embed=new_embed)
            print(f"💚Mensaje {i['message_id']} actualizado correctamente.")
        except discord.NotFound:
            print(f"❌Mensaje {i['message_id']} no encontrado.")
        except discord.Forbidden:
            print("No tengo permisos para editar el mensaje.")
        except discord.HTTPException as e:
            print(f"❌Error: update_sended_messages() - al editar el mensaje: {e}")


async def check_new_post_task(instagram:InstagramAPI, posts: Post, dc_insta_msg, interval: int):
    while interval > 0:
        await check_new_post(instagram, posts, dc_insta_msg)
        await asyncio.sleep(interval)
    print("🔃 Verificación de nuevas publicaciones ❌ Deshabilitado")


async def check_new_post(instagram: InstagramAPI, posts: Post, dc_insta_msg: Dc_insta_msg):
    try:
        all_posts = await instagram.get_all_posts()
        for i in all_posts['data']:
            post_id = i['id']
            if not posts.check_post_exists(post_id): # Guarda y envia papublicación
                print(f"Nuevo post encontrado ({post_id})")
                post_data:dict = await posts.save_new_post(i['id'])
                print(f'Enviando nueva publicación {post_id} a Discord')
                await dc_insta_msg.send_new_post(post_data= post_data, channel_id=INSTAGRAM_DAI_CHANNEL)
                return
            else:
                print(f"Publicación ({post_id}) ya existe en la DB")
    except Exception as e:
        print(f"❌Error: check_new_post() - Al verificar nuevas publicaciones: {e}")
