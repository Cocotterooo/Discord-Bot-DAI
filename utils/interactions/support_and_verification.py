import discord
from discord.ext import commands
from discord import ButtonStyle, Interaction, ui, app_commands

from config import TICKET_CATEGORY_ID, VERIFICATION_CATEGORY_ID, DAI_MEMBER_ROLE_ID, VERIFIED_ROLE_ID, tickets_embed, verification_embed, support_and_verification_embed

class TicketView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        # Crear botones manualmente
        buttons_options = ['📩 Crea un Ticket', '☑️ Verifícate']
        for option in buttons_options:
            if option.startswith("📩"):
                button = discord.ui.Button(label=option, style=ButtonStyle.blurple, custom_id="create_ticket")
                button.callback = self.create_ticket  # Asignar el callback
            elif option.startswith("☑️"):
                button = discord.ui.Button(label=option, style=ButtonStyle.green, custom_id="verify")
                button.callback = self.verify  # Asignar el callback
            
            self.add_item(button)

    async def create_ticket(self, interaction: Interaction):
        guild = interaction.guild  # Accedemos al servidor desde la interacción

        # Comprueba si ya tiene un ticket abierto:
        existing_ticket_channel = discord.utils.get(guild.channels, name=f"🎫⦙{interaction.user.name}")
        if existing_ticket_channel:
            return await interaction.response.send_message("<:no:1288631410558767156> Ya tienes un ticket abierto.", ephemeral=True)

        category = guild.get_channel(TICKET_CATEGORY_ID)
        ticket_channel = await category.create_text_channel(name=f"🎫⦙{interaction.user.name}")

        await ticket_channel.set_permissions(guild.default_role, read_messages=False)
        await ticket_channel.set_permissions(interaction.user, read_messages=True, send_messages=True)
        await ticket_channel.set_permissions(guild.get_role(DAI_MEMBER_ROLE_ID), read_messages=True, send_messages=True)

        embed = tickets_embed(interaction.user)
        
        # Crear vista para el cierre del ticket
        close_button_view = CloseTicketView()
        await ticket_channel.send(embed=embed, view=close_button_view)

        await interaction.response.send_message(f"<:correcto:1288631406452412428> Ticket creado: {ticket_channel.mention}", ephemeral=True)

    async def verify(self, interaction: Interaction):
        guild = interaction.guild  # Accedemos al servidor desde la interacción

        # Comprueba si ya tiene un ticket de verificación abierto:
        existing_ticket_channel = discord.utils.get(guild.channels, name=f"🛡️⦙{interaction.user.name}")
        if existing_ticket_channel:
            return await interaction.response.send_message("<:no:1288631410558767156> Ya tienes un ticket de verificación abierto.", ephemeral=True)
        
        category = guild.get_channel(VERIFICATION_CATEGORY_ID)
        verify_channel = await category.create_text_channel(name=f"🛡️⦙{interaction.user.name}")

        await verify_channel.set_permissions(guild.default_role, read_messages=False)
        await verify_channel.set_permissions(interaction.user, read_messages=True, send_messages=True)
        await verify_channel.set_permissions(guild.get_role(DAI_MEMBER_ROLE_ID), read_messages=True, send_messages=True)

        embed = verification_embed(interaction.user)
        
        # Crear vista para la verificación
        verification_view = VerificationView(interaction.user)
        await verify_channel.send(embed=embed, view=verification_view)

        await interaction.response.send_message(f"<:correcto:1288631406452412428> Canal de verificación creado: {verify_channel.mention}", ephemeral=True)

class CloseTicketView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        # Crear el botón de cerrar ticket manualmente
        close_button = discord.ui.Button(label="Cerrar Ticket", style=ButtonStyle.red, custom_id="close_ticket")
        close_button.callback = self.close_ticket  # Asignar el callback
        self.add_item(close_button)

    async def close_ticket(self, interaction: Interaction):
        await interaction.channel.delete()

class VerificationView(ui.View):
    def __init__(self, user: discord.User):
        super().__init__(timeout=None)
        self.user = user

        # Crear botones de verificación manualmente
        buttons_options = ['No Verificar', 'Verificar']
        for option in buttons_options:
            if option == 'No Verificar':
                button = discord.ui.Button(label=option, style=ButtonStyle.red, custom_id="deny_verification")
                button.callback = self.deny_verification  # Asignar el callback
            elif option == 'Verificar':
                button = discord.ui.Button(label=option, style=ButtonStyle.green, custom_id="accept_verification")
                button.callback = self.accept_verification  # Asignar el callback
            
            self.add_item(button)

    async def deny_verification(self, interaction: Interaction):
        guild = interaction.guild  # Accedemos al servidor
        support_role = guild.get_role(DAI_MEMBER_ROLE_ID)
        if support_role not in interaction.user.roles:
            return await interaction.response.send_message("<:no:1288631410558767156> No tienes permiso para usar este botón.", ephemeral=True)
        
        await interaction.channel.delete()

    async def accept_verification(self, interaction: Interaction):
        guild = interaction.guild  # Accedemos al servidor
        support_role = guild.get_role(DAI_MEMBER_ROLE_ID)
        if support_role not in interaction.user.roles:
            return await interaction.response.send_message("<:no:1288631410558767156> No tienes permiso para usar este botón.", ephemeral=True)

        verified_role = guild.get_role(VERIFIED_ROLE_ID)
        await self.user.add_roles(verified_role)
        await interaction.channel.delete()

def support_and_verification(bot):
    @bot.tree.command(name="soporte_verificacion", description="Enviar el embed principal")
    @app_commands.checks.has_role(DAI_MEMBER_ROLE_ID)
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
