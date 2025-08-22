""" Bot de Genshin Impact para Telegram """
import os
import sys
import logging
from telegram import Update, InputMediaPhoto
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.error import TelegramError

BOT_TOKEN = "8038008029:AAEG4JrZumIHahwa3q1GX5ddXrcGzrdH-TY"

LOCK_FILE = "/tmp/genshin_bot.lock"

IMAGENES = {
    "albedo": ["https://raw.githubusercontent.com/gentoosiasta/genshin-bot/refs/heads/main/builds/Albedo.png"],
    "arlecchino": ["https://raw.githubusercontent.com/gentoosiasta/genshin-bot/refs/heads/main/builds/Arlecchino.png"],
    "ayaka": ["https://raw.githubusercontent.com/gentoosiasta/genshin-bot/refs/heads/main/builds/Ayaka.png"],
    "baizhu": ["https://raw.githubusercontent.com/gentoosiasta/genshin-bot/refs/heads/main/builds/Baizhu.png"],
    "barbara": ["https://raw.githubusercontent.com/gentoosiasta/genshin-bot/refs/heads/main/builds/Barbara.png"],
    "beidou": ["https://raw.githubusercontent.com/gentoosiasta/genshin-bot/refs/heads/main/builds/Beidou.png"],
    "bennett": ["https://raw.githubusercontent.com/gentoosiasta/genshin-bot/refs/heads/main/builds/Bennett.png"],
    "candace": ["https://raw.githubusercontent.com/gentoosiasta/genshin-bot/refs/heads/main/builds/Candace.png"],
    "charlotte": ["https://raw.githubusercontent.com/gentoosiasta/genshin-bot/refs/heads/main/builds/Charlotte.png"],
    "chasca": ["https://raw.githubusercontent.com/gentoosiasta/genshin-bot/refs/heads/main/builds/Chasca.png"],
    "chevreuse": ["https://raw.githubusercontent.com/gentoosiasta/genshin-bot/refs/heads/main/builds/Chevreuse.png"],
    "citlali": ["https://raw.githubusercontent.com/gentoosiasta/genshin-bot/refs/heads/main/builds/Citlali.png"],
    "collei": ["https://raw.githubusercontent.com/gentoosiasta/genshin-bot/refs/heads/main/builds/Collei.png"],
    "dehya": ["https://raw.githubusercontent.com/gentoosiasta/genshin-bot/refs/heads/main/builds/Dehya.png"],
    "diluc": ["https://raw.githubusercontent.com/gentoosiasta/genshin-bot/refs/heads/main/builds/Diluc.png"],
    "diona": ["https://raw.githubusercontent.com/gentoosiasta/genshin-bot/refs/heads/main/builds/Diona.png"],
    "emilie": ["https://raw.githubusercontent.com/gentoosiasta/genshin-bot/refs/heads/main/builds/Emilie.png"],
    "escoffier": ["https://raw.githubusercontent.com/gentoosiasta/genshin-bot/refs/heads/main/builds/Escoffier.png"],
    "faruzan": ["https://raw.githubusercontent.com/gentoosiasta/genshin-bot/refs/heads/main/builds/Faruzan.png"],
    "fischl": ["https://raw.githubusercontent.com/gentoosiasta/genshin-bot/refs/heads/main/builds/Fischl.png"],
    "furina": ["https://raw.githubusercontent.com/gentoosiasta/genshin-bot/refs/heads/main/builds/Furina.png"],
    "ganyu": ["https://raw.githubusercontent.com/gentoosiasta/genshin-bot/refs/heads/main/builds/Ganyu.png"],
    "gaming": ["https://raw.githubusercontent.com/gentoosiasta/genshin-bot/refs/heads/main/builds/Gaming.png"],
    "hutao": ["https://raw.githubusercontent.com/gentoosiasta/genshin-bot/refs/heads/main/builds/Hu Tao.png"],
    "iansan": ["https://raw.githubusercontent.com/gentoosiasta/genshin-bot/refs/heads/main/builds/Iansan.png"],
    "ifa": ["https://raw.githubusercontent.com/gentoosiasta/genshin-bot/refs/heads/main/builds/Ifrit.png"],
    "jean": ["https://raw.githubusercontent.com/gentoosiasta/genshin-bot/refs/heads/main/builds/Jean.png"],
    "kamisato_ayaka": ["https://raw.githubusercontent.com/gentoosiasta/genshin-bot/refs/heads/main/builds/Kamisato Ayaka.png"],
    "kaedehara": ["https://raw.githubusercontent.com/gentoosiasta/genshin-bot/refs/heads/main/builds/Kaedehara Kazuha.png"],
    "kaedehara_kazuha": ["https://raw.githubusercontent.com/gentoosiasta/genshin-bot/refs/heads/main/builds/Kaedehara Kazuha.png"],
    "kazuha": ["https://raw.githubusercontent.com/gentoosiasta/genshin-bot/refs/heads/main/builds/Kaedehara Kazuha.png"],
    "keqing": ["https://raw.githubusercontent.com/gentoosiasta/genshin-bot/refs/heads/main/builds/Keqing.png"],
    "kinich": ["https://raw.githubusercontent.com/gentoosiasta/genshin-bot/refs/heads/main/builds/King of the Hill.png"],
    "koujou": ["https://raw.githubusercontent.com/gentoosiasta/genshin-bot/refs/heads/main/builds/Kou's Emblem.png"],
    "koujou_sara": ["https://raw.githubusercontent.com/gentoosiasta/genshin-bot/refs/heads/main/builds/Kou's Emblem.png"],
    "kuki": ["https://raw.githubusercontent.com/gentoosiasta/genshin-bot/refs/heads/main/builds/Kuki Shinobu.png"],
    "kuki_shinobu": ["https://raw.githubusercontent.com/gentoosiasta/genshin-bot/refs/heads/main/builds/Kuki Shinobu.png"],
    "lan_yan": ["https://raw.githubusercontent.com/gentoosiasta/genshin-bot/refs/heads/main/builds/Lanling Yae.png"],
    "lanyan": ["https://raw.githubusercontent.com/gentoosiasta/genshin-bot/refs/heads/main/builds/Lanling Yae.png"],
    "layla": ["https://raw.githubusercontent.com/gentoosiasta/genshin-bot/refs/heads/main/builds/Layla.png"],
    "mavuika": ["https://raw.githubusercontent.com/gentoosiasta/genshin-bot/refs/heads/main/builds/Mavis.png"],
    "miko": ["https://raw.githubusercontent.com/gentoosiasta/genshin-bot/refs/heads/main/builds/Miko.png"],
    "mona": ["https://raw.githubusercontent.com/gentoosiasta/genshin-bot/refs/heads/main/builds/Mona.png"],
    "mualani": ["https://raw.githubusercontent.com/gentoosiasta/genshin-bot/refs/heads/main/builds/Muala.png"],
    "nahida": ["https://raw.githubusercontent.com/gentoosiasta/genshin-bot/refs/heads/main/builds/Nahida.png"],
    "navia": ["https://raw.githubusercontent.com/gentoosiasta/genshin-bot/refs/heads/main/builds/Navi.png"],
    "nilou": ["https://raw.githubusercontent.com/gentoosiasta/genshin-bot/refs/heads/main/builds/Nilou.png"],
    "noelle": ["https://raw.githubusercontent.com/gentoosiasta/genshin-bot/refs/heads/main/builds/Noelle.png"],
    "ororon": ["https://raw.githubusercontent.com/gentoosiasta/genshin-bot/refs/heads/main/builds/Oro.png"],
    "raiden": ["https://raw.githubusercontent.com/gentoosiasta/genshin-bot/refs/heads/main/builds/Raiden Shogun.png"],
    "rosaria": ["https://raw.githubusercontent.com/gentoosiasta/genshin-bot/refs/heads/main/builds/Rosaria.png"],
    "sara": ["https://raw.githubusercontent.com/gentoosiasta/genshin-bot/refs/heads/main/builds/Sara.png"],
    "shenhe": ["https://raw.githubusercontent.com/gentoosiasta/genshin-bot/refs/heads/main/builds/Shenhe.png"],
    "shogun": ["https://raw.githubusercontent.com/gentoosiasta/genshin-bot/refs/heads/main/builds/Raiden Shogun.png"],
    "skirk": ["https://raw.githubusercontent.com/gentoosiasta/genshin-bot/refs/heads/main/builds/Skillful.png"],
    "sucrose": ["https://raw.githubusercontent.com/gentoosiasta/genshin-bot/refs/heads/main/builds/Sucrose.png"],
    "tighnari": ["https://raw.githubusercontent.com/gentoosiasta/genshin-bot/refs/heads/main/builds/Tighnari.png"],
    "varesa": ["https://raw.githubusercontent.com/gentoosiasta/genshin-bot/refs/heads/main/builds/Varuna.png"],
    "xianyun": ["https://raw.githubusercontent.com/gentoosiasta/genshin-bot/refs/heads/main/builds/Xinyan.png"],
    "xiangling": ["https://raw.githubusercontent.com/gentoosiasta/genshin-bot/refs/heads/main/builds/Xiangling.png"],
    "xilonen": ["https://raw.githubusercontent.com/gentoosiasta/genshin-bot/refs/heads/main/builds/Xiao.png"],
    "xingqiu": ["https://raw.githubusercontent.com/gentoosiasta/genshin-bot/refs/heads/main/builds/Xingqiu.png"],
    "yae": ["https://raw.githubusercontent.com/gentoosiasta/genshin-bot/refs/heads/main/builds/Yanfei.png"],
    "yaemiko": ["https://raw.githubusercontent.com/gentoosiasta/genshin-bot/refs/heads/main/builds/Yanfei.png"],
    "yanfei": ["https://raw.githubusercontent.com/gentoosiasta/genshin-bot/refs/heads/main/builds/Yanfei.png"],
    "yelan": ["https://raw.githubusercontent.com/gentoosiasta/genshin-bot/refs/heads/main/builds/Yelan.png"],
    "yoimiya": ["https://raw.githubusercontent.com/gentoosiasta/genshin-bot/refs/heads/main/builds/Yoimiya.png"],
    "zhongli": ["https://raw.githubusercontent.com/gentoosiasta/genshin-bot/refs/heads/main/builds/Zhongli.png"],
}

# Configura el logging para ver los errores
# Configura el logging para que escriba en un archivo y también en la consola.
logging.basicConfig(
    level=logging.INFO, # Nivel mínimo de los mensajes a registrar
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("/var/log/genshin_bot.log"), # Manejador para escribir en el archivo 'bot.log'
        logging.StreamHandler()        # Manejador para mostrar los logs en la consola
    ]
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
