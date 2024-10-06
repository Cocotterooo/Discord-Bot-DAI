import discord

SERVER_ID = 1288206483091361885
LOG_CHANNEL = 1290404101108269169
WELCOME_CHANNEL = 1288283913181200446
INSTAGRAM_DAI_CHANNEL = 1288210585632112743
INSTAGRAM_DAI_ACCOUNT_URL = "https://www.instagram.com/dai_uvigo/"
ADMIN_ROLE = 1288552528484630598
DAI_ROLES_CHANNEL_ID = 1292469145388191834

ID_INFRAESTRUCTURAS = 1292466487247896699
ID_COMUNICACION = 1292466863707521167
ID_ASUNTOS_EXTERIORES = 1292466970687442984
ID_DEPORTES = 1292468137845067776


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
        color=discord.Color.blue()  # Color del borde del embed
    )
    #embed.(url="/assets/separador.png")
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
        ### <:us:1288631396364976128> Comisiones Delegadas:
        > <@&1292466863707521167>
        > <@&1292466487247896699>
        > <@&1292466970687442984>
        > <@&1292468137845067776>
        ### <:exclamacion:1288628819548176514> Extras:
        > <@&1288552528484630598> <:desarrollador:1288628718423638037>
        > <@&1288206919118618839> <:moderador:1288628804276977735>
        > <@&1288553111119462451>
        ### Selección:
        ''',
        color=discord.Color.blue()
    )
    embed.add_field(name="<:verificado:1288628715982553188> Roles Especiales", value="Para obtener un rol de las secciones **Directiva** o **Extras**, contacta con <@&1288552528484630598>.", inline=False)
    embed.add_field(name="<:verificado:1288628715982553188> Comisiones Delegadas", value="Para **obtener** o **eliminar** un rol de una Comisión Delegada solo haz click en los botones.", inline=False)
    embed.set_image(url='https://i.imgur.com/8GkOfv1.png')
    embed.set_footer(text='Delegación de Alumnos de Industriales - UVigo', icon_url='https://cdn.discordapp.com/emojis/1288628804276977735.webp?size=96&quality=lossless')
    return embed