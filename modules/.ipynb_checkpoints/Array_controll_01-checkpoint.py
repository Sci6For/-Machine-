import tkinter as tk

class Array_controll(tk.Frame):
    def __init__(self, master=None, on_click_callback=None, **kwargs):
        if not 'borderwidth' in kwargs: kwargs['borderwidth'] = 2
        if not 'relief' in kwargs: kwargs['relief'] = "groove"

        self.e_step_K = kwargs.pop('k_e', 1)
        
        super().__init__(master, **kwargs)
        self.master = master
        self.on_click_callback = on_click_callback

        self.step = 5
        self._steps = (0.1, 0.5, 1, 2.5, 5, 10, 25, 50)

        self.listern_keybord_flag = False
        self.key_states = {}      # нужен для блокирования зависаний клавиатуры
        self.master.bind("<Key>", self.on_key_press)
        self.master.bind("<KeyRelease>", self.on_key_release)

        self._draw_widgets()
        
    def _draw_widgets(self):
        # Установка minsize для всех строк
        for row in range(9):
            self.rowconfigure(row, weight=1, minsize=15)

        # Установка minsize для всех столбцов
        for column in range(13):
            self.columnconfigure(column, weight=1, minsize=15)

        # self.columnconfigure(13, weight=1, minsize=20)
        
        xm_bt = tk.Button(self, text="X-", command=lambda : self._handle_click("x", -1))
        xm_bt.grid(row=3, column=0, columnspan=3, rowspan=3, padx=2, pady=2, sticky="nesw")
        
        xp_bt = tk.Button(self, text="X+", command=lambda : self._handle_click("x", 1))
        xp_bt.grid(row=3, column=6, columnspan=3, rowspan=3, padx=2, pady=2, sticky="nesw")
        
        yp_bt = tk.Button(self, text="Y+", command=lambda : self._handle_click("y", 1))
        yp_bt.grid(row=0, column=3, columnspan=3, rowspan=3, padx=2, pady=2, sticky="nesw")

        ym_bt = tk.Button(self, text="Y-", command=lambda : self._handle_click("y", -1))
        ym_bt.grid(row=6, column=3, columnspan=3, rowspan=3, padx=2, pady=2, sticky="nesw")

        zp_bt = tk.Button(self, text="Z+", command=lambda : self._handle_click("z", 1))
        zp_bt.grid(row=0, column=10, columnspan=3, rowspan=2, padx=2, pady=2, sticky="nesw")

        zm_bt = tk.Button(self, text="Z-", command=lambda : self._handle_click("z", -1))
        zm_bt.grid(row=2, column=10, columnspan=3, rowspan=2, padx=2, pady=2, sticky="nesw")
    
        em_bt = tk.Button(self, text="E-", command=lambda : self._handle_click("e", -1))
        em_bt.grid(row=7, column=10, columnspan=3, rowspan=2, padx=2, pady=2, sticky="nesw")
        
        ep_bt = tk.Button(self, text="E+", command=lambda : self._handle_click("e", 1))
        ep_bt.grid(row=5, column=10, columnspan=3, rowspan=2, padx=2, pady=2, sticky="nesw")

        self.label = tk.Label(self, text="0", font=("Arial", 7))
        self.label.grid(row=0, column=13, columnspan=1, rowspan=2, padx=2, pady=0, sticky="esw")

        # Создание вертикального слайдера (Scale)
        slider = tk.Scale(
            self,
            from_=0,          # Верхнее значение
            to=len(self._steps)-1,       # Нижнее значение (переворачиваем для вертикального слайдера)
            orient=tk.VERTICAL, # Ориентация слайдера
            # length=200,         # Длина слайдера
            sliderlength=20,    # Длина "бегунка"
            showvalue=False,    # Отключаем отображение значения возле движка
            command=self.on_slider_change  # Функция, вызываемая при изменении значения
        )
        slider.set(4)  # Устанавливаем начальное значение
        slider.grid(row=2, column=13, columnspan=1, rowspan=8, padx=2, pady=1, sticky="nesw")

    def on_key_press(self, event):
        """
        Обработчик события нажатия клавиши.
        :param event: Объект события, содержащий информацию о нажатой клавише.
        """
        if not self.listern_keybord_flag:
            return
        
        key = event.keysym  # Символ клавиши (например, "a", "Shift", "Return")
        if self.key_states.get(key, False):        # Если клавиша уже нажата, игнорируем автоповтор
            return
        self.key_states[key] = False        # Помечаем клавишу как нажатую
        char = event.char   # Символ, если клавиша генерирует текст (например, "a", "1")
        
        _move = {'x':0, 'y':0, 'z':0, 'e':0}
        if char in ('w', 'W', 'ц', 'Ц'):
            _move['y'] += self.step
        if char in ('s', 'S', 'ы', 'Ы'):
            _move['y'] -= self.step
        if char in ('d', 'D', 'в', 'В'):
            _move['x'] += self.step
        if char in ('a', 'A', 'ф', 'Ф'):
            _move['x'] -= self.step

        if key == 'Up':
            _move['z'] += self.step
        if key == 'Down':
            _move['z'] -= self.step
        if key == 'Left':
            _move['e'] += self.step * self.e_step_K
        if key == 'Right':
            _move['e'] -= self.step * self.e_step_K
        
        # print(_move)
        if self.on_click_callback:
            self.on_click_callback(**_move)

    def on_key_release(self, event):
        """
        Обработчик события отпускания клавиши.
        """
        key = event.keysym       # Символ клавиши (например, "a", "Shift", "Return")
        self.key_states[key] = False            # Помечаем клавишу как отпущенную
    
    def on_slider_change(self, value):
        value = int(value)
        self.step = self._steps[value]
        self.label.config(text=f"шаг:\n{self.step}")  
    
    def _handle_click(self, bt_id, _dir):
        if bt_id != 'e':
            out = {bt_id : _dir*self.step}
        else:
             out = {bt_id : _dir*self.step * self.e_step_K}
        # print(out)
        if self.on_click_callback:
            self.on_click_callback(**out)

    def get_step(self):
        return self.step

    def listern_keybord_mode(self, flag):
        self.listern_keybord_flag = flag
