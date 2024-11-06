# AI-Powered Telegram Bot

The bot will start listening for messages on Telegram. Use the `/start` or `/help` command to initiate interaction, or type any message to receive an AI-generated response.

## Code Overview

- **get_groq_response(content)**: Sends the user's message to the Groq API, where it generates a response using the Llama 70b model. The system prompt ensures the bot is polite, clear, and engaging.
- **@bot.message_handler(commands=['start', 'help'])**: Responds to the `/start` and `/help` commands with a simple welcome message.
- **@bot.message_handler(func=lambda message: True, content_types=["text"])**: Handles all text messages by passing them to the AI for a response.

## Libraries Used

- **telebot**: To interact with the Telegram API.
- **dotenv**: To manage environment variables securely.
- **Groq**: For connecting to the Groq API and generating AI responses.

## Notes

- Make sure you have your Telegram bot token and Groq API key before starting the bot.
- Ensure that you have set the environment variables correctly in the `.env` file.

## License

MIT

## Copyright

(c) 11-2024 Vladyslav Levytskyi