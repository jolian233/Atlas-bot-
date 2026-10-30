import os
import telebot
import google.generativeai as genai

# Recuperamos las credenciales de forma segura desde las variables de entorno de Render
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Verificamos que las llaves existan
if not TELEGRAM_TOKEN or not GEMINI_API_KEY:
    raise ValueError("Faltan TELEGRAM_TOKEN o GEMINI_API_KEY en las variables de entorno.")

# Inicializamos Telegram y Gemini
bot = telebot.TeleBot(TELEGRAM_TOKEN)
genai.configure(api_key=GEMINI_API_KEY)

# Configuramos el modelo de Gemini (usamos gemini-1.5-flash por ser rápido y eficiente)
generation_config = {
    "temperature": 0.7,
}
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    generation_config=generation_config
)

@bot.message_handler(commands=['start', 'help'])
class CommandHandler:
    pass

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "¡Hola! Soy **Atlas**, tu asistente personal en la nube 24/7. ¿En qué te puedo ayudar hoy?")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # Enviamos un mensaje de espera o procesamos la respuesta con Gemini
        chat_response = model.generate_content(message.text)
        bot.reply_to(message, chat_response.text)
    except Exception as e:
        bot.reply_to(message, f"Ocurrió un error procesando tu mensaje: {str(e)}")

# Iniciamos el bot en modo Infinity para que corra de forma continua
if __name__ == "__main__":
    print("Atlas está iniciando...")
    bot.infinity_polling()
  
