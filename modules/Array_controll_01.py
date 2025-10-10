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
# synced: 2025-10-05T17:23:16.955427
# synced: 2025-10-05T17:23:19.880865
# synced: 2025-10-05T17:23:22.756980
# synced: 2025-10-05T17:23:25.481903
# synced: 2025-10-05T17:23:28.223296
# synced: 2025-10-05T17:23:31.175070
# synced: 2025-10-05T17:23:34.037593
# synced: 2025-10-05T17:23:36.770992
# synced: 2025-10-05T17:23:39.600201
# synced: 2025-10-05T17:23:42.255805
# synced: 2025-10-05T17:23:44.994385
# synced: 2025-10-05T17:23:47.899993
# synced: 2025-10-05T17:23:50.638819
# synced: 2025-10-05T17:23:53.448585
# synced: 2025-10-05T17:23:56.279894
# synced: 2025-10-05T17:23:59.062486
# synced: 2025-10-05T17:24:01.845921
# synced: 2025-10-05T17:24:04.664538
# synced: 2025-10-05T17:24:08.117828
# synced: 2025-10-05T17:24:10.745825
# synced: 2025-10-05T17:24:13.609337
# synced: 2025-10-05T17:24:16.392757
# synced: 2025-10-05T17:24:19.265654
# synced: 2025-10-05T17:24:29.634714
# synced: 2025-10-05T17:24:32.124474
# synced: 2025-10-05T17:24:34.347209
# synced: 2025-10-05T17:24:36.503373
# synced: 2025-10-05T17:24:38.655044
# synced: 2025-10-05T17:24:40.750826
# synced: 2025-10-05T17:24:42.894705
# synced: 2025-10-05T17:24:45.035822
# synced: 2025-10-05T17:24:47.301352
# synced: 2025-10-05T17:24:49.461084
# synced: 2025-10-05T17:24:51.567584
# synced: 2025-10-05T17:24:53.661541
# synced: 2025-10-05T17:24:55.883590
# synced: 2025-10-05T17:24:58.010396
# synced: 2025-10-05T17:25:00.239395
# synced: 2025-10-05T17:25:02.470371
# synced: 2025-10-05T17:25:04.574721
# synced: 2025-10-05T17:25:06.790022
# synced: 2025-10-05T17:25:09.042927
# synced: 2025-10-05T17:25:11.191635
# synced: 2025-10-05T17:25:13.474340
# synced: 2025-10-05T17:25:15.668508
# synced: 2025-10-05T17:25:17.907557
# synced: 2025-10-05T17:25:20.137466
# synced: 2025-10-05T17:25:22.349321
# synced: 2025-10-05T17:25:24.526110
# synced: 2025-10-05T17:25:26.756071
# synced: 2025-10-05T17:25:28.934253
# synced: 2025-10-05T17:25:31.180000
# synced: 2025-10-05T17:25:33.419460
# synced: 2025-10-05T17:25:35.602383
# synced: 2025-10-05T17:25:37.848421
# synced: 2025-10-05T17:25:40.095826
# synced: 2025-10-05T17:25:42.351314
# synced: 2025-10-05T17:25:44.553233
# synced: 2025-10-05T17:25:46.736107
# synced: 2025-10-05T17:25:48.928305
# synced: 2025-10-05T17:25:51.147381
# synced: 2025-10-05T17:25:53.353879
# synced: 2025-10-05T17:25:55.533745
# synced: 2025-10-05T17:25:57.735666
# synced: 2025-10-05T17:25:59.970881
# synced: 2025-10-05T17:26:02.151750
# synced: 2025-10-05T17:26:04.360354
# synced: 2025-10-05T17:26:06.639990
# synced: 2025-10-05T17:26:08.905188
# synced: 2025-10-05T17:26:11.146568
# synced: 2025-10-05T17:26:13.390452
# synced: 2025-10-05T17:26:15.624819
# synced: 2025-10-05T17:26:17.913387
# synced: 2025-10-05T17:26:20.179386
# synced: 2025-10-10T17:50:44.569957
# synced: 2025-10-10T17:50:48.359921
# synced: 2025-10-10T17:50:50.588784
# synced: 2025-10-10T17:50:52.751905
# synced: 2025-10-10T17:50:54.994931
# synced: 2025-10-10T17:50:57.746674
# synced: 2025-10-10T17:50:59.854085
# synced: 2025-10-10T17:51:02.011743
# synced: 2025-10-10T17:51:04.195923
# synced: 2025-10-10T17:51:06.348057
# synced: 2025-10-10T17:51:08.472987
# synced: 2025-10-10T17:51:10.701351
# synced: 2025-10-10T17:51:12.861925
# synced: 2025-10-10T17:51:14.992651
# synced: 2025-10-10T17:51:17.134248
# synced: 2025-10-10T17:51:19.628576
# synced: 2025-10-10T17:51:21.785470
# synced: 2025-10-10T17:51:24.151120
# synced: 2025-10-10T17:51:26.498548
# synced: 2025-10-10T17:51:29.104280
# synced: 2025-10-10T17:51:31.296384
# synced: 2025-10-10T17:51:33.415814
# synced: 2025-10-10T17:51:35.551576
# synced: 2025-10-10T17:51:38.105298
# synced: 2025-10-10T17:51:40.699891
# synced: 2025-10-10T17:51:43.254668
# synced: 2025-10-10T17:51:45.409143
# synced: 2025-10-10T17:51:47.538615
# synced: 2025-10-10T17:51:49.704651
# synced: 2025-10-10T17:51:51.848000
# synced: 2025-10-10T17:51:54.052974
# synced: 2025-10-10T17:51:56.181275
# synced: 2025-10-10T17:51:58.384996
# synced: 2025-10-10T17:52:00.639568
# synced: 2025-10-10T17:52:02.847576
# synced: 2025-10-10T17:52:05.082374
# synced: 2025-10-10T17:52:07.240345
# synced: 2025-10-10T17:52:09.403069
# synced: 2025-10-10T17:52:11.653399
# synced: 2025-10-10T17:52:13.865853
# synced: 2025-10-10T17:52:16.075769
# synced: 2025-10-10T17:52:18.358392
# synced: 2025-10-10T17:52:20.728831
# synced: 2025-10-10T17:52:22.823048
# synced: 2025-10-10T17:52:24.913117
# synced: 2025-10-10T17:52:27.023976
# synced: 2025-10-10T17:52:29.179123
# synced: 2025-10-10T17:52:31.585587
# synced: 2025-10-10T17:52:33.713422
# synced: 2025-10-10T17:52:35.884691
# synced: 2025-10-10T17:52:37.995459
# synced: 2025-10-10T17:52:40.042287
# synced: 2025-10-10T17:52:42.422711
# synced: 2025-10-10T17:52:44.571026
# synced: 2025-10-10T17:52:46.776849
# synced: 2025-10-10T17:52:48.958906
# synced: 2025-10-10T17:52:51.112059
# synced: 2025-10-10T17:52:53.307680
# synced: 2025-10-10T17:52:55.458061
# synced: 2025-10-10T17:52:57.537915
# synced: 2025-10-10T17:52:59.634335
# synced: 2025-10-10T17:53:01.707223
# synced: 2025-10-10T17:53:03.891032
# synced: 2025-10-10T17:53:06.183058
# synced: 2025-10-10T17:53:08.323189
# synced: 2025-10-10T17:53:10.512817
# synced: 2025-10-10T17:53:12.808892
# synced: 2025-10-10T17:53:14.873301
# synced: 2025-10-10T17:53:17.165172
# synced: 2025-10-10T17:53:19.305500
# synced: 2025-10-10T17:53:21.522187
# synced: 2025-10-10T17:53:23.717378
# synced: 2025-10-10T17:53:25.774988
# synced: 2025-10-10T17:53:27.956525
# synced: 2025-10-10T17:53:30.095626
# synced: 2025-10-10T17:53:32.249631
# synced: 2025-10-10T17:53:34.382067
# synced: 2025-10-10T17:53:36.477501
# synced: 2025-10-10T17:53:38.903364
# synced: 2025-10-10T17:53:41.103657
# synced: 2025-10-10T17:53:43.284342
# synced: 2025-10-10T17:53:45.350854
# synced: 2025-10-10T17:53:47.505329
# synced: 2025-10-10T17:53:49.555763
# synced: 2025-10-10T17:53:51.831995
# synced: 2025-10-10T17:53:54.032123
# synced: 2025-10-10T17:53:56.378772
# synced: 2025-10-10T17:53:58.542524
# synced: 2025-10-10T17:54:00.698734
# synced: 2025-10-10T17:54:02.871255
# synced: 2025-10-10T17:54:04.964297
# synced: 2025-10-10T17:54:07.071602
# synced: 2025-10-10T17:54:09.186458
# synced: 2025-10-10T17:54:11.242459