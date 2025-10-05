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