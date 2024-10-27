import discord
from discord import app_commands
from config import ASOCIATION_ROLE_IDS, ADMIN_ROLE, spacelab_info_embed, motorsport_info_embed, ces_info_embed


def nuevo_spacelab(bot):
    @bot.tree.command(name="nuevo_spacelab", description="Añadir rol de miembro de Spacelab")
    @app_commands.checks.has_role(ASOCIATION_ROLE_IDS['spacelab']['coord'])
    async def nuevo_spacelab(interaction: discord.Interaction, user: discord.Member):
        await gestionar_rol(interaction, user, 'spacelab', "añadir")

    @nuevo_spacelab.error
    async def nuevo_spacelab_error(interaction: discord.Interaction, error):
        if isinstance(error, app_commands.MissingRole):
            await interaction.response.send_message("<:no:1288631410558767156> No tienes permisos para usar este comando.", ephemeral=True) 


def eliminar_spacelab(bot):
    @bot.tree.command(name="eliminar_spacelab", description="Eliminar rol de miembro de Spacelab")
    @app_commands.checks.has_role(ASOCIATION_ROLE_IDS['spacelab']['coord'])
    async def eliminar_spacelab(interaction: discord.Interaction, user: discord.Member):
        await gestionar_rol(interaction, user, 'spacelab', "eliminar")

    @eliminar_spacelab.error
    async def eliminar_spacelab_error(interaction: discord.Interaction, error):
        if isinstance(error, app_commands.MissingRole):
            await interaction.response.send_message("<:no:1288631410558767156> No tienes permisos para usar este comando.", ephemeral=True) 


def nuevo_motorsport(bot):
    @bot.tree.command(name="nuevo_motorsport", description="Añadir rol de miembro de Motorsport")
    @app_commands.checks.has_role(ASOCIATION_ROLE_IDS['motorsport']['coord'])
    async def nuevo_motorsport(interaction: discord.Interaction, user: discord.Member):
        await gestionar_rol(interaction, user, 'motorsport', "añadir")

    @nuevo_motorsport.error
    async def nuevo_motorsport_error(interaction: discord.Interaction, error):
        if isinstance(error, app_commands.MissingRole):
            await interaction.response.send_message("<:no:1288631410558767156> No tienes permisos para usar este comando.", ephemeral=True) 


def eliminar_motorsport(bot):
    @bot.tree.command(name="eliminar_motorsport", description="Eliminar rol de miembro de Motorsport")
    @app_commands.checks.has_role(ASOCIATION_ROLE_IDS['motorsport']['coord'])
    async def eliminar_motorsport(interaction: discord.Interaction, user: discord.Member):
        await gestionar_rol(interaction, user, 'motorsport', "eliminar")

    @eliminar_motorsport.error
    async def eliminar_motorsport_error(interaction: discord.Interaction, error):
        if isinstance(error, app_commands.MissingRole):
            await interaction.response.send_message("<:no:1288631410558767156> No tienes permisos para usar este comando.", ephemeral=True) 


def nuevo_ces(bot):
    @bot.tree.command(name="nuevo_ces", description="Añadir rol de miembro de CES")
    @app_commands.checks.has_role(ASOCIATION_ROLE_IDS['ces']['coord'])
    async def nuevo_ces(interaction: discord.Interaction, user: discord.Member):
        await gestionar_rol(interaction, user, 'ces', "añadir")

    @nuevo_ces.error
    async def nuevo_ces_error(interaction: discord.Interaction, error):
        if isinstance(error, app_commands.MissingRole):
            await interaction.response.send_message("<:no:1288631410558767156> No tienes permisos para usar este comando.", ephemeral=True) 


def eliminar_ces(bot):
    @bot.tree.command(name="eliminar_ces", description="Eliminar rol de miembro de CES")
    @app_commands.checks.has_role(ASOCIATION_ROLE_IDS['ces']['coord'])
    async def eliminar_ces(interaction: discord.Interaction, user: discord.Member):
        await gestionar_rol(interaction, user, 'ces', "eliminar")

    @eliminar_ces.error
    async def eliminar_ces_error(interaction: discord.Interaction, error):
        if isinstance(error, app_commands.MissingRole):
            await interaction.response.send_message("<:no:1288631410558767156> No tienes permisos para usar este comando.", ephemeral=True) 


