import tkinter as tk
 
from pynput import keyboard

import os
import ctypes
from time import sleep
from random import randint

######################
# variables
######################

user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

size_x = 250
size_y = 120

whitespace = [keyboard.Key.space, keyboard.Key.enter, keyboard.Key.tab]
counter_types = ["Word Count:", "Char Count:", "CC w/ Spaces:"]
d_space = [4, 5, 1]
d_type = ["wc", "cc", "cc_with_space"]

d = {
    "type": 0,
    "cc": 0,
    "cc_with_space": 0,
    "wc": 0,
    "last": '',
    "tracking": True,
    "move mode": False,
    "mini": False,
    "padx": screensize[0] - size_x,
    "pady": screensize[1] - size_y,
    "curr": "",
    "exit": False
}

asset_list = [x for x in os.listdir("assets") if x.endswith(".jpg") or x.endswith(".png") or x.endswith(".jpeg") or x.endswith(".gif")]
d["curr"] = asset_list.pop(randint(0, len(asset_list)-1))

######################
# keyboard functions
######################

def getSpaces():
    return " " * (max(d_space[d["type"]] - len(str(d[d_type[d["type"]]])), 1))

def on_press(key, text):
    try:
        if key == keyboard.Key.esc:
            if d["last"] == keyboard.Key.shift:
                d["move mode"] = True
                moveLabel.grid(column=1, row=2, columnspan=2, pady=4)
                if not d["mini"]:
                    heart.grid_forget()
                root.after(0, moveAnimation)
            elif d["last"] == keyboard.Key.esc:
                d["exit"] = True
            else:
                d["move mode"] = False
                moveLabel.grid_forget()
                if not d["mini"]:
                    heart.grid(column=1, row=3, columnspan=2, pady=4)
        elif d["tracking"]:
            if key == keyboard.Key.space:
                d["cc_with_space"] += 1
                if d["last"] not in whitespace:
                    d["wc"] += 1
            elif key in whitespace and d["last"] not in whitespace:
                d["wc"] += 1
            elif key.char:
                d["cc"] += 1
                d["cc_with_space"] += 1
        d["last"] = key
        text.set("{0}{1}{2}".format(counter_types[d["type"]], getSpaces(), d[d_type[d["type"]]]))
    except AttributeError:
        d["last"] = key
        if d["move mode"]:
            if key == keyboard.Key.right:
                updateFrame(f, 10, 0)
            elif key == keyboard.Key.left:
                updateFrame(f, -10, 0)
            elif key == keyboard.Key.up:
                updateFrame(f, 0, 10)
            elif key == keyboard.Key.down:
                updateFrame(f, 0, -10)

def on_release(key, window):
    if key == keyboard.Key.esc and d["exit"]:
        if d["last"] == keyboard.Key.esc:
            window.destroy()
            return False
        else:
            d["exit"] = False

listener = keyboard.Listener(
    on_press=lambda key: on_press(key, counter),
    on_release=lambda key: on_release(key, root))
listener.start()

######################
# tkinter frames
######################

def updateFrame(frame, x, y):
    d["padx"] = min(max(0, d["padx"] + x), screensize[0] - size_x)
    d["pady"] = min(max(0, d["pady"] - y), screensize[1] - size_y)
    frame.grid(padx=d["padx"], pady=d["pady"])
    root.update()

root = tk.Tk()

ff = tk.Frame(root, bg = 'grey', height=screensize[1], width=screensize[0])
ff.grid()
ff.grid_propagate(0)

f = tk.Frame(ff, bg = 'grey', height=size_y, width=size_x)
updateFrame(f, -30, 50)
f.grid()
f.anchor(tk.SE)
f.grid_propagate(0)

frm = tk.Frame(f, bg='grey')
frm.grid(row=0, column=1, pady=(5, 0))

######################
# tkinter images
######################

