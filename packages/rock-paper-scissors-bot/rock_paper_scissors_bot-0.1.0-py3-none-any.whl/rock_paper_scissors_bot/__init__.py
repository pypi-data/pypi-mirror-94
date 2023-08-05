import os
import sys
import logging

from telegram.ext import (
    Updater, CommandHandler, CallbackQueryHandler,
)

from rock_paper_scissors_bot.handlers import (
    handle_start_game,
    handle_answer
)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    tg_token_env_var = 'TG_TOKEN'
    token = os.getenv(tg_token_env_var)
    if not token:
        sys.stderr.write(f'{tg_token_env_var} not defined')
        exit()

    updater = Updater(token=token, use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler('rock_paper_scissors', handle_start_game))
    dp.add_handler(CallbackQueryHandler(handle_answer))

    updater.start_polling()
    updater.idle()
