from config import TOKEN, WORKERS
import logging
import os
from telegram.ext import Updater

from game_manager import GameManager
from database import db

db.bind('sqlite', os.getenv('UNO_DB', 'uno.sqlite3'), create_db=True)
db.generate_mapping(create_tables=True)

gm = GameManager()
updater = Updater(token=TOKEN, workers=WORKERS, use_context=True)
dispatcher = updater.dispatcher
