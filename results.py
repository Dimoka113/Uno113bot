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


"""Defines helper functions to build the inline result list"""

import numbers
from uuid import uuid4

from telegram import InlineQueryResultArticle, InputTextMessageContent, \
    InlineQueryResultCachedSticker as Sticker
import card_dark as cb
import card as c
from utils import display_color, display_color_group, display_name, display_color_dark, display_color_group_dark
from internationalization import _, __


def add_choose_color(results, game):
    """Add choose color options"""
    for color in c.COLORS:
        results.append(
            InlineQueryResultArticle(
                id=color,
                title=_("Выберите цвет"),
                description=display_color(color),
                input_message_content=InputTextMessageContent(
                    display_color_group(color, game))
            )
        )


def add_choose_color_black(results, game):
    """Add choose color options"""
    for color in cb.COLORS:
        results.append(
            InlineQueryResultArticle(
                id=color,
                title=_("Выберите цвет"),
                description=display_color_dark(color),
                input_message_content=InputTextMessageContent(
                    display_color_group_dark(color, game))
            )
        )


def add_other_cards(player, results, game):
    """Add hand cards when choosing colors"""
    player.cards.sort()
    results.append(
        InlineQueryResultArticle(
            "hand",
            title=_("Карта (нажмите, чтобы увидеть состояние игры):",
                    "Карты (нажмите, чтобы увидеть состояние игры):",
                    len(player.cards)),
            description=', '.join([repr(card) for card in (player.cards)]),
            input_message_content=game_info(game)
        )
    )


def player_list(game):
    """Generate list of player strings"""
    return [_("{number}🃏  {name}",
              "{number}🃏  {name}",
              len(player.cards))
            .format(name=player.user.first_name, number=len(player.cards))
            for player in game.players]


def lose_game(results):
    """Add text result if user is losed in game"""
    results.append(
        InlineQueryResultArticle(
            "nogame",
            title=_("Увы, но вы проиграли!"),
            input_message_content=InputTextMessageContent(_('Вы сейчас не играете. Используйте /new чтобы '
                                                            'начать игру или /join, чтобы присоединиться к игре '
                                                            'текущая игра в этой группе'))
        )
    )


def add_no_game(results):
    """Add text result if user is not playing"""
    results.append(
        InlineQueryResultArticle(
            "nogame",
            title=_("Вы не играете!"),
            input_message_content=InputTextMessageContent(_('Вы сейчас не играете. Используйте /new чтобы '
                                                            'начать игру или /join, чтобы присоединиться к игре '
                                                            'текущая игра в этой группе'))
        )
    )


def add_not_started(results):
    """Add text result if the game has not yet started"""
    results.append(
        InlineQueryResultArticle(
            "nogame",
            title=_("Игра еще не началась!"),
            description=("Только создатель игры может поменять режим!"),
            input_message_content=InputTextMessageContent(
                _('Только создатель игры может поменять режим!'))
        )
    )


def add_mode_classic(results):
    """Change mode to classic"""
    results.append(
        InlineQueryResultArticle(
            "mode_classic",
            title=_("🎻 Classic mode"),
            description=(
                "Карты от 0 до 9, разворот, скип, +2, +4, смена цвета"),
            input_message_content=InputTextMessageContent(_('Обычный 🎻'))
        )
    )


def add_mode_fast(results):
    """Change mode to classic"""
    results.append(
        InlineQueryResultArticle(
            "mode_fast",
            title=_("🚀 Sanic mode"),
            description=(
                "Обычная колода карт UNO, игрок пропускается автоматически после истечения времени"),
            input_message_content=InputTextMessageContent(_('Быстрый! 🚀'))
        )
    )


def add_mode_wild(results):
    """Change mode to classic"""
    results.append(
        InlineQueryResultArticle(
            "mode_wild",
            title=_("🐉 Wild mode"),
            description=(
                "Карты от 1 до 5, разворот, скип, +2, +4, смена цвета (Больше спец.карт)"),
            input_message_content=InputTextMessageContent(
                _('В дикой природе~ 🐉'))
        )
    )