img = tk.PhotoImage(file='assets\{0}'.format(d["curr"]))
factor_x = max((img.width() + 90) // 100, 1)
factor_y = max((img.height() + 90) // 100, 1)
smaller_img = img.subsample(factor_x, factor_y)
limg= tk.Label(f, i=smaller_img, bg='grey')
limg.grid(row=0, column=0)

######################
# color palette
######################

dark_blue = "#0B3142"
dark_green = "#0F5257"
mid_gray = "#9C92A3"
mid_purple = "#C6B9CD"
light_purple = "#D6D3F0"

#########################
# tkinter buttons/labels
#########################

counter = tk.StringVar()
counter.set("{0}{1}{2}".format(counter_types[d["type"]], getSpaces(), d[d_type[d["type"]]]))
label = tk.Label(frm, textvariable=counter,fg=light_purple, bg=dark_green)
label.grid(column=1, columnspan=3, row=0, padx=5,pady=5)

def right(text):
    d["type"] += 1
    if d["type"] >= len(counter_types):
        d["type"] = d["type"] % len(counter_types)
    text.set("{0}{1}{2}".format(counter_types[d["type"]], getSpaces(), d[d_type[d["type"]]]))
def left(text):
    d["type"] -= 1
    if d["type"] < 0:
        d["type"] = d["type"] % len(counter_types)
    text.set("{0}{1}{2}".format(counter_types[d["type"]], getSpaces(), d[d_type[d["type"]]]))
lButton = tk.Button(frm, text="<", command=lambda: left(counter), bg=light_purple, fg=dark_blue)
rButton = tk.Button(frm, text=">", command=lambda: right(counter), bg=light_purple, fg=dark_blue)
lButton.grid(column=0, row=0)
rButton.grid(column=4, row=0)

def moveHelper(txt):
    for i in range(12):
        if not d["move mode"]:
            moveLabel.grid_forget()
            if not d["mini"]:
                heart.grid(column=1, row=3, columnspan=2, pady=4)
            return
        moveText.set(txt)
        root.update()
        sleep(0.05)
def moveAnimation():
    while d["move mode"]:
        moveHelper("Moving")
        moveHelper("Moving.")
        moveHelper("Moving..")
        moveHelper("Moving...")
moveText = tk.StringVar()
moveText.set("Moving")
moveLabel = tk.Label(frm, textvariable=moveText, fg=light_purple, bg=dark_blue)

pause = tk.StringVar()
pause.set("Pause")
def setPause(txt):
    if d["tracking"]:
        txt.set("Start")
    else:
        txt.set("Pause")
    d["tracking"] = not d["tracking"]
p = tk.Button(frm, textvariable=pause, command=lambda: setPause(pause), bg=mid_gray, fg=dark_blue)
p.grid(column=1, row=1, padx=(10,0))

def setMinimalist(txt):
    if d["mini"]:
        limg.grid(row=0, column=0)
        heart.grid(column=1, row=3, columnspan=2, pady=4)
        mini.configure(bg=mid_gray, fg=dark_blue)
        txt.set("Mini")
    else:
        limg.grid_forget()
        heart.grid_forget()
        mini.configure(bg=dark_blue, fg=light_purple)
        txt.set("Max")
    d["mini"] = not d["mini"]
miniText = tk.StringVar()
miniText.set("Mini")
mini = tk.Button(frm, textvariable=miniText, command=lambda: setMinimalist(miniText), bg=mid_gray, fg=dark_blue)
mini.grid(column=2,row=1,padx=(0,6))

def randomizeImg():
    index = randint(0, len(asset_list)-1)
    asset_list.append(d["curr"])
    d["curr"] = asset_list.pop(index)
    img = tk.PhotoImage(file='assets\{0}'.format(d["curr"]))
    factor_x = max((img.width() + 90) // 100, 1)
    factor_y = max((img.height() + 90) // 100, 1)
    smaller_img = img.subsample(factor_x, factor_y)
    limg.configure(image=smaller_img) 
    limg.image = smaller_img
heart = tk.Button(frm, text="★", command=randomizeImg, fg=dark_blue, bg=light_purple)
heart.grid(column=1, row=3, columnspan=2, pady=4)

######################
# main loop
######################

root.wm_attributes("-topmost", 1)
root.wm_attributes('-fullscreen', 'True')
root.attributes('-transparentcolor', 'grey')
root.mainloop()
