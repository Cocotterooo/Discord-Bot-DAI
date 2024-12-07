import discord
from discord import app_commands
from config import (
    ASOCIATION_ROLE_IDS,
    ADMIN_ROLE,
    spacelab_info_embed,
    motorsport_info_embed,
    ces_info_embed,
    ceeibis_info_embed
)


def nuevo_rol_ceeibis(bot):
    """Añadir rol de miembro de CEEIBIS."""
    @bot.tree.command(
        name="nuevo_ceeibis",
        description="Añadir rol de miembro de CEEIBIS"
    )
    @app_commands.checks.has_role(ASOCIATION_ROLE_IDS['ceeibis']['coord'])
    async def nuevo_ceeibis(interaction: discord.Interaction, user: discord.Member):
        await gestionar_rol(interaction, user, 'ceeibis', "añadir")

    @nuevo_ceeibis.error
    async def nuevo_ceeibis_error(interaction: discord.Interaction, error):
        if isinstance(error, app_commands.MissingRole):
            await interaction.response.send_message(
                "<:no:1288631410558767156> No tienes permisos para usar este comando.",
                ephemeral=True
            )


def eliminar_rol_ceeibis(bot):
    """Eliminar rol de miembro de CEEIBIS."""
    @bot.tree.command(
        name="eliminar_ceeibis",
        description="Eliminar rol de miembro de CEEIBIS"
    )
    @app_commands.checks.has_role(ASOCIATION_ROLE_IDS['ceeibis']['coord'])
    async def eliminar_ceeibis(interaction: discord.Interaction, user: discord.Member):
        await gestionar_rol(interaction, user, 'ceeibis', "eliminar")

    @eliminar_ceeibis.error
    async def eliminar_ceeibis_error(interaction: discord.Interaction, error):
        if isinstance(error, app_commands.MissingRole):
            await interaction.response.send_message(
                "<:no:1288631410558767156> No tienes permisos para usar este comando.",
                ephemeral=True
            )


# Similar estructura para spacelab, motorsport y ces

async def gestionar_rol(interaction: discord.Interaction, user: discord.Member, asociacion: str, accion: str):
    """Gestiona la asignación o eliminación de roles para miembros de asociaciones."""
    member_role_id = ASOCIATION_ROLE_IDS[asociacion]['member']
    member_role = interaction.guild.get_role(member_role_id)

    if accion == "añadir":
        if member_role in user.roles:
            await interaction.response.send_message(
                f"<:no:1288631410558767156> {user.mention} ya tiene el rol de miembro de {asociacion}.",
                ephemeral=True
            )
        else:
            await user.add_roles(member_role)
            await interaction.response.send_message(
                f"<:correcto:1288631406452412428> Se ha añadido el rol de miembro de {asociacion} a {user.mention}.",
                ephemeral=True
            )
    elif accion == "eliminar":
        if member_role not in user.roles:
            await interaction.response.send_message(
                f"<:no:1288631410558767156> {user.mention} no tiene el rol de miembro de {asociacion}.",
                ephemeral=True
            )
        else:
            await user.remove_roles(member_role)
            await interaction.response.send_message(
                f"<:correcto:1288631406452412428> Se ha eliminado el rol de miembro de {asociacion} a {user.mention}.",
                ephemeral=True
            )


# Funciones de configuración de embeds
def setup_info_embed(bot, embed_function, command_name, description):
    """Configuración de comandos para enviar embebidos de información."""
    @bot.tree.command(
        name=command_name,
        description=description
    )
    @app_commands.describe(channel='La ID del chat donde se enviará el embed')
    @app_commands.checks.has_role(ADMIN_ROLE)
    async def send_main_embed(interaction: discord.Interaction, channel: discord.TextChannel):
        embed = embed_function()
        await channel.send(embed=embed)
        await interaction.response.send_message(
            f"<:correcto:1288631406452412428> Embed enviado a {channel.mention}",
            ephemeral=True
        )

    @send_main_embed.error
    async def send_main_embed_error(interaction: discord.Interaction, error):
        if isinstance(error, app_commands.MissingRole):
            await interaction.response.send_message(
                "<:no:1288631410558767156> No tienes permisos para usar este comando.",
                ephemeral=True
            )


def setup_ceeibis(bot):
    setup_info_embed(bot, ceeibis_info_embed, "setup_ceeibis", "Enviar el embed de información de CEEIBIS")


def setup_spacelab(bot):
    setup_info_embed(bot, spacelab_info_embed, "setup_spacelab", "Enviar el embed de información de SpaceLab")


def setup_motorsport(bot):
    setup_info_embed(bot, motorsport_info_embed, "setup_motorsport", "Enviar el embed de información de Motorsport")


def setup_ces(bot):
    setup_info_embed(bot, ces_info_embed, "setup_ces", "Enviar el embed de información de CES")
