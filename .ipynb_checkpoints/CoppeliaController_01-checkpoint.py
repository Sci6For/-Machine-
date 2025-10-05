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