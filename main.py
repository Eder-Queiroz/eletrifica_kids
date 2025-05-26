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
        ['disjuntor', 'fio', ''],
        ['voltagem', 'fase', ''],
        ['tomada', 'terra', ''], 
        ['luz', 'neon', 'poste'],
        ['led', 'neutro', ''],
        ['curto', 'aterrar', ''],
        ['fiacao', 'dps', 'idr'],
        ['eletricidade', '', ''],
        ['luz', 'volts', 'watts'],
        ['energia', 'cerca', ''],
        ['circuito', 'qdc', ''],
        ['painel', 'cabo', 'polo'],
        ['rele', 'tensao', ''],
        ['carga', 'corrente', ''],
        ['fdp', 'potencia', '']
    ])
    clues_dict = {
        'disjuntor': 'Dispositivo que interrompe a corrente',
        'fio': 'Condutor elétrico',
        'voltagem': 'Diferença de potencial elétrico',
        'fase': 'Condutor que transporta energia',
        'tomada': 'Ponto de conexão elétrica',
        'terra': 'Condutor de proteção',
        'luz': 'Iluminação elétrica',
        'neon': 'Tipo de lâmpada gasosa',
        'poste': 'Suporte para iluminação',
        'led': 'Diodo emissor de luz',
        'neutro': 'Condutor de retorno',
        'curto': '___ circuito',
        'aterrar': 'Conectar ao solo',
        'fiacao': 'Conjunto de condutores',
        'dps': 'Dispositivo de proteção contra surtos',
        'idr': 'Interruptor diferencial residual',
        'eletricidade': 'Forma de energia',
        'volts': 'Unidade de tensão',
        'watts': 'Unidade de potência',
        'energia': 'Capacidade de realizar trabalho',
        'cerca': '___ elétrica',
        'circuito': 'Caminho da corrente',
        'qdc': 'Quadro de distribuição',
        'painel': '___ solar',
        'cabo': 'Condutor elétrico isolado',
        'polo': 'Terminal elétrico',
        'rele': 'Interruptor eletromagnético',
        'tensao': 'Diferença de potencial',
        'carga': 'Quantidade de eletricidade',
        'corrente': 'Fluxo de elétrons',
        'fdp': 'Fator de potência',
        'potencia': 'Taxa de energia'
    }


    # Convert word grid to a character grid - with proper spacing
    max_width = max(len(' '.join(row)) for row in word_grid)
    letter_grid = []
    for row in word_grid:
        joined = ' '.join(word for word in row if word)  # Only join non-empty words
        letter_grid.append(list(joined.ljust(max_width)))

    letter_grid = np.array(letter_grid)
    
    sample_grid = Grid(letter_grid, 0.8, x0, y0)
    sample_clues = Clues(sample_grid, clues_dict)

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            
            screen.fill((30, 30, 30))
            
            sample_grid.handle_event(event)
            sample_clues.drawClues(sample_grid)  # Draw the clues

            pg.display.flip()
            
        clock.tick(30)
        await asyncio.sleep(0)

    pg.quit()

asyncio.run(main())