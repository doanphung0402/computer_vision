import tkinter as tk
import numpy as np
import cv2
from PIL import Image
from PIL import ImageTk
from tkinter import SUNKEN, filedialog
from skimage import io
from matplotlib import pyplot as plt
from scipy import ndimage

plt.rcParams['figure.figsize'] = [15, 10]


# roberts_cross_v = np.array([[0, 0, 0],
#                             [0, 1, 0],
#                             [0, 0, -1]])

roberts_cross_v = np.array([[1, 0],
                            [0, -1]])

roberts_cross_h = np.array([[0, -1],
                            [-1, 0]])


def select_image():
    global panelA, panelB, entry
    path = filedialog.askopenfilename()
    img = io.imread(path)
    fig = plt.figure(figsize=(10, 7))

    fig.add_subplot(2, 2, 1)
    plt.imshow(img)
    plt.axis('off')
    plt.title("ảnh gốc")

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

    fig1 = plt.figure(figsize=(10, 7))

    # img = img.astype('float64')
    gray_img = np.dot(img[..., :3], [0.2989, 0.5870, 0.1140])
    gray_img /= 255
    vertical = ndimage.convolve(gray_img, roberts_cross_v)
    horizontal = ndimage.convolve(gray_img, roberts_cross_h)
    roberts_cross = np.sqrt(np.square(horizontal) + np.square(vertical))

    # phát hiện cạnh dùng roberts_cross of cv2
    roberts_cross = cv2.Canny(blur, 10, 20)
    fig1.add_subplot(2, 2, 1)
    plt.imshow(roberts_cross, 'gray')
    plt.axis('off')
    plt.title("ảnh sau phát hiện cạnh ")

    # giãn nở rộng ảnh cv2
    kernel_erode = np.ones((5, 5), np.uint8)
    eroded = cv2.erode(roberts_cross, kernel_erode, iterations=1)
    fig1.add_subplot(2, 2, 2)
    plt.imshow(eroded, 'gray')
    plt.axis('off')
    plt.title("ảnh sau erode ")

    # giãn nở rộng ảnh cv2
    kernel_dilate = np.ones((3, 3), np.uint8)
    dilated = cv2.dilate(eroded, kernel_dilate, iterations=1)
    fig1.add_subplot(2, 2, 3)
    plt.imshow(dilated, 'gray')
    plt.axis('off')
    plt.title("ảnh sau dilate ")

    # dem
    cnt, hierarchy = cv2.findContours(
        dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    plt.show()
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    rgb2 = cv2.drawContours(rgb, cnt, -1, (0, 255, 0), 2)
    rgb2 = Image.fromarray(rgb2)
    rgb2 = ImageTk.PhotoImage(rgb2)

    img = Image.fromarray(img)
    img = ImageTk.PhotoImage(img)

    panelA = tk.Label(image=img)
    panelA.image = img
    panelA.grid(row=0, column=0)

    panelB = tk.Label(image=rgb2)
    panelB.image = rgb2
    panelB.grid(row=0, column=1)

    entry = tk.Entry(width=30)
    entry.grid(row=2, column=0, columnspan=2)
    entry.insert(0, 'Number of Objects: ')
    entry.delete(20, tk.END)
    entry.insert(20, len(cnt))


window = tk.Tk()
window.geometry("400x250")
button = tk.Button(text="select image", width=20,
                   relief=SUNKEN, command=select_image)
button.grid(row=1, column=0, columnspan=2, pady=50, padx=40)

window.mainloop()
