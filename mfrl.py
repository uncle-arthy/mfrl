#!/usr/bin/python3
# -*- coding: utf-8 -*-
__author__ = 'Alexei Evdokimov'

import tdl


def main():
    screen_width = 80
    screen_height = 50

    tdl.setFont('arial12x12.png', greyscale=True, altLayout=True)

    console = tdl.init(screen_width, screen_height, title='MFRL v0.1', fullscreen=False)

    playerx = screen_width//2
    playery = screen_height//2

    while not tdl.event.is_window_closed():
        console.draw_char(1, 1, '@', bg=None, fg=(255, 255, 255))

        tdl.flush()


if __name__ == '__main__':
    main()
