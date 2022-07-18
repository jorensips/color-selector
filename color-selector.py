import pyautogui
from pynput import mouse
from functools import partial
from tkinter import Tk, Label


class LabelPrinter:
    def __init__(self, root):
        self.root = root

    @staticmethod
    def rgb_to_hex(r,g,b):
        return f'#{r:02x}{g:02x}{b:02x}'

    def print_color(self, color_rgb):
        color_hex = self.rgb_to_hex(*color_rgb)
        Label(self.root, text=f'RGB: {color_rgb}', bg=color_hex).pack(pady=10)


class MouseListener:
    def __init__(self, subs=[]):
        self.subs = subs
        mouse.Listener(on_click=self.on_click).start()
    
    def subscribe(self, sub):
        self.subs.append(sub)
    
    def on_click(self, x, y, button, pressed):
        if button == mouse.Button.left and not pressed:
            pixel_color_rgb = pyautogui.screenshot().getpixel((x, y))
            for sub in self.subs:
                sub(pixel_color_rgb)


def start_tkinter():
    root = Tk()
    root.title('Color selector')
    root.geometry('400x400')
    return root


if __name__ == '__main__':
    root = start_tkinter()
    label_printer = LabelPrinter(root)
    mouse_listener = MouseListener(subs=[label_printer.print_color])
    root.mainloop()