import sys
import os
import math
import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime

# Путь к модулям
sys.path.append(r"C:\python_control\modules")

from modules.CoppeliaController_01 import CoppeliaController

SESSION_STORE = {
    "machine_dims": {
        "PrintWinder_pos": (0.05, 0.125, 0.025),
        "Joint_E_pos": (-0.03, 0.0, 0.04),
        "cuboid_sizes": [
            (0.05, 0.30, 0.05),
            (0.05, 0.05, 0.10),
            (0.30, 0.25, 0.35),
            (0.01, 0.02, 0.06),
            (0.05, 0.05, 0.30),
            (0.20, 0.20, 0.05),
            (0.20, 0.20, 0.20),
        ]
    },
    "z_top": None,
    "z_bottom": None,
    "slot_height": None,
    "center_xy": (0.05, 0.125)  # default центр намотки (по PrintWinder_pos XY)
}


# ---Утилиты---
def parse_point_line(line):
    """
    Принимает строку с двумя числами: 'x,y' или 'x y'
    Возвращает (x,y) как float.
    """
    if not line:
        return None
    s = line.strip().replace(",", " ").split()
    if len(s) < 2:
        return None
    try:
        x = float(s[0])
        y = float(s[1])
        return (x, y)
    except Exception:
        return None


def parse_points_text(text):
    """
    Текст (несколько строк) -> список (x,y)
    Игнорирует строки, которые не парсятся.
    """
    pts = []
    for ln in text.strip().splitlines():
        p = parse_point_line(ln)
        if p is not None:
            pts.append(p)
    return pts


def mid_point(p1, p2):
    return ((p1[0] + p2[0]) / 2.0, (p1[1] + p2[1]) / 2.0)


def distance(p1, p2):
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])


def polar_to_cart(center, r, theta):
    return (center[0] + r * math.cos(theta), center[1] + r * math.sin(theta))


def safe_float(v, default=0.0):
    try:
        return float(str(v).strip())
    except Exception:
        return default


