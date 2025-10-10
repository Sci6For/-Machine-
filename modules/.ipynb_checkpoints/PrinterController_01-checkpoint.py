# Контроллер 
#     умеет устанавливать соединение и высылать команды G-code

import numpy as np
import serial


class PrinterController:
    def __init__(self, **kwargs):
        """
        Инициализация соединения с принтером.
        :param com_port: Номер COM-порта (например, 'COM3' или '/dev/ttyUSB0').
        :param baud_rate: Скорость передачи данных (по умолчанию 115200).
        :param timeout: Время ожидания ответа от принтера (в секундах).
        """
        self.connection = None         # объект связи с serial
        self.position = np.zeros(4)    # отсчет положения принтера

        # константы
        self.com_port = kwargs.get('com_port', 'COM4')
        self.baud_rate = kwargs.get('baud_rate', 115200)
        self.timeout = kwargs.get('timeout', 1)
        self.speed = kwargs.get('speed', 3000)
        self.k_e = kwargs.get('k_e', 1/9)
        self.invert = kwargs.get('invert', (1, 1, 1, 1))

        # флаги
        self.debug_mode = kwargs.get('debug', False)        # выключатель контольных сообщений
        self.abs_mode = None           # принтер в режиме абсолютных координат

    def connect(self):
        """        Подключение к принтеру.        """
        try:
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
        :return: Текущая позиция (строка).
        """
        _message = self.send_command("M114")

        if auto_print:
            print(_message)
        return _message

    def set_cold_extrusion(self):
        self.send_command("M302 P1 ; Разрешить холодную экструзию")

# synced: 2025-10-05T17:23:16.972274
# synced: 2025-10-05T17:23:19.889446
# synced: 2025-10-05T17:23:22.769311
# synced: 2025-10-05T17:23:25.490206
# synced: 2025-10-05T17:23:28.232813
# synced: 2025-10-05T17:23:31.184976
# synced: 2025-10-05T17:23:34.047443
# synced: 2025-10-05T17:23:36.782418
# synced: 2025-10-05T17:23:39.614777
# synced: 2025-10-05T17:23:42.269809
# synced: 2025-10-05T17:23:45.010931
# synced: 2025-10-05T17:23:47.914960
# synced: 2025-10-05T17:23:50.651042
# synced: 2025-10-05T17:23:53.458250
# synced: 2025-10-05T17:23:56.289117
# synced: 2025-10-05T17:23:59.071487
# synced: 2025-10-05T17:24:01.855923
# synced: 2025-10-05T17:24:04.681370
# synced: 2025-10-05T17:24:08.133485
# synced: 2025-10-05T17:24:10.759827
# synced: 2025-10-05T17:24:13.624410
# synced: 2025-10-05T17:24:16.411540
# synced: 2025-10-05T17:24:19.275710
# synced: 2025-10-05T17:24:29.639136
# synced: 2025-10-05T17:24:32.129472
# synced: 2025-10-05T17:24:34.356167
# synced: 2025-10-05T17:24:36.510664
# synced: 2025-10-05T17:24:38.663625
# synced: 2025-10-05T17:24:40.755453
# synced: 2025-10-05T17:24:42.900244
# synced: 2025-10-05T17:24:45.042659
# synced: 2025-10-05T17:24:47.306349
# synced: 2025-10-05T17:24:49.466084
# synced: 2025-10-05T17:24:51.575184
# synced: 2025-10-05T17:24:53.666541
# synced: 2025-10-05T17:24:55.890061
# synced: 2025-10-05T17:24:58.019899
# synced: 2025-10-05T17:25:00.244252
# synced: 2025-10-05T17:25:02.476367
# synced: 2025-10-05T17:25:04.578981
# synced: 2025-10-05T17:25:06.796310
# synced: 2025-10-05T17:25:09.047718
# synced: 2025-10-05T17:25:11.198114
# synced: 2025-10-05T17:25:13.481340
# synced: 2025-10-05T17:25:15.675554
# synced: 2025-10-05T17:25:17.912611
# synced: 2025-10-05T17:25:20.144465
# synced: 2025-10-05T17:25:22.356464
# synced: 2025-10-05T17:25:24.533001
# synced: 2025-10-05T17:25:26.763084
# synced: 2025-10-05T17:25:28.940914
# synced: 2025-10-05T17:25:31.188784
# synced: 2025-10-05T17:25:33.425109
# synced: 2025-10-05T17:25:35.609405
# synced: 2025-10-05T17:25:37.854435
# synced: 2025-10-05T17:25:40.102827
# synced: 2025-10-05T17:25:42.358315
# synced: 2025-10-05T17:25:44.557625
# synced: 2025-10-05T17:25:46.743935
# synced: 2025-10-05T17:25:48.935974
# synced: 2025-10-05T17:25:51.153999
# synced: 2025-10-05T17:25:53.360456
# synced: 2025-10-05T17:25:55.540201
# synced: 2025-10-05T17:25:57.742208
# synced: 2025-10-05T17:25:59.978342
# synced: 2025-10-05T17:26:02.157801
# synced: 2025-10-05T17:26:04.367353
# synced: 2025-10-05T17:26:06.647031
# synced: 2025-10-05T17:26:08.912383
# synced: 2025-10-05T17:26:11.155356
# synced: 2025-10-05T17:26:13.398746
# synced: 2025-10-05T17:26:15.633260
# synced: 2025-10-05T17:26:17.921395
# synced: 2025-10-05T17:26:20.187901
# synced: 2025-10-10T17:50:44.577960
# synced: 2025-10-10T17:50:48.363922
# synced: 2025-10-10T17:50:50.592788
# synced: 2025-10-10T17:50:52.755907
# synced: 2025-10-10T17:50:55.017983
# synced: 2025-10-10T17:50:57.749673
# synced: 2025-10-10T17:50:59.857083
# synced: 2025-10-10T17:51:02.015797
# synced: 2025-10-10T17:51:04.200923
# synced: 2025-10-10T17:51:06.352120
# synced: 2025-10-10T17:51:08.477064
# synced: 2025-10-10T17:51:10.705350
# synced: 2025-10-10T17:51:12.865985
# synced: 2025-10-10T17:51:14.996717
# synced: 2025-10-10T17:51:17.137247
# synced: 2025-10-10T17:51:19.632684
# synced: 2025-10-10T17:51:21.789520
# synced: 2025-10-10T17:51:24.155186
# synced: 2025-10-10T17:51:26.501617
# synced: 2025-10-10T17:51:29.108284
# synced: 2025-10-10T17:51:31.300473
# synced: 2025-10-10T17:51:33.418813
# synced: 2025-10-10T17:51:35.554575
# synced: 2025-10-10T17:51:38.109298
# synced: 2025-10-10T17:51:40.703884
# synced: 2025-10-10T17:51:43.258670
# synced: 2025-10-10T17:51:45.413232
# synced: 2025-10-10T17:51:47.541615
# synced: 2025-10-10T17:51:49.708724
# synced: 2025-10-10T17:51:51.852000
# synced: 2025-10-10T17:51:54.056076
# synced: 2025-10-10T17:51:56.185278
# synced: 2025-10-10T17:51:58.390993
# synced: 2025-10-10T17:52:00.643572