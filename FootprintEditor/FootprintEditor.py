from functions import *
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox as tmb


root = Tk()
root.geometry('800x600')

icons = icons_image()
root.title(PROGRAM_NAME)
menu_bar = Menu(root)
shortcut_bar = Frame(root, height=35, background='light sea green')
shortcut_bar.pack(expand='no', fill='x')
content_text = Text(root, wrap='word', undo=1)

scroll_bar = Scrollbar(content_text)
content_text.configure(yscrollcommand=scroll_bar.set)
scroll_bar.config(command=content_text.yview())
scroll_bar.pack(side='right', fill='y')

file_name = None
show_line_nom = IntVar()
show_line_nom.set(1)
hl_curr_line = BooleanVar()
show_cursor_info = BooleanVar()
show_cursor_info.set(1)


def on_content_changed(event=None):
	update_line_numbers()
	update_cursor_info_bar()


content_text.bind('<Any-KeyPress>', on_content_changed)

file_menu = Menu(menu_bar, tearoff=0)
# Описание меню, кнопок и функций
# ---File---
menu_bar.add_cascade(label='File', menu=file_menu)


# New File
def new(event=None):
	root.title("Untitled")
	global file_name
	file_name = None
	content_text.delete(1.0, END)
	on_content_changed()


file_menu.add_command(label='New', accelerator='Ctrl + N',
					  compound='left', image=icons['new'], command=new)

content_text.bind('<Control-n>', new)
content_text.bind('<Control-N>', new)


# Open
def open(event=None):
	input_file_name = filedialog.askopenfilename(
		defaultextension=".txt", filetypes=[("All Files", "*.*"), ("Text Documents",
		"*.txt")])
	if input_file_name:
		global file_name
		file_name = input_file_name
		root.title('{} - {}'.format(os.path.basename(file_name), PROGRAM_NAME))
		content_text.delete(1.0, END)
		with open(file_name) as _file:
			content_text.insert(1.0, _file.read())
	on_content_changed()


file_menu.add_command(label='Open', accelerator='Ctrl + O',
					  compound='left', image=icons['open'], underline=0, command=open)

content_text.bind('<Control-o>', open)
content_text.bind('<Control-O>', open)
# Save
def save(event=None):
	global file_name
	if not file_name:
		save_as()
	else:
		write_to_file(file_name)
	return "break"


def write_to_file(file_name):
	try:
		content = content_text.get(1.0, 'end')
		with open(file_name, 'w') as the_file:
			the_file.write(content)
	except IOError:
		pass


file_menu.add_command(label='Save', accelerator='Ctrl + S',
					  compound='left', image=icons['save'], command=save)

content_text.bind('<Control-s>', save)
content_text.bind('<Control-S>', save)


# Save as
def save_as(event=None):
	input_file_name= filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("All Files", "*.*"), ("Text Documents",
		"*.txt")])
	if input_file_name:
		global file_name
		file_name = input_file_name
		write_to_file(file_name)
		root.title('{} - {}'.format(os.path.basename(file_name), PROGRAM_NAME))
	return "break"


file_menu.add_command(label='SaveAs', accelerator='Shift + Ctrl + S',
					  compound='left', underline=0, image=icons['save_as'], command=save_as)
file_menu.add_separator()


# Exit
def close(event=None):
	if tmb.askokcancel("Quit?", "Really quit?"):
		root.destroy()


file_menu.add_command(label='Exit', accelerator='Alt + F4',
					  compound='left', underline=0, image=icons['close'], command=close)
content_text.bind('<Alt-F4>', close)

# ---Edit---
edit_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label='Edit', menu=edit_menu)


# Undo
def undo():
	content_text.event_generate('<<Undo>>')
	on_content_changed()


edit_menu.add_command(label='Undo', accelerator='Ctrl + Z',
					  compound='left', image=icons['undo'], command=undo)


# Redo
def redo(event=None):
	content_text.event_generate('<<Redo>>')
	on_content_changed()
	return "break"


