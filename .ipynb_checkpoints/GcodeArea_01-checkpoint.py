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