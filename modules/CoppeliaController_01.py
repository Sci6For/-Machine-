from modules.PrinterController_01 import PrinterController
from ClientCoppeliaSim_01 import Client_CoppeliaSim
import re
import numpy as np
import time
import sys

# Импортируем модуль sim для доступа к API-функциям
try:
    import sim
except ImportError:
    print('--------------------------------------------------------------', file=sys.stderr)
    print('"sim.py" не найден. Проверьте, что он находится в PYTHONPATH.', file=sys.stderr)
    print('--------------------------------------------------------------', file=sys.stderr)


class CoppeliaController(PrinterController):

    def __init__(self, debug_mode=False, **kwargs):
        super().__init__(**kwargs)
        self.debug_mode = debug_mode
        self.connection = None  # Объект Client_CoppeliaSim
        # Используем словарь для удобства в UI
        self.position = {'x': 0.0, 'y': 0.0, 'z': 0.0, 'e': 0.0}
        # Флаг для управления потоковым чтением M114
        self.is_streaming_initialized = False

    def connect(self):
        """Подключение к CoppeliaSim"""
        try:
            self.connection = Client_CoppeliaSim()
            # __enter__ возвращает сам объект-обертку.
            self.connection.__enter__()

            if not hasattr(self.connection, 'id') or self.connection.id == -1:
                raise ConnectionError("Не удалось получить ClientID от CoppeliaSim.")

            print("Подключено")
        except Exception as e:
            print(f"Ошибка подключения: {e}")
            self.connection = None

    def disconnect(self):
        """Отключение от CoppeliaSim"""
        if self.connection:
            try:
                self.connection.__exit__()
                self.connection = None
                print("Соединение закрыто")
            except Exception as e:
                print(f"Ошибка при отключении: {e}")

    def send_command(self, command, read_response=True):
        """
        Отправка команды (G-кода) в CoppeliaSim.
        Использует медленный канал gcode_str.
        """

        if command.strip().upper() == "M114":
            print("Warning: M114 command blocked from slow channel (send_command). Use get_position().",
                  file=sys.stderr)
            return

        if not self.connection:
            print("Ошибка: соединение не установлено")
            return None

        try:
            # Отправка через медленный канал (gcode_str)
            self.connection.send_string("gcode_str", (command + "\n").encode('utf-8'))
            if self.debug_mode:
                print(f"Отправка G-кода (медленный канал gcode_str): {command}")  # Логирование отправки
        except Exception as e:
            print(f"Ошибка при отправке команды: {e}")
            return None

    def home(self):
        """Возврат всех осей в исходное положение"""
        # Отправляем в абсолютных координатах
        self.send_command("G90\nG1 X0 Y0 Z0 E0 F2000\nG91")
        self.position = {'x': 0.0, 'y': 0.0, 'z': 0.0, 'e': 0.0}

    def _set_abs_cords(self):
        """Установить абсолютные координаты (G90)"""
        self.send_command("G90")

    def _set_rel_cords(self):
        """Установить относительные координаты (G91)"""
        self.send_command("G91")

    def run_gcode(self, gcode_lines, speed=800):
        print("Начало выполнения G-кода...")
        for line in gcode_lines:
            line = line.strip()
            if not line or line.startswith(";"): continue
            if line.startswith(("G0", "G1")):

                x = self._get_value(line, "X");
                y = self._get_value(line, "Y")
                z = self._get_value(line, "Z");
                e = self._get_value(line, "E")
                f = self._get_value(line, "F", default=speed)

                command = "G1"
                if x is not None: command += f" X{x}"
                if y is not None: command += f" Y{y}"
                if z is not None: command += f" Z{z}"
                if e is not None: command += f" E{e}"
                if f is not None: command += f" F{f}"

                if len(command) > 4:
                    self.send_command(command, read_response=False)

                time.sleep(0.1)

            elif line.startswith("M2"):
                print("Получена команда M2. Завершение работы G-кода.");
                break
            else:
                self.send_command(line, read_response=False)

        print("Выполнение G-кода завершено.")

    def _get_value(self, line, key, default=None):
        match = re.search(rf"{key}(-?\d+\.?\d*)", line)
        if match: return float(match.group(1))
        return default

    def move_realtive(self, x=0, y=0, z=0, e=0, speed=None):
        """
        Относительное перемещение.
        """
        self.position = self._position_to_rel(x, y, z, e)
        gcode = self._create_G_code_cord_str("G1", x, y, z, e, speed)

        if len(gcode) > 4:
            self.send_command(gcode)

    def move(self, x=None, y=None, z=None, e=None, speed=None):
        """
        Абсолютное перемещение.
        """
        self.position = self._position_to_abs(x, y, z, e)
        gcode = self._create_G_code_cord_str("G1", x, y, z, e, speed)

        if len(gcode) > 4:
            self.send_command(gcode)

    def _position_to_abs(self, x, y, z, e):
        """Определение положения по абсолютной команде для словаря (переопределение родителя)"""
        pos = self.position.copy()

        if x is not None: pos['x'] = x * self.invert[0]
        if y is not None: pos['y'] = y * self.invert[1]
        if z is not None: pos['z'] = z * self.invert[2]
        if e is not None: pos['e'] = e * self.invert[3] * self.k_e
        return pos

    def _position_to_rel(self, x, y, z, e):
        """Определение положения по относительной команде для словаря (переопределение родителя)"""
        pos = self.position.copy()

        if x is not None: pos['x'] += x * self.invert[0]
        if y is not None: pos['y'] += y * self.invert[1]
        if z is not None: pos['z'] += z * self.invert[2]
        if e is not None: pos['e'] += e * self.invert[3] * self.k_e

        return pos

    def get_position(self):
        """
        Запрашивает текущую позицию через M114, используя потоковое чтение
        для надежного получения последнего значения из буфера.
        """
        GCODE_CMD_SIGNAL = 'GCODE_CMD'
        GCODE_REPLY_SIGNAL = 'GCODE_REPLY'

        try:
            if self.connection is None or not hasattr(self.connection, 'id'):
                print("Ошибка: Соединение с CoppeliaSim не установлено.", file=sys.stderr)
                return None

            client_id = self.connection.id

            # 1. Инициализация потокового режима (только при первом вызове)
            if not self.is_streaming_initialized:
                # Включаем потоковый режим. Все последующие ответы будут храниться в буфере клиента.
                # simx_opmode_streaming: начинается новое потоковое чтение
                res, _ = sim.simxGetStringSignal(client_id, GCODE_REPLY_SIGNAL, sim.simx_opmode_streaming)
                if res == sim.simx_return_ok or res == sim.simx_return_novalue_flag:
                    self.is_streaming_initialized = True
                    # ВЫВОДИМ СООБЩЕНИЕ ДЛЯ ГАРАНТИИ, ДАЖЕ ЕСЛИ debug_mode=False
                    print("M114 Stream Initialized: Потоковое чтение M114 инициировано.")
                else:
                    print(f"M114 Stream Error: Ошибка инициализации потока M114: код {res}", file=sys.stderr)
                    return None

            # 2. Очистка канала отправки перед запросом
            sim.simxSetStringSignal(client_id, GCODE_CMD_SIGNAL, b'', sim.simx_opmode_oneshot)

            # 3. Отправка M114 через БЫСТРЫЙ КАНАЛ
            sim.simxSetStringSignal(client_id, GCODE_CMD_SIGNAL, 'M114\n'.encode('utf-8'), sim.simx_opmode_oneshot)
            if self.debug_mode:
                print("Отправка G-кода (быстрый канал GCODE_CMD): M114")

            # Увеличенная пауза для гарантированного обновления сигнала в CoppeliaSim
            time.sleep(0.1)

            # 4. Чтение из буфера
            # simx_opmode_buffer: читаем последнее известное значение из буфера.
            res, reply = sim.simxGetStringSignal(client_id, GCODE_REPLY_SIGNAL, sim.simx_opmode_buffer)

            # --- КРИТИЧЕСКОЕ ЛОГИРОВАНИЕ ---
            if self.debug_mode:
                print(f"M114 Read Attempt 1: Result Code={res}, Reply Length={len(reply) if reply else 0}")

            if res != sim.simx_return_ok or not reply or reply == b'':
                # Если с первого раза из буфера прочитать не удалось, даем еще одну попытку
                time.sleep(0.05)
                res, reply = sim.simxGetStringSignal(client_id, GCODE_REPLY_SIGNAL, sim.simx_opmode_buffer)

                if self.debug_mode:
                    print(f"M114 Read Attempt 2: Result Code={res}, Reply Length={len(reply) if reply else 0}")

                if res != sim.simx_return_ok or not reply or reply == b'':
                    # ВЫВОДИМ ОШИБКУ ДЛЯ ГАРАНТИИ, ДАЖЕ ЕСЛИ debug_mode=False
                    print(f"M114 Read Fail: Ошибка чтения M114 из буфера после 2 попыток. Последний код: {res}")
                    return None

            # 5. Обработка успешного ответа

            # 5.1. Агрессивная очистка и декодирование
            reply_str = reply.decode('utf-8').replace('\x00', '').strip()

            if self.debug_mode:
                print(f"M114 Raw Reply String: '{reply_str}'")

            if reply_str.startswith('error'):
                print("CoppeliaSim error:", reply_str, file=sys.stderr)
                return None

            # 5.2. Парсинг очищенного ответа "X=0.0,Y=0.0,Z=0.0,E=0.0"
            parts = {}
            # Перед split очищаем строку от 'M114 Handled and replied: '
            # Дополнительная очистка от логов CoppeliaSim
            if 'Handled and replied:' in reply_str:
                reply_str = reply_str.split('Handled and replied:')[1].strip()

            for item in reply_str.split(','):
                try:
                    key, value = item.split('=', 1)
                    parts[key.strip().upper()] = value.strip()
                except ValueError:
                    continue

            # Возвращаем словарь с float значениями
            result_pos = {
                'x': float(parts.get('X', 0.0)),
                'y': float(parts.get('Y', 0.0)),
                'z': float(parts.get('Z', 0.0)),
                'e': float(parts.get('E', 0.0))
            }

            # ВЫВОДИМ УСПЕХ ДЛЯ ГАРАНТИИ, ДАЖЕ ЕСЛИ debug_mode=False
            print(
                f"M114 Success (Parsed): X={result_pos['x']}, Y={result_pos['y']}, Z={result_pos['z']}, E={result_pos['e']}")

            # Обновляем внутреннее положение контроллера
            self.position = result_pos
            return result_pos

        except Exception as e:
            print(f"Критическая ошибка связи с CoppeliaSim при запросе M114: {e}", file=sys.stderr)
            return None
# synced: 2025-10-10T17:50:44.572960
# synced: 2025-10-10T17:50:48.360924
# synced: 2025-10-10T17:50:50.588784
# synced: 2025-10-10T17:50:52.752907
# synced: 2025-10-10T17:50:54.999930
# synced: 2025-10-10T17:50:57.746674
# synced: 2025-10-10T17:50:59.854085
# synced: 2025-10-10T17:51:02.012796
# synced: 2025-10-10T17:51:04.196922
# synced: 2025-10-10T17:51:06.349056
# synced: 2025-10-10T17:51:08.473990
# synced: 2025-10-10T17:51:10.701351
# synced: 2025-10-10T17:51:12.862925
# synced: 2025-10-10T17:51:14.993718
# synced: 2025-10-10T17:51:17.134248
# synced: 2025-10-10T17:51:19.628576
# synced: 2025-10-10T17:51:21.786472
# synced: 2025-10-10T17:51:24.151120
# synced: 2025-10-10T17:51:26.498548
# synced: 2025-10-10T17:51:29.105280
# synced: 2025-10-10T17:51:31.296384
# synced: 2025-10-10T17:51:33.415814
# synced: 2025-10-10T17:51:35.551576