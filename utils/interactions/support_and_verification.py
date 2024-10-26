import discord
from discord.ext import commands
from discord import ButtonStyle, Interaction, ui, app_commands

from config import ADMIN_ROLE, TICKET_CATEGORY_ID, VERIFICATION_CATEGORY_ID, DAI_MEMBER_ROLE_ID, VERIFIED_ROLE_ID, tickets_embed, verification_embed, support_and_verification_embed

class TicketView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(discord.ui.Button(label="📩 Crea un Ticket", style=ButtonStyle.blurple, custom_id="create_ticket"))
        self.add_item(discord.ui.Button(label="☑️ Verifícate", style=ButtonStyle.green, custom_id="verify"))

class CloseTicketView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(discord.ui.Button(label="Cerrar Ticket", style=ButtonStyle.red, custom_id="close_ticket"))

class VerificationView(ui.View):
    def __init__(self, user: discord.User):
        super().__init__(timeout=None)
        self.user = user  # Guardamos al usuario que creó el canal
        self.add_item(discord.ui.Button(label="No Verificar", style=ButtonStyle.red, custom_id="deny_verification"))
        self.add_item(discord.ui.Button(label="Verificar", style=ButtonStyle.green, custom_id="accept_verification"))

async def create_ticket(interaction: discord.Interaction):
    guild = interaction.guild
    existing_ticket_channel = discord.utils.get(guild.channels, name=f"🎫⦙{interaction.user.name}")
    if existing_ticket_channel:
        return await interaction.response.send_message("<:no:1288631410558767156> Ya tienes un ticket abierto.", ephemeral=True)

    category = guild.get_channel(TICKET_CATEGORY_ID)
    ticket_channel = await category.create_text_channel(name=f"🎫⦙{interaction.user.name}")

    await ticket_channel.set_permissions(guild.default_role, read_messages=False)
    await ticket_channel.set_permissions(interaction.user, read_messages=True, send_messages=True)
    await ticket_channel.set_permissions(guild.get_role(DAI_MEMBER_ROLE_ID), read_messages=True, send_messages=True)

    embed = tickets_embed(interaction.user)
    await ticket_channel.send(embed=embed, view=CloseTicketView())

    await interaction.response.send_message(f"<:correcto:1288631406452412428> Ticket creado: {ticket_channel.mention}", ephemeral=True)

async def verify(interaction: discord.Interaction):
    guild = interaction.guild
    existing_ticket_channel = discord.utils.get(guild.channels, name=f"✅⦙{interaction.user.name}")
    if existing_ticket_channel:
        return await interaction.response.send_message("<:no:1288631410558767156> Ya tienes un ticket de verificación abierto.", ephemeral=True)

    category = guild.get_channel(VERIFICATION_CATEGORY_ID)
    verify_channel = await category.create_text_channel(name=f"✅⦙{interaction.user.name}")

    await verify_channel.set_permissions(guild.default_role, read_messages=False)
    await verify_channel.set_permissions(interaction.user, read_messages=True, send_messages=True)
    await verify_channel.set_permissions(guild.get_role(DAI_MEMBER_ROLE_ID), read_messages=True, send_messages=True)

    embed = verification_embed(interaction.user)
    await verify_channel.send(embed=embed, view=VerificationView(interaction.user))

    await interaction.response.send_message(f"<:correcto:1288631406452412428> Canal de verificación creado: {verify_channel.mention}", ephemeral=True)

async def close_ticket(interaction: discord.Interaction):
    await interaction.channel.delete()

async def deny_verification(interaction: discord.Interaction):
    guild = interaction.guild
    support_role = guild.get_role(DAI_MEMBER_ROLE_ID)
    if support_role not in interaction.user.roles:
        return await interaction.response.send_message("<:no:1288631410558767156> No tienes permiso para usar este botón.", ephemeral=True)

    await interaction.channel.delete()

async def accept_verification(interaction: discord.Interaction):
    guild = interaction.guild
    support_role = guild.get_role(DAI_MEMBER_ROLE_ID)
    if support_role not in interaction.user.roles:
        return await interaction.response.send_message("<:no:1288631410558767156> No tienes permiso para usar este botón.", ephemeral=True)

    # Extraer el nombre del usuario del canal
    user_name = interaction.channel.name.replace("✅⦙", "")
    
    # Buscar al usuario en el servidor
    member = discord.utils.get(guild.members, name=user_name)
    if member is None:
        return await interaction.response.send_message("<:no:1288631410558767156> No se encontró al usuario correspondiente.", ephemeral=True)

    verified_role = guild.get_role(VERIFIED_ROLE_ID)
    await member.add_roles(verified_role)  # Asignar el rol al usuario encontrado
    await interaction.channel.delete()

async def handle_ticket_interaction(interaction: discord.Interaction):
    """Encapsula el manejo de interacciones relacionadas con tickets."""
    if interaction.data and interaction.data.get("custom_id"):
        custom_id = interaction.data.get("custom_id")
        if custom_id == "create_ticket":
            await create_ticket(interaction)
        elif custom_id == "verify":
            await verify(interaction)
        elif custom_id == "close_ticket":
            await close_ticket(interaction)
        elif custom_id == "deny_verification":
            await deny_verification(interaction)
        elif custom_id == "accept_verification":
            await accept_verification(interaction)

def support_and_verification(bot):
    @bot.tree.command(name="soporte_verificacion", description="Enviar el embed principal")
    @app_commands.checks.has_role(ADMIN_ROLE)
    async def send_main_embed(interaction: discord.Interaction, channel: discord.TextChannel):
        """Slash Command que envía el embed principal al canal seleccionado"""
        embed = support_and_verification_embed()
        view = TicketView()
        await channel.send(embed=embed, view=view)
        await interaction.response.send_message(f"<:correcto:1288631406452412428> Embed enviado a {channel.mention}", ephemeral=True)

    @send_main_embed.error
    async def send_main_embed_error(interaction: discord.Interaction, error):
        if isinstance(error, app_commands.MissingRole):
            await interaction.response.send_message("<:no:1288631410558767156> No tienes permisos para usar este comando.", ephemeral=True)
