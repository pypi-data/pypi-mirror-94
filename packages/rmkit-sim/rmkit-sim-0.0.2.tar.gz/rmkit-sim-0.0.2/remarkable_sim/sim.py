# Evan Widloski - 2020-09-13

import argparse
import logging
import os
import stat
import subprocess
import sys
import tkinter as tk
from tkinter import ttk
from .evsim import (
    makefifo, write_evdev, codes_stylus, codes_touch, codes_button, code_sync,
    stylus_max_x, stylus_max_y, touch_max_x, touch_max_y, affine_map
)

logging.basicConfig(format='%(message)s')
log = logging.getLogger('resim')

# fake evdev interface
path_fifo_stylus = 'event0'
path_fifo_touch = 'event1'
path_fifo_button = 'event2'
# screen buffer
path_fb = 'fb.pnm'

# period between reading framebuffer
screen_update_delay = 100 # (ms)


def round_rectangle(canvas, x1, y1, x2, y2, r=25, **kwargs):
    points = (
        x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, x2, y1+r, x2,
        y1+r, x2, y2-r, x2, y2-r, x2, y2, x2-r, y2, x2-r, y2, x1+r,
        y2, x1+r, y2, x1, y2, x1, y2-r, x1, y2-r, x1, y1+r, x1, y1+r, x1, y1
    )
    return canvas.create_polygon(points, **kwargs, smooth=True)

