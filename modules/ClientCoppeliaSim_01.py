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

    def read_float(self, signal_name):
        """
        Читает float-сигнал из CoppeliaSim.
        Возвращает значение float или None, если ошибка.
        """
        try:
            res, value = sim.simxGetFloatSignal(self.id, signal_name, sim.simx_opmode_blocking)
            if res == sim.simx_return_ok:
                return value
            else:
                print(f"Ошибка чтения {signal_name}: код {res}")
                return None
        except Exception as e:
            print(f"Ошибка при чтении сигнала {signal_name}: {e}")
            return None

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
# synced: 2025-10-05T17:25:42.352313
# synced: 2025-10-05T17:25:44.553233
# synced: 2025-10-05T17:25:46.737238
# synced: 2025-10-05T17:25:48.929299
# synced: 2025-10-05T17:25:51.147381
# synced: 2025-10-05T17:25:53.354873
# synced: 2025-10-05T17:25:55.533745
# synced: 2025-10-05T17:25:57.735666
# synced: 2025-10-05T17:25:59.971993
# synced: 2025-10-05T17:26:02.151750
# synced: 2025-10-05T17:26:04.360354
# synced: 2025-10-05T17:26:06.641004
# synced: 2025-10-05T17:26:08.905188
# synced: 2025-10-05T17:26:11.146568
# synced: 2025-10-05T17:26:13.390452
# synced: 2025-10-05T17:26:15.624819
# synced: 2025-10-05T17:26:17.913387
# synced: 2025-10-05T17:26:20.180384
# synced: 2025-10-10T17:50:44.571958
# synced: 2025-10-10T17:50:48.359921
# synced: 2025-10-10T17:50:50.588784
# synced: 2025-10-10T17:50:52.752907
# synced: 2025-10-10T17:50:54.997934
# synced: 2025-10-10T17:50:57.746674
# synced: 2025-10-10T17:50:59.854085
# synced: 2025-10-10T17:51:02.011743
# synced: 2025-10-10T17:51:04.196922
# synced: 2025-10-10T17:51:06.348057
# synced: 2025-10-10T17:51:08.473990
# synced: 2025-10-10T17:51:10.701351
# synced: 2025-10-10T17:51:12.862925
# synced: 2025-10-10T17:51:14.992651
# synced: 2025-10-10T17:51:17.134248
# synced: 2025-10-10T17:51:19.628576
# synced: 2025-10-10T17:51:21.786472
# synced: 2025-10-10T17:51:24.151120
# synced: 2025-10-10T17:51:26.498548
# synced: 2025-10-10T17:51:29.105280
# synced: 2025-10-10T17:51:31.296384
# synced: 2025-10-10T17:51:33.415814
# synced: 2025-10-10T17:51:35.551576
# synced: 2025-10-10T17:51:38.105298
# synced: 2025-10-10T17:51:40.700881
# synced: 2025-10-10T17:51:43.255666
# synced: 2025-10-10T17:51:45.409143
# synced: 2025-10-10T17:51:47.538615
# synced: 2025-10-10T17:51:49.705650
# synced: 2025-10-10T17:51:51.848999
# synced: 2025-10-10T17:51:54.052974
# synced: 2025-10-10T17:51:56.181275
# synced: 2025-10-10T17:51:58.384996
# synced: 2025-10-10T17:52:00.639568
# synced: 2025-10-10T17:52:02.847576
# synced: 2025-10-10T17:52:05.082374
# synced: 2025-10-10T17:52:07.240345
# synced: 2025-10-10T17:52:09.403069
# synced: 2025-10-10T17:52:11.654399
# synced: 2025-10-10T17:52:13.866851
# synced: 2025-10-10T17:52:16.075769
# synced: 2025-10-10T17:52:18.358392
# synced: 2025-10-10T17:52:20.728831
# synced: 2025-10-10T17:52:22.823048
# synced: 2025-10-10T17:52:24.913117
# synced: 2025-10-10T17:52:27.023976
# synced: 2025-10-10T17:52:29.180119
# synced: 2025-10-10T17:52:31.586586
# synced: 2025-10-10T17:52:33.713422
# synced: 2025-10-10T17:52:35.884691
# synced: 2025-10-10T17:52:37.995459
# synced: 2025-10-10T17:52:40.042287
# synced: 2025-10-10T17:52:42.422711
# synced: 2025-10-10T17:52:44.572025
# synced: 2025-10-10T17:52:46.776849
# synced: 2025-10-10T17:52:48.958906
# synced: 2025-10-10T17:52:51.113058
# synced: 2025-10-10T17:52:53.307680
# synced: 2025-10-10T17:52:55.459059
# synced: 2025-10-10T17:52:57.537915
# synced: 2025-10-10T17:52:59.635400
# synced: 2025-10-10T17:53:01.707223
# synced: 2025-10-10T17:53:03.891032
# synced: 2025-10-10T17:53:06.183058
# synced: 2025-10-10T17:53:08.323189
# synced: 2025-10-10T17:53:10.513817