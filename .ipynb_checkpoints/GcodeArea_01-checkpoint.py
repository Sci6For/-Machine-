import tkinter as tk
from tkinter import ttk

class GcodeArea(tk.Frame):
    def __init__(self, master=None, on_click_callback=None, **kwargs):
        if not 'borderwidth' in kwargs: kwargs['borderwidth'] = 2
        if not 'relief' in kwargs: kwargs['relief'] = "groove"

        super().__init__(master, **kwargs)
        self.master = master
        self.on_click_callback = on_click_callback

        # Настройка адаптивного размера для текстового поля
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Создание текстового поля с полосой прокрутки
        self.text_area = tk.Text(self, wrap="word", height=10, width=20)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.text_area.yview)
        self.text_area.config(yscrollcommand=scrollbar.set)

        # Размещение текстового поля и полосы прокрутки в сетке
        self.text_area.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        scrollbar.grid(row=0, column=2, sticky="ns", pady=5)

        sub_frame = tk.Frame(self)
        sub_frame.grid(row=0, column=3, padx=2, pady=2, sticky="new")

        # Кнопка "Добавить строку"
        add_G90_button = tk.Button(sub_frame, text="G90 (abs)", command=self.add_G90_bt)
        add_G90_button.pack(side="top", fill="x", expand=True, anchor="n")
        add_G91_button = tk.Button(sub_frame, text="G91 (rel)", command=self.add_G91_bt)
        add_G91_button.pack(side="top", fill="x", expand=True, anchor="n")
        add_G1_button = tk.Button(sub_frame, text="G1", command=self.add_G1_bt)
        add_G1_button.pack(side="top", fill="x", expand=True, anchor="n")

        clear_button = tk.Button(sub_frame, text="clear", command=self.clear_text_area)
        clear_button.pack(side="top", fill="x", expand=True, anchor="n")
        # Кнопка "Распечатать"
        print_button = tk.Button(sub_frame, text="SEND", command=self._handle_click)
        print_button.pack(side="top", fill="x", expand=True, anchor="n")
    
    def add_G90_bt(self):
        """Добавляет строку в текстовое поле."""
        new_line = "G90; absolute cords\n"  # Формируем новую строку
        self.text_area.insert("end", new_line)  # Вставляем новую строку
    
    def add_G91_bt(self):
        """Добавляет строку в текстовое поле."""
        new_line = "G91; relative cords\n"  # Формируем новую строку
        self.text_area.insert("end", new_line)  # Вставляем новую строку


    def add_G1_bt(self):
        """Добавляет строку в текстовое поле."""
        new_line = "G1 X0 Y0 Z0 E0\n"  # Формируем новую строку
        self.text_area.insert("end", new_line)  # Вставляем новую строку
    
    def clear_text_area(self):
        self.text_area.delete("1.0", "end")

    def take_text(self):
        """Выводит содержимое текстового поля в консоль."""
        text_content = self.text_area.get("1.0", "end-1c")  # Получаем текст из текстового поля
        print("Содержимое текстового поля:")
        print(text_content)
        return text_content
    
    def _handle_click(self):
        if self.on_click_callback:
            self.on_click_callback()