# ---Функция генерации G-кода для намотки вокруг пальца (4-я ось включена)---
def generate_winding_gcode(
        right_pts, left_pts,
        z_top, z_bottom,
        turns=5,
        feed=1200,
        start_angle_deg=0.0,
        clockwise=False,
        segments_per_turn=120,
        center=None,
        include_e_axis=True
):
    """
    Генерация G-кода для цикличных проходов по кругу вокруг центра между правой и левой точками.
    - right_pts, left_pts: списки (x,y) или хотя бы по 1 точке в каждом
    - z_top, z_bottom: абсолютные Z (mm)
    - turns: число витков (количество оборотов вокруг пальца)
    - feed: подача в mm/min
    - start_angle_deg: начальный угол в градусах
    - clockwise: направление намотки
    - segments_per_turn: число сегментов на оборот (чем больше — тем плавнее)
    - center: (x,y) центр окружности; если None — вычисляется как midpoint(avg(right), avg(left))
    - include_e_axis: если True — добавляем ось E (в градусах) для вращения статора.
    Возвращает: список строк G-code.
    """
    # ---Валидация/Центр---
    if center is None:
        if right_pts and left_pts:
            avg_r = (sum(p[0] for p in right_pts) / len(right_pts), sum(p[1] for p in right_pts) / len(right_pts))
            avg_l = (sum(p[0] for p in left_pts) / len(left_pts), sum(p[1] for p in left_pts) / len(left_pts))
            center = mid_point(avg_r, avg_l)
        else:
            center = SESSION_STORE.get("center_xy", (0.0, 0.0))

    # Радиус как расстояние от центра до средней точки (между правой и левой)
    if right_pts and left_pts:
        avg_right = (sum(p[0] for p in right_pts) / len(right_pts), sum(p[1] for p in right_pts) / len(right_pts))
        avg_left = (sum(p[0] for p in left_pts) / len(left_pts), sum(p[1] for p in left_pts) / len(left_pts))
        avg_mid = mid_point(avg_right, avg_left)
        r = distance(center, avg_mid)
        if r <= 0:
            # попытаемся взять середину расстояния между правой и левой
            r = distance(avg_right, avg_left) / 2.0
            if r == 0:
                r = 10.0  # Минимальный радиус, если точки совпадают
    else:
        # Fallback радиус
        r = 10.0  # мм

    # --- ОГРАНИЧЕНИЕ: Минимальное количество сегментов ---
    # Исправляем проблему, когда segments_per_turn=1 приводит к некорректному коду
    segments_per_turn = max(12, int(segments_per_turn))  # Минимум 12 сегментов на оборот

    # ---Сегментация и Z---
    total_segments = max(1, int(segments_per_turn * max(1, int(turns))))
    angle_direction = -1.0 if clockwise else 1.0
    total_angle_rad = angle_direction * 2.0 * math.pi * turns
    start_angle = math.radians(start_angle_deg)

    # Создаём массивы theta и Z
    thetas = [start_angle + (i / total_segments) * total_angle_rad for i in range(total_segments + 1)]
    zs = [z_top + (z_bottom - z_top) * (i / total_segments) for i in range(total_segments + 1)]

    # E ось (мы предполагаем: E в градусах; на 1 сегмент — изменение угла в градусах)
    e_positions = []
    if include_e_axis:
        total_angle_deg = math.degrees(abs(total_angle_rad))
        # E распределяется линейно
        for i in range(total_segments + 1):
            e_positions.append((i / total_segments) * total_angle_deg * (-1.0 if clockwise else 1.0))
    else:
        e_positions = [0.0] * (total_segments + 1)

    # ---Формирование G-code---
    gcode = []
    gcode.append(f"(Generated: {datetime.now().isoformat()})")
    gcode.append("G21 ; mm")
    gcode.append("G90 ; absolute positioning")
    gcode.append("G94 ; feed per minute")

    # Безопасный подъем Z
    safe_z = max(z_top, z_bottom) + 5.0
    gcode.append(f"G0 Z{safe_z:.4f}")

    # Перемещение в стартовую XY точку (первый элемент массива thetas/zs)
    start_xy = polar_to_cart(center, r, thetas[0])
    gcode.append(f"G0 X{start_xy[0]:.4f} Y{start_xy[1]:.4f}")

    gcode.append(f"; center X{center[0]:.4f} Y{center[1]:.4f}  radius {r:.4f} turns={turns}")

    # Плавное опускание на рабочую Z (первая точка)
    gcode.append(f"G1 Z{zs[0]:.4f} F{feed:.0f}")

    # Рабочие перемещения
    for i in range(1, total_segments + 1):
        x, y = polar_to_cart(center, r, thetas[i])
        z = zs[i]
        e = e_positions[i]
        if include_e_axis:
            gcode.append(f"G1 X{x:.4f} Y{y:.4f} Z{z:.4f} E{e:.3f} F{feed:.0f}")
        else:
            gcode.append(f"G1 X{x:.4f} Y{y:.4f} Z{z:.4f} F{feed:.0f}")

    gcode.append(f"G0 Z{safe_z:.4f}")
    gcode.append("M2 ; end")
    return gcode


# ---Функция относительной генерации зубца оставлена для обратной совместимости---
def generate_single_tooth_gcode_relative(dx_list, dy_list, dz_list, feedrate=3000):
    gcode = []
    gcode.append("; --- Начало намотки одного зубца ---")
    gcode.append("G90")
    gcode.append(f"G1 F{feedrate}")
    gcode.append("G91")
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


