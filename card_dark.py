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


# Colors
WHITE = 'w'
PINK = 'p'
GREEN = 'g'
ORANGE = 'o'
BLACK = 'x'

COLORS = (WHITE, PINK, GREEN, ORANGE)

COLOR_ICONS = {
    WHITE: '🤍',
    PINK: '💜',
    GREEN: '💚',
    ORANGE: '🧡',
    BLACK: '⬛️'
}

    # RED: '❤️',
    # BLUE: '💙',
    # GREEN: '💚',
    # YELLOW: '💛',
    # BLACK: '⬛️'

    # RED = 'r'
    # BLUE = 'b'
    # GREEN = 'g'
    # YELLOW = 'y'
    # BLACK = 'x'

# Values
ZERO = '0'
ONE = '1'
TWO = '2'
THREE = '3'
FOUR = '4'
FIVE = '5'
SIX = '6'
SEVEN = '7'
EIGHT = '8'
NINE = '9'
DRAW_TWO = '+2'
REVERSE = 'Реверс'
SKIP = 'Пропуск хода'

VALUES = (ZERO, ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE, DRAW_TWO,
          REVERSE, SKIP)
WILD_VALUES = (ONE, TWO, THREE, FOUR, FIVE, DRAW_TWO, REVERSE, SKIP)
SUPER_WILD_VALUES = (DRAW_TWO, REVERSE, SKIP, DRAW_TWO, REVERSE, DRAW_TWO, ZERO, ZERO)
NUMBER_VALUES = (ZERO, ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE)


# Special cards
CHOOSE = 'Смена цвета'
DRAW_FOUR = '+4'
FLIP_CARD = 'Переворот карт'

SPECIALS = (CHOOSE, DRAW_FOUR)

SPECIALS_FLIP = (CHOOSE, DRAW_FOUR, FLIP_CARD)



