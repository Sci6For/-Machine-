# coppelia_tooth_gui.py
import sys
import tkinter as tk
from tkinter import ttk

# Добавляем путь к модулям
sys.path.append(r"C:\python_control\modules")

from modules.CoppeliaController_01 import CoppeliaController

# --- Функция генерации G-code для одного зубца ---
def generate_tooth_gcode(left_x, right_x, z_bottom, z_top, turns=3, feedrate=1000):
    gcode = []
    gcode.append(f"G0 X{left_x} Z{z_bottom} F{feedrate}")
    for turn in range(turns):
        gcode.append(f"G1 X{right_x} Z{z_top} F{feedrate}")
        gcode.append(f"G1 X{left_x} Z{z_bottom} F{feedrate}")
    gcode.append("; Конец намотки одного зубца")
    return gcode

# --- Класс GUI приложения ---
class App:
    def __init__(self, root, **kwargs):
        self.controller = CoppeliaController(**kwargs)
        self.root = root
        self.root.title("Намотка зубца - CoppeliaSim")
        self.root.geometry("500x400")
        self.create_widgets()

    def on_connect_bt(self):
        print("connect")
        self.controller.connect()

    def on_disconnect_bt(self):
        print("disconnect")
        self.controller.disconnect()

    def on_home_bt(self):
        print("home")
        self.controller.home()

    def on_setZero_bt(self):
        print("setZero")
        self.controller.set_zero()

    def on_absalute_bt(self):
        print("absolute")
        self.controller._set_abs_cords()

    def on_relative_bt(self):
        print("relative")
        self.controller._set_rel_cords()

    def on_get_pos_bt(self):
        print("get_pos")
        print(self.controller.get_position())
        print("Internal position:", self.controller.position)

    def on_test_bt(self):
        self.controller.move_realtive(e=360)

    def on_generate_tooth_bt(self):
        left_x = 10
        right_x = 20
        z_bottom = 0
        z_top = 5
        turns = 4
        feedrate = 800
        gcode_lines = generate_tooth_gcode(left_x, right_x, z_bottom, z_top, turns, feedrate)
        print("Сгенерированный G-code для зубца:")
        for line in gcode_lines:
            print(line)
        self.controller.run_gcode(gcode_lines)

    def create_widgets(self):
        self._add_buttons_panel()
        self._add_arrow_panel()

    def _add_buttons_panel(self):
        frame_1 = tk.Frame(self.root, borderwidth=2, relief="groove")
        frame_1.grid(row=0, column=0, rowspan=2, padx=5, pady=5, sticky="nw")
        buttons = [
            ("CONNECT", self.on_connect_bt),
            ("DISCONNECT", self.on_disconnect_bt),
            ("HOME", self.on_home_bt),
            ("set zero", self.on_setZero_bt),
            ("absalute\ncords", self.on_absalute_bt),
            ("relative\ncords", self.on_relative_bt),
            ("get pos", self.on_get_pos_bt),
            ("test", self.on_test_bt),
            ("Намотка 1 зубца", self.on_generate_tooth_bt)
        ]
        for text, cmd in buttons:
            bt = tk.Button(frame_1, text=text, command=cmd)
            bt.pack(side="top", fill="x", expand=True)

    def _add_arrow_panel(self):
        frame = tk.Frame(self.root, borderwidth=2, relief="groove")
        frame.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        tk.Button(frame, text="X-", command=lambda: self.controller.move_realtive(x=-5)).grid(row=1, column=1)
        tk.Button(frame, text="X+", command=lambda: self.controller.move_realtive(x=5)).grid(row=1, column=4)
        tk.Button(frame, text="Y+", command=lambda: self.controller.move_realtive(y=5)).grid(row=0, column=2, columnspan=2)
        tk.Button(frame, text="Y-", command=lambda: self.controller.move_realtive(y=-5)).grid(row=2, column=2, columnspan=2)
        tk.Button(frame, text="E-", command=lambda: self.controller.move_realtive(e=-5)).grid(row=2, column=1)
        tk.Button(frame, text="E+", command=lambda: self.controller.move_realtive(e=5)).grid(row=2, column=4)
        tk.Button(frame, text="Z+", command=lambda: self.controller.move_realtive(z=5)).grid(row=0, column=5)
        tk.Button(frame, text="Z-", command=lambda: self.controller.move_realtive(z=-5)).grid(row=1, column=5)

# --- Запуск приложения ---
root = tk.Tk()
app = App(root, debug=True)
root.mainloop()