# Контроллер
#     умеет устанавливать соединение и высылать команды G-code

import numpy as np
import serial
import sys


class PrinterController:
    def __init__(self, **kwargs):
        """
        Инициализация соединения с принтером.
        :param com_port: Номер COM-порта (например, 'COM3' или '/dev/ttyUSB0').
        :param baud_rate: Скорость передачи данных (по умолчанию 115200).
        :param timeout: Время ожидания ответа от принтера (в секундах).
        """
        self.connection = None  # объект связи с serial
        self.position = np.zeros(4)  # отсчет положения принтера

        # константы
        self.com_port = kwargs.get('com_port', 'COM4')
        self.baud_rate = kwargs.get('baud_rate', 115200)
        self.timeout = kwargs.get('timeout', 1)
        self.speed = kwargs.get('speed', 3000)
        self.k_e = kwargs.get('k_e', 1 / 9)
        self.invert = kwargs.get('invert', (1, 1, 1, 1))

        # флаги
        self.debug_mode = kwargs.get('debug', False)  # выключатель контольных сообщений
        self.abs_mode = None  # принтер в режиме абсолютных координат

    def connect(self):
        """        Подключение к принтеру.        """
        try:
            # В CoppeliaSim этот метод будет переопределен
            self.connection = serial.Serial(self.com_port, self.baud_rate, timeout=self.timeout)
            print(f"Подключено к {self.com_port} со скоростью {self.baud_rate} бод")
        except Exception as e:
            print(f"Ошибка подключения: {e}")

    def disconnect(self):
        """        Отключение от принтера.        """
        if self.connection and self.connection.is_open:
            self.connection.close()
            print("Соединение закрыто")

    def send_command(self, command, read_response=True):
        """
        Отправка команды на принтер.
        :param command: Команда для отправки (строка G-кода).
        :param read_response: Флаг, указывающий, нужно ли читать ответ принтера.
        :return: Ответ принтера (если read_response=True).
        """
        if not self.connection or not self.connection.is_open:
            print("Ошибка: Соединение не установлено")
            return None

        try:
            # Отправка команды
            self.connection.write((command + "\n").encode('utf-8'))
            if self.debug_mode:
                print(f"Отправлено: {command}")
            # Чтение ответа
            if read_response:
                response = ""
                while True:
                    line = self.connection.readline().decode('utf-8').strip()
                    if not line:
                        break
                    response += line + "\n"
                return response.strip()
            else:
                return None

        except Exception as e:
            print(f"Ошибка при отправке команды: {e}")
            return None

    def home(self):
        """        Возврат всех осей в исходное положение (Home).        """
        self.send_command("G28")
        self.position = np.zeros(4)

    def set_temperature(self, tool_temp=None, bed_temp=None, wait=False):
        """
        Установка температуры хотэнда и/или стола.
        :param tool_temp: Температура хотэнда (в °C).
        :param bed_temp: Температура стола (в °C).
        :param wait: Ждать завершения нагрева.
        """
        if tool_temp is not None:
            command = f"M109 S{tool_temp}" if wait else f"M104 S{tool_temp}"
            self.send_command(command)

        if bed_temp is not None:
            command = f"M190 S{bed_temp}" if wait else f"M140 S{bed_temp}"
            self.send_command(command)

    def move(self, x=None, y=None, z=None, e=None, speed=None):
        """
        Перемещение осей и экструдера.
        :param x: Позиция по оси X (в мм).
        :param y: Позиция по оси Y (в мм).
        :param z: Позиция по оси Z (в мм).
        :param e: Экструзия (в мм).
        :param speed: Скорость перемещения (в мм/мин).
        """
        if speed is None:
            speed = self.speed
        if not self.abs_mode or self.abs_mode is None:
            self._set_abs_cords()

        self.position = self._position_to_abs(x, y, z, e)
        command = self._create_G_code_cord_str("G1", x, y, z, e, speed)
        self.send_command(command)

    def _position_to_abs(self, x, y, z, e):
        """        Определение положения по относительной команде        """
        pos = self.position.copy()
        if x is not None: pos[0] = x * self.invert[0]
        if y is not None: pos[1] = y * self.invert[1]
        if z is not None: pos[2] = z * self.invert[2]
        if e is not None: pos[3] = e * self.invert[3] * self.k_e
        return pos

    def move_realtive(self, x=None, y=None, z=None, e=None, speed=None):
        """
        Перемещение осей и экструдера.
        :param x: Позиция по оси X (в мм).
        :param y: Позиция по оси Y (в мм).
        :param z: Позиция по оси Z (в мм).
        :param e: Экструзия (в мм).
        :param speed: Скорость перемещения (в мм/мин).
        """
        if speed is None:
            speed = self.speed
        if self.abs_mode or self.abs_mode is None:
            self._set_rel_cords()

        self.position = self._position_to_rel(x, y, z, e)
        command = self._create_G_code_cord_str("G1", x, y, z, e, speed)
        self.send_command(command)

    def _position_to_rel(self, x, y, z, e):
        """        Определение положения по относительной команде        """
        pos = self.position.copy()

        if x is not None: pos[0] += x * self.invert[0]
        if y is not None: pos[1] += y * self.invert[1]
        if z is not None: pos[2] += z * self.invert[2]
        if e is not None: pos[3] += e * self.invert[3] * self.k_e

        return pos

    def _create_G_code_cord_str(self, prefix, x, y, z, e, speed):
        command = prefix

        if x is not None:            command += f" X{x * self.invert[0]}"
        if y is not None:            command += f" Y{y * self.invert[1]}"
        if z is not None:            command += f" Z{z * self.invert[2]}"
        if e is not None:            command += f" E{e * self.invert[3] * self.k_e}"
        if speed is not None:        command += f" F{speed}"

        return command

    def _set_abs_cords(self):
        """ Установка режима абсолютных координат """
        self.abs_mode = True
        self.send_command("G90")

    def _set_rel_cords(self):
        """ Установка режима относительных координат """
        self.abs_mode = False
        self.send_command("G91")

    def set_zero(self, x=0, y=0, z=0, e=0):
        """
        Установка (начальных) координат.
        :param x: Позиция по оси X (в мм).
        :param y: Позиция по оси Y (в мм).
        :param z: Позиция по оси Z (в мм).
        :param e: Экструзия (в мм).
        """

        command = self._create_G_code_cord_str("G92", x, y, z, e, None)
        self.send_command(command)

    def get_position(self, auto_print=False):
        """
        Получение текущей позиции осей.
        В базовом классе возвращает None, так как команда M114 должна
        обрабатываться через выделенный канал в CoppeliaController.
        """
        # --- ИСПРАВЛЕНО: УДАЛЕН ВЫЗОВ M114 ---
        # Вызов M114 заблокирован, чтобы избежать дублирования в CoppeliaController.
        if self.debug_mode or auto_print:
            print("Base PrinterController get_position called. Use CoppeliaController.get_position().", file=sys.stderr)
        return None

    def set_cold_extrusion(self):
        self.send_command("M302 P1 ; Разрешить холодную экструзию")

