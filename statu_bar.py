from tkinter import *
from PIL import ImageTk, Image

root = Tk()
root.title("hello")
root.iconbitmap('download.ico')

img = Image.open("2.jpg")
img = img.resize((600, 600))
my_img2 = ImageTk.PhotoImage(img)
img = Image.open("3.jpg")
img = img.resize((600, 600))
my_img3 = ImageTk.PhotoImage(img)
img = Image.open("4.jpg")
img = img.resize((600, 600))
my_img4 = ImageTk.PhotoImage(img)
img = Image.open("5.jpg")
img = img.resize((600, 600))
my_img5 = ImageTk.PhotoImage(img)

cur = 0
image_list = [my_img2, my_img3, my_img4, my_img5]
status = Label(root, text="Image "+str(cur+1)+" of "+str(len(image_list)),bd=1,relief=SUNKEN,anchor=E)
status.grid(row=2, column=0,columnspan=3,sticky=W+E)

my_label = Label(image=my_img2)
my_label.grid(row=0, column=0, columnspan=3)


def next():
    global my_label
    global button_next
    global button_back
    global status
    my_label.grid_forget()

    global cur
    if (cur == 3):
        cur = 0
    else:
        cur = cur+1
    my_label = Label(image=image_list[cur])
    my_label.grid(row=0, column=0, columnspan=3)
    status = Label(root, text="Image "+str(cur+1)+" of "+str(len(image_list)),bd=1,relief=SUNKEN,anchor =E)
    status.grid(row=2, column=0,columnspan=3,sticky=W+E)


def back():
    global my_label
    global button_next
    global button_back

    my_label.grid_forget()

    global cur
    if (cur == 0):
        cur = 3
    else:
        cur = cur-1
    my_label = Label(image=image_list[cur])
    my_label.grid(row=0, column=0, columnspan=3)
    status = Label(root, text="Image "+str(cur+1)+" of "+str(len(image_list)),bd=1,relief=SUNKEN,anchor = E)
    status.grid(row=2, column=0,columnspan=3,sticky=W+E)


button_back = Button(root, text='<<', command=back)
button_exit = Button(root, text='exit', command=root.quit)
button_next = Button(root, text='>>', command=next)

button_back.grid(row=1, column=0)
button_exit.grid(row=1, column=1)
button_next.grid(row=1, column=2)

root.mainloop()
