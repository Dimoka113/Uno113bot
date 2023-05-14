#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Telegram bot to play UNO in group chats
# Copyright (c) 2016 Jannes Höke <uno@jhoeke.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

# Modify this file if you want a different startup sequence, for example using
# a Webhook
from telegram.ext import Updater
import subprocess

def start_bot(updater: Updater):
    try:
        updater.start_polling(drop_pending_updates=False)
    except:
        subprocess.call(r"C:\Users\Dimoka113\Desktop\Open113\script\error\error.bat")



def start_botskip(updater):
    try:
        updater.start_polling(drop_pending_updates=True)
    except:
        subprocess.call(r"C:\Users\Dimoka113\Desktop\Open113\script\error\error.bat")