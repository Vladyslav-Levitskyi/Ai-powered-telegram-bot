import os
import telebot
from dotenv import load_dotenv
from groq import Groq
from collections import defaultdict
from dotenv import load_dotenv

load_dotenv()

# Вставте ваш токен, отриманий від BotFather
bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN"))

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hello, how can I help you?")

# Створюємо словник для зберігання історії чату для кожного користувача
# Використовуємо defaultdict для автоматичного створення пустого списку для нових користувачів
chat_histories = defaultdict(list)
MAX_HISTORY_LENGTH = 10  # Максимальна кількість повідомлень в історії

def get_groq_response(chat_id, content):
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
    )
    
    messages = [
        {
            "role": "system",
            "content": "You're a helpful, friendly assistant that always provides accurate and informative answers to any questions. Answer each question clearly and concisely, as if you're chatting with someone who wants straightforward information or assistance. If the question isn`t clear, ask for clarification. Remember to keep your tone polite, engaging, and approachable. If you don't understand the question, politely ask the user to clarify."
        }
    ]
    
    # Використовуємо chat_id замість user_id
    for msg in chat_histories[chat_id]:
        messages.append(msg)
    
    messages.append({
        "role": "user",
        "content": content,
    })

    chat_completion = client.chat.completions.create(
        messages=messages,
        model="llama3-70b-8192",
    )

    # Зберігаємо в історію для конкретного чату
    chat_histories[chat_id].append({
        "role": "user",
        "content": content
    })
    chat_histories[chat_id].append({
        "role": "assistant",
        "content": chat_completion.choices[0].message.content
    })
    
    if len(chat_histories[chat_id]) > MAX_HISTORY_LENGTH * 2:
        chat_histories[chat_id] = chat_histories[chat_id][-MAX_HISTORY_LENGTH * 2:]

    return str(chat_completion.choices[0].message.content)

@bot.message_handler(commands=['clear'])
def clear_history(message):
    # Очищення історії конкретного чату
    chat_id = message.chat.id
    chat_histories[chat_id].clear()
    bot.reply_to(message, "Chat history has been cleared!")

@bot.message_handler(func=lambda message: True, content_types=["text"])
def all_other_message(message):
    chat_id = message.chat.id
    response = get_groq_response(chat_id, message.text)
    bot.send_message(chat_id, str(response))

bot.infinity_polling()