async def gestionar_rol(interaction: discord.Interaction, user, asociacion, accion):
    # Identificar el rol de miembro de la asociación
    member_role_id = ASOCIATION_ROLE_IDS[asociacion]['member']
    member_role = interaction.guild.get_role(member_role_id)
    
    if accion == "añadir":
        if member_role in user.roles:
            await interaction.response.send_message(f"<:no:1288631410558767156> {user.mention} ya tiene el rol de miembro de {asociacion}.", ephemeral=True)
        else:
            await user.add_roles(member_role)
            await interaction.response.send_message(f"<:correcto:1288631406452412428> Se ha añadido el rol de miembro de {asociacion} a {user.mention}.", ephemeral=True)
    elif accion == "eliminar":
        if member_role not in user.roles:
            await interaction.response.send_message(f"<:no:1288631410558767156> {user.mention} no tiene el rol de miembro de {asociacion}.", ephemeral=True)
        else:
            await user.remove_roles(member_role)
            await interaction.response.send_message(f"<:correcto:1288631406452412428> Se ha eliminado el rol de miembro de {asociacion} a {user.mention}.", ephemeral=True)


# SETUP INFO OF ASOCIATIONS

def setup_spacelab(bot):
    @bot.tree.command(name="setup_spacelab", description="Enviar el embed de información de Spacelab")
    @app_commands.describe(channel='La ID del chat donde se enviará el embed')
    @app_commands.checks.has_role(ADMIN_ROLE)
    async def send_main_embed(interaction: discord.Interaction, channel: discord.TextChannel):
        """Slash Command que envía el embed principal al canal seleccionado"""
        embed = spacelab_info_embed()
        await channel.send(embed=embed)
        await interaction.response.send_message(f"<:correcto:1288631406452412428> Embed enviado a {channel.mention}", ephemeral=True)

    @send_main_embed.error
    async def send_main_embed_error(interaction: discord.Interaction, error):
        if isinstance(error, app_commands.MissingRole):
            await interaction.response.send_message("<:no:1288631410558767156> No tienes permisos para usar este comando.", ephemeral=True)


def setup_motorsport(bot):
    @bot.tree.command(name="setup_motorsport", description="Enviar el embed de información de Spacelab")
    @app_commands.describe(channel='La ID del chat donde se enviará el embed')
    @app_commands.checks.has_role(ADMIN_ROLE)
    async def send_main_embed(interaction: discord.Interaction, channel: discord.TextChannel):
        """Slash Command que envía el embed principal al canal seleccionado"""
        embed = motorsport_info_embed()
        await channel.send(embed=embed)
        await interaction.response.send_message(f"<:correcto:1288631406452412428> Embed enviado a {channel.mention}", ephemeral=True)

    @send_main_embed.error
    async def send_main_embed_error(interaction: discord.Interaction, error):
        if isinstance(error, app_commands.MissingRole):
            await interaction.response.send_message("<:no:1288631410558767156> No tienes permisos para usar este comando.", ephemeral=True)


def setup_ces(bot):
    @bot.tree.command(name="setup_ces", description="Enviar el embed de información de Spacelab")
    @app_commands.describe(channel='La ID del chat donde se enviará el embed')
    @app_commands.checks.has_role(ADMIN_ROLE)
    async def send_main_embed(interaction: discord.Interaction, channel: discord.TextChannel):
        """Slash Command que envía el embed principal al canal seleccionado"""
        embed = ces_info_embed()
        await channel.send(embed=embed)
        await interaction.response.send_message(f"<:correcto:1288631406452412428> Embed enviado a {channel.mention}", ephemeral=True)

    @send_main_embed.error
    async def send_main_embed_error(interaction: discord.Interaction, error):
        if isinstance(error, app_commands.MissingRole):
            await interaction.response.send_message("<:no:1288631410558767156> No tienes permisos para usar este comando.", ephemeral=True)