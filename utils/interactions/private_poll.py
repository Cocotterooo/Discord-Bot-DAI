import discord
from discord import app_commands
from discord.ui import Button, View

import discord
from discord import app_commands
from discord.ui import Button, View

class PollView(View):
    def __init__(self, title, options, author_voice_channel):
        super().__init__(timeout=None)
        self.votes = {option: 0 for option in options}  # Diccionario de votos
        self.author_voice_channel = author_voice_channel  # Canal de voz del autor de la encuesta
        self.title = title

        # Crear botones para cada opción
        for option in options:
            button = Button(label=option, style=discord.ButtonStyle.primary, custom_id=f"vote_{option}")
            button.callback = self.vote_callback
            self.add_item(button)

    async def vote_callback(self, interaction: discord.Interaction):
        # Verifica si el usuario está en el mismo canal de voz que el autor de la encuesta
        if interaction.user.voice and interaction.user.voice.channel.id == self.author_voice_channel.id:
            self.votes[interaction.component.label] += 1  # Aumenta el voto en la opción seleccionada
            await interaction.response.edit_message(embed=self.create_embed())  # Actualiza el embed
        else:
            await interaction.response.send_message("❌ Debes estar en el mismo canal de voz para votar.", ephemeral=True)

    def create_embed(self):
        embed = discord.Embed(title=self.title, description="Resultados actuales de la encuesta:", color=0x3498db)
        for option, count in self.votes.items():
            embed.add_field(name=option, value=f"{count} votos", inline=False)
        return embed


class VoicePollCommand:
    def __init__(self, bot):
        self.bot = bot

    async def voice_poll(self, interaction: discord.Interaction, title: str, option1: str = None, 
                         option2: str = None, option3: str = None, option4: str = None, 
                         option5: str = None, option6: str = None, option7: str = None, 
                         option8: str = None, option9: str = None, option10: str = None):
        
        # Verifica si el usuario está en un canal de voz
        if not interaction.user.voice or not interaction.user.voice.channel:
            await interaction.response.send_message("❌ Debes estar en un canal de voz para crear una encuesta.", ephemeral=True)
            return

        # Si no se proporcionan opciones, usa opciones predeterminadas
        options = [opt for opt in [option1, option2, option3, option4, option5, 
                                   option6, option7, option8, option9, option10] if opt]
        if not options:
            options = ["Sí", "No", "Abstención"]

        # Valida el número de opciones
        if len(options) < 3:
            await interaction.response.send_message("❌ Debes proporcionar al menos 3 opciones para la encuesta.", ephemeral=True)
            return
        elif len(options) > 10:
            await interaction.response.send_message("❌ Puedes proporcionar un máximo de 10 opciones para la encuesta.", ephemeral=True)
            return

        # Crea la vista de botones con opciones y la ID del canal de voz del autor
        view = PollView(title=title, options=options, author_voice_channel=interaction.user.voice.channel)

        # Crea el embed inicial con el título de la encuesta
        embed = discord.Embed(title=title, description="Resultados actuales de la encuesta:", color=0x3498db)
        for option in options:
            embed.add_field(name=option, value="0 votos", inline=False)

        # Envía el mensaje con el embed y los botones
        await interaction.response.send_message(embed=embed, view=view)



def voice_poll_cmd(bot):
    @bot.tree.command(name="voice_poll", description="Crea una encuesta en la que solo los usuarios en tu canal de voz pueden votar.")
    @app_commands.describe(title="Título de la encuesta", option1="Opción 1", option2="Opción 2", 
                        option3="Opción 3", option4="Opción 4", option5="Opción 5", 
                        option6="Opción 6", option7="Opción 7", option8="Opción 8",
                        option9="Opción 9", option10="Opción 10")
    async def voice_poll(interaction: discord.Interaction, title: str, option1: str = None, 
                        option2: str = None, option3: str = None, option4: str = None, 
                        option5: str = None, option6: str = None, option7: str = None, 
                        option8: str = None, option9: str = None, option10: str = None):
        voice_poll_cmd = VoicePollCommand(bot)
        await voice_poll_cmd.voice_poll(interaction, title, option1, option2, option3, option4, option5,
                                        option6, option7, option8, option9, option10)