# ------------------------
# GUI
# ------------------------
class App:
    def __init__(self, root, controller_class, **kwargs):
        self.controller = controller_class(**kwargs)

        self.root = root
        self.root.title("Управление принтером в CoppeliaSim")
        self.root.geometry("900x650")

        # Создание виджетов GUI
        self.create_widgets()

        # Локальные параметры
        self.right_pts = []
        self.left_pts = []

    # ---Работа с контроллером/позициями---
    def _get_current_position(self):
        try:
            # Сюда будет приходить словарь с позицией {'x':..., 'y':..., 'z':..., 'e':...}
            pos_dict = self.controller.get_position()
        except Exception as e:
            # Выводим полный текст ошибки в консоль
            print(f"Error in get_position (M114 issue): {e}", file=sys.stderr)
            pos_dict = None

        if pos_dict is None:
            return None

        # Преобразуем словарь в кортеж (x, y, z, e) для совместимости с UI
        return (pos_dict.get('x', 0.0), pos_dict.get('y', 0.0), pos_dict.get('z', 0.0), pos_dict.get('e', 0.0))

    # ---Методы кнопок---
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
        # Здесь 'pos' будет кортежем (X, Y, Z, E)
        pos = self._get_current_position()
        print("get_pos ->", pos)
        print("Internal position:", getattr(self.controller, "position", None))
        if pos:
            # pos[0] = X, pos[1] = Y, pos[2] = Z
            messagebox.showinfo("Current position", f"X={pos[0]:.4f}, Y={pos[1]:.4f}, Z={pos[2]:.4f}")
        else:
            messagebox.showwarning("Current position", "Не удалось получить позицию от контроллера")

    def on_test_bt(self):
        self.controller.move_realtive(e=360)

    # Функции ручного управления (jog)
    def on_Xplus_bt(self):
        self.controller.move_realtive(x=safe_float(self.step_entry.get(), 1.0))

    def on_Xminus_bt(self):
        self.controller.move_realtive(x=-safe_float(self.step_entry.get(), 1.0))

    def on_Yplus_bt(self):
        self.controller.move_realtive(y=safe_float(self.step_entry.get(), 1.0))

    def on_Yminus_bt(self):
        self.controller.move_realtive(y=-safe_float(self.step_entry.get(), 1.0))

    def on_Zplus_bt(self):
        self.controller.move_realtive(z=safe_float(self.step_entry.get(), 1.0))

    def on_Zminus_bt(self):
        self.controller.move_realtive(z=-safe_float(self.step_entry.get(), 1.0))

    def on_Eplus_bt(self):
        self.controller.move_realtive(e=safe_float(self.step_entry.get(), 1.0))

    def on_Eminus_bt(self):
        self.controller.move_realtive(e=-safe_float(self.step_entry.get(), 1.0))

    # ---Новые кнопки связанные с паза/высотой---
    def on_mark_top_bt(self):
        pos = self._get_current_position()
        if pos is None:
            messagebox.showwarning("Ошибка", "Не удалось получить позицию от контроллера")
            return
        z = pos[2]  # Z-координата (третий элемент кортежа)
        SESSION_STORE['z_top'] = z
        self.z_top_entry.delete(0, 'end')
        self.z_top_entry.insert(0, f"{z:.4f}")
        messagebox.showinfo("Запомнено", f"Верх паза (Z_top) = {z:.4f} mm")

    def on_mark_bottom_bt(self):
        pos = self._get_current_position()
        if pos is None:
            messagebox.showwarning("Ошибка", "Не удалось получить позицию от контроллера")
            return
        z = pos[2]  # Z-координата (третий элемент кортежа)
        SESSION_STORE['z_bottom'] = z
        self.z_bottom_entry.delete(0, 'end')
        self.z_bottom_entry.insert(0, f"{z:.4f}")
        messagebox.showinfo("Запомнено", f"Низ паза (Z_bottom) = {z:.4f} mm")

    def on_save_height_bt(self):
        zt = SESSION_STORE.get('z_top')
        zb = SESSION_STORE.get('z_bottom')
        if zt is None or zb is None:
            messagebox.showwarning("Ошибка", "Сначала отметьте верх и низ паза (кнопками).")
            return
        SESSION_STORE['slot_height'] = abs(zt - zb)
        messagebox.showinfo("Запомнено", f"Высота паза = {SESSION_STORE['slot_height']:.4f} mm")

    # ---Парсинг точек из полей---
    def load_points_from_widgets(self):
        right_txt = self.right_text.get("1.0", "end-1c")
        left_txt = self.left_text.get("1.0", "end-1c")
        self.right_pts = parse_points_text(right_txt)
        self.left_pts = parse_points_text(left_txt)
        return self.right_pts, self.left_pts

    # ---Общая функция генерации G-code (для обоих методов)---
    def _generate_gcode(self):
        # Считываем параметры
        self.load_points_from_widgets()

        # Проверка и определение центра/точек
        if not self.right_pts or not self.left_pts:
            center = SESSION_STORE.get("center_xy")
            if center is None:
                messagebox.showerror("Ошибка", "Нет значения центра в SESSION_STORE.")
                return None
            right_pts = []
            left_pts = []
        else:
            center = SESSION_STORE.get("center_xy")  # Используем дефолтный центр

        # Считываем параметры намотки
        # Примечание: Устанавливаем разумные значения по умолчанию для F и Segments/turn
        z_top = safe_float(self.z_top_entry.get(), SESSION_STORE.get('z_top', 0.0))
        z_bottom = safe_float(self.z_bottom_entry.get(), SESSION_STORE.get('z_bottom', 0.0))
        turns = int(safe_float(self.turns_entry.get(), 5))
        feed = max(100.0, safe_float(self.feed_entry.get(), 1200))  # ОГРАНИЧЕНИЕ F МИНИМУМОМ 100
        start_angle = safe_float(self.start_angle_entry.get(), 0.0)
        clockwise = bool(self.clockwise_var.get())
        segments_per_turn = max(12, int(safe_float(self.segm_entry.get(), 120)))  # ОГРАНИЧЕНИЕ СЕГМЕНТОВ МИНИМУМОМ 12
        include_e = bool(self.include_e_var.get())

        # Генерируем код
        gcode_lines = generate_winding_gcode(
            self.right_pts, self.left_pts,
            z_top=z_top, z_bottom=z_bottom,
            turns=turns, feed=feed,
            start_angle_deg=start_angle,
            clockwise=clockwise,
            segments_per_turn=segments_per_turn,
            center=center,
            include_e_axis=include_e
        )
        return gcode_lines

    # ---Генерация G-code для предпросмотра (GUI)---
    def on_generate_winding_bt(self):
        try:
            gcode_lines = self._generate_gcode()
            if gcode_lines:
                PreviewWindow(self.root, gcode_lines, self.controller)
        except Exception as e:
            messagebox.showerror("Ошибка генерации", str(e))

    # ---НОВАЯ ФУНКЦИЯ: Генерация и отправка на симуляцию---
    def on_check_simulation_bt(self):
        try:
            gcode_lines = self._generate_gcode()
            if gcode_lines is None:
                # Сообщение об ошибке уже было показано в _generate_gcode
                return

            # Немедленная отправка на контроллер
            self.controller.run_gcode(gcode_lines)
            messagebox.showinfo("Симуляция запущена", "G-code успешно отправлен в CoppeliaSim для проверки!")

        except Exception as e:
            messagebox.showerror("Ошибка симуляции/отправки", str(e))
            return

    # ---Неперенаписанная кнопка для "Намотать зубец"---
    def on_generate_tooth_bt(self):
        dx_list = [0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5, 5, -5, -5, -5, -5, -5, 0, 0, 0]
        dy_list = [-5, -5, -5, -5, -5, -5, 0, 0, 0, 0, 0, 5, 5, 5, 5, 5, 5, 0, -5, -5]
        dz_list = [0, 0, 0, 0, 0, 0, -5, -5, -5, -5, -5, 0, 0, 0, 0, 0, 0, 5, 5, 5]
        gcode_lines = generate_single_tooth_gcode_relative(dx_list, dy_list, dz_list, feedrate=3000)
        print("Сгенерированный G-code для зубца:")
        for line in gcode_lines:
            print(line)
        self.controller.run_gcode(gcode_lines)

    # --- GUI: создание виджетов---
    def create_widgets(self):
        # панели
        left_frame = tk.Frame(self.root, borderwidth=2, relief="groove")
        left_frame.grid(row=0, column=0, rowspan=3, padx=4, pady=4, sticky="ns")

        right_frame = tk.Frame(self.root, borderwidth=2, relief="groove")
        right_frame.grid(row=0, column=1, padx=4, pady=4, sticky="nsew")

        params_frame = tk.Frame(self.root, borderwidth=2, relief="groove")
        params_frame.grid(row=1, column=1, padx=4, pady=4, sticky="ew")

        # ------------ left_frame: кнопки управления ----------------
        buttons = [
            ("CONNECT", self.on_connect_bt),
            ("DISCONNECT", self.on_disconnect_bt),
            ("HOME", self.on_home_bt),
            ("set zero", self.on_setZero_bt),
            ("absalute\ncords", self.on_absalute_bt),
            ("relative\ncords", self.on_relative_bt),
            ("get pos", self.on_get_pos_bt),
            ("test", self.on_test_bt),
            ("Намотать зубец", self.on_generate_tooth_bt)
        ]
        for text, cmd in buttons:
            bt = tk.Button(left_frame, text=text, command=cmd, width=18)
            bt.pack(pady=2)

        # ------------ right_frame: поля точек и управление -------------
        # Right points
        ttk.Label(right_frame, text="Right points (x,y) — по строкам:").grid(row=0, column=0, sticky="w")
        self.right_text = tk.Text(right_frame, width=30, height=8)
        self.right_text.grid(row=1, column=0, padx=4, pady=4)

        ttk.Label(right_frame, text="Left points (x,y) — по строкам:").grid(row=0, column=1, sticky="w")
        self.left_text = tk.Text(right_frame, width=30, height=8)
        self.left_text.grid(row=1, column=1, padx=4, pady=4)

        ttk.Button(right_frame, text="Считать точки", command=self.load_points_from_widgets).grid(row=2, column=0,
                                                                                                  pady=4)
        ttk.Button(right_frame, text="Очистить поля",
                   command=lambda: (self.right_text.delete("1.0", "end"), self.left_text.delete("1.0", "end"))).grid(
            row=2, column=1, pady=4)

        # ------------ params_frame: параметры намотки -----------------
        ttk.Label(params_frame, text="Z top:").grid(row=0, column=0, sticky="w")
        self.z_top_entry = ttk.Entry(params_frame, width=12);
        self.z_top_entry.grid(row=0, column=1, padx=4)
        ttk.Label(params_frame, text="Z bottom:").grid(row=0, column=2, sticky="w")
        self.z_bottom_entry = ttk.Entry(params_frame, width=12);
        self.z_bottom_entry.grid(row=0, column=3, padx=4)

        ttk.Button(params_frame, text="Это верх паза", command=self.on_mark_top_bt).grid(row=0, column=4, padx=6)
        ttk.Button(params_frame, text="Это низ паза", command=self.on_mark_bottom_bt).grid(row=0, column=5, padx=6)
        ttk.Button(params_frame, text="Запомни высоту", command=self.on_save_height_bt).grid(row=0, column=6, padx=6)

        ttk.Label(params_frame, text="Turns:").grid(row=1, column=0, sticky="w")
        self.turns_entry = ttk.Entry(params_frame, width=8);
        self.turns_entry.insert(0, "1");
        self.turns_entry.grid(row=1, column=1, padx=4)  # Установили 1 по умолчанию

        ttk.Label(params_frame, text="Feed mm/min:").grid(row=1, column=2, sticky="w")
        self.feed_entry = ttk.Entry(params_frame, width=10);
        self.feed_entry.insert(0, "1200");
        self.feed_entry.grid(row=1, column=3, padx=4)  # Установили 1200 по умолчанию

        ttk.Label(params_frame, text="Start angle (deg):").grid(row=1, column=4, sticky="w")
        self.start_angle_entry = ttk.Entry(params_frame, width=8);
        self.start_angle_entry.insert(0, "0");
        self.start_angle_entry.grid(row=1, column=5, padx=4)

        self.clockwise_var = tk.IntVar(value=0)
        ttk.Checkbutton(params_frame, text="Clockwise", variable=self.clockwise_var).grid(row=1, column=6, padx=4)

        ttk.Label(params_frame, text="Segments/turn:").grid(row=2, column=0, sticky="w")
        self.segm_entry = ttk.Entry(params_frame, width=8);
        self.segm_entry.insert(0, "120");
        self.segm_entry.grid(row=2, column=1, padx=4)  # Установили 120 по умолчанию
        self.include_e_var = tk.IntVar(value=1)
        ttk.Checkbutton(params_frame, text="Use E-axis (rotate stator)", variable=self.include_e_var).grid(row=2,
                                                                                                           column=2,
                                                                                                           padx=4)

        ttk.Button(params_frame, text="Сгенерировать код", command=self.on_generate_winding_bt).grid(row=2, column=4,
                                                                                                     padx=6)
        # НОВАЯ КНОПКА
        ttk.Button(params_frame, text="Проверить на симуляторе", command=self.on_check_simulation_bt).grid(row=2,
                                                                                                           column=5,
                                                                                                           padx=6)

        ttk.Button(params_frame, text="Сохранить SESSION_STORE", command=self.save_session_to_file).grid(row=3,
                                                                                                         column=4,
                                                                                                         columnspan=2,
                                                                                                         padx=6, pady=4)

        # ------------ Панель ручного управления (стрелки) -------------
        jog_frame = tk.LabelFrame(self.root, text="Ручное управление", padx=6, pady=6)
        jog_frame.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=6, pady=6)

        ttk.Label(jog_frame, text="Шаг (мм/°):").grid(row=0, column=0, sticky="w")
        self.step_entry = ttk.Entry(jog_frame, width=8)
        self.step_entry.insert(0, "1.0")
        self.step_entry.grid(row=0, column=1, sticky="w")

        # Кнопки ручного управления
        ttk.Button(jog_frame, text="X-", width=6, command=self.on_Xminus_bt).grid(row=1, column=0)
        ttk.Button(jog_frame, text="X+", width=6, command=self.on_Xplus_bt).grid(row=1, column=2)
        ttk.Button(jog_frame, text="Y+", width=6, command=self.on_Yplus_bt).grid(row=0, column=3)
        ttk.Button(jog_frame, text="Y-", width=6, command=self.on_Yminus_bt).grid(row=2, column=3)
        ttk.Button(jog_frame, text="Z+", width=6, command=self.on_Zplus_bt).grid(row=0, column=4)
        ttk.Button(jog_frame, text="Z-", width=6, command=self.on_Zminus_bt).grid(row=1, column=4)
        ttk.Button(jog_frame, text="E+", width=6, command=self.on_Eplus_bt).grid(row=0, column=5)
        ttk.Button(jog_frame, text="E-", width=6, command=self.on_Eminus_bt).grid(row=1, column=5)

    def save_session_to_file(self):
        path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json")])
        if not path:
            return
        with open(path, "w", encoding="utf-8") as f:
            json.dump(SESSION_STORE, f, indent=2)
        messagebox.showinfo("Сохранено", f"SESSION_STORE сохранён в {path}")


