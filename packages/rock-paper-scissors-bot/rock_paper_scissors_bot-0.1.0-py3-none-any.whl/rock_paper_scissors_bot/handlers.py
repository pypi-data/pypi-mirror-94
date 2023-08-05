from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from rock_paper_scissors_bot.db import Database

EMOJI = {
    'Paper': '✋',
    'Rock': '✊',
    'Scissors': '✌️',
}


def handle_start_game(update, context):
    keyboard = [
        [
            InlineKeyboardButton(emoji_icon, callback_data=name)
            for name, emoji_icon in EMOJI.items()
        ],
    ]
    update.message.reply_text(
        'Choose:', reply_markup=InlineKeyboardMarkup(keyboard)
    )


def handle_answer(update, context):
    query = update.callback_query
    data_id = query.message.message_id
    data = Database.get_data(data_id)
    if not data:
        data = {
            'user': query.from_user.username,
            'answer': query.data,
        }
        Database.set_data(data_id, data)
        query.answer('You answered first')
        return

    player1 = data['user']
    player2 = query.from_user.username
    if player1 == player2:
        query.answer('Wait for other player!')
        return

    answer1 = data.get('answer')
    answer2 = query.data

    response = f'{player1} {EMOJI[answer1]} vs {player2} {EMOJI[answer2]}:'
    if answer1 == answer2:
        query.answer('Draw')
        query.edit_message_text(text=f'{response} Draw')
        return

    results = {
        ('Paper', 'Rock'): 'Paper',
        ('Paper', 'Scissors'): 'Scissors',
        ('Rock', 'Paper'): 'Paper',
        ('Rock', 'Scissors'): 'Rock',
        ('Scissors', 'Paper'): 'Scissors',
        ('Scissors', 'Rock'): 'Rock'
    }

    players_answers = {
        answer1: player1,
        answer2: player2,
    }

    winning_answer = results[(answer1, answer2)]
    query.edit_message_text(
        text=f'{response} Winner @{players_answers[winning_answer]} {EMOJI[winning_answer]}'
    )
    query.answer('You lost :(' if winning_answer == answer2 else 'You won!')
