import discord
from discord import app_commands
from discord.ui import Button, View
import asyncio
from config import DAI_MEMBER_ROLE_ID

class PollView(View):
    def __init__(self, title, options, author_voice_channel, duration):
        super().__init__(timeout=duration)
        
        # Opciones y colores predefinidos
        default_options = ['Sí', 'No', 'Abstención']
        default_styles = [discord.ButtonStyle.success, discord.ButtonStyle.danger, discord.ButtonStyle.primary]

        # Usa opciones y estilos predefinidos si no se dan opciones válidas
        if not options:
            options = default_options
            styles = default_styles
        else:
            # Verifica si hay suficientes opciones
            if len(options) < 2:
                raise ValueError("Debes proporcionar al menos 2 opciones si decides personalizarlas.")
            # Todas las opciones personalizadas tendrán el color azul
            styles = [discord.ButtonStyle.primary] * len(options)

        self.votes = {option: {'label': option, 'count': 0} for option in options}
        self.author_voice_channel = author_voice_channel
        self.title = title
        self.voted_users = set()
        self.duration = duration
        self.end_time = discord.utils.utcnow().timestamp() + duration

        # Crear botones para cada opción, añadiendo índice al custom_id para evitar duplicados
        for idx, option in enumerate(options):
            style = styles[idx]  # Aplica el estilo correspondiente
            button = Button(label=option, style=style, custom_id=f"{option}_{idx}")
            button.callback = self.vote_callback
            self.add_item(button)

    async def vote_callback(self, interaction: discord.Interaction):
        # Verifica si el usuario tiene el rol requerido
        role_required_id = DAI_MEMBER_ROLE_ID
        if role_required_id not in [role.id for role in interaction.user.roles]:
            await interaction.response.send_message(f'<:no:1288631410558767156> Esta votación solo puede ser respondida por <@&{DAI_MEMBER_ROLE_ID}>.', ephemeral=True)
            return
        
        # Verifica si el usuario está en el mismo canal de voz que el autor de la encuesta
        if interaction.user.voice and interaction.user.voice.channel.id == self.author_voice_channel.id:
            if interaction.user.id in self.voted_users:
                await interaction.response.send_message('<:no:1288631410558767156> Ya has votado en esta encuesta.', ephemeral=True)
                return

            option_id = interaction.data['custom_id'].rsplit("_", 1)[0]  # Elimina el índice para obtener la opción original
            option_label = self.votes[option_id]['label']
            print(f'Encuestas: {interaction.user} ha votado la opción: {option_label}')

            # Aumenta el voto en la opción seleccionada
            if option_id in self.votes:
                self.votes[option_id]['count'] += 1
                self.voted_users.add(interaction.user.id)

                # Actualiza el embed con los nuevos resultados
                await self.message.edit(embed=self.create_embed())
                await interaction.response.send_message(f'<:correcto:1288631406452412428> Has votado la opción: **{option_label}**', ephemeral=True)
            else:
                await interaction.response.send_message("Opción no válida.", ephemeral=True)
        else:
            await interaction.response.send_message('<:no:1288631410558767156> Debes estar en el mismo canal de voz para votar.', ephemeral=True)

    def create_embed(self):
        remaining_time = max(0, int(self.end_time - discord.utils.utcnow().timestamp())) if self.end_time else None
        time_display = f'<a:online:1288631919352877097> Abierta - {remaining_time // 60}:{remaining_time % 60:02d}' if remaining_time else '<a:offline:1288631912180744205> Votación finalizada'
        total_votes = sum(data['count'] for data in self.votes.values())
        description = f'''
        ## Votación: {self.title}
        ➤ Estado: **{time_display}**
        ➤ Total de votos: **{total_votes}**
        '''
        embed = discord.Embed(description=description, color=discord.Color.blue())

        for option_id, data in self.votes.items():
            count = data['count']
            percentage = (count / total_votes * 100) if total_votes > 0 else 0
            bar_length = 13
            filled_length = int(bar_length * (percentage / 100))
            bar = '🟦' * filled_length + '⬛' * (bar_length - filled_length)
            embed.add_field(name=f'<:chat_ind:1288628721842130976>  {data["label"]}', value=f'> {count} votos ({percentage:.1f}%) \n> {bar}', inline=False)
        
        embed.set_image(url='https://i.imgur.com/8GkOfv1.png')
        embed.set_footer(text='Delegación de Alumnos de Industriales - UVigo', icon_url='https://cdn.discordapp.com/emojis/1288628804276977735.webp?size=96&quality=lossless')
        return embed

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True  # Desactiva todos los botones al finalizar la encuesta
        await self.message.edit(embed=self.create_embed(), view=self)


