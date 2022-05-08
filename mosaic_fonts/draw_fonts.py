from PIL import Image, ImageFont, ImageDraw
import matplotlib.pyplot as plt

fonts_path = [
    "./fonts/FreeMono.ttf",
    "./fonts/PTMono-Regular.ttf",
    #psf is not recognised "./fonts/FullGreek-Terminus12x6.psf",
]

font_path = fonts_path[1]


def get_ascii(n_row=16):
    rows = []
    for r in range(n_row):
        rows.append(''.join([chr(a) for a in range(r*n_row, (r+1)*n_row)]))
    ascii_str = '\n'.join(rows)
    #print(ascii_str)
    return ascii_str


def main():
    n_row = 16 # will output n_row*n_row characters
    font = ImageFont.truetype(font_path, 24)
    string = get_ascii(n_row)
    string_bbox = font.getbbox(string)
    
    padding = 5
    img_size = (string_bbox[2]//n_row+padding, string_bbox[3]*n_row+padding)
    img = Image.new('P', img_size, 255)
    
    canvas = ImageDraw.Draw(img)
    #canvas.rectangle(string_bbox, outline=100)
    canvas.text((0,0), string, font=font)
    
    fig, axs = plt.subplots(1,1)
    axs.imshow(img)
    plt.show()


if __name__=='__main__':
    main()