# --- Окно предпросмотра G-code и отправки на контроллер---
class PreviewWindow(tk.Toplevel):
    def __init__(self, parent, gcode_lines, controller):
        super().__init__(parent)
        self.title("G-code preview")
        self.geometry("800x600")
        self.controller = controller
        self.gcode_lines = gcode_lines

        self.text = tk.Text(self, wrap="none")
        self.text.pack(fill="both", expand=True)

        for ln in gcode_lines:
            self.text.insert("end", ln + "\n")

        btn_frame = tk.Frame(self)
        btn_frame.pack(fill="x")
        tk.Button(btn_frame, text="Сохранить в файл", command=self.save_to_file).pack(side="left", padx=4, pady=4)
        tk.Button(btn_frame, text="Отправить на контроллер", command=self.send_to_controller).pack(side="left", padx=4,
                                                                                                   pady=4)
        tk.Button(btn_frame, text="Закрыть", command=self.destroy).pack(side="right", padx=4, pady=4)

    def save_to_file(self):
        p = filedialog.asksaveasfilename(defaultextension=".gcode",
                                         filetypes=[("G-code", "*.gcode;*.nc;*.txt"), ("All", "*.*")])
        if not p:
            return
        with open(p, "w", encoding="utf-8") as f:
            f.write("\n".join(self.gcode_lines))
        messagebox.showinfo("Сохранено", f"G-code сохранён в {p}")

    def send_to_controller(self):
        try:
            # Передаём список строк — предполагается, что controller.run_gcode умеет это обработать
            self.controller.run_gcode(self.gcode_lines)
            messagebox.showinfo("OK", "G-code отправлен на контроллер")
        except Exception as e:
            messagebox.showerror("Ошибка отправки", str(e))


