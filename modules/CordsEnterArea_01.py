# Исходный код
import tkinter as tk
from tkinter import ttk

class CordsEnterArea(tk.Frame):
    def __init__(self, master=None, on_click_callback=None, **kwargs):
        # if not 'borderwidth' in kwargs: kwargs['borderwidth'] = 2
        # if not 'relief' in kwargs: kwargs['relief'] = "groove"

        super().__init__(master, **kwargs)
        self.master = master
        self.on_click_callback = on_click_callback
        self.text_areas = [None, None, None, None]
        self.data = [0.0, 0.0, 0.0, 0.0]

        # Настройка адаптивного размера для текстового поля
        # self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(5, weight=1)
        self.grid_columnconfigure(7, weight=1)

        label_1 = tk.Label(self, text="X", anchor=tk.CENTER)
        label_1.grid(row=0, column=0, sticky="nsw", pady=2, padx=2)
        label_2 = tk.Label(self, text="Y", anchor=tk.CENTER)
        label_2.grid(row=0, column=2, sticky="nsw", pady=2, padx=2)
        label_3 = tk.Label(self, text="Z", anchor=tk.CENTER)
        label_3.grid(row=0, column=4, sticky="nsw", pady=2, padx=2)
        label_4 = tk.Label(self, text="E", anchor=tk.CENTER)
        label_4.grid(row=0, column=6, sticky="nsw", pady=2, padx=2)
        
        self.text_areas[0] = tk.Entry(self, wrap=None, width=8)
        self.text_areas[0].grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        self.text_areas[1] = tk.Entry(self, wrap=None, width=8)
        self.text_areas[1].grid(row=0, column=3, sticky="nsew", padx=0, pady=0)
        self.text_areas[2] = tk.Entry(self, wrap=None, width=8)
        self.text_areas[2].grid(row=0, column=5, sticky="nsew", padx=0, pady=0)
        self.text_areas[3] = tk.Entry(self, wrap=None, width=8)
        self.text_areas[3].grid(row=0, column=7, sticky="nsew", padx=0, pady=0)

        # Привязка событий
        for n, widget in enumerate(self.text_areas):
            widget.bind("<FocusOut>", lambda e, widget=widget, n=n: self._handle_click(e, widget, n))  # Уход из поля
            widget.bind("<Return>", lambda e, widget=widget, n=n: self._handle_click(e, widget, n))  # Нажатие Enter
            widget.bind("<Key>", lambda e, widget=widget: self.validate_input(e, widget))
    
    def validate_input(self, event, widget):
        # Разрешаем только цифры, десятичную точку и некоторые управляющие клавиши
        allowed_keys = {
            "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
            "-",
            ".",  # Десятичная точка
            "\x08",  # Backspace
            "\x7f",  # Delete
            "\r",  # Enter
            "\t",  # Tab
            "\x1b"  # Escape
        }
        
        # Получаем символ, который был нажат
        char = event.char
        
        # Если символ не в списке разрешенных, игнорируем его
        if char and char not in allowed_keys:
            return "break"  # Блокируем ввод недопустимого символа
    
        # Дополнительная проверка: разрешаем только одну десятичную точку
        if char == "." and "." in widget.get():   #"1.0", tk.END):
            return "break"  # Блокируем вторую точку

        if char == "-" and widget.index(tk.INSERT) != 0:
            return "break"

    def get_data(self):
        return self.data

    def set_data(self, data):
        self.data = data
        for i, widget in enumerate(self.text_areas):
            widget.delete(0, tk.END)  # Очистка поля
            widget.insert(0, str(data[i]))  # Вставка нового текста
            # widget.set(str(data[i]))        
    
    def _handle_click(self, event, widget, widget_N):
        _text = widget.get()
        _num = self.data[widget_N]
        try:
            _num = float(_text)  # Преобразование в целое число
            self.data[widget_N] = _num
        except ValueError:
            pass
        
        if self.on_click_callback:
            self.on_click_callback()

    def _keyboard_dissable(self, on_off):
        for area in self.text_areas:
            if on_off:
                area.config(state="disabled")  # Отключаем
            else:
                area.config(state="normal")

