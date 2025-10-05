import sys
import os
import tkinter as tk
from tkinter import ttk

# Добавляем путь к модулям
sys.path.append(r"C:\python_control\modules")

from modules.CoppeliaController_01 import CoppeliaController

# --- Новая функция генерации одного зубца (относительные координаты) ---
def generate_single_tooth_gcode_relative(
    dx_list, dy_list, dz_list, feedrate=3000
):
    """
    Генерация G-кода для намотки одного зубца в относительных координатах
    :param dx_list: список приращений по X
    :param dy_list: список приращений по Y
    :param dz_list: список приращений по Z
    :param feedrate: скорость подачи
    """
    gcode = []
    gcode.append("; --- Начало намотки одного зубца ---")
    gcode.append("G90")  # сначала абсолютные координаты для стартовой позиции
    gcode.append("G1 F{0}".format(feedrate))
    gcode.append("G91")  # включаем относительные координаты

    for dx, dy, dz in zip(dx_list, dy_list, dz_list):
        cmd = "G1"
        if dx != 0:
            cmd += f" X{dx}"
        if dy != 0:
            cmd += f" Y{dy}"
        if dz != 0:
            cmd += f" Z{dz}"
        cmd += f" F{feedrate}"
        gcode.append(cmd)

    gcode.append("; --- Конец намотки зубца ---")
    return gcode


# --- Класс GUI приложения ---
class App:
    def __init__(self, root, controller_class, **kwargs):
        self.controller = controller_class(**kwargs)

        self.root = root
        self.root.title("Управление принтером в CoppeliaSim")
        self.root.geometry("450x400")

        # Создание виджетов GUI
        self.create_widgets()

    # --- Методы кнопок ---
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

    def on_Xplus_bt(self):
        self.controller.move_realtive(x=5)

    def on_Xminus_bt(self):
        self.controller.move_realtive(x=-5)

    def on_Yplus_bt(self):
        self.controller.move_realtive(y=5)

    def on_Yminus_bt(self):
        self.controller.move_realtive(y=-5)

    def on_Zplus_bt(self):
        self.controller.move_realtive(z=5)

    def on_Zminus_bt(self):
        self.controller.move_realtive(z=-5)

    def on_Eplus_bt(self):
        self.controller.move_realtive(e=5)

    def on_Eminus_bt(self):
        self.controller.move_realtive(e=-5)

    # --- Новая кнопка для намотки одного зубца ---
    def on_generate_tooth_bt(self):
        # Пример шагов (можно заменить на свои)
        dx_list = [0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5, 5, -5, -5, -5, -5, -5, 0, 0, 0]
        dy_list = [-5, -5, -5, -5, -5, -5, 0, 0, 0, 0, 0, 5, 5, 5, 5, 5, 5, 0, -5, -5]
        dz_list = [0, 0, 0, 0, 0, 0, -5, -5, -5, -5, -5, 0, 0, 0, 0, 0, 0, 5, 5, 5]

        gcode_lines = generate_single_tooth_gcode_relative(dx_list, dy_list, dz_list, feedrate=3000)
        print("Сгенерированный G-code для зубца:")
        for line in gcode_lines:
            print(line)
        self.controller.run_gcode(gcode_lines)

    # --- Создание интерфейса ---
    def create_widgets(self):
        self._add_buttons_panel()
        self._add_input_area()
        self._add_arrow_panel()

    def _add_buttons_panel(self):
        frame_1 = tk.Frame(self.root, borderwidth=2, relief="groove")
        frame_1.grid(row=0, column=0, rowspan=2, padx=2, pady=2, sticky="nw")

        buttons = [
            ("CONNECT", self.on_connect_bt),
            ("DISCONNECT", self.on_disconnect_bt),
            ("HOME", self.on_home_bt),
            ("set zero", self.on_setZero_bt),
            ("absalute\ncords", self.on_absalute_bt),
            ("relative\ncords", self.on_relative_bt),
            ("get pos", self.on_get_pos_bt),
            ("test", self.on_test_bt),
            ("Намотать зубец", self.on_generate_tooth_bt)  # новая кнопка
        ]

        for text, cmd in buttons:
            bt = tk.Button(frame_1, text=text, command=cmd)
            bt.pack(side="top", fill="x", expand=True)

    def _add_input_area(self):
        frame = tk.Frame(self.root, borderwidth=2, relief="groove")
        frame.grid(row=1, column=1, padx=2, pady=2, sticky="ew")

        self.text_area = tk.Text(frame, wrap="word", height=10, width=25)
        self.scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.text_area.yview)
        self.text_area.config(yscrollcommand=self.scrollbar.set)

        self.text_area.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        self.scrollbar.grid(row=0, column=2, sticky="ns", pady=5)

        # Кнопки для текстового поля
        self.add_button = tk.Button(frame, text="Добавить строку", command=self.add_line)
        self.add_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        self.print_button = tk.Button(frame, text="Распечатать", command=self.print_text)
        self.print_button.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

    def add_line(self):
        current_text = self.text_area.get("1.0", "end-1c")
        new_line = f"Строка {len(current_text.splitlines()) + 1}\n"
        self.text_area.insert("end", new_line)

    def print_text(self):
        text_content = self.text_area.get("1.0", "end-1c")
        print("Содержимое текстового поля:")
        print(text_content)

    def _add_arrow_panel(self):
        frame = tk.Frame(self.root, borderwidth=2, relief="groove")
        frame.grid(row=0, column=1, padx=2, pady=2, sticky="ew")

        tk.Button(frame, text="X-", command=self.on_Xminus_bt).grid(row=1, column=1)
        tk.Button(frame, text="X+", command=self.on_Xplus_bt).grid(row=1, column=4)
        tk.Button(frame, text="Y+", command=self.on_Yplus_bt).grid(row=0, column=2, columnspan=2)
        tk.Button(frame, text="Y-", command=self.on_Yminus_bt).grid(row=2, column=2, columnspan=2)
        tk.Button(frame, text="E-", command=self.on_Eminus_bt).grid(row=2, column=1)
        tk.Button(frame, text="E+", command=self.on_Eplus_bt).grid(row=2, column=4)
        tk.Button(frame, text="Z+", command=self.on_Zplus_bt).grid(row=0, column=5)
        tk.Button(frame, text="Z-", command=self.on_Zminus_bt).grid(row=1, column=5)


# --- Запуск приложения ---
if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = App(root, controller_class=CoppeliaController, debug=True)
        root.mainloop()

    except Exception as e:
        print(f"Ошибка: {e}")
        root.destroy()

    finally:
        if 'app' in locals() and app.controller.connection is not None:
            app.controller.disconnect()

# synced: 2025-10-05T17:23:19.868872
# synced: 2025-10-05T17:23:22.745173
# synced: 2025-10-05T17:23:25.472445
# synced: 2025-10-05T17:23:28.211693
# synced: 2025-10-05T17:23:31.162532
# synced: 2025-10-05T17:23:34.027550
# synced: 2025-10-05T17:23:36.755200
# synced: 2025-10-05T17:23:39.582802
# synced: 2025-10-05T17:23:42.239939
# synced: 2025-10-05T17:23:44.978122