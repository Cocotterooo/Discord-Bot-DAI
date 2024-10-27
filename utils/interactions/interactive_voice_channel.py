import discord
from discord.ext import commands
from discord import app_commands, ButtonStyle
from discord.ui import Button, View
import asyncio
from supabase import Client

from config import ADMIN_ROLE


def voice_channel_creator(bot: commands.Bot, admin_role: int, embed: discord.Embed):
    @bot.tree.command(name="setup_canales_voz", description="Envía un embed con botones para crear canales de voz personalizados.")
    @app_commands.describe(channel='La ID del chat donde se enviará el embed')
    @app_commands.checks.has_role(ADMIN_ROLE)
    async def enviar_embed(interaction: discord.Interaction, channel: discord.TextChannel):
        await interaction.response.defer(thinking=True)  # Indica que se está procesando

        # Crear los botones
        button1 = Button(label="", style=ButtonStyle.secondary, custom_id="2", emoji='2️⃣')
        button2 = Button(label="", style=ButtonStyle.secondary, custom_id="3", emoji='3️⃣')
        button3 = Button(label="", style=ButtonStyle.secondary, custom_id="4", emoji='4️⃣')
        button4 = Button(label="", style=ButtonStyle.secondary, custom_id="5", emoji='5️⃣')
        button5 = Button(label="", style=ButtonStyle.secondary, custom_id="6", emoji='6️⃣')
        button6 = Button(label="", style=ButtonStyle.secondary, custom_id="7", emoji='7️⃣')
        button7 = Button(label="", style=ButtonStyle.secondary, custom_id="8", emoji='8️⃣')
        button8 = Button(label="", style=ButtonStyle.secondary, custom_id="9", emoji='9️⃣')
        button9 = Button(label="", style=ButtonStyle.secondary, custom_id="10", emoji='🔟')

        # Crear una vista que contenga los botones
        view = View()
        view.add_item(button1)
        view.add_item(button2)
        view.add_item(button3)
        view.add_item(button4)
        view.add_item(button5)
        view.add_item(button6)
        view.add_item(button7)
        view.add_item(button8)
        view.add_item(button9)
        
        # Enviar el mensaje con el embed y los botones
        await channel.send(embed=embed, view=view)
        await interaction.followup.send("<:correcto:1288631406452412428> Creador de canales de voz enviado.", ephemeral=True)

    @enviar_embed.error
    async def enviar_embed_error(interaction: discord.Interaction, error):
        if isinstance(error, app_commands.MissingRole):
            await interaction.response.send_message("<:no:1288631410558767156> No tienes permisos para usar este comando.", ephemeral=True)

async def create_or_update_channel(bot: discord.Client, supabase: Client, interaction: discord.Interaction):
    user_id = interaction.user.id
    category = discord.utils.get(interaction.guild.categories, name="🔊| CANALES DE VOZ |🔊")
    
    # Verificar si el usuario ya existe en la base de datos
    user_data = supabase.table('users').select('voice_channel').eq('id', user_id).execute()
    
    # Acceder correctamente a los datos
    user_channel_id = user_data.data[0]['voice_channel'] if user_data.data else None

    # Limite de usuarios según el botón presionado
    try:
        user_limit = int(interaction.data.get("custom_id"))
    except:
        return
    
    channel_name = f"🔊⦙ {interaction.user.name}"

    if user_channel_id:  # Si el usuario ya tiene un canal
        user_channel = bot.get_channel(int(user_channel_id))
        if user_channel:
            # Editar el límite de usuarios del canal existente
            await user_channel.edit(user_limit=user_limit)
            # Responder al usuario mencionando su canal
            await interaction.response.send_message(
                f"<:correcto:1288631406452412428> El límite de usuarios de tu canal {user_channel.mention} ahora es `{user_limit}`.", 
                ephemeral=True
            )
            # Comenzar a monitorear el canal
            asyncio.create_task(monitor_channel_activity(bot, user_channel, supabase, user_id))
    else:  # Si no tiene un canal, lo creamos
        channel = await interaction.guild.create_voice_channel(
            name=channel_name, 
            category=category, 
            user_limit=user_limit
        )
        
        # Guardar el canal en la base de datos
        user_data = supabase.table('users').select('id').eq('id', user_id).execute()

        if not user_data.data:  # Si el usuario no está en la base de datos
            supabase.table('users').insert({"id": user_id, "voice_channel": channel.id}).execute()
        else:  # Si el usuario ya está en la base de datos, actualizar el canal de voz
            supabase.table('users').update({"voice_channel": channel.id}).eq('id', user_id).execute()

        # Responder al usuario mencionando su canal
        await interaction.response.send_message(
            f"<:correcto:1288631406452412428> Canal {channel.mention} creado con límite de `{user_limit}` usuarios.", 
            ephemeral=True
        )
        
        # Comenzar a monitorear el canal
        asyncio.create_task(monitor_channel_activity(bot, channel, supabase, user_id))

async def monitor_channel_activity(bot: discord.Client, channel: discord.VoiceChannel, supabase: Client, user_id: int):
    """Monitorea la actividad del canal de voz y realiza acciones tras 10 y 15 minutos de inactividad."""
    inactivity_time = 0
    is_inactive = False  # Bandera para saber si el canal ha sido marcado como inactivo

    while True:
        await asyncio.sleep(60)  # Revisa cada 60 segundos

        # Verifica si hay miembros en el canal
        if len(channel.members) == 0:
            inactivity_time += 1
        else:
            # Reiniciar el contador si alguien se une o usa el canal
            inactivity_time = 0
            if is_inactive:
                # Restaurar el nombre original del canal
                await channel.edit(name=f"🔊⦙ {channel.name[3:].strip()}")
                print(f"El nombre del canal {channel.name} ha sido restaurado a su estado original por actividad.")
                is_inactive = False

        # A los 10 minutos de inactividad, cambiar el nombre del canal a "inactivo"
        if inactivity_time == 10 and not is_inactive:
            await channel.edit(name=f"🔇⦙ {channel.name[3:].strip()}")  # Mantener el nombre original
            is_inactive = True
            print(f"El nombre del canal {channel.name} ha sido cambiado por inactividad (10 minutos).")

        # A los 15 minutos de inactividad, eliminar el canal
        if inactivity_time == 15:
            await channel.delete(reason="Canal eliminado por inactividad.")
            print(f"El canal {channel.name} ha sido eliminado por inactividad (15 minutos).")

            # Eliminar la entrada correspondiente en la base de datos
            supabase.table('users').delete().eq('id', user_id).execute()
            print(f"Entrada eliminada de la base de datos para el usuario {user_id}.")
            break


async def resume_channel_monitoring(bot: discord.Client, supabase: Client):
    """Reanuda el monitoreo de los canales de voz al iniciar el bot."""
    # Obtener todos los usuarios que tienen canales de voz registrados en la base de datos
    user_data = supabase.table('users').select('id', 'voice_channel').execute()

    for user in user_data.data:
        user_id = user['id']
        channel_id = user['voice_channel']
        channel = bot.get_channel(int(channel_id))

        if channel:
            # Reiniciar el monitoreo del canal
            print(f"Reanudando el monitoreo del canal {channel.name} del usuario {user_id}.")
            asyncio.create_task(monitor_channel_activity(bot, channel, supabase, user_id))
        else:
            # Si el canal no existe (por algún fallo), eliminar la entrada de la base de datos
            supabase.table('users').delete().eq('id', user_id).execute()
            print(f"El canal {channel_id} no existe. Eliminando la entrada de la base de datos para el usuario {user_id}.")
