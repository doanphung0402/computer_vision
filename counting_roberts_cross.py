import sys
import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt
from tkinter import SUNKEN, filedialog
from skimage import io
import tkinter as tk
import numpy as np
import cv2
from PIL import Image
from PIL import ImageTk
from tkinter import SUNKEN, filedialog
from skimage import io
from matplotlib import pyplot as plt

plt.rcParams['figure.figsize'] = [15, 10]


roberts_cross_v = np.array([[0, 0, 0],
                            [0, 1, 0],
                            [0, 0, -1]])

roberts_cross_h = np.array([[0, 0, 0],
                            [0, 0, 1],
                            [0, -1, 0]])


def select_image():
    global panelA, panelB, entry
    path = filedialog.askopenfilename()
    img = io.imread(path)
    fig = plt.figure(figsize=(10, 7))

    fig.add_subplot(2, 2, 1)
    plt.imshow(img)
    plt.axis('off')
    plt.title("ảnh gốc")

    # img = img.astype('float64')
    v = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # dùng độ sáng tối chanel v thay cho độ đậm nhạt channel S
    fig.add_subplot(2, 2, 3)
    plt.imshow(v, 'gray')
    plt.axis('off')
    plt.title("ảnh sau tách sáng")

    # lọc bỏ nhiễu
    fig.add_subplot(2, 2, 4)
    blur = cv2.GaussianBlur(v, (11, 11), 0)
    plt.imshow(v, 'gray')
    plt.axis('off')
    plt.title("ảnh sau lọc nhiễu ")
    # end figure1

    gray_img = np.dot(blur[..., :3], [0.2989, 0.5870, 0.1140])
    gray_img /= 255

    plt.imshow(gray_img, cmap=plt.get_cmap('gray'))
    plt.show()

    vertical = ndimage.convolve(gray_img, roberts_cross_v)
    horizontal = ndimage.convolve(gray_img, roberts_cross_h)

    edged_img = np.sqrt(np.square(horizontal) + np.square(vertical))

    plt.imshow(edged_img, cmap=plt.get_cmap('gray'))

    plt.show()


window = tk.Tk()
window.geometry("400x250")
button = tk.Button(text="select image", width=20,
                   relief=SUNKEN, command=select_image)
button.grid(row=1, column=0, columnspan=2, pady=50, padx=40)

window.mainloop()