edit_menu.add_command(label='Redo', accelerator='Ctrl + Y',
					  compound='left', image=icons['redo'], command=redo)
edit_menu.add_separator()
content_text.bind('<Control-y>', redo)
content_text.bind('<Control-Y>', redo)


# Cut
def cut():
	content_text.event_generate('<<Cut>>')
	on_content_changed()


edit_menu.add_command(label='Cut', accelerator='Ctrl + X',
					  compound='left', image=icons['cut'], command=cut)


# Copy
def copy():
	content_text.event_generate('<<Copy>>')


edit_menu.add_command(label='Copy', accelerator='Ctrl + C',
					  compound='left', image=icons['copy'], command=copy)


# Paste
def paste():
	content_text.event_generate('<<Paste>>')
	on_content_changed()


edit_menu.add_command(label='Paste', accelerator='Ctrl + V',
					  compound='left', image=icons['paste'], command=paste)
edit_menu.add_separator()


# Find
def find(event=None):
	search_toplevel = Toplevel(root)
	search_toplevel.title('Find Text')
	search_toplevel.transient(root)
	search_toplevel.resizable(False, False)

	Label(search_toplevel, text="Find All:").grid(row=0, column=0,
												  sticky='e')

	search_entry = Entry(search_toplevel, width=25)
	search_entry.grid(row=0, column=1, padx=2, pady=2,
					  sticky='we')
	search_entry.focus_set()

	ignore_case_value = IntVar()
	c = Checkbutton(search_toplevel, text='Ignore Case',
				variable=ignore_case_value)
	c.grid(row=1, column=1, sticky='e', padx=2, pady=2)

	b = Button(search_toplevel, text="Find All", underline=0,
		   command=lambda: search_output(search_entry.get(),
										 ignore_case_value.get(), content_text,
										 search_toplevel,search_entry))
	b.grid(row=0, column=2, sticky='e' + 'w', padx=2, pady=2)

	def close_search_window():
		content_text.tag_remove('match', '1.0', END)
		search_toplevel.destroy()
	search_toplevel.protocol("WM_DELETE_WINDOW", close_search_window)
	return "break"


def search_output(needle, if_ignore_case, content_text,
				  search_toplevel, search_box):
	content_text.tag_remove('match', '1.0', END)
	matches_found = 0
	if needle:
		start_pos = '1.0'
		while True:
			start_pos = content_text.search(needle, start_pos,
											nocase=if_ignore_case, stopindex=END)
			if not start_pos:
				break
			end_pos = '{}+{}c'.format(start_pos, len(needle))
			content_text.tag_add('match', start_pos, end_pos)
			matches_found += 1
			start_pos = end_pos
		content_text.tag_config(
			'match', foreground='red', background='yellow')
	search_box.focus_set()
	search_toplevel.title('{} matches found'.format(matches_found))


edit_menu.add_command(label='Find', accelerator='Ctrl + F',
					  compound='left', image=icons['find'], command=find)
edit_menu.add_separator()

content_text.bind('<Control-f>', find)
content_text.bind('<Control-F>', find)


# Select all
def select_all(event=None):
	content_text.tag_add('sel', '1.0', 'end')
	return "break"


edit_menu.add_command(label='Select all',  compound='left', image=icons['select_all'],
					  accelerator='Ctrl + A', command=select_all)

content_text.bind('<Control-a>', select_all)
content_text.bind('<Control-A>', select_all)

# ---View---
view_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label='View', menu=view_menu)


# Line Number
line_number_bar = Text(root, width=5, padx=3, takefocus=0,
					   border=0, background='khaki',
					   state='disabled', wrap='none')
line_number_bar.pack(side='left', fill='y')


def update_line_numbers(event=None):
	line_numbers = get_line_numbers()
	line_number_bar.config(state='normal')
	line_number_bar.delete('1.0', 'end')
	line_number_bar.insert('1.0', line_numbers)
	line_number_bar.config(state='disabled')


def get_line_numbers():
	output = ''
	if show_line_nom.get():
		row, col = content_text.index(END).split('.')
		for i in range(1, int(row)):
			output += str(i) + '\n'
	return output


