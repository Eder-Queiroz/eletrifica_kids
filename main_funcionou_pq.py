import asyncio
import numpy as np
import pygame as pg
from Grid import Grid
from Clues import Clues

# define pg parameters
pg.init()
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 900
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


async def main():
    clock = pg.time.Clock()
    done = False

    x0, y0 = 10, 10

    # Make all rows same length by padding with empty strings
    word_grid = np.array([
        ['spacecraft', 'sun', ''],
        ['telescope', 'mars', ''],
        ['nebulae', 'moon', ''], 
        ['star', 'nova', 'pluto'],
        ['ray', 'cosmic', ''],
        ['meteor', 'aliens', ''],
        ['orbit', 'solar', 'ice'],
        ['constellations', '', ''],
        ['red', 'venus', 'gamma'],
        ['phasers', 'comet', ''],
        ['asterisk', 'ufo', ''],
        ['gases', 'helm', 'dark'],
        ['void', 'stardust', ''],
        ['nova', 'asteroid', ''],
        ['sky', 'spacetime', '']
    ])
    clues_dict = {
        'spacecraft': 'Vehicle for space travel',
        'sun': 'Center of our solar system',
        'telescope': 'Tool for viewing distant objects',
        'mars': 'The red planet',
        'nebulae': 'Cosmic clouds of gas and dust',
        'moon': "Earth's natural satellite",
        'star': 'Luminous sphere of plasma',
        'nova': 'Sudden brightness in the sky',
        'pluto': 'Dwarf planet in the Kuiper belt',
        'ray': 'Beam of light or energy',
        'cosmic': 'Related to the universe',
        'meteor': 'Shooting star',
        'aliens': 'Extraterrestrial beings',
        'orbit': 'Path around a celestial body',
        'solar': '___ system',
        'ice': 'Found on comets tails',
        'constellations': 'Star patterns in the sky',
        'red': '___ giant star',
        'venus': 'Second planet from the sun',
        'gamma': '___ rays',
        'phasers': 'Science fiction weapons',
        'comet': 'Icy space traveler',
        'asterisk': 'Star-shaped symbol',
        'ufo': 'Unidentified flying object',
        'gases': 'Jupiter is mostly made of these',
        'helm': 'Spaceship control station',
        'dark': '___ matter',
        'void': 'Empty space',
        'stardust': 'Cosmic particles',
        'nova': 'Exploding star',
        'asteroid': 'Space rock',
        'sky': 'Where stars appear',
        'spacetime': 'Four-dimensional continuum'
    }

    # letter_grid = np.apply_along_axis(lambda x:list(x[0]), 1, word_grid)

    # sample_grid = Grid(letter_grid, 0.8, x0, y0)
    # sample_clues = Clues(sample_grid, clues_dict)

    # Convert word grid to a character grid
    max_width = max(len(' '.join(row)) for row in word_grid)
    letter_grid = []
    for row in word_grid:
        joined = ' '.join(row)
        letter_grid.append(list(joined.ljust(max_width)))

    letter_grid = np.array(letter_grid)
    
    sample_grid = Grid(letter_grid, 0.8, x0, y0)

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            # screen.fill((30, 30, 30))

            sample_grid.handle_event(event)

            pg.display.flip()
            
        clock.tick(30)
        await asyncio.sleep(0)

    pg.quit()

asyncio.run(main())