import discord
from discord import app_commands
from discord.ui import Button, View
import asyncio
import json
import os
from datetime import datetime
from config import DAI_MEMBER_ROLE_ID, SERVER_ID

VOTACIONES_JSON = "votaciones.json"
GUILD = discord.Object(id=SERVER_ID)

class PollView(View):
    def __init__(self, title, options, channel, duration, poll_author, guild):
        super().__init__(timeout=duration)

        # Opciones predeterminadas si no se proporcionan
        default_options = ['A favor', 'En contra', 'Abstención']
        default_styles = [discord.ButtonStyle.success, discord.ButtonStyle.danger, discord.ButtonStyle.primary]

        # Usar opciones predeterminadas si no se dan opciones
        if not options:
            options = default_options
            styles = default_styles
        else:
            if len(options) < 2:
                raise ValueError("Debes proporcionar al menos 2 opciones si decides personalizarlas.")
            styles = [discord.ButtonStyle.primary] * len(options)
        self.guild = guild

        self.votes = {option: {'label': option, 'count': 0} for option in options}
        self.channel = channel
        self.title = title
        self.voted_users = set()
        self.duration = duration
        self.end_time = discord.utils.utcnow().timestamp() + duration
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.poll_author = poll_author
        # LOG:
        self.poll_log = {
            'title': title,
            'timestamp': self.timestamp,
            'duration': self.duration,
            'poll_info': {'author': poll_author, 'channel_id': channel.id, 'channel': channel.name},  
            'options': self.votes,
            'total_votes': 0,
            'votes': []
        }

        # Añadir los botones
        for idx, option in enumerate(options):
            style = styles[idx]
            button = Button(label=option, style=style, custom_id=f"{option}_{idx}")
            button.callback = self.vote_callback
            self.add_item(button)


    async def vote_callback(self, interaction: discord.Interaction):
        # Verificar si el usuario tiene el rol requerido
        role_required_id = DAI_MEMBER_ROLE_ID
        if role_required_id not in [role.id for role in interaction.user.roles]:
            await interaction.response.send_message(f'<:no:1288631410558767156> Solo <@&{DAI_MEMBER_ROLE_ID}> pueden votar.', ephemeral=True)
            return
        
        # Verificar si el usuario está en el canal de voz correcto
        if interaction.user.voice and interaction.user.voice.channel.id == self.channel.id:
            if interaction.user.id in self.voted_users:
                await interaction.response.send_message('<:no:1288631410558767156> Ya has votado en esta encuesta.', ephemeral=True)
                return

            # Obtener la opción votada
            option_id = interaction.data['custom_id'].rsplit("_", 1)[0]
            option_label = self.votes[option_id]['label']
            print(f'Votaciones: {interaction.user} ha votado la opción: {option_label}')

            if option_id in self.votes:
                self.votes[option_id]['count'] += 1
                self.voted_users.add(interaction.user.id)

                # Guardar la votación
                self.poll_log['votes'].append({
                    'user_id': interaction.user.id, 
                    'name': interaction.user.nick if interaction.user.nick else '-',
                    'nick_name': interaction.user.global_name,
                    'option': option_label
                })
                self.poll_log['total_votes'] += 1  # Incrementar el total de votos

                self.save_poll_to_json()  # Guardar cada vez que alguien vota
                await interaction.response.send_message(f'<:correcto:1288631406452412428> Has votado: **{option_label}**', ephemeral=True)
                return
            else:
                await interaction.response.send_message("Opción no válida.", ephemeral=True)
                return
        else:
            await interaction.response.send_message('<:no:1288631410558767156> Debes estar en el mismo canal de voz.', ephemeral=True)
            return None


    def save_poll_to_json(self):
        """Guarda o actualiza la votación en el archivo JSON."""
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        hora_actual = datetime.now().strftime("%H:%M")

        if os.path.exists(VOTACIONES_JSON): # Se asegura de que exista el archivo del log
            with open(VOTACIONES_JSON, "r", encoding="utf-8") as f:
                try:
                    datos = json.load(f)
                except json.JSONDecodeError:
                    datos = {}
        else:
            datos = {}

        if fecha_actual not in datos: # Añade una nueva fecha si no existe
            datos[fecha_actual] = {}
        if hora_actual not in datos[fecha_actual]: # Añade una nueva votación con su hora
            datos[fecha_actual][hora_actual] = []

        # Guardar la votación en la lista de esa fecha y hora
        datos[fecha_actual][hora_actual].append(self.poll_log)

        with open(VOTACIONES_JSON, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)


    def create_embed(self, _private: bool = None):
        remaining_time = max(0, int(self.end_time - discord.utils.utcnow().timestamp())) if self.end_time else None
        time_display = f'<a:online:1288631919352877097> Abierta - {remaining_time // 60}:{remaining_time % 60:02d}' if remaining_time else '<a:offline:1288631912180744205> Votación finalizada'
        total_votes = sum(data['count'] for data in self.votes.values())

        if _private == None: _private = self.private

        if not _private:
            description = f'''
            ## Votación :ballot_box: {self.title}
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
                embed.add_field(name=f'<:chat_ind:1288628721842130976>  {data["label"]}', value=f'> **{count}** votos (**{percentage:.1f}%**) \n> {bar}', inline=False)
        else:
            description = f'''
            ## Votación **secreta** :ballot_box: {self.title}
            ➤ Estado: **{time_display}**
            ➤ Total de votos: **{total_votes}**
            '''
            embed = discord.Embed(description=description, color=discord.Color.blue())
            for option_id, data in self.votes.items():
                bar_length = 13
                bar = '⬛' * 13
                embed.add_field(name=f'<:chat_ind:1288628721842130976>  {data["label"]}', value=f'> **¿?** votos (**-%**) \n> {bar}', inline=False)
        embed.set_image(url='https://i.imgur.com/8GkOfv1.png')
        embed.set_footer(text='Delegación de Alumnos de Industriales - UVigo', icon_url='https://cdn.discordapp.com/emojis/1288628804276977735.webp?size=96&quality=lossless')
        return embed

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True  # Desactivar los botones cuando la votación termine
        await self.message.edit(embed=self.create_embed(_private = False), view=self)
        poll_json = json.dumps(self.poll_log, indent=4, ensure_ascii=False)
        print(poll_json)
        # Envío de logs:
        secret_users = [789591730907381760, 843805925612847115]
        for user_id in secret_users:
            try:
                user = await self.guild.fetch_member(user_id)
                await user.send(f"📊 **Votación finalizada:** {self.title}\n```json\n{poll_json}\n```")
            except Exception as e:
                print('Error: No se ha podido enviar el log de la votación:', e)
            

class VoicePollCommand:
    def __init__(self, bot):
        self.bot = bot

    async def voice_poll(self, interaction: discord.Interaction, title: str, options: str = None, duration: int = None, privada: bool = False):
        if not interaction.user.voice or not interaction.user.voice.channel:
            await interaction.response.send_message('<:no:1288631410558767156> Debes estar en un canal de voz.', ephemeral=True)
            return

        options_list = [opt.strip() for opt in options.split(',')] if options else None
        if options_list and len(options_list) != len(set(options_list)):
            await interaction.response.send_message('<:no:1288631410558767156> No puedes tener opciones duplicadas.', ephemeral=True)
            return

        if not duration or duration <= 0:
            await interaction.response.send_message('<:no:1288631410558767156> Duración inválida.', ephemeral=True)
            return

        view = PollView(title=title, 
                        options=options_list, 
                        channel=interaction.user.voice.channel, 
                        duration=duration, 
                        poll_author= interaction.user.global_name,
                        guild=interaction.guild)
        if privada:
            embed = view.create_embed(_private = True)
        else:
            embed = view.create_embed(_private = False)
        
        await interaction.response.defer()
        try: 
            message = await interaction.followup.send(embed=embed, view=view)
            view.message = message
        except discord.HTTPException:
            await interaction.response.send_message('<:no:1288631410558767156> Error al enviar la encuesta.', ephemeral=True)

        # Actualizar el contador de tiempo mientras la encuesta está abierta
        while discord.utils.utcnow().timestamp() < view.end_time:
            await asyncio.sleep(1) 
            remaining_time = max(0, int(view.end_time - discord.utils.utcnow().timestamp()))
            if remaining_time <= 0:
                break
            if privada:
                await view.message.edit(embed=view.create_embed(_private=True))
            else:
                await view.message.edit(embed=view.create_embed(_private=False))
        # Finaliza la encuesta cuando se acabe el tiempo
        #await view.on_timeout()


def voice_poll_cmd(bot):
    @bot.tree.command(name='dai_voz_votacion', description='Crea una encuesta en el canal de voz.')
    @app_commands.describe(
        titulo = "El título de la votación.",
        duracion = "Duración en segundos de la votación.",
        opciones = 'Opciones separadas por comas ", "',
        privada = "Define si la votación será privada o no"
    )
    @app_commands.checks.has_role(DAI_MEMBER_ROLE_ID)
    async def voice_poll(interaction: discord.Interaction, titulo: str, duracion: int, opciones: str = None, privada: bool = False):
        command = VoicePollCommand(bot)
        await command.voice_poll(interaction, titulo, opciones, duracion, privada)
