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
# synced: 2025-10-05T17:24:42.892703
# synced: 2025-10-05T17:24:45.033412
# synced: 2025-10-05T17:24:47.299351
# synced: 2025-10-05T17:24:49.459093
# synced: 2025-10-05T17:24:51.565569
# synced: 2025-10-05T17:24:53.659545
# synced: 2025-10-05T17:24:55.880230
# synced: 2025-10-05T17:24:58.010396
# synced: 2025-10-05T17:25:00.238395
# synced: 2025-10-05T17:25:02.468263
# synced: 2025-10-05T17:25:04.572635
# synced: 2025-10-05T17:25:06.787570
# synced: 2025-10-05T17:25:09.040866
# synced: 2025-10-05T17:25:11.190228
# synced: 2025-10-05T17:25:13.472026
# synced: 2025-10-05T17:25:15.665506
# synced: 2025-10-05T17:25:17.906355
# synced: 2025-10-05T17:25:20.135380
# synced: 2025-10-05T17:25:22.347320
# synced: 2025-10-05T17:25:24.524133
# synced: 2025-10-05T17:25:26.753073
# synced: 2025-10-05T17:25:28.928537
# synced: 2025-10-05T17:25:31.180000
# synced: 2025-10-05T17:25:33.416443
# synced: 2025-10-05T17:25:35.599385
# synced: 2025-10-05T17:25:37.845330
# synced: 2025-10-05T17:25:40.092827
# synced: 2025-10-05T17:25:42.348229
# synced: 2025-10-05T17:25:44.549080
# synced: 2025-10-05T17:25:46.734106
# synced: 2025-10-05T17:25:48.926284
# synced: 2025-10-05T17:25:51.145379
# synced: 2025-10-05T17:25:53.350872
# synced: 2025-10-05T17:25:55.531733
# synced: 2025-10-05T17:25:57.733658
# synced: 2025-10-05T17:25:59.968665
# synced: 2025-10-05T17:26:02.151750
# synced: 2025-10-05T17:26:04.357345
# synced: 2025-10-05T17:26:06.637891
# synced: 2025-10-05T17:26:08.902186
# synced: 2025-10-05T17:26:11.142254
# synced: 2025-10-05T17:26:13.386440
# synced: 2025-10-05T17:26:15.621881
# synced: 2025-10-05T17:26:17.911384
# synced: 2025-10-05T17:26:20.177385
# synced: 2025-10-10T17:50:44.566959
# synced: 2025-10-10T17:50:48.358922
# synced: 2025-10-10T17:50:50.586704
# synced: 2025-10-10T17:50:52.750830
# synced: 2025-10-10T17:50:54.985936
# synced: 2025-10-10T17:50:57.745676
# synced: 2025-10-10T17:50:59.852081
# synced: 2025-10-10T17:51:02.010743
# synced: 2025-10-10T17:51:04.194841
# synced: 2025-10-10T17:51:06.347057
# synced: 2025-10-10T17:51:08.471986
# synced: 2025-10-10T17:51:10.699351