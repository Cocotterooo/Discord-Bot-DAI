    if image_binary is None:
        await channel.send("Ocurrió un error al generar la imagen.")
    else:
        await channel.send(file=discord.File(fp=image_binary, filename='tema_claro_recortado.png'))