import tkinter as tk
import cv2
from PIL import Image
from PIL import ImageTk
from tkinter import SUNKEN, filedialog
from skimage import io
from matplotlib import pyplot as plt
def select_image():
    global panelA,panelB,entry
    path=filedialog.askopenfilename()
    img=io.imread(path)
    fig = plt.figure(figsize=(10, 7))
     
    fig.add_subplot(2,2,1)
    plt.imshow(img)
    plt.axis('off')
    plt.title("ảnh gốc")
    
    v = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    #dùng độ sáng tối chanel v thay cho độ đậm nhạt channel S
    fig.add_subplot(2,2,3)
    plt.imshow(v, 'gray')
    plt.axis('off')
    plt.title("ảnh sau tách sáng")

    #lọc bỏ nhiễu 
    fig.add_subplot(2,2,4)
    blur = cv2.GaussianBlur(v,(11,11),0)
    plt.imshow(v, 'gray')
    plt.axis('off')
    plt.title("ảnh sau lọc nhiễu ")
    #end figure1 

    fig1 = plt.figure(figsize=(10, 7))
    #phát hiện cạnh dùng canny of cv2 
    canny = cv2.Canny(blur, 30, 100) 
    fig1.add_subplot(2,2,1)
    plt.imshow(canny,'gray')
    plt.axis('off')
    plt.title("ảnh sau phát hiện cạnh ")
    
 

    #giãn nở rộng ảnh cv2
    dilated = cv2.dilate(canny, (1, 1), iterations=0)
    fig1.add_subplot(2,2,2)
    plt.imshow(dilated,'gray')
    plt.axis('off')
    plt.title("ảnh sau dilate ")


    #dem 
    cnt, hierarchy = cv2.findContours(dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    plt.show()
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    rgb2 = cv2.drawContours(rgb, cnt, -1, (0, 255, 0), 2)
    rgb2 = Image.fromarray(rgb2)
    rgb2 = ImageTk.PhotoImage(rgb2)

    img = Image.fromarray(img)
    img = ImageTk.PhotoImage(img)

    panelA = tk.Label(image=img)
    panelA.image = img
    panelA.grid(row=0,column=0)
    
    # panelB = tk.Label(image=rgb2)
    # panelB.image = rgb2
    # panelB.grid(row=0,column=1)

    entry=tk.Entry(width=30)
    entry.grid(row=2,column=0,columnspan=2)
    entry.insert(0,'Number of Objects: ')
    entry.delete(20,tk.END)
    entry.insert(20,len(cnt))

window=tk.Tk()
window.geometry("400x250")
button=tk.Button(text="select image",width=20,relief=SUNKEN,command=select_image)
button.grid(row=1,column=0,columnspan=2,pady=50,padx=40)

window.mainloop()
