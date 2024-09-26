from PIL import Image, ImageDraw, ImageFont, ImageOps
from io import BytesIO
import requests

def generate_welcome_image(nombre_usuario, avatar_url, base_image_path):
    #* Cargar la imagen base
    try:
        base_image = Image.open(base_image_path)
    except Exception as e:
        print(f"Error al cargar la imagen base: {e}")
        return None

    #* Obtener el avatar del usuario
    try:
        response = requests.get(avatar_url)
        avatar_image = Image.open(BytesIO(response.content)).resize((200, 200))
    except Exception as e:
        print(f"Error al cargar el avatar: {e}")
        return None
    #* Hacer Cirucular la Imagen
    # Hacer el avatar circular con fondo transparente
    avatar_mask = Image.new("L", avatar_image.size, 0)  # Crear máscara de transparencia
    draw_mask = ImageDraw.Draw(avatar_mask)
    draw_mask.ellipse((0, 0, 200, 200), fill=255)  # Dibujar un círculo completo en la máscara
    avatar_image = avatar_image.convert("RGBA")  # Asegurarse de que el avatar tenga canal alpha
    avatar_image.putalpha(avatar_mask)  # Aplicar la máscara circular como transparencia
    #* Poner Borde a la Imagen
    # Tamaño del borde
    border_size = 6
    # Crear una nueva imagen para el avatar con borde
    avatar_with_border = Image.new("RGBA", (avatar_image.width + border_size * 2, avatar_image.height + border_size * 2), (0, 0, 0, 0))
    draw = ImageDraw.Draw(avatar_with_border)
    # Dibujar un borde circular
    border_color = (0, 172, 226)  # Color del borde
    draw.ellipse([0, 0, avatar_with_border.width, avatar_with_border.height], fill=border_color)
    # Pegar el avatar en la imagen con borde
    avatar_with_border.paste(avatar_image, (border_size, border_size), avatar_image)



    # Crear un objeto de dibujo para la imagen base
    draw = ImageDraw.Draw(base_image)

    # Especificar una fuente (asegúrate de tener la ruta correcta a tu archivo de fuente)
    try:
        # Cargar fuente personalizada
        font_path = "assets/fonts/Comfortaa-Bold.ttf"  # Cambia esto a la ruta de tu fuente
        font_size = 60
        font = ImageFont.truetype(font_path, font_size)
    except Exception as e:
        print(f"Error al cargar la fuente: {e}")
        return None

    #* TEXTO DE BIENVENIDA
    base_image_height = base_image.size[1]
    text_bienvenido = "¡Bienvenid@, "
    text_usuario = f"{nombre_usuario}"
    text_exclamacion = "!"
    x_start = 250
    # Calcular el centro vertical para el texto
    text_height = font.getbbox(text_bienvenido)[1]
    y_centered = (base_image_height - text_height) // 2 - 30
    y_start = y_centered
    #* AVATAR
    # Calcular la posición verticalmente centrada para el avatar
    avatar_position_y = (base_image_height - avatar_image.size[1]) // 2 # Centrado verticalmente
    # Pegar el avatar circular en la imagen base, respetando la transparencia
    base_image.paste(avatar_with_border, (25, avatar_position_y), avatar_with_border)

    #* ESCRIBIR TEXTO
    # Obtener el ancho del primer texto "¡Bienvenid@,"
    draw.text((x_start, y_start), text_bienvenido, (0, 172, 226), font=font)
    text_bienvenido_bbox = font.getbbox(text_bienvenido)
    text_bienvenido_width = text_bienvenido_bbox[2] - text_bienvenido_bbox[0]
    # Escribir el nombre del usuario justo después del primer texto
    x_new = x_start + text_bienvenido_width
    draw.text((x_new, y_start), text_usuario, (0, 125, 164), font=font)
    # Obtener el ancho del nombre del usuario
    text_usuario_bbox = font.getbbox(text_usuario)
    text_usuario_width = text_usuario_bbox[2] - text_usuario_bbox[0]
    # Escribir el "!" después del nombre del usuario
    x_new += text_usuario_width
    draw.text((x_new, y_start), text_exclamacion, (0, 172, 226), font=font)

    # Guardar la imagen final en un buffer y retornarla
    image_binary = BytesIO()
    try:
        base_image.save(image_binary, 'PNG')
        image_binary.seek(0)  # Volver al inicio del buffer
    except Exception as e:
        print(f"Error al guardar la imagen: {e}")
        return None

    return image_binary