def add_mode_super_wild(results):
    """Change mode to classic"""
    results.append(
        InlineQueryResultArticle(
            "mode_super-wild",
            title=_("🔥🐉 SUPER Wild mode"),
            description=(
                "Карта 0, разворот, скип, +2, +4, смена цвета (МНОГО спец.карт)"),
            input_message_content=InputTextMessageContent(
                _('В опасной дикой природе~ 🔥🐉'))
        )
    )


def add_mode_big(results):
    """Change mode to classic"""
    results.append(
        InlineQueryResultArticle(
            "mode_big",
            title=_("🌎 BIG WORLD mode"),
            description=(
                "Обычное UNO, но в начале у вас будет ОЧЕНЬ много карт"),
            input_message_content=InputTextMessageContent(_('В большом мире🌎'))
        )
    )


def add_mode_big_wild(results):
    """Change mode to classic"""
    results.append(
        InlineQueryResultArticle(
            "mode_big",
            title=_("🌎 BIG WORLD mode"),
            description=(
                "Обычное UNO, но в начале у вас будет ОЧЕНЬ много карт"),
            input_message_content=InputTextMessageContent(_('В большом мире🌎'))
        )
    )


def add_mode_big_wild(results):
    """Change mode to classic"""
    results.append(
        InlineQueryResultArticle(
            "mode_big-wild",
            title=_("🌎🐉 BIG WORLD wild TEXT mode"),
            description=(
                "Обычное UNO, но в начале у вас будет ОЧЕНЬ много карт и "),
            input_message_content=InputTextMessageContent(
                _('В большом диком мире🌎🐉'))
        )
    )

def add_mode_big_wild_text(results):
    """Change mode to classic"""
    results.append(
        InlineQueryResultArticle(
            "mode_big-wild-text",
            title=_("🌎🐉✍️ BIG WORLD wild mode"),
            description=(
                "Обычное UNO, но в начале у вас будет ОЧЕНЬ много карт (Больше спец.карт)"),
            input_message_content=InputTextMessageContent(
                _('В большом диком текстовом мире🌎🐉✍️'))
        )
    )


def add_mode_big_text(results):
    """Change mode to classic"""
    results.append(
        InlineQueryResultArticle(
            "mode_big-text",
            title=_("🌎✍️ BIG WORLD TEXT mode"),
            description=(
                "Обычное UNO, но в начале у вас будет ОЧЕНЬ много карт (Больше спец.карт)"),
            input_message_content=InputTextMessageContent(
                _('В большом текстовом мире🌎✍️'))
        )
    )


def add_mode_super_wild_text(results):
    """Change mode to classic"""
    results.append(
        InlineQueryResultArticle(
            "mode_super-wild-text",
            title=_("🔥🐉✍️ SUPER Wild TEXT mode"),
            description=(
                "Карта 0, разворот, скип, +2, +4, смена цвета (МНОГО спец.карт, текстовый режим)"),
            input_message_content=InputTextMessageContent(
                _('В опасной тихой текстовой природе~ 🔥🐉✍️'))
        )
    )


def add_mode_num_text(results):
    """Change mode to classic"""
    results.append(
        InlineQueryResultArticle(
            "mode_number-text",
            title=_("🔢✍️ NUMBER text mode"),
            description=(
                "Карты от 0 до 9, из спец.карт: +4, смена цвета (текстовый режим)"),
            input_message_content=InputTextMessageContent(
                _('Число-текстовый 🔢✍️'))
        )
    )


def add_mode_num(results):
    """Change mode to classic"""
    results.append(
        InlineQueryResultArticle(
            "mode_number",
            title=_("🔢 NUMBER mode"),
            description=("Карты от 0 до 9, из спец.карт: +4, смена цвета"),
            input_message_content=InputTextMessageContent(_('Числовой 🔢'))
        )
    )


