import discord

SERVER_ID = 1288206483091361885
INSTAGRAM_DAI_ACCOUNT_URL = "https://www.instagram.com/dai_uvigo/"
WEB_DAI_URL = "https://dai.uvigo.gal/"

# CHANNELS:
DAI_ROLES_CHANNEL_ID = 1292469145388191834
LOG_CHANNEL = 1290404101108269169
WELCOME_CHANNEL = 1288283913181200446
INSTAGRAM_DAI_CHANNEL = 1288210585632112743
TICKET_CATEGORY_ID = 1299777296714174555
VERIFICATION_CATEGORY_ID = 1299777625421774979

# ROLES:
ID_INFRAESTRUCTURAS = 1292466487247896699
ID_COMUNICACION = 1292466863707521167
ID_ASUNTOS_EXTERIORES = 1292466970687442984
ID_DEPORTES = 1292468137845067776
ADMIN_ROLE = 1288552528484630598
DAI_MEMBER_ROLE_ID = 1288206919118618839
DAI_TUTORING_ROLE_ID = 1288553111119462451
VERIFIED_ROLE_ID = 1299781091451867146

# Asociaciones:
ASOCIATION_ROLE_IDS = {
    'ceeibis': {
        'coord': 1314547388006006814,
        'member': 1314547662036664390
        },
    'spacelab': {
        'coord': 1300181833081950299, 
        'member': 1300181978166988860
        },
    'motorsport': {
        'coord': 1300184532200329339, 
        'member': 1300184607786012732
        },
    'ces': {
        'coord': 1300184021615247380, 
        'member': 1300184160068964403
        }
}
ASOCIATION_COMMANDS = {
    'ceeibis': {
        'nuevo': '/nuevo_ceeibis',
        'eliminar': '/eliminar_ceeibis',
        },
    'spacelab': {
        'nuevo': '/nuevo_spacelab',
        'eliminar': '/eliminar_spacelab',
        },
    'motorsport': {
        'nuevo': '/nuevo_motorsport',
        'eliminar': '/eliminar_motorsport',
        },
    'ces': {
        'nuevo': '/nuevo_ces',
        'eliminar': '/eliminar_ces',
        },
    }
ASOCIATION_CHANNELS = {
    'spacelab': 1300183021416349788,
    'motorsport': 1288508046057930804,
    'ces': 1300189175747842068,
}


def dai_color() -> discord.Color:
    return discord.Color.from_str('#00ACE2')


def instagram_embed(permalink: str, likes: int, comments: int, post_id: int, date_published: str, caption: str = '', media_url: str = ''):
    formatted_caption = '> ' + caption.replace('\n', '\n> ')
    # Crear un objeto Embed
    embed = discord.Embed(
        description=f'''
        ## <a:flecha:1290411623802208257> [¡Nueva Publicación de Insta!]({permalink})
        {formatted_caption}

        🔗 [**Nuestro Instagram**]({INSTAGRAM_DAI_ACCOUNT_URL}) **@dai_uvigo**
        🔗 [**Publicación**]({permalink})

        ❤️ {likes} | 💬 {comments}
        ''',
        color=dai_color()  # Color del borde del embed
    )
    embed.set_image(url=media_url)
    embed.set_footer(text=f"ID: {post_id} - {date_published}\nDelegación de Alumnos de Industriales - UVigo")
    return embed

