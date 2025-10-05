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
        # self.send_command("G1 X0 Y0 Z0 E0")
        self.move(x=0, y=0, z=0, e=0)
        self.position = np.zeros(4)

# synced: 2025-10-05T17:23:16.941891
# synced: 2025-10-05T17:23:19.875782
# synced: 2025-10-05T17:23:22.754078
# synced: 2025-10-05T17:23:25.477572
# synced: 2025-10-05T17:23:28.215354
# synced: 2025-10-05T17:23:31.169839
# synced: 2025-10-05T17:23:34.033286
# synced: 2025-10-05T17:23:36.764859
# synced: 2025-10-05T17:23:39.592748
# synced: 2025-10-05T17:23:42.247695
# synced: 2025-10-05T17:23:44.985180
# synced: 2025-10-05T17:23:47.891763
# synced: 2025-10-05T17:23:50.625562
# synced: 2025-10-05T17:23:53.444194
# synced: 2025-10-05T17:23:56.274892
# synced: 2025-10-05T17:23:59.057487
# synced: 2025-10-05T17:24:01.841921
# synced: 2025-10-05T17:24:04.660527
# synced: 2025-10-05T17:24:08.105883
# synced: 2025-10-05T17:24:10.739061
# synced: 2025-10-05T17:24:13.602232
# synced: 2025-10-05T17:24:16.388337
# synced: 2025-10-05T17:24:19.258604
# synced: 2025-10-05T17:24:29.633253
# synced: 2025-10-05T17:24:32.123471
# synced: 2025-10-05T17:24:34.345459
# synced: 2025-10-05T17:24:36.501370
# synced: 2025-10-05T17:24:38.651023
# synced: 2025-10-05T17:24:40.748651