# synced: 2025-10-05T17:23:16.956438
# synced: 2025-10-05T17:23:19.880865
# synced: 2025-10-05T17:23:22.761201
# synced: 2025-10-05T17:23:25.483716
# synced: 2025-10-05T17:23:28.223296
# synced: 2025-10-05T17:23:31.176072
# synced: 2025-10-05T17:23:34.038593
# synced: 2025-10-05T17:23:36.770992
# synced: 2025-10-05T17:23:39.602200
# synced: 2025-10-05T17:23:42.257738
# synced: 2025-10-05T17:23:44.994385
# synced: 2025-10-05T17:23:47.899993
# synced: 2025-10-05T17:23:50.640266
# synced: 2025-10-05T17:23:53.450241
# synced: 2025-10-05T17:23:56.280895
# synced: 2025-10-05T17:23:59.063486
# synced: 2025-10-05T17:24:01.846923
# synced: 2025-10-05T17:24:04.668584
# synced: 2025-10-05T17:24:08.118981
# synced: 2025-10-05T17:24:10.746835
# synced: 2025-10-05T17:24:13.610409
# synced: 2025-10-05T17:24:16.396869
# synced: 2025-10-05T17:24:19.268399
# synced: 2025-10-05T17:24:29.635714
# synced: 2025-10-05T17:24:32.125472
# synced: 2025-10-05T17:24:34.347209
# synced: 2025-10-05T17:24:36.505372
# synced: 2025-10-05T17:24:38.655044
# synced: 2025-10-05T17:24:40.750826
# synced: 2025-10-05T17:24:42.895708
# synced: 2025-10-05T17:24:45.037142
# synced: 2025-10-05T17:24:47.302354
# synced: 2025-10-05T17:24:49.462085
# synced: 2025-10-05T17:24:51.569582
# synced: 2025-10-05T17:24:53.663546
# synced: 2025-10-05T17:24:55.884605
# synced: 2025-10-05T17:24:58.014620
# synced: 2025-10-05T17:25:00.240395
# synced: 2025-10-05T17:25:02.472367
# synced: 2025-10-05T17:25:04.575770
# synced: 2025-10-05T17:25:06.791475
# synced: 2025-10-05T17:25:09.042927
# synced: 2025-10-05T17:25:11.193687
# synced: 2025-10-05T17:25:13.475339
# synced: 2025-10-05T17:25:15.669506
# synced: 2025-10-05T17:25:17.908616
# synced: 2025-10-05T17:25:20.138464
# synced: 2025-10-05T17:25:22.350792
# synced: 2025-10-05T17:25:24.527480
# synced: 2025-10-05T17:25:26.757074
# synced: 2025-10-05T17:25:28.935913
# synced: 2025-10-05T17:25:31.184462
# synced: 2025-10-05T17:25:33.420769
# synced: 2025-10-05T17:25:35.603384
# synced: 2025-10-05T17:25:37.849430
# synced: 2025-10-05T17:25:40.096832
# synced: 2025-10-05T17:25:42.353313
# synced: 2025-10-05T17:25:44.553233
# synced: 2025-10-05T17:25:46.737238
# synced: 2025-10-05T17:25:48.930297
# synced: 2025-10-05T17:25:51.148379
# synced: 2025-10-05T17:25:53.356022
# synced: 2025-10-05T17:25:55.533745
# synced: 2025-10-05T17:25:57.735666
# synced: 2025-10-05T17:25:59.971993
# synced: 2025-10-05T17:26:02.151750
# synced: 2025-10-05T17:26:04.361352
# synced: 2025-10-05T17:26:06.642006
# synced: 2025-10-05T17:26:08.906190
# synced: 2025-10-05T17:26:11.146568
# synced: 2025-10-05T17:26:13.390452
# synced: 2025-10-05T17:26:15.624819
# synced: 2025-10-05T17:26:17.915389
# synced: 2025-10-05T17:26:20.181384
# synced: 2025-10-10T17:50:44.573961
# synced: 2025-10-10T17:50:48.360924
# synced: 2025-10-10T17:50:50.589783
# synced: 2025-10-10T17:50:52.752907
# synced: 2025-10-10T17:50:55.001932
# synced: 2025-10-10T17:50:57.747674
# synced: 2025-10-10T17:50:59.854085
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
# synced: 2025-10-10T17:51:26.498548
# synced: 2025-10-10T17:51:29.105280
# synced: 2025-10-10T17:51:31.297474
# synced: 2025-10-10T17:51:33.415814
# synced: 2025-10-10T17:51:35.551576
# synced: 2025-10-10T17:51:38.106299
# synced: 2025-10-10T17:51:40.700881
# synced: 2025-10-10T17:51:43.255666
# synced: 2025-10-10T17:51:45.410144
# synced: 2025-10-10T17:51:47.538615
# synced: 2025-10-10T17:51:49.705650
# synced: 2025-10-10T17:51:51.848999
# synced: 2025-10-10T17:51:54.054078
# synced: 2025-10-10T17:51:56.182271
# synced: 2025-10-10T17:51:58.385992
# synced: 2025-10-10T17:52:00.640570
# synced: 2025-10-10T17:52:02.848576
# synced: 2025-10-10T17:52:05.083373
# synced: 2025-10-10T17:52:07.241344
# synced: 2025-10-10T17:52:09.403069
# synced: 2025-10-10T17:52:11.654399
# synced: 2025-10-10T17:52:13.866851
# synced: 2025-10-10T17:52:16.076768
# synced: 2025-10-10T17:52:18.359393
# synced: 2025-10-10T17:52:20.729829
# synced: 2025-10-10T17:52:22.823048
# synced: 2025-10-10T17:52:24.914114
# synced: 2025-10-10T17:52:27.024974
# synced: 2025-10-10T17:52:29.180119
# synced: 2025-10-10T17:52:31.586586
# synced: 2025-10-10T17:52:33.714479
# synced: 2025-10-10T17:52:35.884691
# synced: 2025-10-10T17:52:37.996459
# synced: 2025-10-10T17:52:40.043284
# synced: 2025-10-10T17:52:42.422711
# synced: 2025-10-10T17:52:44.572025
# synced: 2025-10-10T17:52:46.777852
# synced: 2025-10-10T17:52:48.959907
# synced: 2025-10-10T17:52:51.113058
# synced: 2025-10-10T17:52:53.308681
# synced: 2025-10-10T17:52:55.459059
# synced: 2025-10-10T17:52:57.538914