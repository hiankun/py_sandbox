import re
import matplotlib.pyplot as plt
import numpy as np

#font_file = "./fonts/FullGreek-Terminus12x6.txt"
font_file = "./fonts/FullGreek-Terminus24x12.txt"

HEAD = 'GLYPH'
TAIL = 'ENDGLYPH'

def make_uchr(code):
    return chr(int(code.lstrip("U+").zfill(8), 16))

def plot_glyph(glyph):
    glyph_name = glyph[0].replace(HEAD, '').strip()
    glyph_ucode = make_uchr(glyph[1]) if glyph[1] != '' else glyph[1]

    _arr = np.asarray(glyph[2:-1])
    #g_arr = np.zeros((len(_arr), len(_arr[0])))
    g_arr = []
    for ga in _arr:
        g = [_ for _ in ga]
        g_arr.append(g)
    g_arr = np.array(g_arr)
    g_array = np.where(g_arr == 'X', 1, 0)
    #print(glyph_name, glyph_ucode, g_array.shape)

    fig, axs = plt.subplots(1,1)
    axs.set_title(f'{glyph_name}: {glyph_ucode}')
    axs.imshow(g_array)
    plt.show()
    plt.close(fig)


def main():
    with open(font_file) as f:
        lines = f.readlines()
    
    glyph = []
    for line in lines:
        line = line.strip()
        is_head = re.search(f'^{HEAD}', line)
        is_tail = re.search(f'^{TAIL}', line)
        is_u_plus = re.search('U\+\w+', line)
        if is_head:
            glyph = []
            glyph.append(line)
            glyph.append('')
            continue
        if is_u_plus:
            glyph[1] = (is_u_plus.group(0))
        if line != '' and not is_u_plus:
            glyph.append(line)
        if is_tail:
            plot_glyph(glyph)


if __name__=='__main__':
    main()
