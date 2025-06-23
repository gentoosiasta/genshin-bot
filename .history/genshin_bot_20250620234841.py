from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# TOKEN que obtuviste de BotFather
BOT_TOKEN = "8038008029:AAEG4JrZumIHahwa3q1GX5ddXrcGzrdH-TY"

# Diccionario con comandos e imágenes
IMAGENES = {
    "Skirk": "https://ibb.co/VW2W5yNs",
    "skirk": "https://ibb.co/VW2W5yNs",
}

# Función para comandos como /gato, /perro, etc.
async def mostrar_imagen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    comando = update.message.text[1:]  # Remueve el "/"
    imagen_url = IMAGENES.get(comando)

    if imagen_url:
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=imagen_url)
    else:
        await update.message.reply_text("No tengo imagen para ese comando 😿")

# Inicio del bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hola, usa /<nombre_personaje>, por ejemplo /skirk, para ver la build rápidad de dicho personaje")

# Ejecutar el bot
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    for comando in IMAGENES.keys():
        app.add_handler(CommandHandler(comando, mostrar_imagen))

    print("Bot corriendo...")
    app.run_polling()