def dai_roles_embed():
    embed = discord.Embed(
        description='''
        ## <a:flecha:1290411623802208257> Selecciona o solicita tus roles.
        **Selecciona**, **elimina** o **solicita** los roles que pertenezcan a las **funciones que desempeñas** en la **Delegación de Alumnos de Industriales**. Si tienes dudas, contacta con <@&1288552528484630598>.
        
        ### <:escudo:1288628696391090299> Directiva:
        > <@&1292466209165414411> 
        > <@&1292466392439722016> 
        > <@&1292467283284852888> 
        > <@&1292467186320805948> 
        ### <:escudo:1288628696391090299> Directiva Extendida:
        > <@&1292472596146815037> 
        > <@&1296745099497312267> 
        > <@&1299901349994954794> 
        > <@&1299901080745934888> 
        ### <:us:1288631396364976128> Comisiones Delegadas:
        > <@&1292466487247896699>
        > <@&1292466970687442984>
        > <@&1292468137845067776>
        > <@&1292466863707521167>
        ### <:exclamacion:1288628819548176514> Especiales:
        > <@&1288552528484630598> <:desarrollador:1288628718423638037>
        > <@&1288206919118618839> <:moderador:1288628804276977735>
        > <@&1288553111119462451>
        ### Selección:
        ''',
        color=dai_color()
    )
    embed.add_field(name="<:verificado:1288628715982553188> Roles Especiales", value="Para obtener un rol de las secciones **Directiva**, **Directiva Extendida** o **Especiales**, contacta con <@&1288552528484630598>.", inline=False)
    embed.add_field(name="<:verificado:1288628715982553188> Comisiones Delegadas", value="Para **obtener** o **eliminar** un rol de una Comisión Delegada solo haz click en los botones.", inline=False)
    embed.set_image(url='https://i.imgur.com/8GkOfv1.png')
    embed.set_footer(text='Delegación de Alumnos de Industriales - UVigo', icon_url='https://cdn.discordapp.com/emojis/1288628804276977735.webp?size=96&quality=lossless')
    return embed


def voice_channel_creator_embed() -> discord.Embed:
    embed = discord.Embed(
        description='''
        ## <a:flecha:1290411623802208257> ¡Crea tu Sala de Voz!
        **Crea** un canal de voz personalizado para **trabajar**, **estudiar** o **jugar** con tus amigos; solo **elige** la cantidad de usuarios que podrán unirse a tu canal y **listo**. 
        
        ### <:moderador:1288628804276977735> Detalles:
        ''',
        color=dai_color()
    )
    embed.add_field(name="<:info:1288631394502709268> Crear un canal de Voz:", value="> Para crear un canal, solo pulsa uno de los botones de debajo, estos marcan la cantidad de usuarios que podrán unirse a él.", inline=True)
    embed.add_field(name="<:info:1288631394502709268> Cambiar límite de usuarios:", value="> Si ya has creado un canal de voz y quieres cambiar el límite de usuarios del mismo, solo selecciona la cantidad que desees en los botones de debajo", inline=True)
    embed.add_field(name="<:exclamacion:1288628819548176514> Límite de canales:", value="> Cada usuario puede crear un solo canal de voz, este canal desaparecerá si permanece **inactivo durante 15 minutos**, cuando aparezca con el símbolo `🔇` significará que quedan menos de **5 minutos para desaparecer** si este no se vuelve a utilizar.", inline=False)
    embed.set_image(url='https://i.imgur.com/8GkOfv1.png')
    embed.set_footer(text='Delegación de Alumnos de Industriales - UVigo', icon_url='https://cdn.discordapp.com/emojis/1288628804276977735.webp?size=96&quality=lossless')
    return embed

def linktree_embed() -> discord.Embed:
    embed = discord.Embed(
        description=f'''
        ## <a:flecha:1290411623802208257> ¡Visita nuestra web y Redes Sociales!
        ### 🔗 [**Nuestra Página Web**]({WEB_DAI_URL}) `{WEB_DAI_URL}`
        ### 🔗 [**Nuestro Instagram**]({INSTAGRAM_DAI_ACCOUNT_URL}) **@dai_uvigo**
        ''',
        color=dai_color()
    )
    embed.set_image(url='https://i.imgur.com/8GkOfv1.png')
    embed.set_footer(text='Delegación de Alumnos de Industriales - UVigo', icon_url='https://cdn.discordapp.com/emojis/1288628804276977735.webp?size=96&quality=lossless')
    return embed


