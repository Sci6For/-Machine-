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

# synced: 2025-10-05T17:23:16.948172
# synced: 2025-10-05T17:23:19.876782
# synced: 2025-10-05T17:23:22.755231
# synced: 2025-10-05T17:23:25.479440
# synced: 2025-10-05T17:23:28.219841
# synced: 2025-10-05T17:23:31.171859
# synced: 2025-10-05T17:23:34.034286
# synced: 2025-10-05T17:23:36.766257
# synced: 2025-10-05T17:23:39.594763
# synced: 2025-10-05T17:23:42.249712
# synced: 2025-10-05T17:23:44.989248
# synced: 2025-10-05T17:23:47.895967
# synced: 2025-10-05T17:23:50.633714
# synced: 2025-10-05T17:23:53.445357
# synced: 2025-10-05T17:23:56.275893
# synced: 2025-10-05T17:23:59.058486
# synced: 2025-10-05T17:24:01.842921
# synced: 2025-10-05T17:24:04.660527
# synced: 2025-10-05T17:24:08.110145
# synced: 2025-10-05T17:24:10.739472
# synced: 2025-10-05T17:24:13.604232
# synced: 2025-10-05T17:24:16.388337
# synced: 2025-10-05T17:24:19.258604
# synced: 2025-10-05T17:24:29.633253
# synced: 2025-10-05T17:24:32.123471
# synced: 2025-10-05T17:24:34.347209
# synced: 2025-10-05T17:24:36.502373
# synced: 2025-10-05T17:24:38.653031
# synced: 2025-10-05T17:24:40.749649
# synced: 2025-10-05T17:24:42.893709
# synced: 2025-10-05T17:24:45.033412
# synced: 2025-10-05T17:24:47.300350
# synced: 2025-10-05T17:24:49.459093
# synced: 2025-10-05T17:24:51.566571
# synced: 2025-10-05T17:24:53.660541
# synced: 2025-10-05T17:24:55.881227
# synced: 2025-10-05T17:24:58.010396
# synced: 2025-10-05T17:25:00.238395
# synced: 2025-10-05T17:25:02.469364
# synced: 2025-10-05T17:25:04.573637
# synced: 2025-10-05T17:25:06.788926
# synced: 2025-10-05T17:25:09.041922
# synced: 2025-10-05T17:25:11.190228
# synced: 2025-10-05T17:25:13.473308
# synced: 2025-10-05T17:25:15.666509
# synced: 2025-10-05T17:25:17.906355
# synced: 2025-10-05T17:25:20.135380
# synced: 2025-10-05T17:25:22.348321
# synced: 2025-10-05T17:25:24.525111
# synced: 2025-10-05T17:25:26.754078
# synced: 2025-10-05T17:25:28.932400
# synced: 2025-10-05T17:25:31.180000
# synced: 2025-10-05T17:25:33.416443
# synced: 2025-10-05T17:25:35.600381
# synced: 2025-10-05T17:25:37.846423
# synced: 2025-10-05T17:25:40.093827
# synced: 2025-10-05T17:25:42.349231
# synced: 2025-10-05T17:25:44.549080
# synced: 2025-10-05T17:25:46.735109
# synced: 2025-10-05T17:25:48.927284
# synced: 2025-10-05T17:25:51.146379
# synced: 2025-10-05T17:25:53.352884
# synced: 2025-10-05T17:25:55.533745
# synced: 2025-10-05T17:25:57.734667
# synced: 2025-10-05T17:25:59.969665
# synced: 2025-10-05T17:26:02.151750
# synced: 2025-10-05T17:26:04.358350
# synced: 2025-10-05T17:26:06.638891
# synced: 2025-10-05T17:26:08.903189
# synced: 2025-10-05T17:26:11.146568
# synced: 2025-10-05T17:26:13.390452
# synced: 2025-10-05T17:26:15.621881
# synced: 2025-10-05T17:26:17.911384
# synced: 2025-10-05T17:26:20.178385
# synced: 2025-10-10T17:50:44.567958
# synced: 2025-10-10T17:50:48.358922
# synced: 2025-10-10T17:50:50.587784
# synced: 2025-10-10T17:50:52.751905
# synced: 2025-10-10T17:50:54.987932
# synced: 2025-10-10T17:50:57.745676
# synced: 2025-10-10T17:50:59.853078
# synced: 2025-10-10T17:51:02.010743
# synced: 2025-10-10T17:51:04.195923
# synced: 2025-10-10T17:51:06.348057
# synced: 2025-10-10T17:51:08.472987
# synced: 2025-10-10T17:51:10.700350
# synced: 2025-10-10T17:51:12.861925
# synced: 2025-10-10T17:51:14.991652
# synced: 2025-10-10T17:51:17.133247
# synced: 2025-10-10T17:51:19.627577
# synced: 2025-10-10T17:51:21.785470