class VoicePollCommand:
    def __init__(self, bot):
        self.bot = bot

    async def voice_poll(self, interaction: discord.Interaction, title: str, options: str = None, duration: int = None):
        if not interaction.user.voice or not interaction.user.voice.channel:
            await interaction.response.send_message('<:no:1288631410558767156> Debes estar en un canal de voz para crear una encuesta.', ephemeral=True)
            raise ValueError("El usuario no está en un canal de voz.")

        # Valida si las opciones están duplicadas, en caso de que haya opciones
        options_list = [opt.strip() for opt in options.split(',')] if options else None
        if options_list and len(options_list) != len(set(options_list)):  # Revisa si hay duplicados
            await interaction.response.send_message('<:no:1288631410558767156> No puedes tener opciones duplicadas en la encuesta.', ephemeral=True)
            raise ValueError("Opciones duplicadas en la encuesta.")

        # Valida que la duración sea positiva
        if not duration or duration <= 0:
            await interaction.response.send_message('<:no:1288631410558767156> Debes proporcionar una duración válida para la encuesta.', ephemeral=True)
            raise ValueError("Duración de la encuesta no válida.")

        # Crea la vista de botones con opciones y el canal de voz del autor
        view = PollView(title=title, options=options_list, author_voice_channel=interaction.user.voice.channel, duration=duration)

        # Crea el embed inicial con el título de la encuesta y tiempo restante
        embed = view.create_embed()
        
        await interaction.response.defer()  # Defer para evitar timeout en la respuesta inicial
        try: 
            message = await interaction.followup.send(embed=embed, view=view)
            print(f'Encuestas: {interaction.user} ha creado una encuesta en el canal de voz {interaction.user.voice.channel}:\n-Título: {title}\n-Opciones: {"Sí, No, Abstención" if options == None else options}\n-Duración: {duration}s')
            view.message = message  # Guarda el mensaje en la vista para que pueda actualizarse
        except discord.HTTPException:
            await interaction.response.send_message('<:no:1288631410558767156> Ocurrió un error al enviar la encuesta.', ephemeral=True)
            raise ValueError("Error al enviar la encuesta.")
        # Actualizar el contador de tiempo mientras la encuesta está abierta
        while discord.utils.utcnow().timestamp() < view.end_time:
            await asyncio.sleep(1)  # Ahora se actualiza cada segundo
            remaining_time = max(0, int(view.end_time - discord.utils.utcnow().timestamp()))
            if remaining_time <= 0:
                break
            await view.message.edit(embed=view.create_embed())
        
        # Finaliza la encuesta cuando se acabe el tiempo
        await view.on_timeout()


def voice_poll_cmd(bot): # COMANDO
    @bot.tree.command(name='dai_voz_votacion', description='Crea una encuesta en la que solo los usuarios en tu canal de voz pueden votar.')
    @app_commands.describe(
        titulo='Título de la encuesta',
        opciones='Opciones de la encuesta, separadas por comas (Ejemplo: Sí, No, Tal vez)',
        duracion='Duración de la encuesta en segundos (obligatoria)'
    )
    @app_commands.checks.has_role(DAI_MEMBER_ROLE_ID)
    async def voice_poll(interaction: discord.Interaction, titulo: str, duracion: int, opciones: str = None):
        voice_poll_cmd = VoicePollCommand(bot)
        await voice_poll_cmd.voice_poll(interaction, titulo, opciones, duracion)

    @voice_poll.error
    async def voice_poll_error(interaction: discord.Interaction, error):
        if isinstance(error, app_commands.MissingRole):
            await interaction.response.send_message("<:no:1288631410558767156> No tienes permisos para usar este comando.", ephemeral=True)