def support_and_verification_embed() -> discord.Embed:
    embed = discord.Embed(
        description=f'''
        # <:dai:1288623399672741930> Soporte y Verificación
        ## 🎫 Crea un Ticket para recibir **ayuda** de la administración.
        > Una vez creado, **descríbenos tu duda o **problema** para que podamos asistirte de manera adecuada.
        >  
        > Nos esforzaremos por ayudarte lo antes posible.
        ## <:verificado:1288628715982553188> Verifica tu cuenta para acceder a todos los canales del servidor.
        > Para obtener **acceso** a **eventos** exclusivos de la **EEI**, así como a **canales privados** y de **apuntes**, **verifica que eres estudiante de la EEI** enviándonos tu **matrícula** o una captura de **Moovi**.
        >  
        > Procesaremos tu verificación a la mayor brevedad posible.
        ''',
        color=dai_color()
    )
    embed.set_image(url='https://i.imgur.com/8GkOfv1.png')
    embed.set_footer(text='Delegación de Alumnos de Industriales - UVigo', icon_url='https://cdn.discordapp.com/emojis/1288628804276977735.webp?size=96&quality=lossless')
    return embed


def tickets_embed(user: discord.User) -> discord.Embed:
    embed = discord.Embed(
        description=f'''
        ## <:info:1288631394502709268> ¡Bienvenido al Soporte {user.mention}!
        ### Te atenderá un miembro de la DAI lo antes posible.
        Por favor, cuéntanos tu problema o duda para que podamos ayudarte.
        ''',
        color=dai_color()
    )
    embed.set_image(url='https://i.imgur.com/8GkOfv1.png')
    embed.set_footer(text='Delegación de Alumnos de Industriales - UVigo', icon_url='https://cdn.discordapp.com/emojis/1288628804276977735.webp?size=96&quality=lossless')
    return embed


def verification_embed(user: discord.User) -> discord.Embed:
    embed = discord.Embed(
        description=f'''
        ## <:verificado:1288628715982553188> ¡Hola {user.mention}!
        ### ¡Para que podamos verificarte necesitamos pruebas!
        Por favor, envíanos tu **matrícula** o una captura de pantalla de **Moovi** que confirme que eres estudiante en la **EEI**.
        ''',
        color=dai_color()
    )
    embed.set_image(url='https://i.imgur.com/8GkOfv1.png')
    embed.set_footer(text='Delegación de Alumnos de Industriales - UVigo', icon_url='https://cdn.discordapp.com/emojis/1288628804276977735.webp?size=96&quality=lossless')
    return embed



def ceeibis_info_embed() -> discord.Embed:
    embed = discord.Embed(
        description=f'''
        ## <a:flecha:1290411623802208257> **¡Bienvenid@ a la categoría de CEEIBIS!**
        ''',
        color=dai_color()
    )
    embed.add_field(name='<:info:1288631394502709268> Configuración de la Categoría', value=f'> La categoría es totalemte configurable por el rol <@&{ASOCIATION_ROLE_IDS["ceeibis"]["coord"]}>', inline=False)
    embed.add_field(name='<:entrar:1288631392070012960> Añadir nuevos Miembros', value=f'> Utiliza el comando `{ASOCIATION_COMMANDS["ceeibis"]["nuevo"]}`\n > Otorgará el rol <@&{ASOCIATION_ROLE_IDS["ceeibis"]["member"]}> al usuario', inline=False)
    embed.add_field(name='<:salir:1288975442828726374> Eliminar Miembros', value=f'> Utiliza el comando `{ASOCIATION_COMMANDS["ceeibis"]["eliminar"]}`\n > Eliminará el rol <@&{ASOCIATION_ROLE_IDS["ceeibis"]["member"]}> del usuario', inline=False)
    embed.set_image(url='https://i.imgur.com/8GkOfv1.png')
    embed.set_footer(text='Delegación de Alumnos de Industriales - UVigo', icon_url='https://cdn.discordapp.com/emojis/1288628804276977735.webp?size=96&quality=lossless')
    return embed

