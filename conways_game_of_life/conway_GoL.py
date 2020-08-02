# https://www.conwaylife.com/wiki/Main_Page
# Known issue: 
# * Boundary conditions.
# * Final generation - 2.

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
        self.rows = size[0]
        self.cols = size[1]
        self.density = density
        self.cell_type = self.cell_type[0]
        self.cell_number = 0
        self.cell_number_old = 0
        self.population = np.zeros(self.size).astype(np.bool)
        self.position = (np.random.choice(size[0]), np.random.choice(size[1]))
        self.alive_position = []


    def pad_with(self, vector, pad_width, iaxis, kwargs):
        # https://numpy.org/doc/stable/reference/generated/numpy.pad.html
        pad_value = kwargs.get('padder', '"')
        vector[:pad_width[0]] = pad_value
        vector[-pad_width[1]:] = pad_value


    def draw_canvas(self):
        canvas = np.where(self.population, self.cell_type, ' ')
        canvas = np.pad(canvas, 1, self.pad_with)
        for row in canvas:
            r = [str(_) for _ in row]
            print(''.join(r))
        print(  f'Pattern: {self.pattern_name}, '
                f'Generation: {self.generation}, '
                f'Population: {self.cell_number}')

    def steady_state(self, r, c):
        now_pos = [r,c]
        self.alive_position.append(now_pos)
        if len(self.alive_position) > 3:
            self.alive_position.pop(0)
            prev_pos = self.alive_position[0]
            return np.array_equal(prev_pos, now_pos)
        else:
            return False

    
    def update_population(self):
        pad_w = 1 #FIX
        arr = np.where(self.population, True, False)
        p_arr = np.pad(arr, pad_w, mode='constant')
        status_alive = np.zeros(p_arr.shape).astype(np.bool)
    
        # check live cell
        r, c = np.nonzero(p_arr)
        steady = self.steady_state(r, c)
        for _r,_c in zip(r,c):
            _arr = p_arr[_r-1:_r+2, _c-1:_c+2].copy()
            _arr[1,1] = 0 #replace the center point
            neighbours = np.count_nonzero(_arr)
            if neighbours in [2, 3]:
                status_alive[_r,_c] = True
    
        # check dead cell
        r,c = np.nonzero(np.invert(p_arr))
        for _r,_c in zip(r,c):
            #if _r in [0,self.rows-1] or _c in [0,self.cols-1]: #border, skip
            #    continue
            _arr = p_arr[_r-1:_r+2, _c-1:_c+2].copy()
            neighbours = np.count_nonzero(_arr)
            if neighbours in [3]:
                status_alive[_r,_c] = True

        if pad_w != 0:
            self.population = status_alive[pad_w:-pad_w,pad_w:-pad_w]
        else:
            self.population = status_alive

        self.generation += 1
        self.cell_number = np.count_nonzero(self.population)

        # how to know there's no further evolution?
        # compare states between t and t-2?
        return steady

    def load_pattern(self, pattern):
        r,c = self.position
        if pattern == 'Glider':
            pattern_arr = np.array([
                [0,1,0],
                [0,0,1],
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

    def init_population(self, pattern=None, rand=False):
        if pattern:
            self.pattern_name = pattern
            r,c,pattern = self.load_pattern(pattern)
            if not rand: #set position to the center of canvas
                r = int(self.rows/2)
                c = int(self.cols/2)
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
    rows = 42
    cols = 110
    density = 0.80
    sleep = 0.25
    gol = GameOfLife((rows, cols), density)
    gol.init_population(pattern=PATTERNS[5], rand=False)

    steady = False
    while not steady:
        os.system('clear')
        gol.draw_canvas()
        steady = gol.update_population()
        time.sleep(sleep)


if __name__=='__main__':
    main()
