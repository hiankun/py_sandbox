import tkinter as tk
from tkinter.filedialog import (
        askdirectory, 
        asksaveasfile,
        askopenfilename)
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageTk
import cv2
import numpy as np


class DoGrabCut():
    def __init__(self, *args, **kwargs):
        self.bgdmodel = np.zeros((1, 65), np.float64)
        self.fgdmodel = np.zeros((1, 65), np.float64)

    def cal_mask(self, mode, gc_rect=None):
        #TODO: to scale gc_rect to original size
        Common.polygon = []
        self.img = cv2.imread(Common.img_file)
        if mode == 4:
            self.method = cv2.GC_INIT_WITH_RECT
            x1,y1,x2,y2 = gc_rect
            self.rect = [x1, y1, x2-x1, y2-y1]
            Common.mask = np.zeros(self.img.shape[:2], np.uint8)
        else:
            self.method = cv2.GC_INIT_WITH_MASK
            self.rect = None
        cv2.grabCut(self.img, Common.mask, self.rect, 
                self.bgdmodel, self.fgdmodel, 1, self.method)
        res_mask = np.where(
                (Common.mask==1) + (Common.mask==3), 255, 0).astype('uint8')
        Common.polygon = self.get_polygon(res_mask)
        Common.gc_res_mask = res_mask
        #output = cv2.bitwise_and(self.img, self.img, mask=res_mask)
        #res = np.hstack((self.img, output))
        #return res
        #return res_mask

    def get_polygon(self, mask):
        cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in cnts:
            epsilon = 0.002*cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)
            approx = np.squeeze(approx, axis=1)
        # append the first point to the end
        #area = cv2.contourArea(approx)
        approx = np.append(approx, [approx[0]], axis=0)
        return approx #, area


class Common:
    mask = None
    polygon = []
    grabcut_rect = []
    grabcut_mask = []
    grabcut_res = None
    gc_res_mask = None
    roi_pts = []
    img_file = None
    current_tool = None
    tool_set = [
       ("Rectangle", 4),
       ("0: BG", 0),
       ("1: FG", 1),
       ("2:PBG", 2),
       ("3:PFG", 3),
       ]
    tool_info = "Key strokes usage\n"\
               +"-----------------\n"\
               +"Esc: Cancel points\n"\
               +"c: Toggle guiding\n"\
               +"   cross on/off\n"\
               +"g: Do GrabCut\n"\
               +"p: Draw polygon\n"\
               +"x: Clear\n"\
               +"-----------------"

class Draw:
    canvas_bg_color = '#0a082e'
    cross_line_color = '#aa9cff'
    cross_line_width = 1
    roi_line_color = '#aacc00'
    roi_line_width = 2
    brush_size = 3
    mask_BG = {'color' : '#ff0000',  'val' : 0}
    mask_FG = {'color' : '#00ff00',  'val' : 1}
    mask_PR_BG = {'color' : '#ff9933',  'val' : 2}
    mask_PR_FG = {'color' : '#66ff66',  'val' : 3}
    set_guding_cross = True


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("GrabCut")
        self.minsize(900,600)
        #self.attributes('-zoomed', True)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Create the menu
        menubar = AppMenu(self)
        self.config(menu=menubar)
        self.bind('<Control-o>', menubar.open_img)
        self.bind('<Control-s>', menubar.saveas_img)
        self.bind('<Control-q>', quit)

        ''' Tool Panel '''
        toolpanel = ToolPanel(self)
        toolpanel.pack(side='left',fill='y',expand=False) 
        
        ''' Canvas '''
        self.imagecanvas = ImageCanvas(self)
        self.imagecanvas.pack(side='left',fill='both',expand=True) 

        self.bind('<c>', self.toggle_cross_guide)

        # the grabCut part
        self.gc = DoGrabCut(self)

    def toggle_cross_guide(self, event='toggle_cross_guide'):
        Draw.set_guding_cross = not Draw.set_guding_cross
        self.imagecanvas.canvas.delete('guiding_cross')

    def set_img2canvas(self):
        filename = Common.img_file
        self.imagecanvas.load_image(filename)

    def set_img2canvas_failed(self):
        messagebox.showerror("No image", 
                "Make sure you've opened the correct image folder")