def add_mode_text(results):
    """Change mode to text"""
    results.append(
        InlineQueryResultArticle(
            "mode_text",
            title=_("✍️ Text mode"),
            description=(
                "Карты от 0 до 9, разворот, скип, +2, +4, смена цвета (текстовый режим)"),
            input_message_content=InputTextMessageContent(_('Текст ✍️'))
        )
    )


def add_mode_text_wild(results):
    """Change mode to text"""
    results.append(
        InlineQueryResultArticle(
            "mode_text-wild",
            title=_("🐉✍️ Text-Wild mode"),
            description=(
                "Карты от 1 до 5, разворот, скип, +2, +4, смена цвета (Больше спец.карт, текстовый режим)"),
            input_message_content=InputTextMessageContent(_('🐉✍️ Дикий Текст'))
        )
    )


def add_mode_inverse_text(results):
    """Change mode to inverse text"""
    results.append(
        InlineQueryResultArticle(
            "mode_inverse-text",
            title=_("🔁✍️ INVERSE text mode"),
            description=(
                "В этом игровом режиме МОЖНО кидать карты которые НЕЛЬЗЯ! И НАОБОРОТ! (Текстовый режим)"),
            input_message_content=InputTextMessageContent(
                _('Inverse-текстовый 🔁✍️'))
        )
    )


def add_mode_inverse(results):
    """Change mode to classic"""
    results.append(
        InlineQueryResultArticle(
            "mode_inverse",
            title=_("🔁 INVERSE mode"),
            description=(
                "В этом игровом режиме МОЖНО кидать карты которые НЕЛЬЗЯ! И НАОБОРОТ!"),
            input_message_content=InputTextMessageContent(_('Inverse 🔁'))
        )
    )


def add_not_bignumber(results):
    """Change mode to classic"""
    results.append(
        InlineQueryResultArticle(
            f"not_bignumber", 
            title=_(f"⚙️Вы указали слишком много карт! (максимум 35)"),
            description=(
                f"Обычное UNO, но в начале у вас будет то кол-во карт, которое вы укажите."),
            input_message_content=InputTextMessageContent(
                _(f'⚙️Вы указали слишком много карт! (Макс. 35)'))
        )
    )





def add_not_big_settigs(results):
    """Change mode to classic"""
    results.append(
        InlineQueryResultArticle(
            f"not_number",
            title=_(f"⚙️BIG settings mode (Введите кол-во)"),
            description=(
                f"Обычное UNO, но в начале у вас будет то кол-во карт, которое вы укажите."),
            input_message_content=InputTextMessageContent(
                _(f'⚙️Вы не указали количество карт!'))
        )
    )




def add_mode_big_settigs(results, nun):
    """Change mode to classic"""
    text_nun = f"Кол-во карт: {nun}"
    results.append(
        InlineQueryResultArticle(
            f"mode_big-sets_{nun}",
            title=_(f"⚙️BIG settings mode ({text_nun})"),
            description=(
                f"Обычное UNO, но в начале у вас будет то кол-во карт, которое вы укажите."),
            input_message_content=InputTextMessageContent(
                _(f'В настраиваемом мире⚙️({text_nun})'))
        )
    )

def add_mode_bigtext_settigs(results, nun):
    """Change mode to classic"""
    text_nun = f"Кол-во карт: {nun}"
    results.append(
        InlineQueryResultArticle(
            f"mode_big-sets-text_{nun}",
            title=_(f"⚙️✍️BIG settings mode ({text_nun})"),
            description=(
                f"Обычное UNO, но в начале у вас будет то кол-во карт, которое вы укажите."),
            input_message_content=InputTextMessageContent(
                _(f'В настраиваемом текстовом мире⚙️✍️({text_nun})'))
        )
    )

def add_mode_random_settigs(results):
    """Change mode to classic"""
    results.append(
        InlineQueryResultArticle(
            f"mode_random",
            title=_(f"🪐Random mode"),
            description=(
                f"Обычное UNO, но при кажом ходе у каждого игрока будут меняться карты"),
            input_message_content=InputTextMessageContent(
                _(f'В рандомном мире🪐'))
        )
    )

