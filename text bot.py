from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram import ReplyKeyboardMarkup
import re

TOKEN = "8276185141:AAG9fIGDTghlWa4Ludohyu5ukRgyJMEnATM"

keyboard = ReplyKeyboardMarkup(
    [
        ['📝 Убрать пробелы и переносы'],
        ['📊 Посчитать слова и символы'],
        ['🔤 Преобразовать в заглавные буквы', '🔤 Преобразовать в строчные буквы']
    ],
    resize_keyboard=True
)

async def start(update, context):
    await update.message.reply_text(
        'Приветствую! Отправь мне текст, затем выбери действие ниже с помощью кнопок.',
        reply_markup=keyboard
    )

async def handle_message(update, context):
    text = update.message.text
    user_id = update.effective_user.id

    button_list = ['📝 Убрать пробелы и переносы', '📊 Посчитать слова и символы', '🔤 Преобразовать в заглавные буквы', '🔤 Преобразовать в строчные буквы']

    if text not in button_list:
        context.user_data['last_text'] = text
        await update.message.reply_text('✅ Текст сохранён! Теперь выбери действие.', reply_markup=keyboard)
        return

    if 'last_text' not in context.user_data:
        await update.message.reply_text('❌ Сначала отправь текст!')
        return

    user_text = context.user_data['last_text']

    if text == '📝 Убрать пробелы и переносы':
        cleaned_text = re.sub(r'\s+', ' ', user_text).strip()
        await update.message.reply_text(f'{cleaned_text}')

    elif text == '📊 Посчитать слова и символы':
        chars = len(user_text)
        words = len(user_text.split())
        spaces = user_text.count(' ')
        sentences = len(re.findall(r'[.!?]+', user_text))
        await update.message.reply_text(
            f'**Статистика текста:**\n\n'
            f'• Символов (всего): {chars}\n'
            f'• Символов (без пробелов): {chars - spaces}\n'
            f'• Слов: {words}\n'
            f'• Предложений: {sentences}'
        )

    elif text == '🔤 Преобразовать в заглавные буквы':
        await update.message.reply_text(user_text.upper())

    elif text == '🔤 Преобразовать в строчные буквы':
        await update.message.reply_text(user_text.lower())

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Текстовый бот запущен")
    application.run_polling()

if __name__ == '__main__':
    main()
