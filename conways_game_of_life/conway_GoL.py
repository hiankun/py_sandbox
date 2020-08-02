# https://www.conwaylife.com/wiki/Main_Page

import numpy as np
import random
import time
import os


PATTERNS = [
        'Glider',
        'R-pentomino',
        'Bun',
        'Beacon',
        'Wing',
        'Dove',
        'Unix',
        None,
        ]

class GameOfLife():

    cell_type = ['O', '@', '█']
    def __init__(self, size, density):
        self.generation = 0
        self.size = size
        self.density = density
        self.cell_type = self.cell_type[0]
        self.cell_number = 0
        self.cell_number_old = 0
        self.population = np.zeros(self.size).astype(np.bool)
        self.position = (np.random.choice(size[0]), np.random.choice(size[1]))


    def draw_canvas(self):
        canvas = np.where(self.population, self.cell_type, ' ')
        for row in canvas:
            r = [str(_) for _ in row]
            print(''.join(r))
        print(  f'Pattern: {self.pattern_name}, '
                f'Generation: {self.generation}, '
                f'Population: {self.cell_number}')

    
    def update_population(self):
        arr = np.where(self.population, True, False)
        p_arr = np.pad(arr, 1, mode='constant')
        status_alive = np.zeros(p_arr.shape).astype(np.bool)
    
        # check live cell
        r,c = np.where(p_arr)
        for _r,_c in zip(r,c):
            _arr = p_arr[_r-1:_r+2, _c-1:_c+2].copy()
            _arr[1,1] = 0 #replace the center point
            neighbours = np.count_nonzero(_arr)
            if neighbours in [2, 3]:
                status_alive[_r,_c] = True
    
        # check dead cell
        r,c = np.where(np.invert(p_arr))
        for _r,_c in zip(r,c):
            if _r == 0 or _c == 0: #border, skip
                continue
            _arr = p_arr[_r-1:_r+2, _c-1:_c+2].copy()
            neighbours = np.count_nonzero(_arr)
            if neighbours in [3]:
                status_alive[_r,_c] = True

        self.population = status_alive[1:-1,1:-1]
        self.generation += 1
        self.cell_number = np.count_nonzero(self.population)

        # how to know there's no further evolution?
        # compare states between t and t-2?
        if self.cell_number != self.cell_number_old:
            self.cell_number_old = self.cell_number
            return True
        else:
            return False


    def load_pattern(self, pattern):
        r,c = self.position
        if pattern == 'Glider':
            pattern_arr = np.array([
                [0,1,0],
                [1,0,0],
                [1,1,1],
                ]).astype(np.bool)
        if pattern == 'R-pentomino':
            pattern_arr = np.array([
                [0,1,1],
                [1,1,0],
                [0,1,0],
                ]).astype(np.bool)
        if pattern == 'Bun':
            pattern_arr = np.array([
                [0,1,1,0],
                [1,0,0,1],
                [0,1,1,1],
                ]).astype(np.bool)
        if pattern == 'Beacon':
            pattern_arr = np.array([
                [1,1,0,0],
                [1,0,0,0],
                [0,0,0,1],
                [0,0,1,1],
                ]).astype(np.bool)
        if pattern == 'Wing':
            pattern_arr = np.array([
                [0,1,1,0],
                [1,0,0,1],
                [0,1,0,1],
                [0,0,1,1],
                ]).astype(np.bool)
        if pattern == 'Dove':
            pattern_arr = np.array([
                [0,0,1,1,0],
                [0,1,0,0,1],
                [1,0,0,1,0],
                [1,1,1,0,0],
                ]).astype(np.bool)
        if pattern == 'Unix':
            pattern_arr = np.array([
                [0,1,1,0,0,0,0,0],
                [0,1,1,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,1,0,0,0,0,0,0],
                [1,0,1,0,0,0,0,0],
                [1,0,0,1,0,0,1,1],
                [0,0,0,0,1,0,1,1],
                [0,0,1,1,0,0,0,0],
                ]).astype(np.bool)
        return r,c,pattern_arr

    def init_population(self, pat=None, rand=False):
        if pat:
            self.pattern_name = pattern
            r,c,pattern = self.load_pattern(pat)
            if not rand: #set position to the center of canvas
                _r,_c = self.size
                r = int(_r/2)
                c = int(_c/2)
            _r,_c = pattern.shape
            _r_low = r - int(_r/2)
            _r_up = _r_low + _r
            _c_low = c - int(_c/2)
            _c_up = _c_low + _c
            self.population[_r_low:_r_up, _c_low:_c_up] = pattern
        else:
            self.pattern_name = '(None)'
            d = self.density
            self.population = np.random.choice(
                    a=[True,False], size=self.size, p=[d, 1-d])


def main():
    row = 42
    col = 110
    density = 0.50
    sleep = 0.3
    gol = GameOfLife((row, col), density)
    gol.init_population(pat=PATTERNS[-1], rand=False)
    evolution = gol.update_population()

    while True:
        os.system('clear')
        evolution = gol.update_population()
        gol.draw_canvas()
        time.sleep(sleep)


if __name__=='__main__':
    main()
