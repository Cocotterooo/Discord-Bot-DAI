import os
import asyncio
import discord
from discord import app_commands
from dotenv import load_dotenv

# Utilidades y módulos personalizados
from utils.welcome_image import generate_welcome_image
from utils.api.instagram.Instagram import InstagramAPI
from utils.db.authentication import supabase_autenticated
from utils.periodic_tasks.autoupdate_messages import (
    renew_all_likes_comments_task,
    renew_media_url_task,
    check_new_post_task,
)
from utils.db.Posts import Post
from utils.db.Discord_instagram_messsage import Dc_insta_msg
from utils.interactions.instagram_commands import instagram_send_command
from utils.interactions.dai_roles import dai_roles_interaction, dai_roles
from utils.interactions.interactive_voice_channel import (
    voice_channel_creator,
    create_or_update_channel,
    monitor_channel_activity,
    resume_channel_monitoring,
)
from utils.interactions.private_poll import voice_poll_cmd
from utils.interactions.support_and_verification import (
    support_and_verification,
    handle_ticket_interaction,
)
from utils.interactions.asociations import (
    nuevo_spacelab,
    eliminar_spacelab,
    nuevo_motorsport,
    eliminar_motorsport,
    nuevo_ces,
    eliminar_ces,
    setup_spacelab,
    setup_motorsport,
    setup_ces,
    nuevo_ceeibis,
    eliminar_ceeibis,
    setup_ceeibis,
)
from config import (
    SERVER_ID,
    LOG_CHANNEL,
    WELCOME_CHANNEL,
    INSTAGRAM_DAI_CHANNEL,
    ADMIN_ROLE,
    linktree_embed,
    voice_channel_creator_embed,
)

# Cargar el archivo .env
load_dotenv()

# Crear instancias necesarias
TOKEN = os.getenv("DISCORD_TOKEN")
MY_GUILD = discord.Object(id=SERVER_ID)

DB_URL = os.getenv("DB_URL")
DB_API_KEY = os.getenv("DB_API_KEY")
DB_EMAIL = os.getenv("DB_EMAIL")
DB_EMAIL_PASSWORD = os.getenv("DB_EMAIL_PASSWORD")
supabase = supabase_autenticated(DB_URL, DB_API_KEY, DB_EMAIL, DB_EMAIL_PASSWORD)

INSTAGRAM_API_KEY = os.getenv("INSTAGRAM_API_KEY")
instagram = InstagramAPI(INSTAGRAM_API_KEY)
posts = Post(supabase, instagram)


class Bot(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        dai_roles(self)
        instagram_send_command(
            self, supabase, instagram, dc_insta_msg, INSTAGRAM_DAI_CHANNEL, ADMIN_ROLE
        )
        voice_channel_creator(self, ADMIN_ROLE, voice_channel_creator_embed())
        voice_poll_cmd(self)
        support_and_verification(self)
        nuevo_ceeibis(self)
        eliminar_ceeibis(self)
        nuevo_spacelab(self)
        eliminar_spacelab(self)
        nuevo_motorsport(self)
        eliminar_motorsport(self)
        nuevo_ces(self)
        eliminar_ces(self)
        setup_spacelab(self)
        setup_motorsport(self)
        setup_ces(self)
        setup_ceeibis(self)
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)


intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.guilds = True
client = Bot(intents=intents)

dc_insta_msg = Dc_insta_msg(supabase, client, instagram)


@client.event
async def on_ready():
    print(f"Bot conectado como {client.user}")
    await resume_channel_monitoring(client, supabase)
    asyncio.create_task(
        renew_all_likes_comments_task(posts, 3600, client, supabase, INSTAGRAM_DAI_CHANNEL)
    )
    asyncio.create_task(renew_media_url_task(posts, 86400))
    asyncio.create_task(check_new_post_task(instagram, posts, dc_insta_msg, 3600))


@client.event
async def on_interaction(interaction: discord.Interaction):
    await dai_roles_interaction(interaction)

    if interaction.data and interaction.data.get("custom_id"):
        custom_id = interaction.data["custom_id"]
        ticket_related_ids = [
            "create_ticket",
            "verify",
            "close_ticket",
            "deny_verification",
            "accept_verification",
        ]
        if custom_id in ticket_related_ids:
            await handle_ticket_interaction(interaction)
        await create_or_update_channel(client, supabase, interaction)


@client.event
async def on_member_join(member: discord.Member):
    print(f"{member} se ha unido al servidor")
    avatar_url = member.avatar.url if member.avatar else member.default_avatar.url
    nombre_usuario = member.name

    channel = client.get_channel(WELCOME_CHANNEL)
    image_binary = generate_welcome_image(
        nombre_usuario, avatar_url, "assets/tema_spp.png"
    )
    if image_binary is None:
        print(f"Ocurrió un error al generar la imagen de Bienvenida de {nombre_usuario}")
    else:
        await channel.send(file=discord.File(fp=image_binary, filename="bienvenida.png"))
        await channel.send(
            f"<:entrar:1288631392070012960> {member.mention} ¡Bienvenid@ a la "
            "**Comunidad Oficial** de la **EEI**! 🎉 \n"
            "> <:verificado:1288628715982553188> Si eres estudiante en la **EEI verifica tu cuenta** en "
            "<#1299775062215229460>\n-#       **Delegación de Alumnos** EEI - Uvigo"
        )


@client.tree.command(name="bienvenida", description="Imagen de Bienvenida")
@app_commands.checks.has_role(ADMIN_ROLE)
async def welcome(interaction: discord.Interaction):
    avatar_url = interaction.user.avatar.url
    nombre_usuario = interaction.user.name

    channel = client.get_channel(WELCOME_CHANNEL)
    image_binary = generate_welcome_image(
        nombre_usuario, avatar_url, "assets/tema_spp.png"
    )
    if image_binary is None:
        print(f"Ocurrió un error al generar la imagen de Bienvenida de {nombre_usuario}")
    else:
        await channel.send(file=discord.File(fp=image_binary, filename="bienvenida.png"))
        await channel.send(
            f"<:entrar:1288631392070012960> ¡Bienvenid@ a la **Comunidad Oficial** de la "
            "**EEI**! 🎉\n-#       **Delegación de Alumnos** EEI - Uvigo"
        )


@client.tree.command(
    name="rss",
    description="Muestra las redes sociales y la web de la Delegación de Alumnos de Industriales",
)
async def web(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True)
    await interaction.followup.send(embed=linktree_embed(), ephemeral=False)


client.run(TOKEN)