class AppMenu(tk.Menu):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        ''' Menu bar '''
        # File menu
        filemenu = tk.Menu(self, tearoff=True)
        self.add_cascade(label='File', 
                underline=0,
                menu=filemenu)
        filemenu.add_command(label='Open image file', 
                underline=0,
                command=self.open_img,
                accelerator='Ctrl+O')
        filemenu.add_command(label='Save as', 
                underline=1,
                command=self.saveas_img,
                accelerator='Ctrl+S')
        filemenu.add_separator()
        filemenu.add_command(label='Exit', 
                underline=1,
                command=quit,
                accelerator='Ctrl+Q')
        # Help menu
        helpmenu = tk.Menu(self, tearoff=True)
        helpmenu.add_command(label='Usage', command=self.usage_info)
        helpmenu.add_separator()
        helpmenu.add_command(label='About', command=None)
        self.add_cascade(label='Help', menu=helpmenu)

    def usage_info(self):
        usage_text = "This is a simple help info.\n"\
                  + "The basic usage:\n"\
                  + "TODO...\n"
        messagebox.showinfo('Usage', usage_text)

    def saveas_img(self, event='saveas_img'):
        save_img = asksaveasfile(title='Save the result',
                initialdir='./',
                filetypes = (
                    ("jpg files","*.jpg"),
                    ("all files","*.*"))
                )

    def open_img(self, event='open_img'):
        Common.img_file = askopenfilename(title='Select image',
                initialdir='./',
                filetypes = (
                    ('image files',('.jpg', '.jpeg', '.png')),
                    ('all files','.*'))
                )
        #try: # show the first image in the folder
        self.root.set_img2canvas()
        #except:
        #    self.root.set_img2canvas_failed()