# synced: 2025-10-05T17:23:16.963435
# synced: 2025-10-05T17:23:19.885246
# synced: 2025-10-05T17:23:22.765273
# synced: 2025-10-05T17:23:25.490206
# synced: 2025-10-05T17:23:28.228579
# synced: 2025-10-05T17:23:31.182628
# synced: 2025-10-05T17:23:34.045443
# synced: 2025-10-05T17:23:36.779337
# synced: 2025-10-05T17:23:39.611775
# synced: 2025-10-05T17:23:42.266350
# synced: 2025-10-05T17:23:45.006564
# synced: 2025-10-05T17:23:47.908621
# synced: 2025-10-05T17:23:50.647722
# synced: 2025-10-05T17:23:53.455252
# synced: 2025-10-05T17:23:56.286971
# synced: 2025-10-05T17:23:59.069486
# synced: 2025-10-05T17:24:01.852923
# synced: 2025-10-05T17:24:04.676935
# synced: 2025-10-05T17:24:08.128822
# synced: 2025-10-05T17:24:10.755442
# synced: 2025-10-05T17:24:13.620409
# synced: 2025-10-05T17:24:16.407598
# synced: 2025-10-05T17:24:19.275710
# synced: 2025-10-05T17:24:29.636794
# synced: 2025-10-05T17:24:32.127472
# synced: 2025-10-05T17:24:34.351706
# synced: 2025-10-05T17:24:36.508663
# synced: 2025-10-05T17:24:38.659361
# synced: 2025-10-05T17:24:40.753011
# synced: 2025-10-05T17:24:42.898798
# synced: 2025-10-05T17:24:45.040596
# synced: 2025-10-05T17:24:47.304353
# synced: 2025-10-05T17:24:49.465084
# synced: 2025-10-05T17:24:51.573031
# synced: 2025-10-05T17:24:53.666541
# synced: 2025-10-05T17:24:55.887055
# synced: 2025-10-05T17:24:58.017069
# synced: 2025-10-05T17:25:00.242712
# synced: 2025-10-05T17:25:02.474367
# synced: 2025-10-05T17:25:04.577983
# synced: 2025-10-05T17:25:06.793772
# synced: 2025-10-05T17:25:09.045459
# synced: 2025-10-05T17:25:11.196082
# synced: 2025-10-05T17:25:13.479340
# synced: 2025-10-05T17:25:15.672554
# synced: 2025-10-05T17:25:17.910612
# synced: 2025-10-05T17:25:20.141461
# synced: 2025-10-05T17:25:22.353464
# synced: 2025-10-05T17:25:24.531777
# synced: 2025-10-05T17:25:26.760074
# synced: 2025-10-05T17:25:28.937932
# synced: 2025-10-05T17:25:31.184462
# synced: 2025-10-05T17:25:33.423305
# synced: 2025-10-05T17:25:35.607212
# synced: 2025-10-05T17:25:37.852423
# synced: 2025-10-05T17:25:40.099827
# synced: 2025-10-05T17:25:42.356313
# synced: 2025-10-05T17:25:44.557625
# synced: 2025-10-05T17:25:46.740937
# synced: 2025-10-05T17:25:48.932308
# synced: 2025-10-05T17:25:51.150380
# synced: 2025-10-05T17:25:53.358028
# synced: 2025-10-05T17:25:55.540201
# synced: 2025-10-05T17:25:57.739719
# synced: 2025-10-05T17:25:59.976341
# synced: 2025-10-05T17:26:02.157801
# synced: 2025-10-05T17:26:04.365350
# synced: 2025-10-05T17:26:06.645001
# synced: 2025-10-05T17:26:08.909188
# synced: 2025-10-05T17:26:11.150900
# synced: 2025-10-05T17:26:13.394682
# synced: 2025-10-05T17:26:15.629161
# synced: 2025-10-05T17:26:17.919393
# synced: 2025-10-05T17:26:20.185385
# synced: 2025-10-10T17:50:44.575958
# synced: 2025-10-10T17:50:48.362922
# synced: 2025-10-10T17:50:50.590784
# synced: 2025-10-10T17:50:52.754905
# synced: 2025-10-10T17:50:55.011931
# synced: 2025-10-10T17:50:57.748673
# synced: 2025-10-10T17:50:59.856085
# synced: 2025-10-10T17:51:02.013796
# synced: 2025-10-10T17:51:04.199924
# synced: 2025-10-10T17:51:06.351121
# synced: 2025-10-10T17:51:08.476066
# synced: 2025-10-10T17:51:10.704351
# synced: 2025-10-10T17:51:12.864986
# synced: 2025-10-10T17:51:14.995718
# synced: 2025-10-10T17:51:17.136247
# synced: 2025-10-10T17:51:19.630682
# synced: 2025-10-10T17:51:21.788521
# synced: 2025-10-10T17:51:24.154184
# synced: 2025-10-10T17:51:26.500612
# synced: 2025-10-10T17:51:29.107286
# synced: 2025-10-10T17:51:31.298473
# synced: 2025-10-10T17:51:33.417814
# synced: 2025-10-10T17:51:35.553575
# synced: 2025-10-10T17:51:38.108299
# synced: 2025-10-10T17:51:40.702881
# synced: 2025-10-10T17:51:43.257666
# synced: 2025-10-10T17:51:45.412234
# synced: 2025-10-10T17:51:47.540615