STICKERS = {
    'p_0': 'CAACAgIAAx0CbhAEhQACYMFj-LN59QAB8_O7FqEWowAByyGYJhqvAAK8IgACE9TBS9Y5q3-zQHrZLgQ',
    'p_1': 'CAACAgIAAx0CbhAEhQACYMNj-LN-1JPxjDDh7TsooA58Jr759wACvyEAAmmxwEvNNztyS7sByC4E',
    'p_2': 'CAACAgIAAx0CbhAEhQACYMVj-LOD4dKy8DXLBbFWyjokTlbpvwACnCcAAil6yEsNKCghtUbWZC4E',
    'p_3': 'CAACAgIAAx0CbhAEhQACYMdj-LOHTSLNqzEckYsoHtFrOeY1TwACAygAAt99yEu1eN46-C26zS4E',
    'p_4': 'CAACAgIAAx0CbhAEhQACYMlj-LOLVv0sldJS3EH7W4MonzmiGgACBiwAAtCcwEteH8SdCdLuNC4E',
    'p_5': 'CAACAgIAAx0CbhAEhQACYMtj-LOPEqvhE20Myc51yw7ek3jXCwACDSUAAubdwUsFIM5v2b5XaS4E',
    'p_6': 'CAACAgIAAx0CbhAEhQACYM1j-LOTi-jlWwZWcLe6GpBJz3EDWwACVCEAAg_nyEsvVEEqoLFg9y4E',
    'p_7': 'CAACAgIAAx0CbhAEhQACYM9j-LOYTTgIDTlPQgPv-zyoLyZVLQACSycAAqlQwEs999aBgJQDRy4E',
    'p_8': 'CAACAgIAAx0CbhAEhQACYNFj-LOd3uwChGIrELdTcxsfo91augACGyEAAiTkwUuPHvEJqyBLay4E',
    'p_9': 'CAACAgIAAx0CbhAEhQACYNNj-LOgedMDqZ61CrvapbSLg8BaZgACcx4AAgGtyEv6udYwOMX4jy4E',
    'p_+2': 'CAACAgIAAx0CbhAEhQACYNVj-LOksvI8B4-y09qrB5A8E4uWIgACVSUAAsCMwEtWpmuBV7l4ey4E',
    'p_Пропуск хода': 'CAACAgIAAx0CbhAEhQACYNlj-LOsR2hszx7VHSCJFGTwGSjo8AACWSIAAhRiwEuIMUlnYuNV_C4E',
    'p_Реверс': 'CAACAgIAAx0CbhAEhQACYNdj-LOo-fzyn_S46Zl9nkQvjA9_0gACFCYAAlXywUsCTUbQznZLvi4E',
    'g_0': 'CAACAgIAAxkBAAKPumP4rzz31WMK7YtFMcAMkNZbAAFGJQACvyQAAnZMyEsrFjHgqQWNEi4E',
    'g_1': 'CAACAgIAAxkBAAKPvGP4rz3i0-G29XZd9dZQnkNHNWoeAAKyIwACEWbIS1O3HKOtwJXGLgQ',
    'g_2': 'CAACAgIAAxkBAAKPvmP4rz9fkyzWpwJ8EyuKDaZSSRfNAAL2IgACou3IS6AMamTLxkXRLgQ',
    'g_3': 'CAACAgIAAxkBAAKPwGP4r0DMy_Hwl7c3FsdLuJ9eoNFHAAJyJAACnp_BS9H_P5rX4-QgLgQ',
    'g_4': 'CAACAgIAAxkBAAKPwmP4r0IpKX-YhxYpvp0ONZhCJRrOAAIZKAACZHzBS97KJ3aAIPWILgQ',
    'g_5': 'CAACAgIAAxkBAAKPxGP4r0SReUEAAbDGOo7Dj6UUZGmMEwACHSgAAsufwUsVbDv_rAABja8uBA',
    'g_6': 'CAACAgIAAxkBAAKPxmP4r0asWIHY2V16Mw_qT_7VV2aeAAJ_JgACzh_AS4NQKBHjXsadLgQ',
    'g_7': 'CAACAgIAAxkBAAKPyGP4r0dWwES6gwABMIwIbXgOKKqbXQACLyMAAmP-yEuEhVn1Q0JezC4E',
    'g_8': 'CAACAgIAAxkBAAKPymP4r0mfruNHOtBjigABcxwCB5TNgQACdCYAAubeyUtY_7ZzK_8WTC4E',
    'g_9': 'CAACAgIAAxkBAAKPzGP4r2pGuAeofdBIJiyAz3IhzROZAAL1IwACr5rJS0i-EwpRMAnwLgQ',
    'g_+2': 'CAACAgIAAxkBAAKP0GP4r3GCZUtbLTP6IT4vfhL2q9jjAAIkKAACGKHBS9G-WlxCtMKYLgQ',
    'g_Пропуск хода': 'CAACAgIAAxkBAAKP1GP4r3RiDy8NT5XjCS5sb-3fpBdpAAJ3JAACGk3AS6IPF4lmUJQlLgQ',
    'g_Реверс': 'CAACAgIAAxkBAAKP0mP4r3K7hje4_zHj3wraSmLcn-UHAAL6JgACUNTBS5Wbzs4l0Ex2LgQ',
    'w_0': 'CAACAgIAAx0CbhAEhQACYNtj-LOw1FlGrcict7fmu_bePPhIlgACIiwAAqCWyEsn8AABd1o00NIuBA',
    'w_1': 'CAACAgIAAx0CbhAEhQACYN1j-LOzrE_AknFfz6wDy6XCa599dgACWiYAAi4JwUsh_OzaiIV1TC4E',
    'w_2': 'CAACAgIAAx0CbhAEhQACYN9j-LO3CKIcJzv_BH_ug1QalWtfjQACGCgAAnYfwEuqPDzvi1q7Ji4E',
    'w_3': 'CAACAgIAAx0CbhAEhQACYOFj-LO6Fv3uTbnd2z0VNtnLSEhnpQACtCUAArQIyEtR3HFOQPzg6C4E',
    'w_4': 'CAACAgIAAx0CbhAEhQACYONj-LO-RzGkXhwzoCSDcuzrfq0PjQACBSgAAsSwyUt5N0GI94zfOi4E',
    'w_5': 'CAACAgIAAx0CbhAEhQACYOVj-LPCAAF_TO1n2zVcAAFcvglk7XwkAAKgHwACKbjIS9WdZxS5OFlyLgQ',
    'w_6': 'CAACAgIAAx0CbhAEhQACYOdj-LPGj3zBGzQZhnZ8Da2-kX3-3gAC4yQAArBlyUuyq8tchLjRFy4E',
    'w_7': 'CAACAgIAAx0CbhAEhQACYOlj-LPKL1b089_DNbyXv-_cQvyNVAACsSgAAkrjyEsdvH9a0cyXii4E',
    'w_8': 'CAACAgIAAx0CbhAEhQACYOtj-LPP9p2cF9NJdjFwBUkh_1GUzgAC-CYAAliLwUtv6OsenqDo5C4E',
    'w_9': 'CAACAgIAAx0CbhAEhQACYO1j-LPTO5Bd0f8JTb0c7Or9koVvzgACeyEAAtBfyUskM6GtWs9OnS4E',
    'w_+2': 'CAACAgIAAx0CbhAEhQACYO9j-LPY7NvmY3CvqhaLlxDxRW_hVwACKisAAnbSwEsVnGUL0VHa1C4E',
    'w_Пропуск хода': 'CAACAgIAAx0CbhAEhQACYPNj-LPlsTjAgPYOiQeZU0SH0QLP5QAC3ycAAorNyEvQat_olWIfZi4E',
    'w_Реверс': 'CAACAgIAAx0CbhAEhQACYPFj-LPhn4ddCGT41-Hh3lA-Ud2XEwAC-yEAAoRZyUunm3IVdeVaPi4E',
    'o_0': 'CAACAgIAAxkBAAKP1mP4s1cuLXXlIosG78AmvwMaTxuUAAL5IgACgFfIS2gtkT7ZaJPeLgQ',
    'o_1': 'CAACAgIAAx0CbhAEhQACYKlj-LNGiGHQJO_wN3sMnyaR9OCSwwAC-iQAAsw4yEs3iXGEya1q1y4E',
    'o_2': 'CAACAgIAAx0CbhAEhQACYKtj-LNLG5zN_HjAJYqu7tSlSXO9WAACpygAAgaWwUttLLvIBe597i4E',
    'o_3': 'CAACAgIAAx0CbhAEhQACYK1j-LNPxAIq0lMhcYGYbxWOtIWZ1AACXCUAAnSvwUsMh8vYCVaVVC4E',
    'o_4': 'CAACAgIAAx0CbhAEhQACYK9j-LNTXpMmBP2xISGwLTVzDA49VAACwSsAAnVHyUvqwEZMnV9A9C4E',
    'o_5': 'CAACAgIAAx0CbhAEhQACYLFj-LNWJKWNQkj8Zf9s_zkKJVHd0wACSSEAAludwEvcPkWbD7PsRS4E',
    'o_6': 'CAACAgIAAx0CbhAEhQACYLNj-LNajQ6h2kTfTQG5nVJIWwhk3AACsygAAn_gwUtS4Ql3oWvYay4E',
    'o_7': 'CAACAgIAAx0CbhAEhQACYLVj-LNdizDBRkXdShYEZ3agPw24VAAC4CUAAh-ryEv-ZA6CmcFg5C4E',
    'o_8': 'CAACAgIAAx0CbhAEhQACYLdj-LNitp_uzlTjpV53TC3zCXm2awACjiEAAi7XwUswgDvQblpVGS4E',
    'o_9': 'CAACAgIAAx0CbhAEhQACYLlj-LNmM-Dbk8u5QXCMNBrGWj5vVQACCiQAAnv4wUtEi0gkzOSwSS4E',
    'o_+2': 'CAACAgIAAx0CbhAEhQACYLtj-LNqyRGGS96Yc9g-AbPfApYmYQACKSkAAvGUyEtKuazvxX89zi4E',
    'o_Пропуск хода': 'CAACAgIAAx0CbhAEhQACYL9j-LNxppn44WTqCNGmqhbiFaAVngACfCQAAvw9wEvdgn3YCWdIhC4E',
    'o_Реверс': 'CAACAgIAAx0CbhAEhQACYL1j-LNuFUf9TcY5TyEoBSjBSD49-AACrSwAAphpwEutzCUHXh3L0S4E',
    '+4': 'CAACAgIAAx0CbhAEhQACYPdj-LPsdkgqhCGo0bG8Z8F3HDgYqgACzygAAk9XyEtsEFN9dVmiki4E',
    'Смена цвета': 'CAACAgIAAx0CbhAEhQACYPVj-LPpgSBQePgun2cJHCIidQ0XswACmiMAAlVPyUsM7XWKUtWqBy4E',
    'Переворот карт': 'CAACAgIAAxkBAAKP6GP7HU_RnN8paAWAu_5Xo_NarUPOAAItKQACd_PYS2Cn2gABRAu6si4E',
    'option_draw': 'BQADBAAD-AIAAl9XmQABxEjEcFM-VHIC',
    'option_pass': 'BQADBAAD-gIAAl9XmQABcEkAAbaZ4SicAg',
    'option_bluff': 'BQADBAADygIAAl9XmQABJoLfB9ntI2UC',
    'option_info': 'BQADBAADxAIAAl9XmQABC5v3Z77VLfEC'
}

