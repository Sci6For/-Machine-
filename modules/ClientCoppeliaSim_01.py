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
# synced: 2025-10-05T17:23:16.956438
# synced: 2025-10-05T17:23:19.880865
# synced: 2025-10-05T17:23:22.756980
# synced: 2025-10-05T17:23:25.481903
# synced: 2025-10-05T17:23:28.223296
# synced: 2025-10-05T17:23:31.176072
# synced: 2025-10-05T17:23:34.037593
# synced: 2025-10-05T17:23:36.770992
# synced: 2025-10-05T17:23:39.601201
# synced: 2025-10-05T17:23:42.255805
# synced: 2025-10-05T17:23:44.994385
# synced: 2025-10-05T17:23:47.899993
# synced: 2025-10-05T17:23:50.638819
# synced: 2025-10-05T17:23:53.448585
# synced: 2025-10-05T17:23:56.279894
# synced: 2025-10-05T17:23:59.063486
# synced: 2025-10-05T17:24:01.845921
# synced: 2025-10-05T17:24:04.668584
# synced: 2025-10-05T17:24:08.117828
# synced: 2025-10-05T17:24:10.745825
# synced: 2025-10-05T17:24:13.609337
# synced: 2025-10-05T17:24:16.396869
# synced: 2025-10-05T17:24:19.267392
# synced: 2025-10-05T17:24:29.634714
# synced: 2025-10-05T17:24:32.125472
# synced: 2025-10-05T17:24:34.347209
# synced: 2025-10-05T17:24:36.504371
# synced: 2025-10-05T17:24:38.655044
# synced: 2025-10-05T17:24:40.750826
# synced: 2025-10-05T17:24:42.895708
# synced: 2025-10-05T17:24:45.035822
# synced: 2025-10-05T17:24:47.302354
# synced: 2025-10-05T17:24:49.461084
# synced: 2025-10-05T17:24:51.568583
# synced: 2025-10-05T17:24:53.662542
# synced: 2025-10-05T17:24:55.883590
# synced: 2025-10-05T17:24:58.010396
# synced: 2025-10-05T17:25:00.240395
# synced: 2025-10-05T17:25:02.471364
# synced: 2025-10-05T17:25:04.574721
# synced: 2025-10-05T17:25:06.790022
# synced: 2025-10-05T17:25:09.042927
# synced: 2025-10-05T17:25:11.192635
# synced: 2025-10-05T17:25:13.475339
# synced: 2025-10-05T17:25:15.668508
# synced: 2025-10-05T17:25:17.907557
# synced: 2025-10-05T17:25:20.137466
# synced: 2025-10-05T17:25:22.349321
# synced: 2025-10-05T17:25:24.527480
# synced: 2025-10-05T17:25:26.756071
# synced: 2025-10-05T17:25:28.934726
# synced: 2025-10-05T17:25:31.184462
# synced: 2025-10-05T17:25:33.419460
# synced: 2025-10-05T17:25:35.602383
# synced: 2025-10-05T17:25:37.848421
# synced: 2025-10-05T17:25:40.095826