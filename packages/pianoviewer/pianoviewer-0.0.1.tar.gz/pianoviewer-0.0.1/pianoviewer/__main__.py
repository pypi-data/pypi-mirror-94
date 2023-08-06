import argparse
import atexit
import sys

import mido
import pygame


def handle_midi(msg):
    if msg.type == 'note_on':
        active_keys.append(msg.note)
    elif msg.type == 'note_off':
        active_keys.remove(msg.note)

def handle_events():
    global running
    for e in pygame.event.get():
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                running = False
        if e.type == pygame.QUIT:
            running = False

def draw_white_key(i, pressed):
    if pressed:
        color = (127, 127, 127)
    else:
        color = (255, 255, 255)
    pygame.draw.rect(surf, color, (i * KEY_WIDTH_FULL, 0, KEY_WIDTH, args.height))

def draw_black_key(pos, pressed):
    if pressed:
        color = (111, 111, 111)
    else:
        color = (31, 31, 31)
    pygame.draw.rect(surf, color, (pos, 0, KEY_WIDTH_BLACK, args.height / 2 + (args.height / 6)))

def draw():
    # Clear screen.
    surf.fill((0, 0, 0))
    
    for i in range(OCTAVE_COUNT):
        i1 = i * 7
        i2 = (args.first_octave + i) * 12
        
        # Draw white keys.
        draw_white_key(i1, i2 in active_keys)
        draw_white_key(i1 + 1, i2 + 2 in active_keys)
        draw_white_key(i1 + 2, i2 + 4 in active_keys)
        draw_white_key(i1 + 3, i2 + 5 in active_keys)
        draw_white_key(i1 + 4, i2 + 7 in active_keys)
        draw_white_key(i1 + 5, i2 + 9 in active_keys)
        draw_white_key(i1 + 6, i2 + 11 in active_keys)
        if i == OCTAVE_COUNT - 1:
            draw_white_key(i1 + 7, i2 + 12 in active_keys)
        
        # Draw black keys.
        pos = i1 * KEY_WIDTH_FULL
        draw_black_key(pos + KEY_WIDTH - KEY_WIDTH_BLACK + KEY_SPACING + KEY_WIDTH_BLACK_SPACING, i2 + 1 in active_keys)
        draw_black_key(pos + KEY_WIDTH_FULL + KEY_WIDTH - KEY_WIDTH_BLACK_SPACING, i2 + 3 in active_keys)
        draw_black_key(pos + (KEY_WIDTH_FULL * 3) + KEY_WIDTH - KEY_WIDTH_BLACK + KEY_SPACING + KEY_WIDTH_BLACK_SPACING, i2 + 6 in active_keys)
        draw_black_key(pos + (KEY_WIDTH_FULL * 4) + KEY_WIDTH - 2, i2 + 8 in active_keys)
        draw_black_key(pos + (KEY_WIDTH_FULL * 5) + KEY_WIDTH - KEY_WIDTH_BLACK_SPACING, i2 + 10 in active_keys)
    
    screen.blit(pygame.transform.scale(surf, SCR_SIZE), (0, 0))
    pygame.display.flip()

def main():
    # Handle command line arguments
    ap = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ap.add_argument('-p', '--port', required=False, help='Sets the port.')
    ap.add_argument('-P', '--list-ports', required=False, action='store_true', help='Lists all available ports.')
    ap.add_argument('-s', '--scale', required=False, type=int, default=2, help='Sets the window scale.')
    ap.add_argument('-o', '--first-octave', required=False, type=int, default=1, help='Sets the first octave.')
    ap.add_argument('-O', '--last-octave', required=False, type=int, default=6, help='Sets the last octave.')
    ap.add_argument('--height', required=False, type=int, default=48, help='Sets the piano height.')
    global args
    args = ap.parse_args()

    if args.list_ports:
        for p in mido.get_input_names():
            print(p)
        sys.exit(0)
    elif not args.port:
        print('A port needs to be specified!', file=sys.stderr)
        sys.exit(1)
    
    LAST_OCTAVE = args.last_octave + 1
    if LAST_OCTAVE <= args.first_octave:
        print('The last octave cannot be lower as the first!', file=sys.stderr)
        sys.exit(1)

    # Constants
    # How many octaves the piano display has.
    global OCTAVE_COUNT
    OCTAVE_COUNT = LAST_OCTAVE - args.first_octave
    # How many keys the piano display has.
    global KEY_COUNT
    KEY_COUNT = OCTAVE_COUNT * 7 + 1
    # Space between keys. (Don't change!)
    global KEY_SPACING
    KEY_SPACING = 2
    # Width of white keys.
    global KEY_WIDTH
    KEY_WIDTH = 12
    # Width of black keys.
    global KEY_WIDTH_BLACK
    KEY_WIDTH_BLACK = KEY_WIDTH / 2
    # Spacing of black keys.
    global KEY_WIDTH_BLACK_SPACING
    KEY_WIDTH_BLACK_SPACING = 1
    # Width of black keys. (with spacing)
    global KEY_WIDTH_FULL
    KEY_WIDTH_FULL = KEY_WIDTH + KEY_SPACING

    # Width of surface.
    global SURF_W
    SURF_W = KEY_COUNT * KEY_WIDTH_FULL - KEY_SPACING
    # Height of surface.
    global SURF_H
    SURF_H = args.height
    # Size of surface. (as tuple)
    global SURF_SIZE
    SURF_SIZE = (SURF_W, SURF_H)

    # Width of screen.
    global SCR_W
    SCR_W = SURF_W * args.scale
    # Height of screen
    global SCR_H
    SCR_H = SURF_H * args.scale
    # Size of screen (as tuple)
    global SCR_SIZE
    SCR_SIZE = (SCR_W, SCR_H)

    # Initialize pygame
    pygame.init()
    atexit.register(pygame.quit)

    pygame.display.set_caption(f'Piano Viewer - {args.port}')
    global screen
    screen = pygame.display.set_mode(SCR_SIZE)
    global surf
    surf = pygame.Surface(SURF_SIZE)

    global active_keys
    active_keys = []
    # Open MIDI device.
    mido.open_input(args.port, callback=handle_midi)

    global running
    running = True
    while running:
        handle_events()
        draw()

if __name__ == '__main__':
    main()
