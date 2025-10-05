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
# synced: 2025-10-05T17:23:16.966342
# synced: 2025-10-05T17:23:19.885246
# synced: 2025-10-05T17:23:22.765273
# synced: 2025-10-05T17:23:25.490206
# synced: 2025-10-05T17:23:28.230769
# synced: 2025-10-05T17:23:31.182628
# synced: 2025-10-05T17:23:34.045443
# synced: 2025-10-05T17:23:36.779337
# synced: 2025-10-05T17:23:39.611775
# synced: 2025-10-05T17:23:42.266350
# synced: 2025-10-05T17:23:45.006564
# synced: 2025-10-05T17:23:47.908621
# synced: 2025-10-05T17:23:50.648899
# synced: 2025-10-05T17:23:53.455252
# synced: 2025-10-05T17:23:56.286971
# synced: 2025-10-05T17:23:59.069486
# synced: 2025-10-05T17:24:01.852923