import tkinter as tk
import cv2
from PIL import Image
from PIL import ImageTk
from tkinter import SUNKEN, filedialog, Label

def count_obj():
     global panelA,panelB,entry
     #chọn ảnh 
     path=filedialog.askopenfilename()
     image=cv2.imread(path)
     


top=tk.Tk()
top.geometry("400x250")
name = Label(top, text = "chon anh").place(x = 30, y = 50)
button=tk.Button(text="select image",width=10,relief=SUNKEN,command=count_obj).place(x = 90, y = 50)
top.mainloop()
