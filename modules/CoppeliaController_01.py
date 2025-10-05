from PrinterController_01 import PrinterController
from ClientCoppeliaSim_01 import Client_CoppeliaSim
import re
import numpy as np
import time

class CoppeliaController(PrinterController):
    def connect(self):
        """Подключение к CoppeliaSim"""
        try:
            self.connection = Client_CoppeliaSim()
            self.connection.__enter__()
            print("Подключено")
        except Exception as e:
            print(f"Ошибка подключения: {e}")

    def disconnect(self):
        """Отключение от CoppeliaSim"""
        if self.connection:
            try:
                self.connection.__exit__()
                print("Соединение закрыто")
            except Exception as e:
                print(f"Ошибка при отключении: {e}")

    def send_command(self, command, read_response=True):
        """
        Отправка команды (G-кода) в CoppeliaSim.
        """
        if not self.connection:
            print("Ошибка: соединение не установлено")
            return None

        try:
            self.connection.send_string("gcode_str", (command + "\n").encode('utf-8'))
            if self.debug_mode:
                print(f"Отправлено: {command}")
        except Exception as e:
            print(f"Ошибка при отправке команды: {e}")
            return None

    def home(self):
        """Возврат всех осей в исходное положение"""
        self.send_command("G90\nG1 X0 Y0 Z0 E0\nG91")
        self.position = np.zeros(4)

    # --- Новый функционал ниже ---
    def run_gcode(self, gcode_lines, speed=800):
        """
        Выполняет список строк G-кода (G0/G1) в CoppeliaSim.
        """
        print("Начало выполнения G-кода...")
        for line in gcode_lines:
            line = line.strip()
            if not line or line.startswith(";"):
                continue

            if line.startswith(("G0", "G1")):
                x = self._get_value(line, "X")
                y = self._get_value(line, "Y")
                z = self._get_value(line, "Z")
                f = self._get_value(line, "F", default=speed)
                self.move(x=x, y=y, z=z, speed=f)
                time.sleep(0.1)

        print("Выполнение G-кода завершено.")

    def _get_value(self, line, key, default=None):
        """Извлекает значение координаты из строки G-кода"""
        match = re.search(rf"{key}(-?\d+\.?\d*)", line)
        if match:
            return float(match.group(1))
        return default

# synced: 2025-10-05T17:23:16.956438
# synced: 2025-10-05T17:23:19.880865
# synced: 2025-10-05T17:23:22.761201
# synced: 2025-10-05T17:23:25.481903
# synced: 2025-10-05T17:23:28.223296
# synced: 2025-10-05T17:23:31.176072
# synced: 2025-10-05T17:23:34.037593
# synced: 2025-10-05T17:23:36.770992
# synced: 2025-10-05T17:23:39.601201