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

# synced: 2025-10-05T17:23:16.972274
# synced: 2025-10-05T17:23:19.889446
# synced: 2025-10-05T17:23:22.769311
# synced: 2025-10-05T17:23:25.490206
# synced: 2025-10-05T17:23:28.232813
# synced: 2025-10-05T17:23:31.183963
# synced: 2025-10-05T17:23:34.047443
# synced: 2025-10-05T17:23:36.782418
# synced: 2025-10-05T17:23:39.613775
# synced: 2025-10-05T17:23:42.269809
# synced: 2025-10-05T17:23:45.010931
# synced: 2025-10-05T17:23:47.914960
# synced: 2025-10-05T17:23:50.651042
# synced: 2025-10-05T17:23:53.457252
# synced: 2025-10-05T17:23:56.289117
# synced: 2025-10-05T17:23:59.071487
# synced: 2025-10-05T17:24:01.855923
# synced: 2025-10-05T17:24:04.681370
# synced: 2025-10-05T17:24:08.132171
# synced: 2025-10-05T17:24:10.759827
# synced: 2025-10-05T17:24:13.623409
# synced: 2025-10-05T17:24:16.410541
# synced: 2025-10-05T17:24:19.275710
# synced: 2025-10-05T17:24:29.638124
# synced: 2025-10-05T17:24:32.128472
# synced: 2025-10-05T17:24:34.351706
# synced: 2025-10-05T17:24:36.510664
# synced: 2025-10-05T17:24:38.662616
# synced: 2025-10-05T17:24:40.755453
# synced: 2025-10-05T17:24:42.900244
# synced: 2025-10-05T17:24:45.042659
# synced: 2025-10-05T17:24:47.306349
# synced: 2025-10-05T17:24:49.466084
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
# synced: 2025-10-05T17:25:13.481340
# synced: 2025-10-05T17:25:15.674558
# synced: 2025-10-05T17:25:17.912611
# synced: 2025-10-05T17:25:20.143468
# synced: 2025-10-05T17:25:22.355470
# synced: 2025-10-05T17:25:24.533001
# synced: 2025-10-05T17:25:26.763084
# synced: 2025-10-05T17:25:28.939913
# synced: 2025-10-05T17:25:31.188784
# synced: 2025-10-05T17:25:33.425109
# synced: 2025-10-05T17:25:35.607212
# synced: 2025-10-05T17:25:37.854435
# synced: 2025-10-05T17:25:40.101828
# synced: 2025-10-05T17:25:42.358315
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
# synced: 2025-10-05T17:26:06.647031
# synced: 2025-10-05T17:26:08.911383
# synced: 2025-10-05T17:26:11.150900
# synced: 2025-10-05T17:26:13.398746