def spacelab_info_embed() -> discord.Embed:
    embed = discord.Embed(
        description=f'''
        ## <a:flecha:1290411623802208257> **¡Bienvenid@ a la categoría de SpaceLab!**
        ''',
        color=dai_color()
    )
    embed.add_field(name='<:info:1288631394502709268> Configuración de la Categoría', value=f'> La categoría es totalemte configurable por el rol <@&{ASOCIATION_ROLE_IDS["spacelab"]["coord"]}>', inline=False)
    embed.add_field(name='<:entrar:1288631392070012960> Añadir nuevos Miembros', value=f'> Utiliza el comando `{ASOCIATION_COMMANDS["spacelab"]["nuevo"]}`\n > Otorgará el rol <@&{ASOCIATION_ROLE_IDS["spacelab"]["member"]}> al usuario', inline=False)
    embed.add_field(name='<:salir:1288975442828726374> Eliminar Miembros', value=f'> Utiliza el comando `{ASOCIATION_COMMANDS["spacelab"]["eliminar"]}`\n > Eliminará el rol <@&{ASOCIATION_ROLE_IDS["spacelab"]["member"]}> del usuario', inline=False)
    embed.set_image(url='https://i.imgur.com/8GkOfv1.png')
    embed.set_footer(text='Delegación de Alumnos de Industriales - UVigo', icon_url='https://cdn.discordapp.com/emojis/1288628804276977735.webp?size=96&quality=lossless')
    return embed

def motorsport_info_embed() -> discord.Embed:
    embed = discord.Embed(
        description=f'''
        ## <a:flecha:1290411623802208257> **¡Bienvenid@ a la categoría de MotorSport!**
        ''',
        color=dai_color()
    )
    embed.add_field(name='<:info:1288631394502709268> Configuración de la Categoría', value=f'> La categoría es totalemte configurable por el rol <@&{ASOCIATION_ROLE_IDS["motorsport"]["coord"]}>', inline=False)
    embed.add_field(name='<:entrar:1288631392070012960> Añadir nuevos Miembros', value=f'> Utiliza el comando `{ASOCIATION_COMMANDS["motorsport"]["nuevo"]}`\n > Otorgará el rol <@&{ASOCIATION_ROLE_IDS["motorsport"]["member"]}> al usuario', inline=False)
    embed.add_field(name='<:salir:1288975442828726374> Eliminar Miembros', value=f'> Utiliza el comando `{ASOCIATION_COMMANDS["motorsport"]["eliminar"]}`\n > Eliminará el rol <@&{ASOCIATION_ROLE_IDS["motorsport"]["member"]}> del usuario', inline=False)
    embed.set_image(url='https://i.imgur.com/8GkOfv1.png')
    embed.set_footer(text='Delegación de Alumnos de Industriales - UVigo', icon_url='https://cdn.discordapp.com/emojis/1288628804276977735.webp?size=96&quality=lossless')
    return embed

def ces_info_embed() -> discord.Embed:
    embed = discord.Embed(
        description=f'''
        ## <a:flecha:1290411623802208257> **¡Bienvenid@ a la categoría de CES!**
        ''',
        color=dai_color()
    )
    embed.add_field(name='<:info:1288631394502709268> Configuración de la Categoría', value=f'> La categoría es totalemte configurable por el rol <@&{ASOCIATION_ROLE_IDS["ces"]["coord"]}>', inline=False)
    embed.add_field(name='<:entrar:1288631392070012960> Añadir nuevos Miembros', value=f'> Utiliza el comando `{ASOCIATION_COMMANDS["ces"]["nuevo"]}`\n > Otorgará el rol <@&{ASOCIATION_ROLE_IDS["ces"]["member"]}> al usuario', inline=False)
    embed.add_field(name='<:salir:1288975442828726374> Eliminar Miembros', value=f'> Utiliza el comando `{ASOCIATION_COMMANDS["ces"]["eliminar"]}`\n > Eliminará el rol <@&{ASOCIATION_ROLE_IDS["ces"]["member"]}> del usuario', inline=False)
    embed.set_image(url='https://i.imgur.com/8GkOfv1.png')
    embed.set_footer(text='Delegación de Alumnos de Industriales - UVigo', icon_url='https://cdn.discordapp.com/emojis/1288628804276977735.webp?size=96&quality=lossless')
    return embed