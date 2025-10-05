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
# synced: 2025-10-05T17:23:42.255805
# synced: 2025-10-05T17:23:44.994385
# synced: 2025-10-05T17:23:47.899993
# synced: 2025-10-05T17:23:50.638819
# synced: 2025-10-05T17:23:53.449735
# synced: 2025-10-05T17:23:56.279894
# synced: 2025-10-05T17:23:59.063486
# synced: 2025-10-05T17:24:01.846923
# synced: 2025-10-05T17:24:04.668584
# synced: 2025-10-05T17:24:08.117828
# synced: 2025-10-05T17:24:10.746835
# synced: 2025-10-05T17:24:13.610409
# synced: 2025-10-05T17:24:16.396869
# synced: 2025-10-05T17:24:19.267392
# synced: 2025-10-05T17:24:29.635714
# synced: 2025-10-05T17:24:32.125472
# synced: 2025-10-05T17:24:34.347209
# synced: 2025-10-05T17:24:36.504371
# synced: 2025-10-05T17:24:38.655044
# synced: 2025-10-05T17:24:40.750826
# synced: 2025-10-05T17:24:42.895708
# synced: 2025-10-05T17:24:45.035822
# synced: 2025-10-05T17:24:47.302354
# synced: 2025-10-05T17:24:49.462085
# synced: 2025-10-05T17:24:51.568583
# synced: 2025-10-05T17:24:53.662542
# synced: 2025-10-05T17:24:55.883590
# synced: 2025-10-05T17:24:58.014620
# synced: 2025-10-05T17:25:00.240395
# synced: 2025-10-05T17:25:02.471364
# synced: 2025-10-05T17:25:04.574721
# synced: 2025-10-05T17:25:06.790022
# synced: 2025-10-05T17:25:09.042927
# synced: 2025-10-05T17:25:11.192635
# synced: 2025-10-05T17:25:13.475339
# synced: 2025-10-05T17:25:15.669506
# synced: 2025-10-05T17:25:17.908616
# synced: 2025-10-05T17:25:20.138464
# synced: 2025-10-05T17:25:22.350792
# synced: 2025-10-05T17:25:24.527480
# synced: 2025-10-05T17:25:26.757074
# synced: 2025-10-05T17:25:28.934726
# synced: 2025-10-05T17:25:31.184462
# synced: 2025-10-05T17:25:33.420769
# synced: 2025-10-05T17:25:35.603384
# synced: 2025-10-05T17:25:37.849430
# synced: 2025-10-05T17:25:40.096832
# synced: 2025-10-05T17:25:42.352313
# synced: 2025-10-05T17:25:44.553233
# synced: 2025-10-05T17:25:46.737238
# synced: 2025-10-05T17:25:48.929299
# synced: 2025-10-05T17:25:51.147381
# synced: 2025-10-05T17:25:53.354873
# synced: 2025-10-05T17:25:55.533745
# synced: 2025-10-05T17:25:57.735666
# synced: 2025-10-05T17:25:59.971993
# synced: 2025-10-05T17:26:02.151750