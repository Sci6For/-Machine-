# Исходный код
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

    def _keyboard_dissable(self, on_off):
        if on_off:
            self.text_area.config(state="disabled")  # Отключаем
        else:
            self.text_area.config(state="normal")

    def add_string(self, string):
        self.text_area.insert("end", string)

# synced: 2025-10-05T17:23:16.958439
# synced: 2025-10-05T17:23:19.882728
# synced: 2025-10-05T17:23:22.761201
# synced: 2025-10-05T17:23:25.483716
# synced: 2025-10-05T17:23:28.225383
# synced: 2025-10-05T17:23:31.177286
# synced: 2025-10-05T17:23:34.039691
# synced: 2025-10-05T17:23:36.773263
# synced: 2025-10-05T17:23:39.603546
# synced: 2025-10-05T17:23:42.258588
# synced: 2025-10-05T17:23:44.998223
# synced: 2025-10-05T17:23:47.904455
# synced: 2025-10-05T17:23:50.642500
# synced: 2025-10-05T17:23:53.451251
# synced: 2025-10-05T17:23:56.281893
# synced: 2025-10-05T17:23:59.064486
# synced: 2025-10-05T17:24:01.847920
# synced: 2025-10-05T17:24:04.668584
# synced: 2025-10-05T17:24:08.120915
# synced: 2025-10-05T17:24:10.749128
# synced: 2025-10-05T17:24:13.612409
# synced: 2025-10-05T17:24:16.400018
# synced: 2025-10-05T17:24:19.268399
# synced: 2025-10-05T17:24:29.635714
# synced: 2025-10-05T17:24:32.126472
# synced: 2025-10-05T17:24:34.347209
# synced: 2025-10-05T17:24:36.505372
# synced: 2025-10-05T17:24:38.657583
# synced: 2025-10-05T17:24:40.752002
# synced: 2025-10-05T17:24:42.896800
# synced: 2025-10-05T17:24:45.037142
# synced: 2025-10-05T17:24:47.303350
# synced: 2025-10-05T17:24:49.462085
# synced: 2025-10-05T17:24:51.569582
# synced: 2025-10-05T17:24:53.663546
# synced: 2025-10-05T17:24:55.884605
# synced: 2025-10-05T17:24:58.014620
# synced: 2025-10-05T17:25:00.240395
# synced: 2025-10-05T17:25:02.472367
# synced: 2025-10-05T17:25:04.575770
# synced: 2025-10-05T17:25:06.791475
# synced: 2025-10-05T17:25:09.044388
# synced: 2025-10-05T17:25:11.193687
# synced: 2025-10-05T17:25:13.476339
# synced: 2025-10-05T17:25:15.670544
# synced: 2025-10-05T17:25:17.908616
# synced: 2025-10-05T17:25:20.139464
# synced: 2025-10-05T17:25:22.350792
# synced: 2025-10-05T17:25:24.528957
# synced: 2025-10-05T17:25:26.758073
# synced: 2025-10-05T17:25:28.935913
# synced: 2025-10-05T17:25:31.184462
# synced: 2025-10-05T17:25:33.420769
# synced: 2025-10-05T17:25:35.604382
# synced: 2025-10-05T17:25:37.850424
# synced: 2025-10-05T17:25:40.097826
# synced: 2025-10-05T17:25:42.353313
# synced: 2025-10-05T17:25:44.553233
# synced: 2025-10-05T17:25:46.738323
# synced: 2025-10-05T17:25:48.930297
# synced: 2025-10-05T17:25:51.148379
# synced: 2025-10-05T17:25:53.356022
# synced: 2025-10-05T17:25:55.533745
# synced: 2025-10-05T17:25:57.735666
# synced: 2025-10-05T17:25:59.971993
# synced: 2025-10-05T17:26:02.151750
# synced: 2025-10-05T17:26:04.362354
# synced: 2025-10-05T17:26:06.642006
# synced: 2025-10-05T17:26:08.907189
# synced: 2025-10-05T17:26:11.146568
# synced: 2025-10-05T17:26:13.394682
# synced: 2025-10-05T17:26:15.624819
# synced: 2025-10-05T17:26:17.915389
# synced: 2025-10-05T17:26:20.182389
# synced: 2025-10-10T17:50:44.573961
# synced: 2025-10-10T17:50:48.360924
# synced: 2025-10-10T17:50:50.589783
# synced: 2025-10-10T17:50:52.752907
# synced: 2025-10-10T17:50:55.005931
# synced: 2025-10-10T17:50:57.747674
# synced: 2025-10-10T17:50:59.855084
# synced: 2025-10-10T17:51:02.012796
# synced: 2025-10-10T17:51:04.197927
# synced: 2025-10-10T17:51:06.349056
# synced: 2025-10-10T17:51:08.473990
# synced: 2025-10-10T17:51:10.702352
# synced: 2025-10-10T17:51:12.862925
# synced: 2025-10-10T17:51:14.993718
# synced: 2025-10-10T17:51:17.135246
# synced: 2025-10-10T17:51:19.629580
# synced: 2025-10-10T17:51:21.786472
# synced: 2025-10-10T17:51:24.152185
# synced: 2025-10-10T17:51:26.499549
# synced: 2025-10-10T17:51:29.105280
# synced: 2025-10-10T17:51:31.297474
# synced: 2025-10-10T17:51:33.416813
# synced: 2025-10-10T17:51:35.552576
# synced: 2025-10-10T17:51:38.106299
# synced: 2025-10-10T17:51:40.700881
# synced: 2025-10-10T17:51:43.255666
# synced: 2025-10-10T17:51:45.410144
# synced: 2025-10-10T17:51:47.539615
# synced: 2025-10-10T17:51:49.705650
# synced: 2025-10-10T17:51:51.848999
# synced: 2025-10-10T17:51:54.054078
# synced: 2025-10-10T17:51:56.182271
# synced: 2025-10-10T17:51:58.386993
# synced: 2025-10-10T17:52:00.640570
# synced: 2025-10-10T17:52:02.848576
# synced: 2025-10-10T17:52:05.083373
# synced: 2025-10-10T17:52:07.241344
# synced: 2025-10-10T17:52:09.403069
# synced: 2025-10-10T17:52:11.654399
# synced: 2025-10-10T17:52:13.867919
# synced: 2025-10-10T17:52:16.076768
# synced: 2025-10-10T17:52:18.359393
# synced: 2025-10-10T17:52:20.729829
# synced: 2025-10-10T17:52:22.823048
# synced: 2025-10-10T17:52:24.914114
# synced: 2025-10-10T17:52:27.024974
# synced: 2025-10-10T17:52:29.181121
# synced: 2025-10-10T17:52:31.586586
# synced: 2025-10-10T17:52:33.714479
# synced: 2025-10-10T17:52:35.885691
# synced: 2025-10-10T17:52:37.996459
# synced: 2025-10-10T17:52:40.043284
# synced: 2025-10-10T17:52:42.423712
# synced: 2025-10-10T17:52:44.572025
# synced: 2025-10-10T17:52:46.777852
# synced: 2025-10-10T17:52:48.959907
# synced: 2025-10-10T17:52:51.113058
# synced: 2025-10-10T17:52:53.308681
# synced: 2025-10-10T17:52:55.459059
# synced: 2025-10-10T17:52:57.538914
# synced: 2025-10-10T17:52:59.635400
# synced: 2025-10-10T17:53:01.708313
# synced: 2025-10-10T17:53:03.892034
# synced: 2025-10-10T17:53:06.184058
# synced: 2025-10-10T17:53:08.324190
# synced: 2025-10-10T17:53:10.513817
# synced: 2025-10-10T17:53:12.809892
# synced: 2025-10-10T17:53:14.874366
# synced: 2025-10-10T17:53:17.166171
# synced: 2025-10-10T17:53:19.306558
# synced: 2025-10-10T17:53:21.523184
# synced: 2025-10-10T17:53:23.719378
# synced: 2025-10-10T17:53:25.777059
# synced: 2025-10-10T17:53:27.958526
# synced: 2025-10-10T17:53:30.096625
# synced: 2025-10-10T17:53:32.251634
# synced: 2025-10-10T17:53:34.384066
# synced: 2025-10-10T17:53:36.478501
# synced: 2025-10-10T17:53:38.904364
# synced: 2025-10-10T17:53:41.104656
# synced: 2025-10-10T17:53:43.285343
# synced: 2025-10-10T17:53:45.351855
# synced: 2025-10-10T17:53:47.506332
# synced: 2025-10-10T17:53:49.557763
# synced: 2025-10-10T17:53:51.833994
# synced: 2025-10-10T17:53:54.034124