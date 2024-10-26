import discord
from discord import app_commands
from discord.ui import Button, View

class PollView(View):
    def __init__(self, title, options, author_voice_channel):
        super().__init__(timeout=None)
        self.votes = {option: {'label': option, 'count': 0} for option in options}
        self.author_voice_channel = author_voice_channel
        self.title = title
        self.voted_users = set()  # Conjunto para rastrear quién ha votado

        # Crear botones para cada opción
        for option in options:
            if option.lower() == 'sí':
                button = Button(label=option, style=discord.ButtonStyle.success, custom_id=option)  # Verde
            elif option.lower() == 'no':
                button = Button(label=option, style=discord.ButtonStyle.danger, custom_id=option)  # Rojo
            else:
                button = Button(label=option, style=discord.ButtonStyle.primary, custom_id=option)  # Color por defecto
            button.callback = self.vote_callback
            self.add_item(button)


    async def vote_callback(self, interaction: discord.Interaction):
        # Verifica si el usuario está en el mismo canal de voz que el autor de la encuesta
        if interaction.user.voice and interaction.user.voice.channel.id == self.author_voice_channel.id:
            if interaction.user.id in self.voted_users:
                await interaction.response.send_message('<:no:1288631410558767156> Ya has votado en esta encuesta.', ephemeral=True)
                return  # El usuario ya votó

            option_id = interaction.data['custom_id']  # Usamos el custom_id para identificar la opción
            option_label = self.votes[option_id]['label']  # Obtiene la etiqueta de la opción
            print(f'{interaction.user} ha votado la opción: {option_label}')

            # Aumenta el voto en la opción seleccionada
            if option_id in self.votes:
                self.votes[option_id]['count'] += 1  # Aumenta el conteo de votos
                self.voted_users.add(interaction.user.id)  # Agrega el ID del usuario al conjunto
                
                # Edita el mensaje de la interacción para actualizar el embed
                await interaction.response.send_message(embed=self.create_embed())  # Envía el nuevo embed
                # Responde a la interacción que ha votado
                await interaction.followup.send(f'<:correcto:1288631406452412428> Has votado la opción: **{option_label}**', ephemeral=True)

            else:
                await interaction.response.send_message("Opción no válida.", ephemeral=True)
        else:
            await interaction.response.send_message('<:no:1288631410558767156> Debes estar en el mismo canal de voz para votar.', ephemeral=True)


    def create_embed(self):
        embed = discord.Embed(title=self.title, description='Resultados actuales de la encuesta:', color=discord.Color.blue())
        total_votes = sum(data['count'] for data in self.votes.values())

        for option_id, data in self.votes.items():
            count = data['count']
            percentage = (count / total_votes * 100) if total_votes > 0 else 0
            bar_length = 10  # Longitud de la barra de progreso
            filled_length = int(bar_length * (percentage / 100))  # Cuántos bloques llenos
            bar = '🟦' * filled_length + '⬛' * (bar_length - filled_length)  # Representación gráfica

            # Agrega el campo con la información de los votos y el porcentaje
            embed.add_field(name=f'<:chat_ind:1288628721842130976>  {data["label"]}', value=f'> {count} votos ({percentage:.1f}%) \n> {bar}', inline=False)
            embed.set_image(url='https://i.imgur.com/8GkOfv1.png')
            embed.set_footer(text='Delegación de Alumnos de Industriales - UVigo', icon_url='https://cdn.discordapp.com/emojis/1288628804276977735.webp?size=96&quality=lossless')

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
            await interaction.response.send_message('<:no:1288631410558767156> Debes estar en un canal de voz para crear una encuesta.', ephemeral=True)
            return

        # Si no se proporcionan opciones, usa opciones predeterminadas
        options = [opt for opt in [option1, option2, option3, option4, option5, 
                                   option6, option7, option8, option9, option10] if opt]
        if not options:
            options = ['Sí', 'No', 'Abstención']

        # Valida el número de opciones
        if len(options) < 2:
            await interaction.response.send_message('<:no:1288631410558767156> Debes proporcionar al menos 2 opciones para la encuesta.', ephemeral=True)
            return
        elif len(options) > 10:
            await interaction.response.send_message('<:no:1288631410558767156> Puedes proporcionar un máximo de 10 opciones para la encuesta.', ephemeral=True)
            return

        # Crea la vista de botones con opciones y la ID del canal de voz del autor
        view = PollView(title=title, options=options, author_voice_channel=interaction.user.voice.channel)

        # Crea el embed inicial con el título de la encuesta
        embed = discord.Embed(title=title, description='Resultados actuales de la encuesta:', color=discord.Color.blue())
        for option in options:
            embed.add_field(name=f'<:chat_ind:1288628721842130976>  {option}', value='> 0 votos (0.0%) \n> 🟦' + '⬛' * 9, inline=False)  # Barra inicial vacía
        embed.set_image(url='https://i.imgur.com/8GkOfv1.png')
        embed.set_footer(text='Delegación de Alumnos de Industriales - UVigo', icon_url='https://cdn.discordapp.com/emojis/1288628804276977735.webp?size=96&quality=lossless')
        # Envía el mensaje con el embed y los botones
        await interaction.response.send_message(embed=embed, view=view)


def voice_poll_cmd(bot):
    @bot.tree.command(name='voice_poll', description='Crea una encuesta en la que solo los usuarios en tu canal de voz pueden votar.')
    @app_commands.describe(title='Título de la encuesta', option1='Opción 1', option2='Opción 2', 
                        option3='Opción 3', option4='Opción 4', option5='Opción 5', 
                        option6='Opción 6', option7='Opción 7', option8='Opción 8',
                        option9='Opción 9', option10='Opción 10')
    async def voice_poll(interaction: discord.Interaction, title: str, option1: str = None, 
                        option2: str = None, option3: str = None, option4: str = None, 
                        option5: str = None, option6: str = None, option7: str = None, 
                        option8: str = None, option9: str = None, option10: str = None):
        voice_poll_cmd = VoicePollCommand(bot)
        await voice_poll_cmd.voice_poll(interaction, title, option1, option2, option3, option4, option5,
                                        option6, option7, option8, option9, option10)
