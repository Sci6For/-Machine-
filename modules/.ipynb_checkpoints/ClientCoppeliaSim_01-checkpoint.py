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
# synced: 2025-10-05T17:24:04.676935
# synced: 2025-10-05T17:24:08.129820
# synced: 2025-10-05T17:24:10.756531
# synced: 2025-10-05T17:24:13.620409
# synced: 2025-10-05T17:24:16.407598
# synced: 2025-10-05T17:24:19.275710
# synced: 2025-10-05T17:24:29.638124
# synced: 2025-10-05T17:24:32.127472
# synced: 2025-10-05T17:24:34.351706
# synced: 2025-10-05T17:24:36.508663
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
# synced: 2025-10-05T17:25:02.474367
# synced: 2025-10-05T17:25:04.577983
# synced: 2025-10-05T17:25:06.793772
# synced: 2025-10-05T17:25:09.045459
# synced: 2025-10-05T17:25:11.196082
# synced: 2025-10-05T17:25:13.479340
# synced: 2025-10-05T17:25:15.673551
# synced: 2025-10-05T17:25:17.911611
# synced: 2025-10-05T17:25:20.142464
# synced: 2025-10-05T17:25:22.354465
# synced: 2025-10-05T17:25:24.531777
# synced: 2025-10-05T17:25:26.761079
# synced: 2025-10-05T17:25:28.938913
# synced: 2025-10-05T17:25:31.188784
# synced: 2025-10-05T17:25:33.423305
# synced: 2025-10-05T17:25:35.607212
# synced: 2025-10-05T17:25:37.853421
# synced: 2025-10-05T17:25:40.100826
# synced: 2025-10-05T17:25:42.356313
# synced: 2025-10-05T17:25:44.557625
# synced: 2025-10-05T17:25:46.741935
# synced: 2025-10-05T17:25:48.933853
# synced: 2025-10-05T17:25:51.151992
# synced: 2025-10-05T17:25:53.359452
# synced: 2025-10-05T17:25:55.540201
# synced: 2025-10-05T17:25:57.741197
# synced: 2025-10-05T17:25:59.976341
# synced: 2025-10-05T17:26:02.157801