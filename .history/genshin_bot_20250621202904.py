import os
import sys
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# TOKEN que obtuviste de BotFather
BOT_TOKEN = "8038008029:AAEG4JrZumIHahwa3q1GX5ddXrcGzrdH-TY"

LOCK_FILE = "/tmp/genshin_bot.lock"

# Diccionario con comandos e imágenes
IMAGENES = {
    "skirk": "https://ibb.co/VW2W5yNs",
    "citlali": "https://ibb.co/hJzghc1k",
    "escoffier": "https://ibb.co/nM8jCx8r",

}

# Función para comandos como /gato, /perro, etc.
async def mostrar_imagen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    comando = update.message.text[1:]  # Remueve el "/"
    imagen_url = IMAGENES.get(comando.lower())

    if imagen_url:
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=imagen_url)
    else:
        await update.message.reply_text("No tengo imagen para ese comando 😿")

# Inicio del bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hola, usa /<nombre_personaje>, por ejemplo /skirk, para ver la build rápidad de dicho personaje")

def check_lock():
    if os.path.exists(LOCK_FILE):
        print("Ya hay una instancia en ejecución.")
        sys.exit()
    else:
        with open(LOCK_FILE, "w") as f:
            f.write(str(os.getpid()))

def remove_lock():
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)

# Ejecutar el bot
if __name__ == "__main__":
    try:
        check_lock()

        app = ApplicationBuilder().token(BOT_TOKEN).build()

        app.add_handler(CommandHandler("start", start))
        for comando in IMAGENES.keys():
            app.add_handler(CommandHandler(comando, mostrar_imagen))

        print("Bot corriendo...")
        app.run_polling()

    finally:
        remove_lock()

