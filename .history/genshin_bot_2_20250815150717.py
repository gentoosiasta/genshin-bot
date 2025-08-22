import os
import sys
import logging
from telegram import Update, InputMediaPhoto
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.error import TelegramError

BOT_TOKEN = "8038008029:AAEG4JrZumIHahwa3q1GX5ddXrcGzrdH-TY"

LOCK_FILE = "/tmp/genshin_bot.lock"

IMAGENES = {
    "skirk": ["https://ibb.co/VW2W5yNs"],
    "citlali": ["https://ibb.co/hJzghc1k"],
    "escoffier": ["https://ibb.co/nM8jCx8r"],
    "rosaria": ["https://ibb.co/V0X59Yfp", "https://ibb.co/ZRnV1zRX"],
    "arlecchino": ["https://ibb.co/Y4TK2my1"],
    "bennett": ["https://ibb.co/xS9QnbQV"],
    "chevreuse": ["https://ibb.co/zVG3PfK3"],
    "diluc": ["https://ibb.co/SZsjHwr"],
    "gaming": ["https://ibb.co/VWQx4cw3"],
    "hutao": ["https://ibb.co/JR1RQdRj"],
    "mavuika": ["https://ibb.co/8nXrXcX1", "https://ibb.co/PkWsFh2"],
    "xiangling": ["https://ibb.co/WNF6wB1L"],
    "yanfei": ["https://ibb.co/TxfnGccY"],
    "yoimiya": ["https://ibb.co/DPBZTKQn"],
    "dehya": ["https://ibb.co/XkVc4ktk", "https://ibb.co/TB8XqrLz"],
    "barbara": ["https://ibb.co/fV960HbN"],
    "candace": ["https://ibb.co/zWpvWdYS", "https://ibb.co/FkkqmL2P"],
    "furina": ["https://ibb.co/JFmcPG1S"],
    "mona": ["https://ibb.co/zVVJLYNw"],
    "mualani": ["https://ibb.co/60sFtqws"],
    "nilou": ["https://ibb.co/n8qndhrT"],
    "xingqiu": ["https://ibb.co/5XfPJZhy"],
    "yelan": ["https://ibb.co/7dWfC91c"],
    "beidou": ["https://ibb.co/FbCbKFPH"],
    "fischl": ["https://ibb.co/m556Q2X8"],
    "iansan": ["https://ibb.co/VcHTxtJm"],
    "keqing": ["https://ibb.co/h11JPHzt", "https://ibb.co/qLzJDTf6"],
    "ororon": ["https://ibb.co/Nnp9r1hD"],
    "raiden": ["https://ibb.co/nJfcHpC", "https://ibb.co/cSFsGWVR", "https://ibb.co/spsnKTVb"],
    "shogun": ["https://ibb.co/nJfcHpC", "https://ibb.co/cSFsGWVR", "https://ibb.co/spsnKTVb"],
    "sara": ["https://ibb.co/rT94chr"],
    "koujou": ["https://ibb.co/rT94chr"],
    "koujou_sara": ["https://ibb.co/rT94chr"],
    "kuki": ["https://ibb.co/vv47NpZV", "https://ibb.co/0pyq3RN6"],
    "shinobu": ["https://ibb.co/vv47NpZV", "https://ibb.co/0pyq3RN6"],
    "kuki_shinobu": ["https://ibb.co/vv47NpZV", "https://ibb.co/0pyq3RN6"],
    "varesa": ["https://ibb.co/XxWVJvH5"],
    "yae": ["https://ibb.co/cXrQ6Sb4"],
    "yaemiko": ["https://ibb.co/cXrQ6Sb4"],
    "miko": ["https://ibb.co/cXrQ6Sb4"],
    "chasca": ["https://ibb.co/VpxmSmbn"],
    "faruzan": ["https://ibb.co/6RB9yMry"],
    "ifa": ["https://ibb.co/hJrHcsTP"],
    "jean": ["https://ibb.co/NnYGDWs6"],
    "kazuha": ["https://ibb.co/0jswK3Yt"],
    "kaedehara": ["https://ibb.co/0jswK3Yt"],
    "kaedehara_kazuha": ["https://ibb.co/0jswK3Yt"],
    "lanyan": ["https://ibb.co/4hRndbC"],
    "lan_yan": ["https://ibb.co/4hRndbC"],
    "sucrose": ["https://ibb.co/HTwXrjJb"],
    "xianyun": ["https://ibb.co/Zz6GVmNV"],
    "navia": ["https://ibb.co/LDGxM4nv"],
    "noelle": ["https://ibb.co/r2hZB3f7"],
    "xilonen": ["https://ibb.co/v4Sfjvx9"],
    "zhongli": ["https://ibb.co/vC9F3RfR"],
    "baizhu": ["https://ibb.co/M5D4jn07"],
    "collei": ["https://ibb.co/nMC2KTgx"],
    "emilie": ["https://ibb.co/twFD7nDH"],
    "nahida": ["https://ibb.co/vxgQ3fxW"],
    "tighnari": ["https://ibb.co/9jCzsD0"],
    "ayaka": ["https://ibb.co/0p5ztT7K"],
    "kamisato_ayaka": ["https://ibb.co/0p5ztT7K"],
    "charlotte": ["https://ibb.co/8nNFTJJR"],
    "diona": ["https://ibb.co/sd9xrhC6"],
    "ganyu": ["https://ibb.co/yFHT52Fg", "https://ibb.co/xKL3JCSV"],
    "shenhe": ["https://ibb.co/9mqhrz26"],
    "layla": ["https://ibb.co/yFKN065n"],
    "kinich": ["https://ibb.co/mFS3rRJG"]
}

