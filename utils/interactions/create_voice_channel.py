import discord
from discord.ext import commands
from discord import app_commands, ButtonStyle
from discord.ui import Button, View
import asyncio

from config import voice_channel_creator_embed

def voice_channel_creator(bot: commands.Bot, admin_role: int):
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

        embed = voice_channel_creator_embed()
        
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
}
async def dai_roles_interaction(interaction: discord.Interaction):
    if interaction.type == discord.InteractionType.component:
        user = interaction.user
        guild = interaction.guild
        
        # Obtener el rol correspondiente basado en el botón presionado
        role_id = ROLE_IDS.get(interaction.data.get('custom_id'))
        role = guild.get_role(role_id)
        
        if role:
            if role in user.roles:
                # Si el usuario ya tiene el rol, se lo quitamos
                await user.remove_roles(role)
                await interaction.response.send_message(f"<:no:1288631410558767156> Se te ha **eliminado** el rol {role.mention}.", ephemeral=True)
            else:
                # Si no tiene el rol, se lo asignamos
                await user.add_roles(role)
                await interaction.response.send_message(f"<:correcto:1288631406452412428> Se te ha **asignado** el rol {role.mention}.", ephemeral=True)
                '''