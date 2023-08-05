import shelve


class Database:
    db_name = 'rps_bot_data'

    @classmethod
    def get_data(cls, chat_id):
        with shelve.open(cls.db_name) as db:
            return db.get(str(chat_id))

    @classmethod
    def set_data(cls, chat_id, data):
        with shelve.open(cls.db_name) as db:
            db[str(chat_id)] = data
            db.sync()