# synced: 2025-10-05T17:23:16.944175
# synced: 2025-10-05T17:23:19.876782
# synced: 2025-10-05T17:23:22.755231
# synced: 2025-10-05T17:23:25.479440
# synced: 2025-10-05T17:23:28.215354
# synced: 2025-10-05T17:23:31.170840
# synced: 2025-10-05T17:23:34.034286
# synced: 2025-10-05T17:23:36.766257
# synced: 2025-10-05T17:23:39.593767
# synced: 2025-10-05T17:23:42.249712
# synced: 2025-10-05T17:23:44.989248
# synced: 2025-10-05T17:23:47.891763
# synced: 2025-10-05T17:23:50.633714
# synced: 2025-10-05T17:23:53.445357
# synced: 2025-10-05T17:23:56.275893
# synced: 2025-10-05T17:23:59.058486
# synced: 2025-10-05T17:24:01.842921
# synced: 2025-10-05T17:24:04.660527
# synced: 2025-10-05T17:24:08.110145
# synced: 2025-10-05T17:24:10.739472
# synced: 2025-10-05T17:24:13.604232
# synced: 2025-10-05T17:24:16.388337
# synced: 2025-10-05T17:24:19.258604
# synced: 2025-10-05T17:24:29.633253
# synced: 2025-10-05T17:24:32.123471
# synced: 2025-10-05T17:24:34.347209
# synced: 2025-10-05T17:24:36.501370
# synced: 2025-10-05T17:24:38.653031
# synced: 2025-10-05T17:24:40.748651
# synced: 2025-10-05T17:24:42.893709
# synced: 2025-10-05T17:24:45.033412
# synced: 2025-10-05T17:24:47.300350
# synced: 2025-10-05T17:24:49.459093
# synced: 2025-10-05T17:24:51.565569
# synced: 2025-10-05T17:24:53.659545
# synced: 2025-10-05T17:24:55.881227
# synced: 2025-10-05T17:24:58.010396
# synced: 2025-10-05T17:25:00.238395
# synced: 2025-10-05T17:25:02.469364
# synced: 2025-10-05T17:25:04.573637
# synced: 2025-10-05T17:25:06.787570
# synced: 2025-10-05T17:25:09.040866
# synced: 2025-10-05T17:25:11.190228
# synced: 2025-10-05T17:25:13.472026
# synced: 2025-10-05T17:25:15.665506
# synced: 2025-10-05T17:25:17.906355
# synced: 2025-10-05T17:25:20.135380
# synced: 2025-10-05T17:25:22.348321
# synced: 2025-10-05T17:25:24.525111
# synced: 2025-10-05T17:25:26.753073
# synced: 2025-10-05T17:25:28.932400
# synced: 2025-10-05T17:25:31.180000
# synced: 2025-10-05T17:25:33.416443
# synced: 2025-10-05T17:25:35.600381
# synced: 2025-10-05T17:25:37.846423
# synced: 2025-10-05T17:25:40.093827
# synced: 2025-10-05T17:25:42.349231
# synced: 2025-10-05T17:25:44.549080
# synced: 2025-10-05T17:25:46.734106
# synced: 2025-10-05T17:25:48.926284
# synced: 2025-10-05T17:25:51.145379
# synced: 2025-10-05T17:25:53.351874
# synced: 2025-10-05T17:25:55.531733
# synced: 2025-10-05T17:25:57.734667
# synced: 2025-10-05T17:25:59.968665
# synced: 2025-10-05T17:26:02.151750
# synced: 2025-10-05T17:26:04.358350
# synced: 2025-10-05T17:26:06.637891
# synced: 2025-10-05T17:26:08.902186
# synced: 2025-10-05T17:26:11.142254
# synced: 2025-10-05T17:26:13.390452
# synced: 2025-10-05T17:26:15.621881
# synced: 2025-10-05T17:26:17.911384
# synced: 2025-10-05T17:26:20.177385
# synced: 2025-10-10T17:50:44.566959
# synced: 2025-10-10T17:50:48.358922
# synced: 2025-10-10T17:50:50.587784
# synced: 2025-10-10T17:50:52.750830
# synced: 2025-10-10T17:50:54.987932
# synced: 2025-10-10T17:50:57.745676
# synced: 2025-10-10T17:50:59.853078
# synced: 2025-10-10T17:51:02.010743
# synced: 2025-10-10T17:51:04.194841
# synced: 2025-10-10T17:51:06.347057
# synced: 2025-10-10T17:51:08.471986
# synced: 2025-10-10T17:51:10.700350
# synced: 2025-10-10T17:51:12.860927
# synced: 2025-10-10T17:51:14.991652
# synced: 2025-10-10T17:51:17.133247
# synced: 2025-10-10T17:51:19.627577
# synced: 2025-10-10T17:51:21.785470
# synced: 2025-10-10T17:51:24.150120
# synced: 2025-10-10T17:51:26.497545
# synced: 2025-10-10T17:51:29.103280
# synced: 2025-10-10T17:51:31.295381
# synced: 2025-10-10T17:51:33.414814
# synced: 2025-10-10T17:51:35.549578
# synced: 2025-10-10T17:51:38.104297
# synced: 2025-10-10T17:51:40.698882
# synced: 2025-10-10T17:51:43.253665
# synced: 2025-10-10T17:51:45.408144
# synced: 2025-10-10T17:51:47.536615
# synced: 2025-10-10T17:51:49.703653
# synced: 2025-10-10T17:51:51.847003
# synced: 2025-10-10T17:51:54.051978
# synced: 2025-10-10T17:51:56.180278
# synced: 2025-10-10T17:51:58.382998
# synced: 2025-10-10T17:52:00.638569
# synced: 2025-10-10T17:52:02.846488
# synced: 2025-10-10T17:52:05.081309
# synced: 2025-10-10T17:52:07.239269
# synced: 2025-10-10T17:52:09.402069
# synced: 2025-10-10T17:52:11.652401
# synced: 2025-10-10T17:52:13.864860
# synced: 2025-10-10T17:52:16.074770
# synced: 2025-10-10T17:52:18.357394
# synced: 2025-10-10T17:52:20.727830
# synced: 2025-10-10T17:52:22.821982
# synced: 2025-10-10T17:52:24.912116
# synced: 2025-10-10T17:52:27.022976
# synced: 2025-10-10T17:52:29.178120
# synced: 2025-10-10T17:52:31.584585
# synced: 2025-10-10T17:52:33.712422
# synced: 2025-10-10T17:52:35.883691
# synced: 2025-10-10T17:52:37.994459
# synced: 2025-10-10T17:52:40.041286
# synced: 2025-10-10T17:52:42.421715
# synced: 2025-10-10T17:52:44.569948
# synced: 2025-10-10T17:52:46.774750
# synced: 2025-10-10T17:52:48.957906
# synced: 2025-10-10T17:52:51.111056
# synced: 2025-10-10T17:52:53.306682
# synced: 2025-10-10T17:52:55.457060
# synced: 2025-10-10T17:52:57.536914
# synced: 2025-10-10T17:52:59.633334
# synced: 2025-10-10T17:53:01.705220
# synced: 2025-10-10T17:53:03.889976
# synced: 2025-10-10T17:53:06.181864
# synced: 2025-10-10T17:53:08.322190
# synced: 2025-10-10T17:53:10.511818
# synced: 2025-10-10T17:53:12.807892
# synced: 2025-10-10T17:53:14.872299
# synced: 2025-10-10T17:53:17.164099
# synced: 2025-10-10T17:53:19.303498
# synced: 2025-10-10T17:53:21.521185
# synced: 2025-10-10T17:53:23.716378
# synced: 2025-10-10T17:53:25.774988
# synced: 2025-10-10T17:53:27.955526
# synced: 2025-10-10T17:53:30.094626
# synced: 2025-10-10T17:53:32.248630
# synced: 2025-10-10T17:53:34.381069
# synced: 2025-10-10T17:53:36.476502
# synced: 2025-10-10T17:53:38.902363
# synced: 2025-10-10T17:53:41.102657
# synced: 2025-10-10T17:53:43.283343
# synced: 2025-10-10T17:53:45.349857
# synced: 2025-10-10T17:53:47.504330
# synced: 2025-10-10T17:53:49.555763
# synced: 2025-10-10T17:53:51.829904
# synced: 2025-10-10T17:53:54.030122
# synced: 2025-10-10T17:53:56.377709
# synced: 2025-10-10T17:53:58.541525
# synced: 2025-10-10T17:54:00.697730
# synced: 2025-10-10T17:54:02.871255
# synced: 2025-10-10T17:54:04.963297
# synced: 2025-10-10T17:54:07.069540
# synced: 2025-10-10T17:54:09.185459
# synced: 2025-10-10T17:54:11.241460
# synced: 2025-10-10T17:54:13.274666
# synced: 2025-10-10T17:54:15.895655
# synced: 2025-10-10T17:54:17.974979
# synced: 2025-10-10T17:54:20.069505
# synced: 2025-10-10T17:54:22.195509
# synced: 2025-10-10T17:54:24.382017
# synced: 2025-10-10T17:54:26.441194
# synced: 2025-10-10T17:54:28.542998
# synced: 2025-10-10T17:54:30.658082
# synced: 2025-10-10T17:54:32.832765
# synced: 2025-10-10T17:54:35.052450
# synced: 2025-10-10T17:54:37.211397
# synced: 2025-10-10T17:54:39.350897
# synced: 2025-10-10T17:54:41.517389
# synced: 2025-10-10T17:54:43.696761
# synced: 2025-10-10T17:54:45.850131
# synced: 2025-10-10T17:54:47.987658
# synced: 2025-10-10T17:54:50.207835
# synced: 2025-10-10T17:54:52.329601
# synced: 2025-10-10T17:54:54.499529
# synced: 2025-10-10T17:54:56.690632
# synced: 2025-10-10T17:54:59.079670
# synced: 2025-10-10T17:55:01.333806
# synced: 2025-10-10T17:55:03.466074
# synced: 2025-10-10T17:55:33.296795
# synced: 2025-10-10T17:55:35.492713
# synced: 2025-10-10T17:55:37.608275
# synced: 2025-10-10T17:55:39.801678
# synced: 2025-10-10T17:55:41.923218
# synced: 2025-10-10T17:55:44.111119
# synced: 2025-10-10T17:55:46.280835
# synced: 2025-10-10T17:55:48.749909
# synced: 2025-10-10T17:55:51.086463
# synced: 2025-10-10T17:55:53.201368
# synced: 2025-10-10T17:55:55.475988