# Перезагрузка контроллера под работу с CoppeliaSim вместо Serial
from PrinterController_01 import PrinterController
from ClientCoppeliaSim_01 import Client_CoppeliaSim

class CoppeliaController(PrinterController):
    def connect(self):
        """        Подключение к принтеру.        """
        try:
            self.connection = Client_CoppeliaSim()
            self.connection.__enter__()
            print("Подключено")
        except Exception as e:
            print(f"Ошибка подключения: {e}")

    def disconnect(self):
        """        Отключение от принтера.        """
        if self.connection and self.connection.is_open:
            self.connection.__exit__()
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
            self.connection.send_string("gcode_str", (command + "\n").encode('utf-8'))
            if self.debug_mode:
                print(f"Отправлено: {command}")
            else:
                return None
        
        except Exception as e:
            print(f"Ошибка при отправке команды: {e}")
            return None
    
    def home(self):
        """        Возврат всех осей в исходное положение (Home).        """
        # # self.send_command("G1 X0 Y0 Z0 E0")
        # self.move(x=0, y=0, z=0, e=0)
        # self.position = np.zeros(4)
        self.send_command("G90 \n" +
            "G1 X0 Y0 Z0 E0 \n" +
            "G91")

# synced: 2025-10-05T17:23:16.967849
# synced: 2025-10-05T17:23:19.885246
# synced: 2025-10-05T17:23:22.765273
# synced: 2025-10-05T17:23:25.490206
# synced: 2025-10-05T17:23:28.230769
# synced: 2025-10-05T17:23:31.182628
# synced: 2025-10-05T17:23:34.046444
# synced: 2025-10-05T17:23:36.779337
# synced: 2025-10-05T17:23:39.611775
# synced: 2025-10-05T17:23:42.266350
# synced: 2025-10-05T17:23:45.006564
# synced: 2025-10-05T17:23:47.912957
# synced: 2025-10-05T17:23:50.648899
# synced: 2025-10-05T17:23:53.456249
# synced: 2025-10-05T17:23:56.286971
# synced: 2025-10-05T17:23:59.070487
# synced: 2025-10-05T17:24:01.853920
# synced: 2025-10-05T17:24:04.676935
# synced: 2025-10-05T17:24:08.130129
# synced: 2025-10-05T17:24:10.756531
# synced: 2025-10-05T17:24:13.621411
# synced: 2025-10-05T17:24:16.408479
# synced: 2025-10-05T17:24:19.275710
# synced: 2025-10-05T17:24:29.638124
# synced: 2025-10-05T17:24:32.128472
# synced: 2025-10-05T17:24:34.351706
# synced: 2025-10-05T17:24:36.509667
# synced: 2025-10-05T17:24:38.659361
# synced: 2025-10-05T17:24:40.754440
# synced: 2025-10-05T17:24:42.898798
# synced: 2025-10-05T17:24:45.040596
# synced: 2025-10-05T17:24:47.305353
# synced: 2025-10-05T17:24:49.465084
# synced: 2025-10-05T17:24:51.573031
# synced: 2025-10-05T17:24:53.666541
# synced: 2025-10-05T17:24:55.888055
# synced: 2025-10-05T17:24:58.017069
# synced: 2025-10-05T17:25:00.242712
# synced: 2025-10-05T17:25:02.475365
# synced: 2025-10-05T17:25:04.577983
# synced: 2025-10-05T17:25:06.793772
# synced: 2025-10-05T17:25:09.046714
# synced: 2025-10-05T17:25:11.197081
# synced: 2025-10-05T17:25:13.480339
# synced: 2025-10-05T17:25:15.673551
# synced: 2025-10-05T17:25:17.911611
# synced: 2025-10-05T17:25:20.142464
# synced: 2025-10-05T17:25:22.354465
# synced: 2025-10-05T17:25:24.531777
# synced: 2025-10-05T17:25:26.762079
# synced: 2025-10-05T17:25:28.938913