SERVER_ID = 1288206483091361885
LOG_CHANNEL = 1290404101108269169
WELCOME_CHANNEL = 1288283913181200446
INSTAGRAM_DAI_CHANNEL = 1288210585632112743
INSTAGRAM_DAI_ACCOUNT_URL = "https://www.instagram.com/dai_uvigo/"

def instagram_message_format(permalink: str, caption: str, likes: int, comments: int, post_id: int, date_published: str, media_url: str) -> str:
    # Formatear el caption
    formatted_caption = '> ' + caption.replace('\n', '\n> ')
    return f"""
## <a:flecha:1290411623802208257> [Nueva Publicación en Instagram]({permalink}):
{formatted_caption}
`❤️ {likes}` `💬 {comments}`

🔗 [**Nuestro Instagram**]({INSTAGRAM_DAI_ACCOUNT_URL}) **@dai_uvigo**

-# ID: {post_id} Actualizado: {date_published} [.]({media_url})
-# **Delegación de alumnos de Industriales** <a:dinkdonk:1289157144436015174> <@&1288263963812958300>
"""