class ToolPanel(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        toolpanel_label = tk.Label(self, text='Selection Tools')
        toolpanel_label.pack(side='top',ipadx=0,ipady=5,fill='x')

        Common.current_tool = tk.IntVar()
        Common.current_tool.set(4)
        for text, mode in Common.tool_set:
            self.tool = tk.Radiobutton(self, text=text,
                    variable=Common.current_tool, value=mode)
            self.tool.pack(side='top',anchor='w')

        toolpanel_info = tk.Label(self,relief=tk.GROOVE,justify=tk.LEFT,
                font=('Courier',11), text=Common.tool_info)
        toolpanel_info.pack(side='top',pady=(10,0),ipadx=10,ipady=10,
                fill='both',expand=True)


class ImageCanvas(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.canvas = tk.Canvas(self, 
                background=Draw.canvas_bg_color, cursor='crosshair')
        self.canvas.bind_all('<Key>', self.key_pressed)
        self.canvas.bind('<Motion>', self.cursor_move_draw)
        ##self.canvas.bind('<B1-Motion>', self.set_mask)
        self.canvas.bind('<ButtonPress-1>', self.set_mask)
        #self.canvas.bind('<ButtonRelease-1>', self.do_grabcut)
        self.canvas.bind_all('<Escape>', self.cancel_set_points)
        self.img_on_canvas = self.canvas.create_image(
                0,0,image=None,anchor='nw', state=tk.DISABLED)
        self.canvas.pack(side='left', fill='both', expand=True)

        # Scroll
        self.hbar = tk.Scrollbar(self.canvas, orient='horizontal',
                command=self.canvas.xview)
        self.hbar.pack(side='bottom', fill='x')
        self.vbar = tk.Scrollbar(self.canvas, orient='vertical',
                command=self.canvas.yview)
        self.vbar.pack(side='right', fill='y')
        self.canvas.config(xscrollcommand=self.hbar.set, 
                yscrollcommand=self.vbar.set)

        # Mask
        self.mask_img = None

        # Scale
        self.scale = 1.0

    def key_pressed(self, event='key_pressed'):
        self.kp = event.char
        if self.kp == '+':
            self.zoom(ratio=1.2)
        if self.kp == '-':
            self.zoom(ratio=1/1.2)
        if self.kp == 'p':
            self.draw_poly()
        if self.kp == 'x':
            self.clear_roi()
            Common.roi_pts.clear()
        if self.kp == 'g':
            self.do_grabcut()

    def do_grabcut(self):
        mode = Common.current_tool.get()
        print('do GrabCut using mode {}'.format(mode))
        self.root.gc.cal_mask(mode=mode, gc_rect=Common.grabcut_rect)
        self.show_gc_res_mask()
        #Common.grabcut_res = self.root.gc.cal_mask(
        #        mode=mode,
        #        gc_rect=Common.grabcut_rect, 
        #        #gc_mask=Common.grabcut_mask
        #        )
        #self.show_cv2_image(Common.grabcut_res)

    def zoom(self, ratio):
        self.scale = self.scale * ratio
        # canvas image
        self.scaled_img = self.resize_image(self.pil_img, self.scale)
        self.scaled_img = ImageTk.PhotoImage(self.scaled_img)
        self.canvas.itemconfig(self.img_on_canvas, image=self.scaled_img)
        # other items

    def resize_image(self, image, ratio):
        _w, _h = image.size
        # update the draw-able range
        self.img_w = int(_w*ratio)
        self.img_h = int(_h*ratio)
        return image.resize((self.img_w, self.img_w))

    def clear_roi(self):
        for tag in ['rect', 'temp_rect', 'guiding_cross', 'oval_0', 'poly']:
            self.canvas.delete(tag)

    def draw_poly(self):
        self.canvas.delete('poly')
        pts = [int(_) for _ in Common.polygon.flatten()]
        #print(pts)
        self.canvas.create_polygon(pts, tags='poly', outline='blue', width=1, fill='')

    def cursor_move_draw(self, event):
        '''
        To convert from window coordinates to canvas coordinates, 
        use the canvasx and canvasy methods
        https://stackoverflow.com/a/11310847
        '''
        try:
            mode = Common.current_tool.get()
            x = self.canvas.canvasx(event.x)
            y = self.canvas.canvasy(event.y)
            w = self.img_w
            h = self.img_h
        except:
            return

        if x < 0: x = 0
        if y < 0: y = 0
        if x > w: x = w
        if y > h: y = h
        '''guiding_cross'''
        if mode == 4:
            for tag in ['guiding_cross', 'temp_rect']:
                self.canvas.delete(tag)
            if Draw.set_guding_cross:
                self.canvas.create_line(0,y, w,y, x,y, x,0, x,h,
                        tags='guiding_cross', 
                        fill=Draw.cross_line_color, 
                        width=Draw.cross_line_width)
            if len(Common.roi_pts) == 2: # only one point has been set
                _x,_y = Common.roi_pts
                self.canvas.create_rectangle(_x,_y,x,y, 
                        tags='temp_rect', 
                        outline=Draw.roi_line_color,
                        width=Draw.roi_line_width,
                        )

    def set_mask(self, event):
        try:
            mode = Common.current_tool.get()
            x = self.canvas.canvasx(event.x)
            y = self.canvas.canvasy(event.y)
            w = self.img_w
            h = self.img_h
        except:
            return

        if x < 0: x = 0
        if y < 0: y = 0
        if x > w: x = w
        if y > h: y = h

        Common.roi_pts.extend([x,y])

        if mode == 4:
            if len(Common.roi_pts) > 4:
                #self.root.toggle_cross_guide()
                Common.roi_pts.clear()
            if len(Common.roi_pts) == 4:
                #self.root.toggle_cross_guide()
                self.canvas.delete('rect')
                _id = self.canvas.create_rectangle(Common.roi_pts,
                        tags=('rect'),
                        outline=Draw.roi_line_color, 
                        width=Draw.roi_line_width, 
                        )
                # Use coords to transform any rect corners to the format of
                # (xmin,ymin,xmax,ymax)
                Common.grabcut_rect = [int(c/self.scale) 
                        for c in self.canvas.coords(_id)]
            # Keep only the starting point
            #Common.roi_pts = Common.roi_pts[:2]
            return

        if mode == 0:
            fill_color = Draw.mask_BG['color']
            mask_val = Draw.mask_BG['val']
        elif mode == 1:
            fill_color = Draw.mask_FG['color']
            mask_val = Draw.mask_FG['val']
        elif mode == 2:
            fill_color = Draw.mask_PR_BG['color']
            mask_val = Draw.mask_PR_BG['val']
        elif mode == 3:
            fill_color = Draw.mask_PR_FG['color']
            mask_val = Draw.mask_PR_FG['val']
        else:
            pass
        #TODO: scale these...
        r = Draw.brush_size
        self.canvas.create_oval(
                x-r,y-r,x+r,y+r, tags='oval_0', fill=fill_color, width=0)
        #print(x,y, len(Common.roi_pts))
        _mask_img = Image.fromarray(Common.mask)
        _mask_draw = ImageDraw.Draw(_mask_img)
        _mask_draw.ellipse([x-r,y-r,x+r,y+r], fill=mask_val)
        #_mask_img.save('tmp_mask.jpg')
        Common.mask = np.array(_mask_img)

    def cancel_set_points(self, event='cancel_set_points'):
        '''drop the last points from the roi_pts'''
        Common.roi_pts = Common.roi_pts[:-2]

    def show_gc_res_mask(self):
        #TODO: create transparent bg
        _alpha = 0.4
        _mask = np.stack((Common.gc_res_mask,)*4, axis=-1)
        np_mask = np.where(_mask==(255,255,255,255),
                (0,0,255,int(_alpha*255)), (0,0,0,0)).astype(np.uint8)
        pil_mask = Image.fromarray(np_mask)
        blended = Image.alpha_composite(self.pil_img.convert('RGBA'), pil_mask)
        self.tk_mask = ImageTk.PhotoImage(blended)
        self.canvas.itemconfig(self.img_on_canvas, image=self.tk_mask)
        #self.canvas.config(scrollregion=(0,0,self.img_w, self.img_h))

    def show_cv2_image(self, cv2img):
        pil_img = Image.fromarray(
                cv2.cvtColor(cv2img, cv2.COLOR_BGR2RGB))
        self.tk_img = ImageTk.PhotoImage(pil_img.resize((self.img_w, self.img_h))) 
        self.canvas.itemconfig(self.img_on_canvas, image=self.tk_img)

    def load_image(self, img_filename):
        '''NOTE:
        Use `self.tk_img` instead of `tk_img` so that it won't be released
        http://effbot.org/pyfaq/why-do-my-tkinter-images-not-appear.htm
        '''
        self.pil_img = Image.open(img_filename)
        self.img_w, self.img_h = self.pil_img.size
        self.tk_img = ImageTk.PhotoImage(self.pil_img)
        self.canvas.itemconfig(self.img_on_canvas, image=self.tk_img)
        self.canvas.config(scrollregion=(0,0,self.img_w, self.img_h))


if __name__ == '__main__':
    app = App()
    app.mainloop()
