from supabase import Client
import discord

class Dc_insta_msg():
    def __init__(self, supabase: Client) -> None:
        self.supabase = supabase
    
    async def save_message_id(self, message_id:int, post_id:int):
        try:
            response = self.supabase.table('instagram_post_discord').insert(
                                [{'id': post_id,
                                'message_id': message_id}]
                            ).execute()
            print(f'response: {response}')
            return
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

'''
    async def edit_publication_sended(channel_id: int, message_id: int):
        try:
            # Obtener el canal donde está el mensaje
            channel = bot.get_channel(channel_id)
            if channel is None:
                print("No se pudo encontrar el canal.")
                return
            # Obtener el mensaje usando el ID
            message = await channel.fetch_message(message_id)
            # Crear el nuevo embed
            new_embed = discord.Embed(
                title="Título actualizado",
                description="Descripción actualizada del embed",
                color=discord.Color.blue()
            )
            new_embed.add_field(name="Nuevo Campo", value="Este es el nuevo valor", inline=False)

            # Editar el mensaje con el nuevo embed
            await message.edit(embed=new_embed)
            print(f"Mensaje {message_id} editado correctamente.")
        
        except discord.NotFound:
            print("No se encontró el mensaje con ese ID.")
        except discord.Forbidden:
            print("No tengo permisos para editar el mensaje.")
        except discord.HTTPException as e:
            print(f"Error al editar el mensaje: {e}")'''