def add_mode_random_text_settigs(results):
    """Change mode to classic"""
    results.append(
        InlineQueryResultArticle(
            f"mode_random-text",
            title=_(f"🪐✍️Random text mode"),
            description=(
                f"Обычное UNO, но при кажом ходе у каждого игрока будут меняться карты"),
            input_message_content=InputTextMessageContent(
                _(f'В рандомном текстовом мире🪐✍️'))
        )
    )




def add_all_modes(results):
    """All modes"""
    add_mode_classic(results)
    add_mode_text(results)

    add_mode_fast(results)

    add_mode_wild(results)
    add_mode_text_wild(results)

    add_mode_super_wild(results)
    add_mode_super_wild_text(results)

    add_mode_inverse(results)
    add_mode_inverse_text(results)

    add_mode_num(results)
    add_mode_num_text(results)

    add_mode_big(results)
    add_mode_big_text(results)

    add_mode_big_wild(results)
    add_mode_big_wild_text(results)
    
    add_mode_random_settigs(results)
    add_mode_random_text_settigs(results)

def add_text_modes(results):
    """Text modes"""
    add_mode_text(results)
    add_mode_text_wild(results)
    add_mode_super_wild_text(results)
    add_mode_inverse_text(results)
    add_mode_num_text(results)
    add_mode_big_text(results)
    add_mode_big_wild_text(results)
    add_mode_random_text_settigs(results)

def add_none_text_modes(results):
    """None text modes"""
    add_mode_classic(results)
    add_mode_fast(results)
    add_mode_wild(results)
    add_mode_super_wild(results)
    add_mode_inverse(results)
    add_mode_num(results)
    add_mode_big(results)
    add_mode_big_wild(results)
    add_mode_random_settigs(results)


def add_draw(player, results):
    """Add option to draw"""
    n = player.game.draw_counter or 1

    results.append(
        Sticker(
            "draw", sticker_file_id=c.STICKERS['option_draw'],
            input_message_content=InputTextMessageContent(__('Взял(а) {number} карту',
                                                             'Взял(а) {number} карт(ы)', n,
                                                             multi=player.game.translate)
                                                          .format(number=n))
        )
    )


def add_gameinfo(game, results):
    """Add option to show game info"""

    results.append(
        Sticker(
            "gameinfo",
            sticker_file_id=c.STICKERS['option_info'],
            input_message_content=game_info(game)
        )
    )


def add_pass(results, game):
    """Add option to pass"""
    results.append(
        Sticker(
            "pass", sticker_file_id=c.STICKERS['option_pass'],
            input_message_content=InputTextMessageContent(
                __('Пропускаю', multi=game.translate)
            )
        )
    )


def add_call_bluff(results, game):
    """Add option to call a bluff"""
    results.append(
        Sticker(
            "call_bluff",
            sticker_file_id=c.STICKERS['option_bluff'],
            input_message_content=InputTextMessageContent(__("Я думаю, это блеф!",
                                                             multi=game.translate))
        )
    )


