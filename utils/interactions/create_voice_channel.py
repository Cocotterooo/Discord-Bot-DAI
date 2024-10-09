import discord
from discord.ext import commands
from discord import app_commands, ButtonStyle
from discord.ui import Button, View
import asyncio
from supabase import Client

def voice_channel_creator(bot: commands.Bot, admin_role: int, channel_creator_embed: discord.Embed):
    @bot.tree.command(name="creador_canales_voz", description="Envía un embed con botones para crear canales de voz personalizados.")
    @app_commands.describe(creator_channel_id='La ID del chat donde se enviará el embed')
    async def enviar_embed(interaction: discord.Interaction, creator_channel_id:str):
        await interaction.response.defer(thinking=True)  # Indica que se está procesando
        role_allowed = discord.utils.get(interaction.guild.roles, id=admin_role)
        if role_allowed not in interaction.user.roles:
            await interaction.response.send_message("<:no:1288631410558767156> No tienes permiso para usar este comando.", ephemeral=True)
            return

        try:
            creator_channel_id = int(creator_channel_id)
        except ValueError:
            await interaction.followup.send("<:no:1288631410558767156> La ID del no es válida.", ephemeral=True)
            return
        channel = bot.get_channel(creator_channel_id)
        # Crear el embed
        embed = channel_creator_embed
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
        await interaction.followup.send("<:correcto:1288631406452412428> Selector de roles enviado.", ephemeral=True)


'''ROLE_IDS = {
    '1': ID_INFRAESTRUCTURAS,
    '2': ID_COMUNICACION,
    '3': ID_ASUNTOS_EXTERIORES,
    '4': ID_DEPORTES
}'''
async def create_or_update_channel(bot: discord.Client, supabase: Client, interaction: discord.Interaction):
    user_id = interaction.user.id
    category = discord.utils.get(interaction.guild.categories, name="🔊| CANALES DE VOZ |🔊")
    
    # Verificar si el usuario ya existe en la base de datos
    user_data = supabase.table('users').select('voice_channel').eq('id', user_id).execute()
    
    # Acceder correctamente a los datos
    user_channel_id = user_data.data[0]['voice_channel'] if user_data.data else None

    # Limite de usuarios según el botón presionado
    user_limit = int(interaction.data.get("custom_id"))
    channel_name = f"🔊⦙ {interaction.user.name}"

    if user_channel_id:  # Si el usuario ya tiene un canal
        user_channel = bot.get_channel(int(user_channel_id))
        if user_channel:
            # Editar el límite de usuarios del canal existente
            await user_channel.edit(user_limit=user_limit)
            # Responder al usuario mencionando su canal
            await interaction.response.send_message(
                f"<:correcto:1288631406452412428> El **límite de usuarios** de tu canal {user_channel.mention} ahora es `{user_limit}`.", 
                ephemeral=True
            )
    else:  # Si no tiene un canal, lo creamos
        channel = await interaction.guild.create_voice_channel(
            name=channel_name, 
            category=category, 
            user_limit=user_limit
        )
        
        # Guardar el canal en la base de datos (integrando la lógica de save_user_channel)
        user_data = supabase.table('users').select('id').eq('id', user_id).execute()

        if not user_data.data:  # Si el usuario no está en la base de datos
            supabase.table('users').insert({"id": user_id, "voice_channel": channel.id}).execute()
        else:  # Si el usuario ya está en la base de datos, actualizar el canal de voz
            supabase.table('users').update({"voice_channel": channel.id}).eq('id', user_id).execute()

        # Responder al usuario mencionando su canal
        await interaction.response.send_message(
            f"<:correcto:1288631406452412428> Canal {channel.mention} creado con **límite de** `{user_limit}` **usuarios**.", 
            ephemeral=True
        )