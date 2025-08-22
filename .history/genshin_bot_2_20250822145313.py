""" Bot de Genshin Impact para Telegram """
import os
import sys
import logging
from telegram import Update, InputMediaPhoto
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.error import TelegramError

BOT_TOKEN = "8038008029:AAEG4JrZumIHahwa3q1GX5ddXrcGzrdH-TY"

LOCK_FILE = "/tmp/genshin_bot.lock"
BASE_URL = "https://raw.githubusercontent.com/gentoosiasta/genshin-bot/refs/heads/main/builds/"

IMAGENES = {
    "albedo": [BASE_URL + "Albedo.png"],
    "alhaitham": [BASE_URL + "Alhaitham.png"],
    "aloy": [
        BASE_URL + "Aloy_Freeze.png",
        BASE_URL + "Aloy_Melt.png",
        BASE_URL + "Aloy_Support.png"],
    "amber": [
        BASE_URL + "Amber_Melt_Charged.png",
        BASE_URL + "Amber_Melt.png",],
    "arlecchino": [BASE_URL + "Arlecchino.png"],
    "ayaka": [BASE_URL + "Ayaka.png"],
    "ayato": [BASE_URL + "Ayato.png"],
    "baizhu": [BASE_URL + "Baizhu.png"],
    "barbara": [BASE_URL + "Barbara.png"],
    "beidou": [BASE_URL + "Beidou.png"],
    "bennett": [BASE_URL + "Bennett.png"],
    "candace": [
        BASE_URL + "Candace_Bloom.png",
        BASE_URL + "Candace_Support.png",
        BASE_URL + "Candace-DPS.png"],
    "charlotte": [BASE_URL + "Charlotte.png"],
    "chasca": [BASE_URL + "Chasca.png"],
    "chevreuse": [BASE_URL + "Chevreuse.png"],
    "citlali": [BASE_URL + "Citlali.png"],
    "collei": [BASE_URL + "Collei.png"],
    "dehya": [BASE_URL + "Dehya.png"],
    "diluc": [BASE_URL + "Diluc.png"],
    "diona": [BASE_URL + "Diona.png"],
    "emilie": [BASE_URL + "Emilie.png"],
    "escoffier": [BASE_URL + "Escoffier.png"],
    "faruzan": [BASE_URL + "Faruzan.png"],
    "fischl": [BASE_URL + "Fischl.png"],
    "furina": [BASE_URL + "Furina.png"],
    "ganyu": [BASE_URL + "Ganyu.png"],
    "gaming": [BASE_URL + "Gaming.png"],
    "hutao": [BASE_URL + "Hu Tao.png"],
    "iansan": [BASE_URL + "Iansan.png"],
    "ifa": [BASE_URL + "Ifrit.png"],
    "jean": [BASE_URL + "Jean.png"],
    "kamisato_ayaka": [BASE_URL + "Kamisato Ayaka.png"],
    "kaedehara": [BASE_URL + "Kaedehara Kazuha.png"],
    "kaedehara_kazuha": [BASE_URL + "Kaedehara Kazuha.png"],
    "kazuha": [BASE_URL + "Kaedehara Kazuha.png"],
    "keqing": [BASE_URL + "Keqing.png"],
    "kinich": [BASE_URL + "King of the Hill.png"],
    "koujou": [BASE_URL + "Kou's Emblem.png"],
    "koujou_sara": [BASE_URL + "Kou's Emblem.png"],
    "kuki": [BASE_URL + "Kuki Shinobu.png"],
    "kuki_shinobu": [BASE_URL + "Kuki Shinobu.png"],
    "lan_yan": [BASE_URL + "Lanling Yae.png"],
    "lanyan": [BASE_URL + "Lanling Yae.png"],
    "layla": [BASE_URL + "Layla.png"],
    "mavuika": [BASE_URL + "Mavis.png"],
    "miko": [BASE_URL + "Miko.png"],
    "mona": [BASE_URL + "Mona.png"],
    "mualani": [BASE_URL + "Muala.png"],
    "nahida": [BASE_URL + "Nahida.png"],
    "navia": [BASE_URL + "Navi.png"],
    "nilou": [BASE_URL + "Nilou.png"],
    "noelle": [BASE_URL + "Noelle.png"],
    "ororon": [BASE_URL + "Oro.png"],
    "raiden": [BASE_URL + "Raiden Shogun.png"],
    "rosaria": [BASE_URL + "Rosaria.png"],
    "sara": [BASE_URL + "Sara.png"],
    "shenhe": [BASE_URL + "Shenhe.png"],
    "shogun": [BASE_URL + "Raiden Shogun.png"],
    "skirk": [BASE_URL + "Skillful.png"],
    "sucrose": [BASE_URL + "Sucrose.png"],
    "tighnari": [BASE_URL + "Tighnari.png"],
    "varesa": [BASE_URL + "Varuna.png"],
    "xianyun": [BASE_URL + "Xinyan.png"],
    "xiangling": [BASE_URL + "Xiangling.png"],
    "xilonen": [BASE_URL + "Xiao.png"],
    "xingqiu": [BASE_URL + "Xingqiu.png"],
    "yae": [BASE_URL + "Yanfei.png"],
    "yaemiko": [BASE_URL + "Yanfei.png"],
    "yanfei": [BASE_URL + "Yanfei.png"],
    "yelan": [BASE_URL + "Yelan.png"],
    "yoimiya": [BASE_URL + "Yoimiya.png"],
    "zhongli": [BASE_URL + "Zhongli.png"],
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