def add_card(game, card, results, can_play):
    """Add an option that represents a card"""

    if game.color_mode == "white":
        if can_play:
            if str(game.mode).lower().find('text') == -1:
                results.append(
                    Sticker(str(card), sticker_file_id=c.STICKERS[str(card)])
                )
            if str(game.mode).lower().find('text') != -1:
                results.append(
                    Sticker(str(card), sticker_file_id=c.STICKERS[str(card)], input_message_content=InputTextMessageContent("Кинул карту: {card}".format(card=repr(card).replace('Беру +4', '+4').replace('Беру +2', '+2').replace('Меняю цвет', 'Color selection')))
                            ))
        else:
            results.append(
                Sticker(f"game_info_{uuid4()}", sticker_file_id=c.STICKERS_GREY[str(card)],
                        input_message_content=game_info(game))
            )
    elif game.color_mode == "black":
        if can_play:
            if str(game.mode).lower().find('text') == -1:
                results.append(
                    Sticker(str(card), sticker_file_id=cb.STICKERS[str(card)])
                )
            if str(game.mode).lower().find('text') != -1:
                results.append(
                    Sticker(str(card), sticker_file_id=cb.STICKERS[str(card)], input_message_content=InputTextMessageContent("Кинул карту: {card}".format(card=repr(card).replace('Беру +4', '+4').replace('Беру +2', '+2').replace('Меняю цвет', 'Color selection')))
                            ))
        else:
            results.append(
                Sticker(f"game_info_{uuid4()}", sticker_file_id=cb.STICKERS_GREY[str(card)],
                        input_message_content=game_info(game))
            )
    elif game.color_mode == "flip":
        if game.flip_color == "white":
            if can_play:
                if str(game.mode).lower().find('text') == -1:
                    results.append(
                        Sticker(
                            str(card), sticker_file_id=c.STICKERS[str(card)])
                    )
                if str(game.mode).lower().find('text') != -1:
                    results.append(
                        Sticker(str(card), sticker_file_id=c.STICKERS[str(card)], input_message_content=InputTextMessageContent("Кинул карту: {card}".format(card=repr(card).replace('Беру +4', '+4').replace('Беру +2', '+2').replace('Меняю цвет', 'Color selection')))
                                ))
            else:
                results.append(
                    Sticker(f"game_info_{uuid4()}", sticker_file_id=c.STICKERS_GREY[str(card)],
                            input_message_content=game_info(game))
                )
        elif game.flip_color == "black":
            if can_play:
                if str(game.mode).lower().find('text') == -1:
                    results.append(
                        Sticker(
                            str(card), sticker_file_id=cb.STICKERS[str(card)])
                    )
                if str(game.mode).lower().find('text') != -1:
                    results.append(
                        Sticker(str(card), sticker_file_id=cb.STICKERS[str(card)], input_message_content=InputTextMessageContent("Кинул карту: {card}".format(card=repr(card).replace('Беру +4', '+4').replace('Беру +2', '+2').replace('Меняю цвет', 'Color selection')))
                                ))
            else:
                results.append(
                    Sticker(f"game_info_{uuid4()}", sticker_file_id=cb.STICKERS_GREY[str(card)],
                            input_message_content=game_info(game))
                )


def game_info_text(game):
    players = player_list(game)
    return (
        _("Текущий игрок: {name}")
        .format(name=display_name(game.current_player.user)) +
        "\n" +
        _("Последняя карта: {card}").format(card=repr(game.last_card)) +
        "\n" +
        _("Игрок: {player_list}",
          "Игроки:\n• {player_list}",
          len(players))
        .format(player_list="\n• ".join(players))
    )


def game_info(game):
    return InputTextMessageContent(game_info_text(game))


def add_color_replace(results):
    add_color_white(results)
    add_color_black(results)
    add_color_flip(results)


def add_color_black(results):
    results.append(
        InlineQueryResultArticle(
            "colormode_black",
            title=_("🖤 Черные карты"),
            description=("Изменить оформление карт на чёрный"),
            input_message_content=InputTextMessageContent(_('🖤 Черные карты'))
        )
    )


def add_color_white(results):
    results.append(
        InlineQueryResultArticle(
            "colormode_white",
            title=_("🤍 Белые карты"),
            description=("Изменить оформление карт на белый"),
            input_message_content=InputTextMessageContent(_('🤍 Белые карты'))
        )
    )


def add_color_flip(results):
    """Change mode to classic"""
    results.append(
        InlineQueryResultArticle(
            "colormode_flip",
            title=_("🔀 Flip карты"),
            description=("В это колоде используется карты уно FLIP!"),
            input_message_content=InputTextMessageContent(_("Flip 🔀"))
        )
    )
