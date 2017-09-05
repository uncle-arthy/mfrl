#!/usr/bin/python3
# -*- coding: utf-8 -*-
__author__ = 'Alexei Evdokimov'
'''
Change tutorial from RogueBasin to rogueliketutorials.com
More Pythonic style and seems more OOP-ish ))
'''

import tdl
from input_handlers import handle_keys


def main():
    # set main game window size
    screen_width = 80
    screen_height = 60

    player_x = int(screen_width / 2)
    player_y = int(screen_height / 2)

    # Font differs from one in tutorial as I use this ti work in REXpaint
    tdl.set_font('cp437_12x12.png', greyscale=True, altLayout=False)

    # Main game window
    root_console = tdl.init(screen_width, screen_height, title='MFRL revised tutorial')
    con = tdl.Console(screen_width, screen_height)

    while not tdl.event.is_window_closed():
        con.draw_char(player_x, player_y, '@', bg=None, fg=(128, 102, 64))
        root_console.blit(con, 0, 0, screen_width, screen_height, 0, 0)

        # And draw it all
        tdl.flush()

        con.draw_char(player_x, player_y, ' ', bg=None)

        for event in tdl.event.get():
            if event.type == 'KEYDOWN':
                user_input = event
                break
        else:
            user_input = None
        '''
        As in tutorial:
        Python has a lesser-known feature where you can put an 'else' statement
        after a for loop, and that else statement only executes
        if we didn't break out of the loop!
        So in this scenario, if we didn't encounter any 'KEYDOWN' event,
        then we set user_input to None by default.
        '''

        if not user_input:
            continue

        action = handle_keys(user_input)

        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        if move:
            dx, dy = move
            player_x += dx
            player_y += dy

        if exit:
            return True  # Exit main loop and the game

        if fullscreen:
            tdl.set_fullscreen(not tdl.get_fullscreen())


if __name__ == '__main__':
    main()