STICKERS_GREY = {
    'p_0': 'CAACAgIAAx0CbhAEhQACYrFj-VNE7i0UCqJePZMl5m06NP2-WgACEywAAsZSyEtoXJeJUlMOii4E',
    'p_1': 'CAACAgIAAx0CbhAEhQACYrNj-VNKiBgkYZRBBwkjRT0vV0wxiQACQSQAAg8q0EsCFM6sAAHibhkuBA',
    'p_2': 'CAACAgIAAxkBAAKP3mP5VLFuCLNUAfw8MY1xpDSCGNQCAAJbKwACP2zJS0sR68HOzDRkLgQ',
    'p_3': 'CAACAgIAAx0CbhAEhQACYrVj-VNYl9FzzndhNTOdz21wbc4EUwACbCUAAvFo0UuOrAPMpIWyNS4E',
    'p_4': 'CAACAgIAAx0CbhAEhQACYrdj-VNgE4AfpyCNTM9Q2avuJj226AACPTUAAuuHyUue_3SvH4VBny4E',
    'p_5': 'CAACAgIAAx0CbhAEhQACYrlj-VNmfOznG3OYQaNDzsFEAYDg0AACJioAAormyEsIPs0lsLtpUC4E',
    'p_6': 'CAACAgIAAx0CbhAEhQACYrtj-VNucTIAAYVtGojnBXW2rvIcBJoAAjIvAAJf2shLP3bEG0Z0AAHlLgQ',
    'p_7': 'CAACAgIAAx0CbhAEhQACYr1j-VN30egk4OkTZuOVMYzsOH4WxAAC1yIAAi090EvFw5hiSVK3pC4E',
    'p_8': 'CAACAgIAAx0CbhAEhQACYr9j-VN-nE2ysTrISTH2_vekbp6v0AACmCsAAuChyEv4woAP3hwAAZYuBA',
    'p_9': 'CAACAgIAAx0CbhAEhQACYsFj-VOE2E4eE-1qTK_qi6KVJdNYvgACHjEAAk7-yUsMOdkSpUu3Ui4E',
    'p_+2': 'CAACAgIAAx0CbhAEhQACYsNj-VONRP2_Q7hVVgmeguCiRY3epwACdCoAAqrVyUs34CByTZ_8Zi4E',
    'p_Пропуск хода': 'CAACAgIAAx0CbhAEhQACYsdj-VOcPryPrXn1kAI0DLscSYdIrQACASEAAr-n0UtkCSZqaxEnKS4E',
    'p_Реверс': 'CAACAgIAAx0CbhAEhQACYsVj-VOWp-6mQe0umjTSKGHyujRbYQAC9CIAAsMq0Est5wZEbs0AAQIuBA',
    'g_0': 'CAACAgIAAx0CbhAEhQACYldj-VGyK4laOvULUFjAK0tXzutvfAAC_SYAAqMqyEvQdSMvqX-7YC4E',
    'g_1': 'CAACAgIAAx0CbhAEhQACYllj-VGzSuuRA_MU_-X1Swv1oIMq8QACfi4AAiE8yUuDnYv7c0QaFS4E',
    'g_2': 'CAACAgIAAx0CbhAEhQACYltj-VGzRas4lo4k-9jG3X9UEBczSAACsSwAAgcjyUsYU7t6eNdJ3y4E',
    'g_3': 'CAACAgIAAx0CbhAEhQACYl1j-VG00Y0RAAEtZYeoQF-nnPeG4pIAAj0kAALSl9FLnOrxLP2BZj8uBA',
    'g_4': 'CAACAgIAAx0CbhAEhQACYnNj-VIBHLR2SPiQcVFzL93bze101gACLyQAAs1N0EtjlB8j0gx7bC4E',
    'g_5': 'CAACAgIAAx0CbhAEhQACYnFj-VH4gn-8WxXy6lHhhH8HHrVUzQACbCQAAhh30UvQwcsMSVuNai4E',
    'g_6': 'CAACAgIAAx0CbhAEhQACYnVj-VIIhBnDgQs-BYp4hOtI9SrpewAC7CIAAg1f0Utztn50ccDayC4E',
    'g_7': 'CAACAgIAAx0CbhAEhQACYndj-VIOC5FGlE9DbLB2HHfvyniI_QACbCAAAv760EtvPavwjRVRpC4E',
    'g_8': 'CAACAgIAAx0CbhAEhQACYnlj-VIWXGqukYFF5FR7cquAVlOuawACwiEAAk330UsLAAGahPYyIzcuBA',
    'g_9': 'CAACAgIAAx0CbhAEhQACYnlj-VIWXGqukYFF5FR7cquAVlOuawACwiEAAk330UsLAAGahPYyIzcuBA',
    'g_+2': 'CAACAgIAAx0CbhAEhQACYn1j-VIhYx0ocphlT3Q9m4DLh7N-hAACkyEAAm6b0Uu-xTZI6exmuy4E',
    'g_Пропуск хода': 'CAACAgIAAx0CbhAEhQACYoFj-VIxOPV8Nl9KXgYaQ94juBY8lwACSycAAr4cyEuNA8_WKYaymi4E',
    'g_Реверс': 'CAACAgIAAxkBAAKP9mP9Bzgu7MVTV7aX1oG2ShMDNpvLAAI9LAACw2zJS-5GjHwM5JULLgQ',
    'w_0': 'CAACAgIAAx0CbhAEhQACYslj-VOkVaZck_Ashr_Y3von18eT9wACZS8AAndMyEuMBI4Qjy98Fy4E',
    'w_1': 'CAACAgIAAx0CbhAEhQACYstj-VOtJCiuVRYuzZJ5tK-h2aQoYAACdSsAArJzyEsAAbHXfcYf8VguBA',
    'w_2': 'CAACAgIAAx0CbhAEhQACYs1j-VOyQChopbv5If8BoQ2LmsZTwwACvSMAAtLT0EuHs3bgQJbEli4E',
    'w_3': 'CAACAgIAAx0CbhAEhQACYs9j-VO4YdJdIxsNTCRqa8DI9nA_HgACiScAAiT5yUu-dgU0i9xM9C4E',
    'w_4': 'CAACAgIAAx0CbhAEhQACYtFj-VO-sb67njZKK4E1fwptsjQXUQACkikAAsBvyEvFUaAsMOgxxy4E',
    'w_5': 'CAACAgIAAx0CbhAEhQACYtNj-VPFI013wAFhqxW7xg-FockupgACpyoAAteayEsLPEOtSkJPHS4E',
    'w_6': 'CAACAgIAAx0CbhAEhQACYtVj-VPJv5qAbepKt7QFWE0ZOzDeBQACwSUAAntC0Uuk4N8td87d1C4E',
    'w_7': 'CAACAgIAAx0CbhAEhQACYtdj-VPP2wqx03P3g0g9ya52xo7YegACIScAAoOh0Uu_nTF65ZwAAb8uBA',
    'w_8': 'CAACAgIAAx0CbhAEhQACYttj-VPauZpVnwe84QOmUvnAmRw7QAACzS0AAs3-yUu50U7NWuRELi4E',
    'w_9': 'CAACAgIAAx0CbhAEhQACYtlj-VPVXCIsZyg9nvTi6ywAAU5ZKVAAAtkoAAKfIchL5kmbzUxMEXcuBA',
    'w_+2': 'CAACAgIAAx0CbhAEhQACYt1j-VPhI6-ElfgSkou_-HkwpXH_ewAC7ykAAtbCyUtVlWykjv6OHC4E',
    'w_Пропуск хода': 'CAACAgIAAx0CbhAEhQACYuNj-VPyHtGBAVsP3j197VFiG-CGUAAC4yQAAiDtyEuevgXhLD86ci4E',
    'w_Реверс': 'CAACAgIAAx0CbhAEhQACYuFj-VPrhG3KHmDQmX2PIz7V6XBTsgACJiMAApiq0EuU2wABrIuyAR0uBA',
    'o_0': 'CAACAgIAAx0CbhAEhQACYqNj-VK_c2Zr1tBPHIYjZih1ZwUGTgACvysAApiFyEvQX_M2ZgGCXy4E',
    'o_1': 'CAACAgIAAx0CbhAEhQACYqFj-VKnrCv0dHy1brRH2u6rsVl_OwACfisAAt1OyUvkcG2w03ADxy4E',
    'o_2': 'CAACAgIAAx0CbhAEhQACYp9j-VKhFgbZAAGj7BxRSJrZkHuo0qQAAtsiAALzR9FL6waqdE9VjWYuBA',
    'o_3': 'CAACAgIAAx0CbhAEhQACYp1j-VKa4jeEX8-PRaZ8-mFUkylguwACIScAAsLbyEv3IPgjWQFqgS4E',
    'o_4': 'CAACAgIAAx0CbhAEhQACYptj-VKSETbF0ouZ7WigAY9OPTpu5gACryEAAls50UuBg7LMiGRttC4E',
    'o_5': 'CAACAgIAAx0CbhAEhQACYpVj-VJ4ft5bi81_BODf-korLUDEowACMCgAAjI9yUvmD2vluUY1Gi4E',
    'o_6': 'CAACAgIAAx0CbhAEhQACYpdj-VKB-QABUCXVs5vf7fo16yOMoncAAtwkAALrJMlLiA6Zz7G9HWAuBA',
    'o_7': 'CAACAgIAAx0CbhAEhQACYqVj-VMJC81tcStch1J7lHmc7rFAfgACjCgAAhpG0UuuH6s5yxbK2C4E',
    'o_8': 'CAACAgIAAx0CbhAEhQACYqdj-VMUF1_5Wlny0QwhKifINvhAPgACEx8AAgfL0Etta5KwdCQt8i4E',
    'o_9': 'CAACAgIAAx0CbhAEhQACYqlj-VMbZNY4FUG0VwGVaxG3v_LbpwAC7iMAAmTU0EsBf-KUk_5J8C4E',
    'o_+2': 'CAACAgIAAx0CbhAEhQACYqtj-VMgOl2h8Obwi1W8xBzFCHGBOAACpygAAnueyUvoTcxcm6IT_i4E',
    'o_Пропуск хода': 'CAACAgIAAx0CbhAEhQACYq9j-VM8B5hov4o6AV-scyeooCb_HAACHyMAAp1Z0UvQCJ7S1n_ACy4E',
    'o_Реверс': 'CAACAgIAAx0CbhAEhQACYq1j-VMtiwQJ0FgOe8_3hT9YhYNkhwACKiYAAgGFyEt70o13DmdK4C4E',
    '+4': 'CAACAgIAAx0CbhAEhQACYudj-VP_dkibPeiUXo3_imR3WklRZwAC7yYAAqAbyUvRmON4Lw8Gwy4E',
    'Смена цвета': 'CAACAgIAAx0CbhAEhQACYuVj-VP5hoUQOMmKg1mmH9PhVpiBywACTiQAAgSA0UuHIC5vD8Xfey4E',
    'Переворот карт': 'CAACAgIAAxkBAAKP82P7HojAQRlVt2z64m9nocGYMsCFAAJqKAACIofRSxuZeFw4a-YWLgQ',
}


class Card_Black(object):
    """This class represents an UNO card"""

    def __init__(self, color, value, special=None):
        self.color = color
        self.value = value
        self.special = special

    def __str__(self):
        if self.special:
            return self.special
        else:
            return '%s_%s' % (self.color, self.value)

    def __repr__(self):
        if self.special:
            return '%s%s%s' % (COLOR_ICONS.get(self.color, ''),
                               COLOR_ICONS[BLACK],
                               ' '.join([s.capitalize()
                                         for s in self.special.split('_')]))
        else:
            return '%s%s' % (COLOR_ICONS[self.color], self.value.capitalize())

    def __eq__(self, other):
        """Needed for sorting the cards"""
        return str(self) == str(other)

    def __lt__(self, other):
        """Needed for sorting the cards"""
        return str(self) < str(other)


def from_str(string):
    """Decodes a Card object from a string"""
    if string not in SPECIALS:
        color, value = string.split('_')
        return Card_Black(color, value)
    else:
        return Card_Black(None, None, string)
        
        
def from_str_flip(string):
    """Decodes a Card object from a string"""
    if string not in SPECIALS_FLIP:
        color, value = string.split('_')
        return Card_Black(color, value)
    else:
        return Card_Black(None, None, string)