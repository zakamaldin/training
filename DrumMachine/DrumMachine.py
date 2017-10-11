from functions import *


class DrumMachine:
    def __init__(self, root):
        self.root = root
        root.title(PROGRAM_NAME)
        self.current_pattern = IntVar()
        self.number_of_units = IntVar()
        self.bpu = IntVar()
        self.to_loop = BooleanVar()
        self.loop = BooleanVar()
        self.keep_playing = BooleanVar()
        self.now_playing = BooleanVar()
        self.beats_per_minute = IntVar()
        self.icons = icons_image()
        self.sample_load_entry = [None] * MAX_NUMBER_OF_DRUM_SAMPLES
        self.root.protocol('WM_DELETE_WINDOW', self.exit_app)
        self.init_gui()


    def init_all_patterns(self):
        self.all_patterns = [
            {
                'list_of_drum_files':
                    [None]*MAX_NUMBER_OF_DRUM_SAMPLES,
                'number_of_units': INITIAL_NUMBER_OF_UNITS,
                'bpu': INITIAL_BPU,
                'beats_per_minute': INITIAL_BEATS_PER_MINUTE,
                'is_button_click_list':
                    self.init_is_button_clicked_list(
                        MAX_NUMBER_OF_DRUM_SAMPLES,
                        INITIAL_NUMBER_OF_UNITS * INITIAL_BPU
                    )
            }
            for k in range(MAX_NUMBER_OF_PATTERNS)
        ]

    def init_is_button_clicked_list(self, num_of_rows, num_of_col):
        return [[False]*num_of_col for x in range(num_of_rows)]

    def init_gui(self):
        self.init_all_patterns()
        self.create_top_bar()
        self.create_drum_loader()
        self.create_drum_matrix()
        self.create_play_bar()
        self.create_top_menu()

    def init_pygame(self):
        pygame.init()
        pygame.mixer.pre_init(44100, 16, 1, 512)


    def play_pattern(self):
        self.keep_playing = True
        while self.keep_playing:
            self.now_playing = True
            play_list = self.get_is_button_clicked_list()
            num_columns = len(play_list[0])
            for column_index in range(num_columns):
                column_to_play =self.get_column_from_matrix(play_list, column_index)
                for i, item in enumerate(column_to_play):
                    if item:
                        sound_filename = self.get_drum_file_path(i)
                        self.play_sound(sound_filename)
                time.sleep(self.time_to_play_each_column())
                if not self.keep_playing:
                    break
            if not self.loop:
                self.keep_playing =self.loop
        self.now_playing = False
        self.toggle_play_button_state()

    def create_top_menu(self):
        self.menu_bar = Menu(self.root)
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label='Load Project', command=self.load_project)
        self.file_menu.add_command(label='Save Project', command=self.save_project)
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Exit', command=self.exit_app)
        self.menu_bar.add_cascade(label='File', menu=self.file_menu)
        self.about_menu = Menu(self.menu_bar, tearoff=0)
        self.about_menu.add_command(label='About', command=self.show_about)
        self.menu_bar.add_cascade(label='About', menu=self.about_menu)
        self.root.config(menu=self.menu_bar)

    def load_project(self):
        file_path = filedialog.askopenfilename(filetypes=[('Beat File', '*.btf')], title='Load Project')
        if not file_path: return
        pickled_file_object = open(file_path, 'rb')
        try:
            self.all_patterns = pickle.load(pickled_file_object)
        except EOFError:
            messagebox.showerror('Error', 'Beat file seems corrupted or invalid !')
            pickled_file_object.close()
        try:
            self.reconstruct_first_pattern()
            self.root.title(os.path.basename(file_path) + '-' + PROGRAM_NAME)
        except:
            messagebox.showerror('Error', 'An unexpected error occured trying to process the beat file')

    def save_project(self):
        save_as_file_name = filedialog.asksaveasfilename(filetypes=[('Beat File', '*.btf')],
                                                         title='Save project as...', defaultextension='.btf')
        if save_as_file_name is None:
            return
        pickle.dump(self.all_patterns, open(save_as_file_name, "wb"))
        self.root.title(os.path.basename(save_as_file_name) + PROGRAM_NAME)

    def show_about(self):
        messagebox.showinfo(PROGRAM_NAME, 'Tkinter GUI Application\n Development Blueprints')

    def create_top_bar(self):
        top_bar_frame = Frame(self.root, height=25)
        top_bar_frame.grid(row=0, column=0, columnspan=7, padx=5, pady=5)

        Label(top_bar_frame, text='Pattern Number:').grid(row=0, column=1)
        self.current_pattern.set(0)
        Spinbox(top_bar_frame, from_=0, to=MAX_NUMBER_OF_PATTERNS - 1, width=5, textvariable=self.current_pattern,
                command=self.on_pattern_changed).grid(row=0, column=2)

        self.current_pattern_name_widget = Entry(top_bar_frame)
        self.current_pattern_name_widget.grid(row=0, column=3)

        Label(top_bar_frame, text='Number of Units:').grid(row=0, column=4)
        self.number_of_units.set(INITIAL_NUMBER_OF_UNITS)
        Spinbox(top_bar_frame, from_=0, to=MAX_NUMBER_OF_UNITS - 1, width=5, textvariable=self.number_of_units,
                command=self.on_number_of_units_changed).grid(row=0, column=5)

        Label(top_bar_frame, text='BPUs:').grid(row=0, column=6)
        self.bpu.set(INITIAL_BPU)
        Spinbox(top_bar_frame, from_=0, to=MAX_BPU - 1, width=5, textvariable=self.bpu,
                command=self.on_bpu_changed).grid(row=0, column=7)
        self.display_pattern_name()

    def create_drum_loader(self):
        drum_loader_frame = Frame(self.root)
        drum_loader_frame.grid(row=1, column=0, columnspan=2, pady=4, sticky='wens')
        for i in range(MAX_NUMBER_OF_DRUM_SAMPLES):
            open_file_button = Button(drum_loader_frame,
                                      image=self.icons['open'],
                                      command=self.on_open_file_button_clicked(i))
            open_file_button.grid(row=i, column=0, padx=7, pady=2)

            self.sample_load_entry[i] = Entry(drum_loader_frame)
            self.sample_load_entry[i].grid(row=i, column=1, padx=7, pady=2)

    def on_open_file_button_clicked(self, drum_index):
        def event_handler():
            file_path = filedialog.askopenfilename(defaultextension='.wav',
                                                   filetypes=[('Wave Files', '*.wav'),
                                                              ('OGG Files', '*.ogg')])
            if not file_path:
                return
            self.set_drum_file_path(drum_index, file_path)
            self.display_all_drum_file_names()
        return event_handler

    def display_all_drum_file_names(self):
        for i, drum_name in enumerate(self.get_list_of_drum_files()):
            self.display_drum_name(i, drum_name)

    def display_drum_name(self, text_widget_num, file_path):
        if file_path is None:
            return
        drum_name = os.path.basename(file_path)
        self.sample_load_entry[text_widget_num].delete(0, END)
        self.sample_load_entry[text_widget_num].insert(0, drum_name)

    def create_drum_matrix(self):
        drum_matrix_frame = Frame(self.root)
        drum_matrix_frame.grid(row=1, column=2, columnspan=40, sticky='wens', padx=15, pady=4)

        self.buttons = [[None for i in range(
            self.find_number_of_columns())]
                        for i in range(MAX_NUMBER_OF_DRUM_SAMPLES)]
        for row in range(MAX_NUMBER_OF_DRUM_SAMPLES):
            for col in range(self.find_number_of_columns()):
                self.buttons[row][col] = Button(
                    drum_matrix_frame, width=2, height=1, command=self.on_button_clicked(row, col))
                self.buttons[row][col].grid(row=row, column=col)
                self.display_button_color(row, col)

    def create_play_bar(self):
        play_bar_frame = Frame(self.root)
        play_bar_frame.grid(row=11, column=0, columnspan=10, sticky='wens', padx=40, pady=4)

        self.play_button = Button(play_bar_frame, text='Play', image=self.icons['play'],
                             compound='left', width=50, command=self.on_play_button)
        self.play_button.grid(row=0, column=0, padx=5, pady=2)

        stop_button = Button(play_bar_frame, text='Stop', image=self.icons['stop'],
                             compound='left', width=50, command=self.on_stop_button).grid(
            row=0, column=1, padx=5, pady=2)

        ttk.Separator(play_bar_frame, orient='vertical').grid(row=0, column=3, sticky='ns', padx=5)

        loop_checkbox = Checkbutton(play_bar_frame, text='loop', variable=self.to_loop, command=self.on_loop_button_toggled).grid(row=0, column=4, padx=5, pady=2)

        ttk.Separator(play_bar_frame, orient='vertical').grid(row=0, column=5, sticky='ns', padx=5)

        Label(play_bar_frame, text='Beats Per Minute: ').grid(row=0, column=6)
        self.beats_per_minute.set(INITIAL_BEATS_PER_MINUTE)
        Spinbox(play_bar_frame, from_=0, to=MAX_BEATS_PER_MINUTE, width=5, textvariable=self.beats_per_minute,
                command=self.on_beats_per_minute_changed).grid(row=0, column=7)

        ttk.Separator(play_bar_frame, orient='vertical').grid(row=0, column=8, sticky='ns', padx=5)

        logo = Label(play_bar_frame, image=self.icons['logo']).grid(row=0, column=9, sticky='ns', padx=5)


    def find_number_of_columns(self):
        return self.number_of_units.get() * self.bpu.get()

    def on_button_clicked(self, row, col):
        def event_handler():
            self.process_button_clicked(row, col)
        return event_handler

    def display_button_color(self, row, col):
        bpu = self.bpu.get()
        original_color = COLOR_1 if ((col//bpu)%2) else COLOR_2
        button_color = BUTTON_CLICKED_COLOR if self.get_button_value(row, col) else original_color
        self.buttons[row][col].config(bg=button_color)

    def display_all_button_color(self):
        number_of_col = self.find_number_of_columns()
        for r in range(MAX_NUMBER_OF_DRUM_SAMPLES):
            for c in range(number_of_col):
                self.display_button_color(r, c)

    def on_play_button(self):
        self.start_play()
        self.toggle_play_button_state()

    def start_play(self):
        self.init_pygame()
        self.play_in_thread()

    def play_sound(self, sound_filename):
        if sound_filename is not None:
            pygame.mixer.Sound(sound_filename).play()

    def play_in_thread(self):
        self.thread = threading.Thread(target=self.play_pattern)
        self.thread.start()

    def toggle_play_button_state(self):
        if self.now_playing:
            self.play_button.config(state="disabled")
        else:
            self.play_button.config(state="normal")

    def on_stop_button(self):
        self.stop_play()
        self.toggle_play_button_state()

    def stop_play(self):
        self.keep_playing = False

    def on_loop_button_toggled(self):
        self.loop = self.to_loop.get()
        self.keep_playing = self.loop
        if self.now_playing:
            self.now_playing = self.loop
        self.toggle_play_button_state()

    def process_button_clicked(self, row, col):
        self.set_button_value(row, col, not self.get_button_value(row, col))
        self.display_button_color(row, col)

    # Button value
    def get_button_value(self, row, col):
        return self.all_patterns[self.current_pattern.get()]['is_button_click_list'][row][col]

    def set_button_value(self, row, col, bool_value):
        self.all_patterns[self.current_pattern.get()]['is_button_click_list'][row][col] = bool_value

    # Current pattern
    def on_pattern_changed(self):
        self.change_pattern()

    def change_pattern(self):
        if self.now_playing:
            self.stop_play()
            self.now_playing = True
        self.display_pattern_name()
        self.create_drum_loader()
        self.display_all_drum_file_names()
        self.number_of_units.set(self.get_number_of_units())
        self.bpu.set(self.get_bpu())
        self.beats_per_minute.set(self.get_beats_per_minute())
        self.create_drum_matrix()
        self.display_all_button_color()
        if self.now_playing:
            self.restart_play_of_new_pattern()

    def restart_play_of_new_pattern(self):
        self.start_play()

    def get_current_pattern_dict(self):
        return self.all_patterns[self.current_pattern.get()]

    def display_pattern_name(self):
        self.current_pattern_name_widget.config(state='normal')
        self.current_pattern_name_widget.delete(0, END)
        self.current_pattern_name_widget.insert(0, 'Pattern {}'.format(self.current_pattern.get()))
        self.current_pattern_name_widget.config(state='readonly')


    # Bpu
    def on_bpu_changed(self):
        self.set_bpu()
        self.set_is_button_clicked_list(MAX_NUMBER_OF_DRUM_SAMPLES, self.find_number_of_columns())
        self.create_drum_matrix()

    def get_bpu(self):
        return self.get_current_pattern_dict()['bpu']

    def set_bpu(self):
        self.get_current_pattern_dict()['bpu'] = self.bpu.get()

    # Number of Units
    def on_number_of_units_changed(self):
        self.set_number_of_units()
        self.set_is_button_clicked_list(MAX_NUMBER_OF_DRUM_SAMPLES, self.find_number_of_columns())
        self.create_drum_matrix()

    def get_number_of_units(self):
        return self.get_current_pattern_dict()['number_of_units']

    def set_number_of_units(self):
        self.get_current_pattern_dict()['number_of_units'] = self.number_of_units.get()

    # List of Drum Files
    def get_list_of_drum_files(self):
        return self.get_current_pattern_dict()['list_of_drum_files']

    def get_drum_file_path(self, drum_index):
        return self.get_list_of_drum_files()[drum_index]

    def set_drum_file_path(self, drum_index, file_path):
        self.get_list_of_drum_files()[drum_index] = file_path

    # Is Button clicked list
    def get_is_button_clicked_list(self):
        return  self.get_current_pattern_dict()['is_button_click_list']

    def set_is_button_clicked_list(self, num_or_rows, num_of_cols):
        self.get_current_pattern_dict()['is_button_click_list'] = \
            [[False] * num_of_cols for x in range(num_or_rows)]

    # Beats per minute
    def on_beats_per_minute_changed(self):
        self.set_beats_per_minute()

    def get_beats_per_minute(self):
        return self.get_current_pattern_dict()['beats_per_minute']

    def set_beats_per_minute(self):
        self.get_current_pattern_dict()['beats_per_minute'] = self.beats_per_minute.get()

    def get_column_from_matrix(self, matrx, i):
        return [row[i] for row in matrx]

    def time_to_play_each_column(self):
        beats_per_minute = self.get_beats_per_minute()
        beats_per_second = beats_per_minute / 60
        time_to_play_each_column = 1 / beats_per_second
        return time_to_play_each_column

    def exit_app(self):
        self.keep_playing = False
        if messagebox.askokcancel('Quit?', 'Really quit?'):
            self.root.destroy()

    def reconstruct_first_pattern(self):
        self.change_pattern()


if __name__ == '__main__':
    root = Tk()
    DrumMachine(root)
    root.mainloop()
