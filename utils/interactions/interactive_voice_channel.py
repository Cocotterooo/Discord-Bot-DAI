import asyncio
import discord
from discord.ext import commands
from discord import app_commands, ButtonStyle
from discord.ui import Button, View
from supabase import Client

from config import ADMIN_ROLE


def voice_channel_creator(bot: commands.Bot, admin_role: int, embed: discord.Embed):
    @bot.tree.command(
        name="setup_canales_voz",
        description="Envía un embed con botones para crear canales de voz personalizados.",
    )
    @app_commands.describe(channel='La ID del chat donde se enviará el embed')
    @app_commands.checks.has_role(ADMIN_ROLE)
    async def enviar_embed(interaction: discord.Interaction, channel: discord.TextChannel):
        await interaction.response.defer(thinking=True)  # Indica que se está procesando

        # Crear los botones
        buttons = [
            Button(label="", style=ButtonStyle.secondary, custom_id=str(i), emoji=f"{i}️⃣")
            for i in range(2, 10)
        ]
        buttons.append(
            Button(label="", style=ButtonStyle.secondary, custom_id="10", emoji="🔟")
        )

        # Crear una vista que contenga los botones
        view = View()
        for button in buttons:
            view.add_item(button)

        # Enviar el mensaje con el embed y los botones
        await channel.send(embed=embed, view=view)
        await interaction.followup.send(
            "<:correcto:1288631406452412428> Creador de canales de voz enviado.",
            ephemeral=True,
        )

    @enviar_embed.error
    async def enviar_embed_error(interaction: discord.Interaction, error):
        if isinstance(error, app_commands.MissingRole):
            await interaction.response.send_message(
                "<:no:1288631410558767156> No tienes permisos para usar este comando.",
                ephemeral=True,
            )


async def create_or_update_channel(
    bot: discord.Client,
    supabase: Client,
    interaction: discord.Interaction,
):
    user_id = interaction.user.id
    category = discord.utils.get(interaction.guild.categories, name="🔊| CANALES DE VOZ |🔊")

    # Verificar si el usuario ya existe en la base de datos
    user_data = supabase.table('users').select('voice_channel').eq('id', user_id).execute()

    # Acceder correctamente a los datos
    user_channel_id = user_data.data[0]['voice_channel'] if user_data.data else None

    # Limite de usuarios según el botón presionado
    try:
        user_limit = int(interaction.data.get("custom_id"))
    except ValueError:
        return

    channel_name = f"🔊⦙ {interaction.user.name}"

    if user_channel_id:
        # Si el usuario ya tiene un canal
        user_channel = bot.get_channel(int(user_channel_id))
        if user_channel:
            await user_channel.edit(user_limit=user_limit)
            await interaction.response.send_message(
                f"<:correcto:1288631406452412428> El límite de usuarios de tu canal {user_channel.mention} ahora es `{user_limit}`.",
                ephemeral=True,
            )
            asyncio.create_task(
                monitor_channel_activity(bot, user_channel, supabase, user_id)
            )
    else:
        # Si no tiene un canal, lo creamos
        channel = await interaction.guild.create_voice_channel(
            name=channel_name,
            category=category,
            user_limit=user_limit,
        )

        user_data = supabase.table('users').select('id').eq('id', user_id).execute()

        if not user_data.data:
            supabase.table('users').insert({"id": user_id, "voice_channel": channel.id}).execute()
        else:
            supabase.table('users').update({"voice_channel": channel.id}).eq('id', user_id).execute()

        await interaction.response.send_message(
            f"<:correcto:1288631406452412428> Canal {channel.mention} creado con límite de `{user_limit}` usuarios.",
            ephemeral=True,
        )
        asyncio.create_task(monitor_channel_activity(bot, channel, supabase, user_id))


async def monitor_channel_activity(
    bot: discord.Client,
    channel: discord.VoiceChannel,
    supabase: Client,
    user_id: int,
):
    """Monitorea la actividad del canal de voz y realiza acciones tras 10 y 15 minutos de inactividad."""
    inactivity_time = 0
    is_inactive = False

    while True:
        await asyncio.sleep(60)

        if len(channel.members) == 0:
            inactivity_time += 1
        else:
            inactivity_time = 0
            if is_inactive:
                await channel.edit(name=f"🔊⦙ {channel.name[3:].strip()}")
                is_inactive = False

        if inactivity_time == 10 and not is_inactive:
            await channel.edit(name=f"🔇⦙ {channel.name[3:].strip()}")
            is_inactive = True

        if inactivity_time == 15:
            await channel.delete(reason="Canal eliminado por inactividad.")
            supabase.table('users').delete().eq('id', user_id).execute()
            break


async def resume_channel_monitoring(bot: discord.Client, supabase: Client):
    """Reanuda el monitoreo de los canales de voz al iniciar el bot."""
    user_data = supabase.table('users').select('id', 'voice_channel').execute()

    for user in user_data.data:
        user_id = user['id']
        channel_id = user['voice_channel']
        channel = bot.get_channel(int(channel_id))

        if channel:
            asyncio.create_task(monitor_channel_activity(bot, channel, supabase, user_id))
        else:
            supabase.table('users').delete().eq('id', user_id).execute()
