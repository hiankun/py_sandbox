# source: https://www.youtube.com/watch?v=U0sVp1xLiyo
from tkinter import *

def paint(event):
    color = 'red'
    x1, y1 = (event.x-1), (event.y-1)
    x2, y2 = (event.x+1), (event.y+1)
    c.create_oval(x1,y1,x2,y2,fill=color,outline=color)


master = Tk()

c = Canvas(master, width=600, height=400, bg='white')
c.pack(expand=True, fill=BOTH)
c.bind('<B1-Motion>', paint)

master.mainloop()
