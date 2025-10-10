# Объект функций API CoppeliaSim

import numpy as np

try:
    import sim
except:
    print('--------------------------------------------------------------')
    print('"sim.py" could not be imported. This means very probably that')
    print('either "sim.py" or the remoteApi library could not be found.')
    print('Make sure both are in the same folder as this file,')
    print('or appropriately adjust the file "sim.py"')
    print('--------------------------------------------------------------')
    print('')


class Client_CoppeliaSim:
    def __enter__(self):
        sim.simxFinish(-1)  # just in case, close all opened connections
        self.id = sim.simxStart('127.0.0.1', 19999, True, True, 5000, 5)  # Connect to CoppeliaSim
        if self.id != -1:
            self.send_status_mesage('Python report!')
            self.is_open = True
        else:
            self.is_open = False
        return self

    def __exit__(self, *err):
        # Для проверки, что все команды дошли засылаем ненужную команду возвращающую ответ
        res, ping = sim.simxGetPingTime(self.id)
        if res == 0:
            print("ping time {0} ms".format(ping))
        else:
            print("ping error Code {0}".format(res))
        self.is_open = False
        sim.simxFinish(-1)

    def send_string(self, signal_name, signal):
        sim.simxSetStringSignal(
                clientID = self.id, 
                signalName = signal_name, 
                signalValue = signal, 
                operationMode = sim.simx_opmode_oneshot
            )

    def send_status_mesage(self, message):
        sim.simxAddStatusbarMessage(self.id, message, sim.simx_opmode_oneshot)
# synced: 2025-10-05T17:23:16.937625
# synced: 2025-10-05T17:23:19.874783
# synced: 2025-10-05T17:23:22.754078
# synced: 2025-10-05T17:23:25.477572
# synced: 2025-10-05T17:23:28.215354
# synced: 2025-10-05T17:23:31.169839
# synced: 2025-10-05T17:23:34.033286
# synced: 2025-10-05T17:23:36.762100
# synced: 2025-10-05T17:23:39.591679
# synced: 2025-10-05T17:23:42.247695
# synced: 2025-10-05T17:23:44.985180
# synced: 2025-10-05T17:23:47.891763
# synced: 2025-10-05T17:23:50.625562
# synced: 2025-10-05T17:23:53.444194
# synced: 2025-10-05T17:23:56.273861
# synced: 2025-10-05T17:23:59.057487
# synced: 2025-10-05T17:24:01.841921
# synced: 2025-10-05T17:24:04.660527
# synced: 2025-10-05T17:24:08.105883
# synced: 2025-10-05T17:24:10.738171
# synced: 2025-10-05T17:24:13.602232
# synced: 2025-10-05T17:24:16.388337
# synced: 2025-10-05T17:24:19.258604
# synced: 2025-10-05T17:24:29.632237
# synced: 2025-10-05T17:24:32.122470
# synced: 2025-10-05T17:24:34.345459
# synced: 2025-10-05T17:24:36.500364
# synced: 2025-10-05T17:24:38.651023
# synced: 2025-10-05T17:24:40.748651
# synced: 2025-10-05T17:24:42.892703
# synced: 2025-10-05T17:24:45.033412
# synced: 2025-10-05T17:24:47.299351
# synced: 2025-10-05T17:24:49.459093
# synced: 2025-10-05T17:24:51.564569
# synced: 2025-10-05T17:24:53.658543
# synced: 2025-10-05T17:24:55.880230
# synced: 2025-10-05T17:24:58.010396
# synced: 2025-10-05T17:25:00.237268
# synced: 2025-10-05T17:25:02.468263
# synced: 2025-10-05T17:25:04.572635
# synced: 2025-10-05T17:25:06.787570
# synced: 2025-10-05T17:25:09.040866
# synced: 2025-10-05T17:25:11.188936
# synced: 2025-10-05T17:25:13.471026
# synced: 2025-10-05T17:25:15.664432
# synced: 2025-10-05T17:25:17.905282
# synced: 2025-10-05T17:25:20.134379
# synced: 2025-10-05T17:25:22.347320
# synced: 2025-10-05T17:25:24.524133
# synced: 2025-10-05T17:25:26.752073
# synced: 2025-10-05T17:25:28.928537
# synced: 2025-10-05T17:25:31.180000
# synced: 2025-10-05T17:25:33.416443
# synced: 2025-10-05T17:25:35.599385
# synced: 2025-10-05T17:25:37.845330
# synced: 2025-10-05T17:25:40.092827
# synced: 2025-10-05T17:25:42.348229
# synced: 2025-10-05T17:25:44.549080
# synced: 2025-10-05T17:25:46.733098
# synced: 2025-10-05T17:25:48.925289
# synced: 2025-10-05T17:25:51.144250
# synced: 2025-10-05T17:25:53.350872
# synced: 2025-10-05T17:25:55.531733
# synced: 2025-10-05T17:25:57.733658
# synced: 2025-10-05T17:25:59.967667
# synced: 2025-10-05T17:26:02.149661
# synced: 2025-10-05T17:26:04.357345
# synced: 2025-10-05T17:26:06.636481
# synced: 2025-10-05T17:26:08.901188
# synced: 2025-10-05T17:26:11.142254
# synced: 2025-10-05T17:26:13.386440
# synced: 2025-10-05T17:26:15.621881
# synced: 2025-10-05T17:26:17.909382
# synced: 2025-10-05T17:26:20.176387
# synced: 2025-10-10T17:50:44.565957
# synced: 2025-10-10T17:50:48.357922
# synced: 2025-10-10T17:50:50.586704
# synced: 2025-10-10T17:50:52.750830
# synced: 2025-10-10T17:50:54.983933
# synced: 2025-10-10T17:50:57.745676
# synced: 2025-10-10T17:50:59.852081
# synced: 2025-10-10T17:51:02.010743
# synced: 2025-10-10T17:51:04.194841
# synced: 2025-10-10T17:51:06.347057
# synced: 2025-10-10T17:51:08.471986
# synced: 2025-10-10T17:51:10.699351
# synced: 2025-10-10T17:51:12.860927
# synced: 2025-10-10T17:51:14.990652
# synced: 2025-10-10T17:51:17.132247
# synced: 2025-10-10T17:51:19.626575
# synced: 2025-10-10T17:51:21.784475
# synced: 2025-10-10T17:51:24.149122