# Configura el logging para ver los errores
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envía un mensaje de bienvenida con la lista de comandos."""
    nombre_usuario = update.effective_user.first_name
    
    # Crea una lista de todas las claves disponibles para el mensaje
    nombres_disponibles = ", ".join(sorted(IMAGENES.keys()))
    
    mensaje_bienvenida = (
        f"¡Hola, {nombre_usuario}! 👋\n\n"
        "Usa el comando `/build <nombre>` para recibir una o más imágenes.\n\n"
        "**Nombres disponibles:**\n"
        f"`{nombres_disponibles}`"
    )
    
    await update.message.reply_text(mensaje_bienvenida, parse_mode='Markdown')

async def enviar_imagen(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Busca un nombre en el diccionario y envía todas las imágenes asociadas."""
    try:
        # Obtiene el nombre solicitado por el usuario (en minúsculas)
        nombre_clave = context.args[0].lower()
    except IndexError:
        await update.message.reply_text("Por favor, especifica un nombre. Ejemplo: /build raiden")
        return

    # Busca la lista de URLs en el diccionario
    lista_urls = IMAGENES.get(nombre_clave)

    if lista_urls:
        # Si se encontraron URLs, se envían
        await update.message.reply_text(f"Enviando builds para '{nombre_clave}'...")
        
        # Opción 1: Enviar como un álbum (si hay entre 2 y 10 imágenes)
        if 1 < len(lista_urls) <= 10:
            media_group = [InputMediaPhoto(url) for url in lista_urls]
            try:
                await context.bot.send_media_group(chat_id=update.effective_chat.id, media=media_group)
            except TelegramError as e:
                await update.message.reply_text(f"Hubo un error al crear el álbum. Error: {e}")
                # Si falla el álbum, se envían una por una como respaldo
                for url in lista_urls:
                    try:
                       await context.bot.send_photo(chat_id=update.effective_chat.id, photo=url)
                    except TelegramError as e_photo:
                       await update.message.reply_text(f"No se pudo enviar la build desde {url}. Error: {e_photo}")

        # Opción 2: Enviar una por una (si es solo una imagen o más de 10)
        else:
            for url in lista_urls:
                try:
                    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=url)
                except TelegramError as e:
                    # Informa al usuario si una URL específica falla
                    await update.message.reply_text(f"No se pudo enviar la build desde {url}. Asegúrate de que sea un enlace directo válido. Error: {e}")

    else:
        # Si el nombre no está en el diccionario
        await update.message.reply_text(f"Lo siento, no encontré builds para '{nombre_clave}'. Usa /start para ver la lista de nombres disponibles.")


def main() -> None:
    """Inicia el bot."""
    print("Iniciando bot...")
    application = Application.builder().token(BOT_TOKEN).build()

    # Registra los manejadores de comandos
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("build", enviar_imagen))

    # Inicia el bot para que escuche peticiones
    print("Bot iniciado. Presiona Ctrl+C para detener.")
    application.run_polling()

def check_lock() -> None:
    """Comprueba si hay una instancia en ejecución."""
    if os.path.exists(LOCK_FILE):
        print("Ya hay una instancia en ejecución.")
        sys.exit()
    else:
        with open(LOCK_FILE, "w") as f:
            f.write(str(os.getpid()))

def remove_lock() -> None:
    """Elimina el archivo de bloqueo."""
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)

if __name__ == '__main__':
    try:
        check_lock()
        main()

    finally:
        remove_lock()
