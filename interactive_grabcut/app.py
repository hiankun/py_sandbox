import tkinter as tk
from tkinter.filedialog import (
        askdirectory, 
        asksaveasfile,
        askopenfilename)
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np


def grabcut():
    mask = np.zeros(img.shape[:2],np.uint8)
    bgdmodel = np.zeros((1, 65), np.float64)
    fgdmodel = np.zeros((1, 65), np.float64)
    rect = #TODO
    cv2.grabCut(img2, mask, rect, bgdmodel, fgdmodel, 1, cv2.GC_INIT_WITH_RECT)
    mask2 = np.where((mask==1) + (mask==3), 255, 0).astype('uint8')
    output = cv2.bitwise_and(img, img, mask=mask2)


class Common:
    roi_pts = []
    img_file = None
    current_tool = None
    tool_set = [
       ("0:Rectangle", 0),
       ("1:Curves", 1),
       ]
    tool_info = "Key strokes usage\n"\
               +"-----------------\n"\
               +"Esc: Cancel points\n"\
               +"g: Toggle guiding\n"\
               +"   cross on/off\n"\
               +"-----------------"

class Draw:
    canvas_bg_color = '#0a082e'
    cross_line_color = '#aa9cff'
    cross_line_width = 1
    roi_line_color = '#aacc00'
    roi_line_width = 2
    set_guding_cross = True


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("GrabCut")
        self.minsize(1200,900)
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

        self.bind('<g>', self.toggle_cross_guide)

    def toggle_cross_guide(self, event='toggle_cross_guide'):
        Draw.set_guding_cross = not Draw.set_guding_cross
        self.imagecanvas.canvas.delete('guiding_cross')

    def set_img2canvas(self):
        filename = Common.img_file
        print(filename)
        self.imagecanvas.show_image(filename)

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
        Common.current_tool.set(0)
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
        self.canvas.bind('<ButtonPress-1>', self.set_points)
        self.canvas.bind_all('<Escape>', self.cancel_set_points)
        self.img_on_canvas = self.canvas.create_image(
                0,0,image=None,anchor='nw',
                state=tk.DISABLED)
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

    def key_pressed(self, event='key_pressed'):
        self.kp = event.char
        if self.kp == 'n':
            print('do GrabCut')

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
        # only rect need cursor guide?
        if mode == 0:
            self.canvas.delete('guiding_cross')
            self.canvas.delete('temp_rect')
            #if x>0 and y>0 and x<w and y<h and Draw.set_guding_cross:
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
                        width=Draw.roi_line_width)
        elif mode == 1:
            pass
        else:
            pass

    def set_points(self, event):
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        if x < 0: x = 0
        if y < 0: y = 0
        if x > self.img_w: x = self.img_w
        if y > self.img_h: y = self.img_h
        Common.roi_pts.extend([x,y])

        mode = Common.current_tool.get()
        if mode == 0:
            if len(Common.roi_pts) >= 4:
                self.draw_roi(Common.roi_pts)
                Common.roi_pts.clear()
        else:
            Common.roi_pts.clear()
            pass

    def cancel_set_points(self, event='cancel_set_points'):
        '''drop the last points from the roi_pts'''
        Common.roi_pts = Common.roi_pts[:-2]

    def get_image(self, img_filename, resize=False):
        pil_img = Image.open(img_filename)
        self.img_w, self.img_h = pil_img.size
        '''TODO:
        The following code doesn't resize properly...
        '''
        if resize:
            _w, _ = pil_img.size
            if _w > self.root.width:
                pil_img = self.resize_image(pil_img, self.root.width/_w)
            _, _h = pil_img.size
            if _h > self.root.height:
                pil_img = self.resize_image(pil_img, self.root.height/_h)
        return ImageTk.PhotoImage(pil_img)

    def show_image(self, img_filename):
        '''NOTE:
        Use `self.img` instead of `img` so that it won't be released
        http://effbot.org/pyfaq/why-do-my-tkinter-images-not-appear.htm
        '''
        self.img = self.get_image(img_filename)
        self.canvas.itemconfig(self.img_on_canvas, image=self.img)
        self.canvas.config(scrollregion=(0,0,self.img_w, self.img_h))

    def draw_roi(self, pts):
        mode = Common.current_tool.get()
        if mode == 0:
            roi_id = self.canvas.create_rectangle(pts, tags=('rect'),
                    outline=Draw.roi_line_color, width=Draw.roi_line_width, 
                    )
        elif mode == 1:
            pass


if __name__ == '__main__':
    app = App()
    app.mainloop()
