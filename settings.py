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

from telegram import ParseMode, InlineKeyboardMarkup, \
    InlineKeyboardButton, Update
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import CommandHandler, Filters, MessageHandler, CallbackContext

from utils import send_async
from user_setting import UserSetting
from shared_vars import dispatcher
from locales import available_locales
from internationalization import _, user_locale

@user_locale
def kb_select(update: Update, context: CallbackContext):
    chat = update.message.chat
    user = update.message.from_user
    us = UserSetting.get(id=user.id)
    
    if us:
        if us.stats == 1:
            stats_text = list()

            n = us.games_played
            stats_text.append(
                _("Игр сыграно: {number}",
                "Игр сыграно: {number}",
                n).format(number=n)
            )

            n = us.first_places
            m = round((us.first_places / us.games_played) * 100) if us.games_played else 0
            stats_text.append(
                _("Выйгранно игр: {number}. ({percent}%)",
                "Выйгранно игр: {number}. ({percent}%)",
                n).format(number=n, percent=m)
            )

            n = us.cards_played
            stats_text.append(
                _("Использованно карт: {number}",
                "Использованно карт: {number}",
                n).format(number=n)
            )
            TEXT_STATS = ('\n'.join(stats_text))
            send_async(context.bot, update.message.chat_id,
                    text="<b>У вас уже была включена статистика!</b> :\n" + TEXT_STATS,
                    parse_mode=ParseMode.HTML)
            return


    us.stats = True
    send_async(context.bot, chat.id, text=_("Статистика включена!"))


@user_locale
def delete_stats(update: Update, context: CallbackContext):
    chat = update.message.chat
    user = update.message.from_user
    us = UserSetting.get(id=user.id)
    if update.message.chat.type != 'private':
        
        if not us or not us.stats:
            send_async(context.bot, chat.id,      
                    text=_("У вас не включена статистика!"))   
            return
        ping = [[InlineKeyboardButton(text=_("Удалить статистику!"), url='https://t.me/Uno113bot?start=stats_del')]]
        send_async(context.bot, chat.id,      
                   text=_("Чтобы удалить всю статистику, нажмите на эту кнопку."),
                    reply_to_message_id=update.message.message_id,
                    reply_markup=InlineKeyboardMarkup(ping),
                    parse_mode=ParseMode.HTML)    
        return
    
    if us:
        if us.stats == 1:
            chat = update.message.chat
            user = update.message.from_user
            us.stats = False
            us.first_places = 0
            us.games_played = 0
            us.cards_played = 0
            send_async(context.bot, chat.id, text=_("Статистика удалена и отключена!"))
        else:
            send_async(context.bot, chat.id,      
                        text=_("У вас не включена статистика!")) 
    else:
        send_async(context.bot, chat.id,      
                    text=_("У вас не включена статистика!")) 

@user_locale
def delete_select(update: Update, context: CallbackContext):
    chat = update.message.chat
    user = update.message.from_user
    us = UserSetting.get(id=user.id)
    if not us or not us.stats:
        send_async(context.bot, chat.id,      
                text=_("У вас не включена статистика!"))   
        return

    if us:
        if us.stats == 1:
            chat = update.message.chat
            user = update.message.from_user
            us.stats = False
            us.first_places = 0
            us.games_played = 0
            us.cards_played = 0
            send_async(context.bot, chat.id, text=_("Статистика удалена и отключена!"))
        else:
            send_async(context.bot, chat.id,      
                        text=_("У вас не включена статистика!")) 
    else:
        send_async(context.bot, chat.id,      
                    text=_("У вас не включена статистика!")) 

@user_locale
def locale_select(update: Update, context: CallbackContext):
    chat = update.message.chat
    user = update.message.from_user
    option = context.match[1]

    if option in available_locales:
        us = UserSetting.get(id=user.id)
        us.lang = option
        _.push(option)
        send_async(context.bot, chat.id, text=_("Установите язык!"))
        _.pop()

def register():
    dispatcher.add_handler(CommandHandler('delstats', delete_stats))