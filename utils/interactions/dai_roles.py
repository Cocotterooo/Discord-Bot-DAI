import discord
from discord import app_commands
from discord.ext import commands
from discord import Embed, ButtonStyle
from discord.ui import Button, View

from config import ADMIN_ROLE, DAI_MEMBER_ROLE_ID, DAI_TUTORING_ROLE_ID, dai_roles_embed, ID_INFRAESTRUCTURAS, ID_COMUNICACION, ID_ASUNTOS_EXTERIORES, ID_DEPORTES

def dai_roles(bot: commands.Bot):
    @bot.tree.command(name="dai_roles", description="Envía un embed con botones para asignar o remover roles")
    @app_commands.describe(channel='La ID del chat donde se enviará el embed')
    @app_commands.checks.has_role(ADMIN_ROLE)
    async def enviar_embed(interaction: discord.Interaction, channel: discord.TextChannel):
        await interaction.response.defer(thinking=True)  # Indica que se está procesando
        
        embed = dai_roles_embed()
        
        # Crear los botones
        button1 = Button(label="Infraestructuras", style=ButtonStyle.success, custom_id="dai_role_1", emoji='💻')
        button2 = Button(label="Comunicación", style=ButtonStyle.success, custom_id="dai_role_2", emoji='📣')
        button3 = Button(label="Asuntos Exteriores", style=ButtonStyle.success, custom_id="dai_role_3", emoji='🫂')
        button4 = Button(label="Deportes y Ocio", style=ButtonStyle.success, custom_id="dai_role_4", emoji='🏃')
        
        # Crear una vista que contenga los botones
        view = View()
        view.add_item(button1)
        view.add_item(button2)
        view.add_item(button3)
        view.add_item(button4)
        
        # Enviar el mensaje con el embed y los botones
        await channel.send(f'{discord.utils.get(interaction.guild.roles, id=DAI_MEMBER_ROLE_ID).mention} {discord.utils.get(interaction.guild.roles, id=DAI_TUTORING_ROLE_ID).mention}', embed=embed, view=view)
        await interaction.followup.send("<:correcto:1288631406452412428> Selector de roles enviado.", ephemeral=True)

    @enviar_embed.error
    async def enviar_embed_error(interaction: discord.Interaction, error):
        if isinstance(error, app_commands.MissingRole):
            await interaction.response.send_message("<:no:1288631410558767156> No tienes permisos para usar este comando.", ephemeral=True)

ROLE_IDS = {
    'dai_role_1': ID_INFRAESTRUCTURAS,
    'dai_role_2': ID_COMUNICACION,
    'dai_role_3': ID_ASUNTOS_EXTERIORES,
    'dai_role_4': ID_DEPORTES
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