# ------------------------
# Запуск приложения
# ------------------------
if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = App(root, controller_class=CoppeliaController, debug_mode=True)
        root.mainloop()

    except Exception as e:
        print(f"Ошибка: {e}")
        try:
            root.destroy()
        except Exception:
            pass

    finally:
        if 'app' in locals() and getattr(app.controller, "connection", None) is not None:
            try:
                app.controller.disconnect()
            except Exception:
                pass

# synced: 2025-10-10T17:50:44.563881
# synced: 2025-10-10T17:50:48.356919
# synced: 2025-10-10T17:50:50.584704
# synced: 2025-10-10T17:50:52.749830
# synced: 2025-10-10T17:50:54.978933
# synced: 2025-10-10T17:50:57.743673
# synced: 2025-10-10T17:50:59.849994
# synced: 2025-10-10T17:51:02.008742
# synced: 2025-10-10T17:51:04.193839
# synced: 2025-10-10T17:51:06.344954
# synced: 2025-10-10T17:51:08.470987
# synced: 2025-10-10T17:51:10.698174
# synced: 2025-10-10T17:51:12.859926
# synced: 2025-10-10T17:51:14.989652
# synced: 2025-10-10T17:51:17.131245
# synced: 2025-10-10T17:51:19.625577
# synced: 2025-10-10T17:51:21.783470
# synced: 2025-10-10T17:51:24.148119
# synced: 2025-10-10T17:51:26.494424
# synced: 2025-10-10T17:51:29.101220
# synced: 2025-10-10T17:51:31.292381
# synced: 2025-10-10T17:51:33.412753
# synced: 2025-10-10T17:51:35.547576
# synced: 2025-10-10T17:51:38.102297
# synced: 2025-10-10T17:51:40.696883
# synced: 2025-10-10T17:51:43.250665
# synced: 2025-10-10T17:51:45.406144
# synced: 2025-10-10T17:51:47.535615
# synced: 2025-10-10T17:51:49.702654
# synced: 2025-10-10T17:51:51.844998
# synced: 2025-10-10T17:51:54.049974
# synced: 2025-10-10T17:51:56.178272
# synced: 2025-10-10T17:51:58.379905
# synced: 2025-10-10T17:52:00.636204
# synced: 2025-10-10T17:52:02.844486
# synced: 2025-10-10T17:52:05.079309
# synced: 2025-10-10T17:52:07.236269
# synced: 2025-10-10T17:52:09.400068
# synced: 2025-10-10T17:52:11.651336
# synced: 2025-10-10T17:52:13.862852
# synced: 2025-10-10T17:52:16.072679
# synced: 2025-10-10T17:52:18.355305
# synced: 2025-10-10T17:52:20.725830
# synced: 2025-10-10T17:52:22.819988