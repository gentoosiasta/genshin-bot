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
    "chevreuse": [
        BASE_URL + "Chevreuse-DPS.png",
        BASE_URL + "Chevreuse-Support.png"],
    "chiori": [BASE_URL + "Chiori.png"],
    "chongyun": [BASE_URL + "Chongyun.png"],
    "citlali": [BASE_URL + "Citlali.png"],
    "clorinde": [BASE_URL + "Clorinde.png"],
    "collei": [BASE_URL + "Collei.png"],
    "cyno": [BASE_URL + "Cyno.png"],
    "Dahlia": [BASE_URL + "Dahlia.png"],
    "dehya": [
        BASE_URL + "Dehya_DPS.png",
        BASE_URL + "Dehya_Support.png"],
    "diluc": [BASE_URL + "Diluc.png"],
    "diona": [BASE_URL + "Diona.png"],
    "dori": [
        BASE_URL + "Dori_DPS.png",
        BASE_URL + "Dori_Hyperbloom.png",
        BASE_URL + "Dori_Support.png"],
    "emilie": [BASE_URL + "Emilie.png"],
    "escoffier": [
        BASE_URL + "Escoffier_Freeze.png",
        BASE_URL + "Escoffier_Support.png"],
    "eula": [BASE_URL + "Eula.png"],
    "faruzan": [BASE_URL + "Faruzan.png"],
    "fischl": [BASE_URL + "Fischl.png"],
    "freminet": [
        BASE_URL + "Freminet_Cryo.png",
        BASE_URL + "Freminet_Fisical.png"],
    "furina": [BASE_URL + "Furina.png"],
    "gaming": [BASE_URL + "Gaming.png"],
    "ganyu": [
        BASE_URL + "Ganyu_Freeze.png",
        BASE_URL + "Ganyu_Melt.png"],
    "gorou": [BASE_URL + "Gorou.png"],
    "Heizou": [
        BASE_URL + "Heizou_DPS.png",
        BASE_URL + "Heizou_Driver.png",
        BASE_URL + "Heizou_Support.png"],
    "hutao": [BASE_URL + "Hu Tao.png"],
    "iansan": [BASE_URL + "Iansan.png"],
    "ifa": [
        BASE_URL + "Ifa_Anemo_DPS.png",
        BASE_URL + "Ifa_Swirl_DPS.png"],
    "ineffa": [BASE_URL + "Ineffa.png"],
    "itto": [BASE_URL + "Itto.png"],
    "jean": [
        BASE_URL + "Jean_Healer.png",
        BASE_URL + "Jean_Sunfire.png"],
    "kashina": [BASE_URL + "Kashina.png"],
    "kaeya": [
        BASE_URL + "Kaeya_Freeze.png",
        BASE_URL + "Kaeya_Melt.png"],
    "Kaveh": [BASE_URL + "Kaveh.png"],
    "kazuha": [BASE_URL + "Kazuha.png"],
    "keqing": [
        BASE_URL + "Keqing_Aggravate.png",
        BASE_URL + "Keqing_Electro.png"],
    "kinich": [BASE_URL + "Kinich.png"],
    "kirara": [BASE_URL + "Kirara.png"],
    "kokomi": [
        BASE_URL + "Kokomi_Bloom.png",
        BASE_URL + "Kokomi_Driver.png",
        BASE_URL + "Kokomi_Support.png"],
    "kuki": [
        BASE_URL + "Shinobu_Hyperbloom.png",
        BASE_URL + "Shinobu_Quicken.png"],
    "lanyan": [BASE_URL + "Lanyan.png"],
    "layla": [
        BASE_URL + "Layla_DPS.png",
        BASE_URL + "Layla_Shielder.png"],
    "lisa": [BASE_URL + "Lisa.png"],
    "lynette": [
        BASE_URL + "Lynette_DPS.png",
        BASE_URL + "Lynette_Reaction.png",
        BASE_URL + "Lynette_Support.png"],
    "lyney": [BASE_URL + "Lyney.png"],
    "mavuika": [
        BASE_URL + "Mavuika_DPS.png",
        BASE_URL + "Mavuika_Support.png"],
    "mika": [BASE_URL + "Mika.png"],
    "mizuki": [BASE_URL + "Mizuki.png"],
    "mona": [BASE_URL + "Mona.png"],
    "mualani": [BASE_URL + "Mualani.png"],
    "nahida": [BASE_URL + "Nahida.png"],
    "navia": [BASE_URL + "Navia.png"],
    "neuvillette": [BASE_URL + "Neuvillette.png"],
    "nilou": [BASE_URL + "Nilou.png"],
    "ningguang": [BASE_URL + "Ningguang.png"],
    "noelle": [BASE_URL + "Noelle.png"],
    "ororon": [BASE_URL + "Oro.png"],
    "qiqi": [BASE_URL + "Qiqi.png"],
    "raiden": [
        BASE_URL + "Raiden_Shogun_Aggravate.png",
        BASE_URL + "Raiden_Shogun_DPS.png",
        BASE_URL + "Raiden_Shogun_Hyper-bloom.png"],
    "razor": [
        BASE_URL + "Razor_Aggravate.png",
        BASE_URL + "Razor_Physical.png",
        BASE_URL + "Razor_Transformative.png"],
    "rosaria": [
        BASE_URL + "Rosaria_Freeze.png",
        BASE_URL + "Rosaria_Melt.png"],
    "sara": [BASE_URL + "Kujou_Sara.png"],
    "sayu": [
        BASE_URL + "Sayu_DPS.png",
        BASE_URL + "Sayu_Support.png"],
    "sethos": [BASE_URL + "Sethos.png"],
    "shenhe": [BASE_URL + "Shenhe.jpg"],
    "sigewinne": [BASE_URL + "Sigewinne.png"],
    "skirk": [BASE_URL + "Skirk.png"],
    "sucrose": [BASE_URL + "Sucrose.png"],
    "tartaglia": [BASE_URL + "Tartaglia.png"],
    "thoma": [
        BASE_URL + "Thoma_Burgeon.png",
        BASE_URL + "Thoma_Support.png"],
    "tighnari": [BASE_URL + "Tighnari.png"],
    "traveler": [
        BASE_URL + "Traveler_Dendro_1.png",
        BASE_URL + "Traveler_Dendro_2.png",
        BASE_URL + "Traveler_Hydro.png",
        BASE_URL + "Traveler_Pyro_DPS.png",
        BASE_URL + "Traveler_Pyro_Support.png",],
    "varesa": [BASE_URL + "Varuna.png"],
    "venti": [BASE_URL + "Venti.png"],
    "wanderer": [BASE_URL + "Wanderer.png"],
    "wriothesley": [
        BASE_URL + "Wriothesley_Freeze.png",
        BASE_URL + "Wriothesley_Melt.png"],
    "xiangling": [
        BASE_URL + "Xiangling_DPS.png",
        BASE_URL + "Xiangling_Support.png"],
    "xianyun": [BASE_URL + "Xianyun.png"],
    "xiao": [BASE_URL + "Xiao.png"],
    "xilonen": [BASE_URL + "Xilonen.png"],
    "xingqiu": [BASE_URL + "Xingqiu.png"],
    "xinyan": [
        BASE_URL + "Xinyan_Physical_DPS.png",
        BASE_URL + "Xinyan_Pyro_DPS.png",
        BASE_URL + "Xinyan_Shielder.png"],
    "yae": [BASE_URL + "Yae_Miko.png"],
    "yaemiko": [BASE_URL + "Yane_Miko.png"],
    "yanfei": [BASE_URL + "Yanfei.png"],
    "yaoyao": [BASE_URL + "Yaoyao.png"],
    "yelan": [BASE_URL + "Yelan.png"],
    "yoimiya": [BASE_URL + "Yoimiya.png"],
    "yunjin": [BASE_URL + "Yun_Jin.png"],
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
