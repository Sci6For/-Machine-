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

# synced: 2025-10-05T17:23:16.967849
# synced: 2025-10-05T17:23:19.889446
# synced: 2025-10-05T17:23:22.765273
# synced: 2025-10-05T17:23:25.490206
# synced: 2025-10-05T17:23:28.230769
# synced: 2025-10-05T17:23:31.182628
# synced: 2025-10-05T17:23:34.046444
# synced: 2025-10-05T17:23:36.779337
# synced: 2025-10-05T17:23:39.612778
# synced: 2025-10-05T17:23:42.266350
# synced: 2025-10-05T17:23:45.009183
# synced: 2025-10-05T17:23:47.912957
# synced: 2025-10-05T17:23:50.648899
# synced: 2025-10-05T17:23:53.456249
# synced: 2025-10-05T17:23:56.286971
# synced: 2025-10-05T17:23:59.070487
# synced: 2025-10-05T17:24:01.853920
# synced: 2025-10-05T17:24:04.676935
# synced: 2025-10-05T17:24:08.130129
# synced: 2025-10-05T17:24:10.757680
# synced: 2025-10-05T17:24:13.621411
# synced: 2025-10-05T17:24:16.408479
# synced: 2025-10-05T17:24:19.275710
# synced: 2025-10-05T17:24:29.638124
# synced: 2025-10-05T17:24:32.128472
# synced: 2025-10-05T17:24:34.351706
# synced: 2025-10-05T17:24:36.509667
# synced: 2025-10-05T17:24:38.662616
# synced: 2025-10-05T17:24:40.754440
# synced: 2025-10-05T17:24:42.900244
# synced: 2025-10-05T17:24:45.041611
# synced: 2025-10-05T17:24:47.305353
# synced: 2025-10-05T17:24:49.465084
# synced: 2025-10-05T17:24:51.574168
# synced: 2025-10-05T17:24:53.666541
# synced: 2025-10-05T17:24:55.889055
# synced: 2025-10-05T17:24:58.018871
# synced: 2025-10-05T17:25:00.243747
# synced: 2025-10-05T17:25:02.475365
# synced: 2025-10-05T17:25:04.578981
# synced: 2025-10-05T17:25:06.795198
# synced: 2025-10-05T17:25:09.046714
# synced: 2025-10-05T17:25:11.198114
# synced: 2025-10-05T17:25:13.480339
# synced: 2025-10-05T17:25:15.674558
# synced: 2025-10-05T17:25:17.912611
# synced: 2025-10-05T17:25:20.143468
# synced: 2025-10-05T17:25:22.355470
# synced: 2025-10-05T17:25:24.533001
# synced: 2025-10-05T17:25:26.762079
# synced: 2025-10-05T17:25:28.939913
# synced: 2025-10-05T17:25:31.188784
# synced: 2025-10-05T17:25:33.423305
# synced: 2025-10-05T17:25:35.607212
# synced: 2025-10-05T17:25:37.854435
# synced: 2025-10-05T17:25:40.101828
# synced: 2025-10-05T17:25:42.357314
# synced: 2025-10-05T17:25:44.557625
# synced: 2025-10-05T17:25:46.742939
# synced: 2025-10-05T17:25:48.934974
# synced: 2025-10-05T17:25:51.153004
# synced: 2025-10-05T17:25:53.360456
# synced: 2025-10-05T17:25:55.540201
# synced: 2025-10-05T17:25:57.742208
# synced: 2025-10-05T17:25:59.977340
# synced: 2025-10-05T17:26:02.157801
# synced: 2025-10-05T17:26:04.366349
# synced: 2025-10-05T17:26:06.646031
# synced: 2025-10-05T17:26:08.911383
# synced: 2025-10-05T17:26:11.150900
# synced: 2025-10-05T17:26:13.398746
# synced: 2025-10-05T17:26:15.629161
# synced: 2025-10-05T17:26:17.919393
# synced: 2025-10-05T17:26:20.186899
# synced: 2025-10-10T17:50:44.576958
# synced: 2025-10-10T17:50:48.363922
# synced: 2025-10-10T17:50:50.591785
# synced: 2025-10-10T17:50:52.754905
# synced: 2025-10-10T17:50:55.015938
# synced: 2025-10-10T17:50:57.749673
# synced: 2025-10-10T17:50:59.857083
# synced: 2025-10-10T17:51:02.014796
# synced: 2025-10-10T17:51:04.199924
# synced: 2025-10-10T17:51:06.351121
# synced: 2025-10-10T17:51:08.476066
# synced: 2025-10-10T17:51:10.705350
# synced: 2025-10-10T17:51:12.864986
# synced: 2025-10-10T17:51:14.995718
# synced: 2025-10-10T17:51:17.137247
# synced: 2025-10-10T17:51:19.631681
# synced: 2025-10-10T17:51:21.788521
# synced: 2025-10-10T17:51:24.154184
# synced: 2025-10-10T17:51:26.501617
# synced: 2025-10-10T17:51:29.108284
# synced: 2025-10-10T17:51:31.299474
# synced: 2025-10-10T17:51:33.418813
# synced: 2025-10-10T17:51:35.554575
# synced: 2025-10-10T17:51:38.108299
# synced: 2025-10-10T17:51:40.703884
# synced: 2025-10-10T17:51:43.258670
# synced: 2025-10-10T17:51:45.413232
# synced: 2025-10-10T17:51:47.541615
# synced: 2025-10-10T17:51:49.708724
# synced: 2025-10-10T17:51:51.851001
# synced: 2025-10-10T17:51:54.056076
# synced: 2025-10-10T17:51:56.185278
# synced: 2025-10-10T17:51:58.390993
# synced: 2025-10-10T17:52:00.643572
# synced: 2025-10-10T17:52:02.851580
# synced: 2025-10-10T17:52:05.085372
# synced: 2025-10-10T17:52:07.243345
# synced: 2025-10-10T17:52:09.405132
# synced: 2025-10-10T17:52:11.656398
# synced: 2025-10-10T17:52:13.869918
# synced: 2025-10-10T17:52:16.078770
# synced: 2025-10-10T17:52:18.361394
# synced: 2025-10-10T17:52:20.731831
# synced: 2025-10-10T17:52:22.826046
# synced: 2025-10-10T17:52:24.916115
# synced: 2025-10-10T17:52:27.028015
# synced: 2025-10-10T17:52:29.183199
# synced: 2025-10-10T17:52:31.588659
# synced: 2025-10-10T17:52:33.715984
# synced: 2025-10-10T17:52:35.887691
# synced: 2025-10-10T17:52:37.998457
# synced: 2025-10-10T17:52:40.045795
# synced: 2025-10-10T17:52:42.425711
# synced: 2025-10-10T17:52:44.574026
# synced: 2025-10-10T17:52:46.779851
# synced: 2025-10-10T17:52:48.962411
# synced: 2025-10-10T17:52:51.115058
# synced: 2025-10-10T17:52:53.310741
# synced: 2025-10-10T17:52:55.462063
# synced: 2025-10-10T17:52:57.540914
# synced: 2025-10-10T17:52:59.637399
# synced: 2025-10-10T17:53:01.712328
# synced: 2025-10-10T17:53:03.894033
# synced: 2025-10-10T17:53:06.187058
# synced: 2025-10-10T17:53:08.326190
# synced: 2025-10-10T17:53:10.516820
# synced: 2025-10-10T17:53:12.811892
# synced: 2025-10-10T17:53:14.876367
# synced: 2025-10-10T17:53:17.168170
# synced: 2025-10-10T17:53:19.308559
# synced: 2025-10-10T17:53:21.525184
# synced: 2025-10-10T17:53:23.720377
# synced: 2025-10-10T17:53:25.778060
# synced: 2025-10-10T17:53:27.960526
# synced: 2025-10-10T17:53:30.098626
# synced: 2025-10-10T17:53:32.253629
# synced: 2025-10-10T17:53:34.386129
# synced: 2025-10-10T17:53:36.480598
# synced: 2025-10-10T17:53:38.906363
# synced: 2025-10-10T17:53:41.106720
# synced: 2025-10-10T17:53:43.287343
# synced: 2025-10-10T17:53:45.354862
# synced: 2025-10-10T17:53:47.508331
# synced: 2025-10-10T17:53:49.559763
# synced: 2025-10-10T17:53:51.837995