# synced: 2025-10-05T17:23:16.959437
# synced: 2025-10-05T17:23:19.882728
# synced: 2025-10-05T17:23:22.761201
# synced: 2025-10-05T17:23:25.485992
# synced: 2025-10-05T17:23:28.225383
# synced: 2025-10-05T17:23:31.177286
# synced: 2025-10-05T17:23:34.039691
# synced: 2025-10-05T17:23:36.773263
# synced: 2025-10-05T17:23:39.604590
# synced: 2025-10-05T17:23:42.258588
# synced: 2025-10-05T17:23:44.998223
# synced: 2025-10-05T17:23:47.904455
# synced: 2025-10-05T17:23:50.642500
# synced: 2025-10-05T17:23:53.451251
# synced: 2025-10-05T17:23:56.281893
# synced: 2025-10-05T17:23:59.065487
# synced: 2025-10-05T17:24:01.847920
# synced: 2025-10-05T17:24:04.668584
# synced: 2025-10-05T17:24:08.121974
# synced: 2025-10-05T17:24:10.749128
# synced: 2025-10-05T17:24:13.613408
# synced: 2025-10-05T17:24:16.401039
# synced: 2025-10-05T17:24:19.268399
# synced: 2025-10-05T17:24:29.635714
# synced: 2025-10-05T17:24:32.126472
# synced: 2025-10-05T17:24:34.347209
# synced: 2025-10-05T17:24:36.506372
# synced: 2025-10-05T17:24:38.657583
# synced: 2025-10-05T17:24:40.752002
# synced: 2025-10-05T17:24:42.896800
# synced: 2025-10-05T17:24:45.038157
# synced: 2025-10-05T17:24:47.303350
# synced: 2025-10-05T17:24:49.463085
# synced: 2025-10-05T17:24:51.570617
# synced: 2025-10-05T17:24:53.664541
# synced: 2025-10-05T17:24:55.884605
# synced: 2025-10-05T17:24:58.014620
# synced: 2025-10-05T17:25:00.241564
# synced: 2025-10-05T17:25:02.472367
# synced: 2025-10-05T17:25:04.575770
# synced: 2025-10-05T17:25:06.791475
# synced: 2025-10-05T17:25:09.044388
# synced: 2025-10-05T17:25:11.193687
# synced: 2025-10-05T17:25:13.476339
# synced: 2025-10-05T17:25:15.670544
# synced: 2025-10-05T17:25:17.909611
# synced: 2025-10-05T17:25:20.139464
# synced: 2025-10-05T17:25:22.351967
# synced: 2025-10-05T17:25:24.528957
# synced: 2025-10-05T17:25:26.758073
# synced: 2025-10-05T17:25:28.935913
# synced: 2025-10-05T17:25:31.184462
# synced: 2025-10-05T17:25:33.420769
# synced: 2025-10-05T17:25:35.604382
# synced: 2025-10-05T17:25:37.850424
# synced: 2025-10-05T17:25:40.097826
# synced: 2025-10-05T17:25:42.354312
# synced: 2025-10-05T17:25:44.553233
# synced: 2025-10-05T17:25:46.738323
# synced: 2025-10-05T17:25:48.931301
# synced: 2025-10-05T17:25:51.149379
# synced: 2025-10-05T17:25:53.357027
# synced: 2025-10-05T17:25:55.538084
# synced: 2025-10-05T17:25:57.735666
# synced: 2025-10-05T17:25:59.971993
# synced: 2025-10-05T17:26:02.155904
# synced: 2025-10-05T17:26:04.362354
# synced: 2025-10-05T17:26:06.643004
# synced: 2025-10-05T17:26:08.907189
# synced: 2025-10-05T17:26:11.150900
# synced: 2025-10-05T17:26:13.394682
# synced: 2025-10-05T17:26:15.624819
# synced: 2025-10-05T17:26:17.915389
# synced: 2025-10-05T17:26:20.182389
# synced: 2025-10-10T17:50:44.573961
# synced: 2025-10-10T17:50:48.360924
# synced: 2025-10-10T17:50:50.589783
# synced: 2025-10-10T17:50:52.753905
# synced: 2025-10-10T17:50:55.007938
# synced: 2025-10-10T17:50:57.747674
# synced: 2025-10-10T17:50:59.855084
# synced: 2025-10-10T17:51:02.012796
# synced: 2025-10-10T17:51:04.197927
# synced: 2025-10-10T17:51:06.349056
# synced: 2025-10-10T17:51:08.474990
# synced: 2025-10-10T17:51:10.702352
# synced: 2025-10-10T17:51:12.863927
# synced: 2025-10-10T17:51:14.994720
# synced: 2025-10-10T17:51:17.135246
# synced: 2025-10-10T17:51:19.629580
# synced: 2025-10-10T17:51:21.787471
# synced: 2025-10-10T17:51:24.152185
# synced: 2025-10-10T17:51:26.499549
# synced: 2025-10-10T17:51:29.106286
# synced: 2025-10-10T17:51:31.297474
# synced: 2025-10-10T17:51:33.416813
# synced: 2025-10-10T17:51:35.552576
# synced: 2025-10-10T17:51:38.106299
# synced: 2025-10-10T17:51:40.701887
# synced: 2025-10-10T17:51:43.255666
# synced: 2025-10-10T17:51:45.410144
# synced: 2025-10-10T17:51:47.539615
# synced: 2025-10-10T17:51:49.706721
# synced: 2025-10-10T17:51:51.849998
# synced: 2025-10-10T17:51:54.054078
# synced: 2025-10-10T17:51:56.182271
# synced: 2025-10-10T17:51:58.386993
# synced: 2025-10-10T17:52:00.640570
# synced: 2025-10-10T17:52:02.849576
# synced: 2025-10-10T17:52:05.083373
# synced: 2025-10-10T17:52:07.241344
# synced: 2025-10-10T17:52:09.404131
# synced: 2025-10-10T17:52:11.654399
# synced: 2025-10-10T17:52:13.867919
# synced: 2025-10-10T17:52:16.076768
# synced: 2025-10-10T17:52:18.359393
# synced: 2025-10-10T17:52:20.729829
# synced: 2025-10-10T17:52:22.824048
# synced: 2025-10-10T17:52:24.915115
# synced: 2025-10-10T17:52:27.026012
# synced: 2025-10-10T17:52:29.181121
# synced: 2025-10-10T17:52:31.587586
# synced: 2025-10-10T17:52:33.714479
# synced: 2025-10-10T17:52:35.885691
# synced: 2025-10-10T17:52:37.996459
# synced: 2025-10-10T17:52:40.043284