view_menu.add_checkbutton(label='Show Line Number', variable=show_line_nom)


# Cursor location
cursor_info_bar = Label(content_text, text='Line: 1 | Col: 1')
cursor_info_bar.pack(expand=NO, fill=None, side='right', anchor='se')


def show_cursor_info_bar():
	show_cursor_info_checked = show_cursor_info.get()
	if show_cursor_info_checked:
		cursor_info_bar.pack(expand=NO, fill=None, side='right', anchor='se')
	else:
		cursor_info_bar.pack_forget()


def update_cursor_info_bar(event=None):
	row, col = content_text.index(INSERT).split('.')
	line_num, col_num = str(int(row)), str(int(col)+1)
	infotext = 'Line: {0} | Col: {1}'.format(line_num, col_num)
	cursor_info_bar.config(text=infotext)


view_menu.add_checkbutton(label='Show Cursor Location at Bottom', variable=show_cursor_info,
						  command=show_cursor_info_bar)


# Highlight
def highlight_line(interval=100):
	content_text.tag_remove('active_line', 1.0, 'end')
	content_text.tag_add("active_line", 'insert linestart', 'insert lineend+1c')
	content_text.after(interval, toggle_highlight)


def undo_highlight():
	content_text.tag_remove("active_line", 1.0, 'end')


def toggle_highlight(event=None):
	if hl_curr_line.get():
		highlight_line()
	else:
		undo_highlight()


view_menu.add_checkbutton(label='Highlight Current Line', variable=hl_curr_line,
						  command=toggle_highlight)

# Themes


def change_theme(event=None):
	selected_theme = theme_name.get()
	fg_bg_colors = color_shemes.get(selected_theme)
	foreground_color, background_color = fg_bg_colors.split('.')
	content_text.config(background=background_color, foreground=foreground_color)


theme_name = StringVar()
themes_menu = Menu(view_menu, tearoff=0)
view_menu.add_cascade(label='Themes', menu=themes_menu)
color_shemes = {
	'Default': '#000000.#FFFFFF',
	'Hacker': '#8ffe09.#000000',
	'Visual Studio': '#5B8340.#D1E7E0',
	'Vim': '#83406A.#D1D4D1',
	'JetBrains': '#D1E7E0.#5B8340'
	}


theme_name.set('Default')


for c in sorted(color_shemes):
	themes_menu.add_radiobutton(label=c, variable=theme_name, command=change_theme)

# ---About---
about_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label='About', menu=about_menu)


# About
def about(event=None):
	tmb.showinfo(
		"About", "{}{}".format(PROGRAM_NAME, "\nTkinter GUI "
		"Application\n Development Blueprints")
	)


about_menu.add_command(label='About', compound='left', image=icons['about'], command=about)


# Help
def help(event=None):
	tmb.showinfo(
		"Help", "Help Book: \nTkinter GUI "
				"Application\n Development Blueprints", icon='question')


content_text.bind('<KeyPress-F1>', help)


# Popup menu
def show_popup_menu(event):
	popup_menu.tk_popup(event.x_root, event.y_root)


popup_menu = Menu(content_text)
for i in ('cut', 'copy', 'paste', 'redo', 'undo'):
	cmd = eval(i)
	popup_menu.add_command(label=i, compound='left', command=cmd)
popup_menu.add_separator()
popup_menu.add_command(label='Select All', underline=7, command=select_all)
content_text.bind('<Button-3>', show_popup_menu)
# Shortcut bar
about_menu.add_command(label='Help', compound='left', image=icons['help'], command=help)

root.config(menu=menu_bar)
for i in icons:
	cmd = eval(i)
	tool_bar = Button(shortcut_bar, image=icons[i], command=cmd)
	tool_bar.image = icons[i]
	tool_bar.pack(side='left')


content_text.tag_configure('active_line', background='ivory2')
content_text.pack(expand='yes', fill='both')
content_text.focus_set()
on_content_changed()
root.mainloop()