class GUI(object):
    def __init__(self, root, display_scale, executable):

        self.display_scale = display_scale
        self.screen_width = int(1404 // self.display_scale)
        self.screen_height = int(4 * self.screen_width // 3)

        self.root = root
        root.title("reMarkable simulator")

        # ----- Screen Area -----

        self.f1 = tk.Frame(
            self.root,
            width=1.3 * self.screen_width,
            height=1.7 * self.screen_width,
            background='white'
        )
        self.f1.grid(row=1, column=1)
        self.tablet = tk.Canvas(
            self.f1,
            width=1.1278 * self.screen_width,
            height=1.6256 * self.screen_width,
            background='white',
            highlightthickness=0,
            bd=0
        )
        # center tablet canvas in frame
        # TODO: use .pack() instead of manual positioning
        self.tablet.place(
            # TODO: tkinter bug, canvas['width'] is a string?
            x=(self.f1['width'] - int(self.tablet['width'])) / 2,
            y=(self.f1['height'] - int(self.tablet['height'])) / 2,
        )
        round_rectangle(
            self.tablet,
            0, 0,
            1.1278 * self.screen_width - 1, 1.6256 * self.screen_width - 1,
            r=30,
            fill='gray98',
            outline='gray80'
        )
        round_rectangle(
            self.tablet,
            0.0132 * self.screen_width, 0.0132 * self.screen_width,
            1.1146 * self.screen_width, 1.6124 * self.screen_width,
            r=15,
            fill='gray90'
        )
        self.screen = tk.Canvas(
            self.tablet,
            width=self.screen_width,
            height=self.screen_height,
            background='gray90'
        )
        self.screen.place(x=0.0600 * self.screen_width, y=0.1215 * self.screen_width)
        self.screen.bind('<ButtonPress-1>', self.screen_press)
        self.screen.bind('<B1-Motion>', self.screen_motion)
        self.screen.bind('<ButtonRelease-1>', self.screen_release)

        # Buttons

        self.b1 = tk.Button(
            self.tablet,
            relief='groove',
            width=int(0.0805 * self.screen_width),
            height=int(0.0805 * self.screen_width),
            background='gray95'
        )
        self.b1.place(x=0.0644 * self.screen_width, y=1.4919 * self.screen_width)
        self.b1.configure(width=2, height=2)
        self.b1.bind('<ButtonPress>', lambda _: self.press('left'))
        self.b1.bind('<ButtonRelease>', lambda _: self.release('left'))
        self.b2 = tk.Button(
            self.tablet,
            relief='groove',
            width=int(0.0805 * self.screen_width),
            height=int(0.0805 * self.screen_width),
            background='gray95'
        )
        self.b2.place(x=0.5142 * self.screen_width, y=1.4919 * self.screen_width)
        self.b2.configure(width=2, height=2)
        self.b2.bind('<ButtonPress>', lambda _: self.press('home'))
        self.b2.bind('<ButtonRelease>', lambda _: self.release('home'))
        self.b3 = tk.Button(
            self.tablet,
            relief='groove',
            width=int(0.0805 * self.screen_width),
            height=int(0.0805 * self.screen_width),
            background='gray95'
        )
        self.b3.place(x=0.9640 * self.screen_width, y=1.4919 * self.screen_width)
        self.b3.configure(width=2, height=2)
        self.b3.bind('<ButtonPress>', lambda _: self.press('right'))
        self.b3.bind('<ButtonRelease>', lambda _: self.release('right'))
        self.bpow = tk.Button(
            self.tablet,
            relief='groove',
            width=int(0.0805 * self.screen_width),
            height=int(0.0805 * self.screen_width),
            background='gray95'
        )
        self.bpow.place(x=0.5142 * self.screen_width, y=0.0300 * self.screen_width)
        self.bpow.configure(width=2, height=1)
        self.bpow.bind('<ButtonPress>', lambda _: self.press('power'))
        self.bpow.bind('<ButtonRelease>', lambda _: self.release('power'))

        # ----- Settings Area -----

        self.f2 = tk.Frame(self.root)
        self.f2.grid(row=0, column=1)

        self.input = tk.StringVar()
        self.input.set('Stylus')
        tk.Label(self.f2, text='Input Method').grid(row=0, column=0)
        tk.OptionMenu(self.f2, self.input, 'Stylus', 'Touch').grid(row=0, column=1)

#        tk.Label(self.f2, text='Stylus Pressure').grid(row=1, column=0)
#        self.pressure = tk.Scale(self.f2, from_=0, to=4095, orient='horizontal')
#        self.pressure.set(4000)
#        self.pressure.grid(row=1, column=1)
#        tk.Label(self.f2, text='Stylus Tilt X').grid(row=2, column=0)
#        self.tiltx = tk.Scale(self.f2, from_=-6300, to=6300, orient='horizontal')
#        self.tiltx.grid(row=2, column=1)
#        self.tiltx.set(1000)
#        tk.Label(self.f2, text='Stylus Tilt Y').grid(row=3, column=0)
#        self.tilty = tk.Scale(self.f2, from_=-6300, to=6300, orient='horizontal')
#        self.tilty.set(1000)
#        self.tilty.grid(row=3, column=1)
#
#        ttk.Separator(self.f2, orient='vertical').grid(row=0, column=2, rowspan=3, sticky='ns')

        # Checkboxes

        # make colums 4, 5, 6 equal width for checkboxes
        self.f2.grid_columnconfigure(4, uniform='check')
        self.f2.grid_columnconfigure(5, uniform='check')
        self.f2.grid_columnconfigure(6, uniform='check')

        self.check1 = tk.IntVar()
        self.check2 = tk.IntVar()
        self.check3 = tk.IntVar()
        self.checkpow = tk.IntVar()
#        self.c1 = tk.Checkbutton(self.f2, variable=self.check1, text='Button 1')
#        self.c1.grid(row=0, column=4, sticky='w')
#        self.c2 = tk.Checkbutton(self.f2, variable=self.check2, text='Button 2')
#        self.c2.grid(row=0, column=5, sticky='w')
#        self.c3 = tk.Checkbutton(self.f2, variable=self.check3, text='Button 3')
#        self.c3.grid(row=0, column=6, sticky='w')
#        self.cpow = tk.Checkbutton(self.f2, variable=self.checkpow, text='Power')
#        self.cpow.grid(row=1, column=4, sticky='w')

#        self.hold = tk.Button(self.f2, text='Multi Press')
#        self.hold.grid(row=2, column=5)
#        self.hold.bind('<ButtonPress>', self.multi_press)
#        self.hold.bind('<ButtonRelease>', self.multi_release)

        self.root.after(screen_update_delay, self.load_screen)

        # ----- FIFOs -----

        self.fifo_stylus = makefifo(path_fifo_stylus)
        self.fifo_touch = makefifo(path_fifo_touch)
        self.fifo_button = makefifo(path_fifo_button)

        if executable is not None:
            # prepend exec so that executable inherits shell process and can be killed
            self.subprocess = subprocess.Popen('exec ' + executable, shell=True)
        else:
            self.subprocess = None


    def load_screen(self):
        # FIXME: file is sometimes read before writing is finished
        from PIL import Image, ImageTk
        if os.path.exists(path_fb):
            try:
                img = Image.open(path_fb)
            except tk.TclError:
                return
            except KeyboardInterrupt:
                sys.exit(0)

            self.img_scaled = ImageTk.PhotoImage(
                img.resize((self.screen_width, self.screen_height)))

            self.screen.create_image(0, 0, image=self.img_scaled, anchor='nw')
            self.root.after(screen_update_delay, self.load_screen)
        else:
            print(path_fb + " not found")

    # ----- Event Callbacks -----

    # handle multi button press
    def multi_press(self, _):
        if self.check1.get():
            self.press('left')
        if self.check2.get():
            self.press('home')
        if self.check3.get():
            self.press('right')
        if self.checkpow.get():
            self.press('power')

    # handle multi button release
    def multi_release(self, _):
        if self.check1.get():
            self.release('left')
        if self.check2.get():
            self.release('home')
        if self.check3.get():
            self.release('right')
        if self.checkpow.get():
            self.release('power')

    # handle single button press
    def press(self, button):
        write_evdev(self.fifo_button, *codes_button[button], 1)
        write_evdev(self.fifo_button, *code_sync)

    # handle single button release
    def release(self, button):
        write_evdev(self.fifo_button, *codes_button[button], 0)
        write_evdev(self.fifo_button, *code_sync)

    def emit_screen_coords(self, event):
        if self.input.get() == 'Stylus':
            write_evdev(
                self.fifo_stylus,
                *codes_stylus['abs_y'],
                affine_map(event.x, 0, self.screen_width, 0, stylus_max_y)
            )
            write_evdev(
                self.fifo_stylus,
                *codes_stylus['abs_x'],
                affine_map(event.y, 0, self.screen_height, stylus_max_x, 0)
            )

        if self.input.get() == 'Touch':
            pass

    # screen initial press
    def screen_press(self, event):
        self.emit_screen_coords(event)

        if self.input.get() == 'Stylus':
            write_evdev(self.fifo_stylus, *codes_stylus['toolpen'], 1)
            write_evdev(self.fifo_stylus, *codes_stylus['touch'], 1)
            write_evdev(self.fifo_stylus, *codes_stylus['abs_distance'], 0)
            write_evdev(self.fifo_stylus, *codes_stylus['abs_pressure'], 4000) # self.pressure.get())
            write_evdev(self.fifo_stylus, *codes_stylus['abs_tilt_x'], 1000) # self.tiltx.get())
            write_evdev(self.fifo_stylus, *codes_stylus['abs_tilt_y'], 1000) # self.tilty.get())
            write_evdev(self.fifo_stylus, *code_sync)

        if self.input.get() == 'Touch':
            pass

    # screen motion after press
    def screen_motion(self, event):
        self.emit_screen_coords(event)

        if self.input.get() == 'Stylus':
            write_evdev(self.fifo_stylus, *code_sync)

        if self.input.get() == 'Touch':
            pass

    # screen release
    def screen_release(self, event):
        self.emit_screen_coords(event)

        if self.input.get() == 'Stylus':
            write_evdev(self.fifo_stylus, *codes_stylus['touch'], 0)
            write_evdev(self.fifo_stylus, *codes_stylus['toolpen'], 0)
            write_evdev(self.fifo_stylus, *codes_stylus['abs_distance'], 100)
            write_evdev(self.fifo_stylus, *codes_stylus['abs_pressure'], 0)
            write_evdev(self.fifo_stylus, *code_sync)

        if self.input.get() == 'Touch':
            pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('executable', nargs='?', metavar='PATH', default=None, type=str, help="path to executable")
    parser.add_argument('--display_scale', '-ds', type=float, default=3, help="scale down rM resolution")
    parser.add_argument('--debug', action='store_true', help="enable debugging")

    args = parser.parse_args()

    if args.debug:
        log.setLevel('DEBUG')

    root = tk.Tk()
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(2, weight=1)
    root.columnconfigure(2, weight=1)

    gui = GUI(root, args.display_scale, args.executable)

    try:
        tk.mainloop()
    except KeyboardInterrupt:
        pass

    if gui.subprocess is not None:
        gui.subprocess.terminate()
    os.remove(path_fifo_stylus)
    os.remove(path_fifo_touch)
    os.remove(path_fifo_button)


if __name__ == '__main__':
    main()
