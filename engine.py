#!/usr/bin/python3
# -*- coding: utf-8 -*-
__author__ = 'Alexei Evdokimov'
'''
Change tutorial from RogueBasin to rogueliketutorials.com
More Pythonic style and seems more OOP-ish ))
'''

import tdl

from entity import Entity, get_blocking_entities_at_location
from game_states import GameStates
from input_handlers import handle_keys
from map_utils import GameMap, make_map
from render_functions import clear_all, render_all


def main():
    # set main game window size
    screen_width = 80
    screen_height = 60
    map_width = 80
    map_height = 55

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    fov_algorithm = 'PERMISSIVE'
    fov_light_walls = True
    fov_radius = 10

    max_monsters_per_room = 3

    colors = {
        'dark_wall': (26, 26, 26),
        'dark_ground': (51, 51, 51),
        'light_wall': (26, 20, 13),
        'light_ground': (51, 41, 26),
        'desaturated_green': (63, 127, 63),
        'darker_green': (0, 127, 0)
    }

    player = Entity(0, 0, '@', (128, 102, 64), 'Player', blocks=True)
    entities = [player]

    # Font differs from one in tutorial as I use this ti work in REXpaint
    tdl.set_font('cp437_12x12.png', greyscale=True, altLayout=False)

    # Main game window
    root_console = tdl.init(screen_width, screen_height, title='MFRL revised tutorial')
    con = tdl.Console(screen_width, screen_height)

    game_map = GameMap(map_width, map_height)
    make_map(game_map, max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities,
             max_monsters_per_room, colors)

    fov_recompute = True

    game_state = GameStates.PLAYERS_TURN

    while not tdl.event.is_window_closed():
        if fov_recompute:
            game_map.compute_fov(player.x, player.y, fov=fov_algorithm, radius=fov_radius, light_walls=fov_light_walls)

        render_all(con, entities, game_map, fov_recompute, root_console, screen_width, screen_height, colors)

        # And draw it all
        tdl.flush()

        clear_all(con, entities)

        fov_recompute = False

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
        exit_game = action.get('exit')
        fullscreen = action.get('fullscreen')

        if move and game_state == GameStates.PLAYERS_TURN:
            dx, dy = move
            destination_x = player.x + dx
            destination_y = player.y + dy

            if game_map.walkable[destination_x, destination_y]:
                target = get_blocking_entities_at_location(entities,destination_x, destination_y)

                if target:
                    print('You kicked the ' + target.name + ' in the shins, much to its annoyance!')
                else:
                    player.move(dx, dy)

                    fov_recompute = True

                game_state = GameStates.ENEMY_TURN

        if exit_game:
            return True  # Exit main loop and the game

        if fullscreen:
            tdl.set_fullscreen(not tdl.get_fullscreen())

        if game_state == GameStates.ENEMY_TURN:
            for entity in entities:
                if entity != player:
                    print('The ' + entity.name + ' ponders the meaning of its existence.')

            game_state = GameStates.PLAYERS_TURN


if __name__ == '__main__':
    main()