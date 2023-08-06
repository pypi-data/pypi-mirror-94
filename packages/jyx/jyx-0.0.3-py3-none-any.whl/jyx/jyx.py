#!/usr/bin/env python3

#
# Imports
#

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import font

import json                   # for loading/saving options
from datetime import datetime # for now()
import os                     # for getcwd()
import os.path                # for basename()
from enum import Enum         # for our Logger
import subprocess             # for run
import stat                   # for run
import platform               # for knowing where we are in handling of ctrl
from collections import deque # for parsing

#
# Globals and constants
#

DEFAULT_CONFIG = """{
    "options": {
        "tongue": "en",
        "confirm": false,
        "basename": false,
        "treeview": true,
        'tabasspaces' : true
    },
    "messages": {
        "en" : {
            "started"     : "Started",
            "about_msg"   : "Made with ❤",
            "unsaved"     : "Unsaved changes",
            "unsaved_msg" : "There are unsaved changes.\\nDo you really want to quit Jyx?",
            "open file"   : "Open file...",
            "save file"   : "Save file...",
            "filter all"  : "all files",
            "file name"   : "myfile"
        }
    },
    "menu": {
        "en": {
            "tongue"      : "English",
            "file"        :  "File",
            "new"         : "New",
            "open"        : "Open...",
            "save"        : "Save",
            "save as"     : "Save As...",
            "save all"    : "Save All",
            "run"         : "Run Script",
            "close tab"   : "Close Tab",
            "exit"        : "Exit",
            "edit"        : "Edit",
            "undo"        : "Undo",
            "redo"        : "Redo",
            "cut"         : "Cut",
            "copy"        : "Copy",
            "paste"       : "Paste",
            "select all"  : "Select all",
            "clear"       : "Clear",
            "options"     : "Options",
            "tongues"     : "Tongues",
            "confirm"     : "Confirm before exit",
            "basename"    : "Display only the name",
            "treeview"    : "Display tree",
            "tabasspaces" : "Tab as spaces",
            "languages"   : "Languages",
            "help"        : "Help",
            "about"       : "About..."
        }
    },
    "languages" : {
        "text" : {
            "label"       : "Plain text",
            "extension"   : [".txt"],
            "family"      : "",
            "support"     : "",
            "token"       : [],
            "style"       : {
                "default" : {
                }
            }
        }
    },
    "default_language"    : "text"
}
"""

#
# Classes
#

class Level(Enum):
    INFO = 0
    WARNING = 1
    ERROR = 2

class Output(Enum):
    SILENT = 0
    CONSOLE = 1
    POPUP = 2

class Logger:

    def __init__(self, exit_on_error: bool = True,
                 info=Output.CONSOLE,
                 warn=Output.CONSOLE,
                 error=Output.CONSOLE):
        self.exit_on_error = exit_on_error
        self.flux = {
            Level.INFO : info,
            Level.WARNING : warn,
            Level.ERROR : error,
        }

    def set_warn(self, val: Output) -> None:
        self.flux[Level.WARNING] = val

    def set_info(self, val: Output) -> None:
        self.flux[Level.INFO] = val

    def set_error(self, val: Output) -> None:
        self.flux[Level.ERROR] = val

    def warn(self, msg: str) -> None:
        if self.flux[Level.WARNING] == Output.CONSOLE:
            print('[WARNING] ' + str(msg))
        elif self.flux[Level.WARNING] == Output.POPUP:
            messagebox.showwarning("Warning", str(msg))

    def info(self, msg: str) -> None:
        if self.flux[Level.INFO] == Output.CONSOLE:
            print('[INFO] ' + str(msg))
        elif self.flux[Level.INFO] == Output.POPUP:
            messagebox.showinfo("Information", str(msg))

    def error(self, msg: str) -> None:
        if self.flux[Level.ERROR] == Output.CONSOLE:
            print('[ERROR] ' + str(msg))
        elif self.flux[Level.ERROR] == Output.POPUP:
            messagebox.showerror("Error", str(msg))
        if self.exit_on_error:
            exit()


#-------------------------------------------------------------------------------

class Jyx:

    TITLE = 'Jyx'
    RUN_COMMAND = 6
    CLOSE_TAB = 8
    DATA_FILE_NAME = 'jyx.json'
    LAST_VALUES = 'last_values.json'
    VERSION = '0.0.3'
    
    def __init__(self):
        self.log = Logger(exit_on_error=False, info=Output.CONSOLE, 
                          warn=Output.POPUP, error=Output.POPUP)
        # Path
        home = os.path.expanduser("~")
        self.jyx_dir = os.path.join(home, '.jyx')
        if not os.path.isdir(self.jyx_dir):
            os.mkdir(self.jyx_dir)
        # Load base data (in same dir than jyx.py or we create one in jyx_dir)
        try:
            f = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), Jyx.DATA_FILE_NAME), 'r', encoding='utf8')
            self.log.info('Data file for options found in:')
            self.log.info(os.path.join(os.path.dirname(os.path.realpath(__file__)), Jyx.DATA_FILE_NAME))
        except FileNotFoundError:
            try:
                f = open(os.path.join(self.jyx_dir, Jyx.DATA_FILE_NAME), 'r', encoding='utf8')
                self.log.info('Data file for options found in:')
                self.log.info(os.path.join(self.jyx_dir, Jyx.DATA_FILE_NAME))
            except FileNotFoundError:
                f = open(os.path.join(self.jyx_dir, Jyx.DATA_FILE_NAME), 'w', encoding='utf8')
                f.write(DEFAULT_CONFIG)
                f.close()
                self.log.info('No data file found. Writing default in:')
                self.log.info(os.path.join(self.jyx_dir, Jyx.DATA_FILE_NAME))
                f = open(os.path.join(self.jyx_dir, Jyx.DATA_FILE_NAME), 'r', encoding='utf8')
        self.data = json.load(f)
        f.close()
        # Init
        self.root = tk.Tk(className=Jyx.TITLE)
        self.root.title(Jyx.TITLE)
        self.root.protocol('WM_DELETE_WINDOW', self.exit)
        self.root.minsize(width=800, height=600)
        icon = self.load_icon('polar-star.png')
        if icon is not None:
            self.root.iconphoto(True, icon)
        # Fonts
        self.fonts = {}
        self.fonts['COURRIER_NEW_10'] = font.Font(family='Courier New', size=10)
        self.fonts['COURRIER_NEW_10_BOLD'] = font.Font(family='Courier New', size=10, weight='bold')
        # Options
        try:
            file = open(os.path.join(self.jyx_dir, Jyx.LAST_VALUES), mode='r')
            self.log.info('Last values file for options found in:')
            self.log.info(os.path.join(self.jyx_dir, Jyx.LAST_VALUES))
            last_values = json.load(file)         
            file.close()
        except:
            last_values = {}
        self.options = {}
        for opt, val in self.data['options'].items():
            if opt in last_values:
                val = last_values[opt]
            self.options[opt] = JyxOption(opt, val)
        self.options['language'] = JyxOption('language', self.data['default_language'])
        # Option if we recreate a jyx.json, there is only 'en' inside
        if self.options['tongue'].get() not in self.data['menu']:
            self.options['tongue'].var.set('en')
            self.update('tongue', init=True)
        # UI components
        self.treeview = JyxTree(self)
        self.notebook = JyxNotebook(self)
        # Prend tout Y (relheight = 1.0), se positionne à 0.2 pour le notebook
        self.treeview.place(relx=0.0, rely =0.0, relwidth =0.2, relheight =1.0)
        self.notebook.place(relx=0.2, rely =0.0, relwidth =0.8, relheight =1.0)
        self.menu = JyxMenu(self)
        self.root.config(menu=self.menu)
        # Updall vars, cannot be called until the menu is completed
        self.update_all_options() 
        self.update_title()
        # Starting
        self.auto_update()
        self.root.mainloop()

    def load_icon(self, name: str) -> tk.PhotoImage:
        res = None
        try:
            res = tk.PhotoImage(file=os.path.join(os.path.dirname(__file__), 'icons', name))
        except:
            self.log.info(f'Resource {name} could not be found')
        return res

    def get_root(self):
        return self.root

    def auto_update(self):
        self.after_id = self.root.after(5000, self.auto_update)
        #self.root.bell()
        #print('hello')

    def update_title(self):
        dirty = ' *' if self.notebook.is_dirty() else ''
        tongue = self.options['tongue'].get()
        if self.notebook.get_filepath() is None:
            file = self.data['menu'][tongue]['new']              
        elif self.options['basename'].get():
            file = os.path.basename(self.notebook.get_filepath())
        else:
            file = self.notebook.get_filepath()
        i = self.notebook.current_index() + 1
        nb = len(self.notebook)
        self.root.wm_title(f"{Jyx.TITLE} {Jyx.VERSION} - {i}/{nb} {file}{dirty}")

    def update_status(self, event=None):
        self.notebook.current().status_bar.configure(text=self.notebook.current().lang + ' - ' + self.notebook.get_position())

    def update_all_options(self):
        for key in self.options:
            self.update(key, True)

    def update(self, varname=None, init=False):
        if varname is None and not init:
            self.update_title()
            self.update_status()
            if self.options['treeview'].get():
                self.treeview.rebuild()
            return
        elif varname is None and init:
            return
        if varname not in self.options:
            raise Exception(f'Variable unknown: {varname}')
        opt = self.options[varname]
        val = opt.get()
        print(f"option {opt.name} = {val}")
        if varname == 'language':
            if not self.has(f"languages.{val}.support", "execute"):
                self.menu.file_menu.entryconfig(Jyx.RUN_COMMAND, state=tk.DISABLED)
            else:
                self.menu.file_menu.entryconfig(Jyx.RUN_COMMAND, state=tk.ACTIVE)
            print('setting to : ', val)
            self.notebook.current().change_lang(val)
        elif varname == 'tongue' and not init:
            self.menu.relabel(old=opt.prev, new=val)
            self.notebook.relabel(val)
        elif varname == 'basename' and not init:
            self.update_title()
        elif varname == 'treeview':
            if val:
                self.treeview.place(relx=0.0, rely =0.0, relwidth =0.2, relheight =1.0)
                self.notebook.place(relx=0.2, rely =0.0, relwidth =0.8, relheight =1.0)
                self.treeview.rebuild()
            elif not val:
                self.treeview.place_forget()
                self.notebook.place(relx=0.0, rely =0.0, relwidth =1.0, relheight =1.0)
        elif varname == 'tabasspace':
            pass
        opt.prev = val

    def has(self, prop, value, content=None):
        #print('has', prop, value) #, content)
        if content is None:
            content = self.data
        exploded = prop.split('.')
        if exploded[0] not in content:
            return False
        elif len(exploded) == 1:
            if type(content[exploded[0]]) in [str, int]:
                return content[exploded[0]] == value
            elif type(content[exploded[0]]) == list:
                return value in content[exploded[0]]
            else:
                raise Exception('Type not handled')
        else:
            return self.has('.'.join(exploded[1:]), value, content[exploded[0]])
        
    def exit(self, event=None):
        ending = False
        tongue = self.options['tongue'].get()
        if self.notebook.is_anyone_dirty() and self.options['confirm'].get():
            title = self.data['messages'][tongue]['unsaved']
            msg = self.data['messages'][tongue]['unsaved_msg']
            if messagebox.askyesno("Unsaved changes", msg, default=messagebox.NO):
                ending = True
        else:
            ending = True
        if ending:
            simple_opt = {}
            for opt, val in self.options.items():
                simple_opt[opt] = val.var.get()
            file = open(os.path.join(self.jyx_dir, Jyx.LAST_VALUES), mode='w', encoding='utf8')
            json.dump(simple_opt, file, indent=' ' * 4)
            file.close()
            self.root.after_cancel(self.after_id)
            self.root.destroy()

    def new(self, event=None):
        self.notebook.new_tab()
  
    def save(self, event=None):
        if self.notebook.get_filepath() is None:
            self.save_as(event)
        else:
            self.notebook.current().save()

    def save_as(self, event=None):
        tongue = self.options['tongue'].get()
        lang = self.notebook.current().lang
        options = {}
        #options['defaultextension'] = '.txt'
        options['filetypes'] = [
            (self.data['messages'][tongue]['filter all'], '.*'),
            ('lua files', '.lua'),
            ('python files', '.py'),
            ('text files', '.txt')]
        options['initialdir'] = 'C:\\'
        options['initialfile'] = self.data['messages'][tongue]['file name'] + self.data['languages'][lang]['extension'][0]
        options['parent'] = self.root
        options['title'] = self.data['messages'][tongue]['save file']
        filename = filedialog.asksaveasfilename(**options) # mode='w',
        if type(filename) == str and len(filename) > 0:
            print('save_as', filename)
            self.notebook.current().save(filename)

    def open(self, event=None):
        tongue = self.options['tongue'].get()
        lang = self.notebook.current().lang
        options = {}
        #options['defaultextension'] = '.txt'
        options['filetypes'] = [(self.data['messages'][tongue]['filter all'], '.*')]
        if self.notebook.get_filepath() is None:
            options['initialdir'] = os.getcwd()
        else:
            options['initialdir'] = os.path.dirname(self.notebook.get_filepath())
        options['initialfile'] = self.data['messages'][tongue]['file name'] + self.data['languages'][lang]['extension'][0]
        options['parent'] = self.root
        options['title'] = self.data['messages'][tongue]['open file']
        filename = filedialog.askopenfilename(**options)
        if type(filename) == str and len(filename) > 0:
            f = open(filename, mode='r', encoding='utf8')
            content = None
            try:
                content = f.read()
            except UnicodeDecodeError as ude:
                self.log.error('Encoding error: unable to open file: ' + filename)
                print(ude)
                return
            finally:
                f.close()
            if content is None:
                self.log.error('Impossible to open ' + filename + ' nothing to read.')
                return
            already = False
            num = 0
            cpt = 0
            # Check if already open
            for n in self.notebook:
                msg = n.filepath if n.filepath is not None else 'buffer'
                print('Opened file:', msg)
                if n.filepath == filename:
                    already = True
                    num = cpt
                cpt += 1
            if not already:
                self.log.info('Opening: ' + filename)
                self.notebook.open(filename, content)
                self.treeview.rebuild()
            else:
                self.log.info('Alreay opened, selecting: ' + str(num))
                self.notebook.select(num)

    def run(self, event=None):
        lang = self.notebook.current().lang
        if not self.has(f"languages.{lang}.support", "execute"):
            return
        filepath = self.notebook.current().filepath
        if filepath is None:
            filepath = os.path.join(os.getcwd(), 'temp' + self.data['languages'][lang]['extension'][0])
            self.notebook.current().save(filepath, raw=True) # will not set any filepath nor dirty state (still dirty)
        self.log.info('Executing: ' + filepath)
        if hasattr(os, 'startfile'): # Windows only
            subp = 'python'
        else:
            subp = 'python3'
            os.chmod(filepath, stat.S_IXUSR | stat.S_IWUSR | stat.S_IRUSR)
        cmd = subprocess.run([subp, filepath], capture_output=True)
        stdout = cmd.stdout.decode() # from bytes to str
        print(stdout)

    def about(self, event=None):
        tongue = self.options['tongue'].get()
        title = self.data['menu'][tongue]['about']
        msg = self.data['messages'][tongue]['about_msg']
        messagebox.showinfo(title, f"{Jyx.TITLE} - {Jyx.VERSION}\n{msg}\nDamien Gouteux\n2017 - {datetime.now().year}\n")


class JyxOption:

    def __init__(self, name, val):
        self.name = name
        self.typ = type(val)
        if self.typ == str:
            self.var = tk.StringVar()
        elif self.typ == bool:
            self.var = tk.BooleanVar()
        else:
            raise Exception(f"Option type not handled for {self.name} of type {self.typ}")
        self.var.set(val)
        self.prev = val

    def get(self):
        return self.var.get()


class JyxMenu(tk.Menu):

    def __init__(self, jyx):
        tk.Menu.__init__(self, jyx.get_root())
        self.jyx = jyx
        self.build()

    def relabel(self, old, new):
        #last = self.index(tk.END)
        #for item in range(last + 1)
        data = self.jyx.data

        self.entryconfig(data['menu'][old]['file'], label=data['menu'][new]['file'])
        self.entryconfig(data['menu'][old]['edit'], label=data['menu'][new]['edit'])
        self.entryconfig(data['menu'][old]['options'], label=data['menu'][new]['options'])
        self.entryconfig(data['menu'][old]['languages'], label=data['menu'][new]['languages'])
        self.entryconfig(data['menu'][old]['help'], label=data['menu'][new]['help'])
        
        self.file_menu.entryconfig(data['menu'][old]['new'], label=data['menu'][new]['new'])
        self.file_menu.entryconfig(data['menu'][old]['open'], label=data['menu'][new]['open'])
        self.file_menu.entryconfig(data['menu'][old]['save'], label=data['menu'][new]['save'])
        self.file_menu.entryconfig(data['menu'][old]['save as'], label=data['menu'][new]['save as'])
        self.file_menu.entryconfig(data['menu'][old]['save all'], label=data['menu'][new]['save all'])
        self.file_menu.entryconfig(data['menu'][old]['run'], label=data['menu'][new]['run'])
        self.file_menu.entryconfig(data['menu'][old]['close tab'], label=data['menu'][new]['close tab'])
        self.file_menu.entryconfig(data['menu'][old]['exit'], label=data['menu'][new]['exit'])

        self.edit_menu.entryconfig(data['menu'][old]['undo'], label=data['menu'][new]['undo'])
        self.edit_menu.entryconfig(data['menu'][old]['redo'], label=data['menu'][new]['redo'])
        self.edit_menu.entryconfig(data['menu'][old]['cut'], label=data['menu'][new]['cut'])
        self.edit_menu.entryconfig(data['menu'][old]['copy'], label=data['menu'][new]['copy'])
        self.edit_menu.entryconfig(data['menu'][old]['paste'], label=data['menu'][new]['paste'])
        self.edit_menu.entryconfig(data['menu'][old]['select all'], label=data['menu'][new]['select all'])
        self.edit_menu.entryconfig(data['menu'][old]['clear'], label=data['menu'][new]['clear'])

        self.options_menu.entryconfig(data['menu'][old]['tongues'], label=data['menu'][new]['tongues'])
        self.options_menu.entryconfig(data['menu'][old]['confirm'], label=data['menu'][new]['confirm'])
        self.options_menu.entryconfig(data['menu'][old]['basename'], label=data['menu'][new]['basename'])
        self.options_menu.entryconfig(data['menu'][old]['treeview'], label=data['menu'][new]['treeview'])
        self.options_menu.entryconfig(data['menu'][old]['tabasspaces'], label=data['menu'][new]['tabasspaces'])
        
        self.help_menu.entryconfig(data['menu'][old]['about'], label=data['menu'][new]['about'])

        #self.jyx.notebook.current().status_bar.config(text=data['messages'][new]['started'])

    def build(self):
        data = self.jyx.data
        tongue = self.jyx.options['tongue'].get()
        languages = self.jyx.data['languages']
        
        self.file_menu = tk.Menu(self, tearoff=0)
        self.add_cascade(label=data['menu'][tongue]['file'], menu=self.file_menu)
        self.file_menu.add_command(label=data['menu'][tongue]['new'],
                                   command=self.jyx.new,
                                   accelerator="Ctrl+N")
        self.file_menu.add_command(label=data['menu'][tongue]['open'],
                                   command=self.jyx.open,
                                   accelerator="Ctrl+O")
        self.file_menu.add_command(label=data['menu'][tongue]['save'],
                                   command=self.jyx.save,
                                   accelerator="Ctrl+S")
        self.file_menu.add_command(label=data['menu'][tongue]['save as'],
                                   command=self.jyx.save_as,
                                   accelerator="Ctrl+Shift+S")
        self.file_menu.add_command(label=data['menu'][tongue]['save all'],
                                   command=self.jyx.save,
                                   accelerator="Ctrl+Alt+S")
        self.file_menu.add_separator()
        self.file_menu.add_command(label=data['menu'][tongue]['run'],
                                   command=self.jyx.run,
                                   accelerator="F5")
        self.file_menu.add_separator()
        self.file_menu.add_command(label=data['menu'][tongue]['close tab'],
                                   command=self.jyx.notebook.close_tab,
                                   accelerator="Ctrl+X", state=tk.DISABLED)
        self.file_menu.add_command(label=data['menu'][tongue]['exit'],
                                   command=self.jyx.exit,
                                   accelerator="Ctrl+Q")

        self.edit_menu = tk.Menu(self, tearoff=0)
        self.add_cascade(label=data['menu'][tongue]['edit'], menu=self.edit_menu)
        self.edit_menu.add_command(label=data['menu'][tongue]['undo'],
                                   command=lambda: self.jyx.notebook.send('undo'),
                                   accelerator="Ctrl+Z")
        self.edit_menu.add_command(label=data['menu'][tongue]['redo'],
                                   command=lambda: self.jyx.notebook.send('redo'),
                                   accelerator="Ctrl+Y")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label=data['menu'][tongue]['cut'],
                                   command=lambda: self.jyx.notebook.send('cut'),
                                   accelerator="Ctrl+X")
        self.edit_menu.add_command(label=data['menu'][tongue]['copy'],
                                   command=lambda: self.jyx.notebook.send('copy'),
                                   accelerator="Ctrl+C")
        self.edit_menu.add_command(label=data['menu'][tongue]['paste'],
                                   command=lambda: self.jyx.notebook.send('paste'),
                                   accelerator="Ctrl+V")
        self.edit_menu.add_command(label=data['menu'][tongue]['select all'],
                                   command=lambda: self.jyx.notebook.send('select all'),
                                   accelerator="Ctrl+A")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label=data['menu'][tongue]['clear'],
                                   command=lambda: self.jyx.notebook.send('clear'))

        self.options_menu = tk.Menu(self, tearoff=0)
        self.add_cascade(label=data['menu'][tongue]['options'], menu=self.options_menu)
        tongues = data['menu'].keys()
        sub_tongue_menu = tk.Menu(self.options_menu, tearoff=0)
        self.options_menu.add_cascade(label=data['menu'][tongue]['tongues'], menu=sub_tongue_menu)
        for tong in sorted(tongues):
            sub_tongue_menu.add_radiobutton(label=data['menu'][tong]['tongue'],
                                            variable=self.jyx.options['tongue'].var,
                                            value=tong,
                                            command=lambda: self.jyx.update('tongue'))
        self.options_menu.add_checkbutton(label=data['menu'][tongue]['confirm'],
                                          onvalue=True, offvalue=False,
                                          variable=self.jyx.options['confirm'].var,
                                          command=lambda: self.jyx.update('confirm'))
        self.options_menu.add_checkbutton(label=data['menu'][tongue]['basename'],
                                          onvalue=True, offvalue=False,
                                          variable=self.jyx.options['basename'].var,
                                          command=lambda: self.jyx.update('basename'))
        self.options_menu.add_checkbutton(label=data['menu'][tongue]['treeview'],
                                          onvalue=True, offvalue=False,
                                          variable=self.jyx.options['treeview'].var,
                                          command=lambda: self.jyx.update('treeview'))
        self.options_menu.add_checkbutton(label=data['menu'][tongue]['tabasspaces'],
                                          onvalue=True, offvalue=False,
                                          variable=self.jyx.options['tabasspaces'].var,
                                          command=lambda: self.jyx.update('tabasspaces'))

        self.langmenu = tk.Menu(self, tearoff=0)
        self.add_cascade(label=data['menu'][tongue]['languages'], menu=self.langmenu)

        base = {}
        families = {}
        for lang, prop in languages.items():
            if prop['family'] == "":
                base[lang] = prop
                continue
            elif prop['family'] not in families:
                families[prop['family']] = {}
            families[prop['family']][lang] = prop
        for lang in sorted(base):
            self.langmenu.add_radiobutton(label=languages[lang]['label'],
                                          variable=self.jyx.options['language'].var,
                                          value=lang,
                                          command=lambda: self.jyx.update('language'))
        if len(families) > 0:
            self.langmenu.add_separator()
        for fam in sorted(families):
            menu = tk.Menu(self.langmenu, tearoff=0)
            self.langmenu.add_cascade(label=fam, menu=menu)
            for lang in sorted(families[fam]):
                menu.add_radiobutton(label=languages[lang]['label'],
                                     variable=self.jyx.options['language'].var,
                                     value=lang,
                                     command=lambda: self.jyx.update('language'))

        self.help_menu = tk.Menu(self, tearoff=0)
        self.add_cascade(label=data['menu'][tongue]['help'], menu=self.help_menu)
        self.help_menu.add_command(label=data['menu'][tongue]['about'], command=self.jyx.about)


class JyxTree(ttk.Treeview):

    def __init__(self, jyx):
        ttk.Treeview.__init__(self, jyx.get_root())
        self.jyx = jyx
        self.links = {}
        self.bind('<Button-1>', self.selection)

    def selection(self, event):
        current = self.identify('item', event.x, event.y)
        if current not in self.links: # prevent when clicking on top bar of the tree
            return
        at = self.links[current].at
        #print('Node :', self.links[current], '@', at)
        self.jyx.notebook.current().text.see("1.0+%d chars" % (at,))
        #print('Node:', self.links[current])
        #print(self.item(current))

    def explore(self, parent, counter, node):
        counter += 1
        identifier = f"Item_{counter}"
        self.insert(parent, counter, identifier, text=str(node))
        self.links[identifier] = node
        for n in node.get_children():
            counter = self.explore(identifier, counter, n)
        return counter

    def rebuild(self):
        self.delete(*self.get_children())
        self.links = {}
        try:
            lang = self.jyx.notebook.current().lang
            text = self.jyx.notebook.current().text.get('1.0', tk.END)
            if lang in PARSERS:
                ast = PARSERS[lang]().parse(text)
                self.column("#0", stretch=True)
                self.heading("#0", text="Element", anchor="w")
                self.explore("", 0, ast)
        except ValueError as e:
            print('Error on parsing:', e)


class JyxNotebookIterator:

    def __init__(self, parent):
        self.cpt = -1
        self.parent = parent

    def __next__(self):
        self.cpt += 1
        if self.cpt < self.parent.index(tk.END):
            return self.parent.notes[self.cpt]
        else:
            raise StopIteration


class JyxNotebook(ttk.Notebook):

    def __init__(self, jyx):
        ttk.Notebook.__init__(self, jyx.get_root())
        self.jyx = jyx
        self.notes = []
        self.is_loading_file = True # for the first time, to desactivate jyx#update
        self.new_tab()
        self.bind('<<NotebookTabChanged>>', self.on_tab_change)
        self.current().focus()
        self.is_loading_file = False

    def __iter__(self):
        return JyxNotebookIterator(self)

    def relabel(self, new):
        for i in range(self.index('end')):
            if self.notes[i].filepath is None:
                self.notes[i].update_title()

    def new_tab(self, event=None, lang=None):
        if lang is None: lang = self.jyx.data['default_language']
        jn = JyxNote(self, lang)
        self.add(jn.frame, text=self.jyx.data['menu'][self.jyx.options['tongue'].get()]['new'])
        jn.index = self.index('end') - 1
        self.select(jn.index)
        self.notes.append(jn)
        jn.focus()
        if self.index("end") > 1:
            self.jyx.menu.file_menu.entryconfig(Jyx.CLOSE_TAB, state=tk.ACTIVE)
        if not self.is_loading_file:
            self.jyx.update()
        return jn.index

    def close_tab(self):
        del self.notes[self.index("current")]
        self.forget(self.index("current"))
        if self.index("end") == 1:
            self.jyx.menu.file_menu.entryconfig(Jyx.CLOSE_TAB, state=tk.DISABLED)
        self.jyx.update()

    def on_tab_change(self, event):
        if self.is_loading_file:
            return
        self.jyx.options['language'].var.set(self.current().lang)
        self.jyx.update()

    def current(self):
        return self.notes[self.index("current")]

    def current_index(self):
        return self.index("current")

    def __len__(self):
        return self.index("end")

    def get_position(self):
        return self.current().text.index(tk.INSERT)

    def is_anyone_dirty(self):
        for i in range(self.index("end")):
            if self.notes[i].dirty:
                return True
        return False
    
    def is_dirty(self):
        return self.current().dirty

    def get_filepath(self):
        return self.current().filepath

    def open(self, filename, content):
        self.is_loading_file = True
        _, ext = os.path.splitext(filename)
        lang = self.jyx.data['default_language']
        for key, lg in self.jyx.data['languages'].items():
            if ext in lg['extension']:
                lang = key
                break
        if self.current().dirty or self.current().filepath is not None or len(self) > 1:
            self.new_tab(lang=lang)
        else:
            self.current().change_lang(lang)
        self.jyx.options['language'].var.set(lang)
        self.current().load(filename, content)
        self.is_loading_file = False

    def send(self, order):
        if order == 'cut':
            self.current().cut()
        elif order == 'paste':
            self.current().paste()
        elif order == 'copy':
            self.current().copy()
        elif order == 'select all':
            self.current().select_all()
        elif order == 'clear':
            self.current().clear()
        elif order == 'undo':
            self.current().undo()
        elif order == 'redo':
            self.current().redo()


class JyxNote:

    #MOD_NUM_LOCK  = 0x0010
    MOD_CAPS_LOCK = 0b00000010
    MOD_SHIFT     = 0b00000001
    # Linux
    MOD_CONTROL_WIN   = 0b00001100
    MOD_CONTROL_LIN   = 0b00010100
    MOD_ALT_LEFT_LIN  = 0b00011000
    MOD_ALT_LEFT_WIN  = 0b100000000000001000
    MOD_ALT_RIGHT_LIN = 0b10010000
    MOD_ALT_RIGHT_WIN = 0b100000000000001100
    
    def __init__(self, notebook, lang):
        self.notebook = notebook

        self.frame = ttk.Frame(self.notebook) #, bd=2, relief=tk.SUNKEN)
        self.scrollbar = ttk.Scrollbar(self.frame)
        self.text = tk.Text(self.frame, wrap=tk.NONE, bd=0, undo=True,
                            yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.text.yview)
        
        self.text.config(font=('consolas', 12), undo=True, wrap='word')
        self.text.bind('<KeyPress>', self.update_text_before)
        #self.text.bind('<KeyRelease>', self.update_text_after)
        self.text.bind('<ButtonRelease-1>', self.notebook.jyx.update_status)
        if platform.system() == 'Windows':
            self.text.bind('<Control-Key-a>', self.select_all)
            self.text.bind('<Control-Key-n>', self.notebook.new_tab)
            self.text.bind('<Control-Key-t>', self.notebook.new_tab)
            self.text.bind('<Control-Key-z>', self.undo)
            self.text.bind('<Control-Key-y>', self.redo)
            self.text.bind('<Control-Key-c>', self.copy)
            self.text.bind('<Control-Key-x>', self.cut)
            self.text.bind('<Control-Key-v>', self.paste)
            self.text.bind('<Control-Key-p>', self.notebook.jyx.treeview.rebuild)
            self.text.bind('<Control-Key-s>', self.notebook.jyx.save)

        # Status bas
        jyx = self.notebook.jyx
        self.status_bar = tk.Label(self.frame, bd=1, relief=tk.SUNKEN)
        #jyx.data['messages'][jyx.options['tongue'].get()]['started'] text will be updated ASAP
        self.status_bar.config(text='', anchor=tk.E, padx=20)

        # Attributes
        self.filepath = None
        self.dirty = False
        self.lang = lang

        # Layout
        self.frame.grid_rowconfigure(0, weight=100)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        self.text.grid(row=0, column=0, sticky=tk.NS+tk.EW)
        self.scrollbar.grid(row=0, column=1, sticky=tk.NS)
        self.status_bar.grid(row=2, column=0, columnspan=2, sticky=tk.EW)
        
        # Tags
        self.tokens = {}
        self.tags = {}
        self.change_lang(lang, True)

    def focus(self):
        self.text.focus_force()

    def update_title(self):
        dirty = ' *' if self.dirty else ''
        tongue = self.notebook.jyx.options['tongue'].get()
        if self.filepath is None:
            file = self.notebook.jyx.data['menu'][tongue]['new']
        else:
            file = os.path.basename(self.filepath)
        self.notebook.tab(self.index, text=f"{file}{dirty}")
        self.notebook.jyx.update()

    def change_lang(self, lang, init=False):
        if not init:
            # Clear all tags
            for tag in self.text.tag_names():
                if tag == 'sel':
                    continue # sans cela, bug du selection_delete qui ne supprime pas le 1er caractere ! XXX
                self.text.tag_delete(tag, 1.0, tk.END)
            self.tokens.clear()
            self.tags.clear()
        # Load new lang
        self.lang = lang
        self.tokens = self.notebook.jyx.data['languages'][lang]['token']
        for tag, val in self.notebook.jyx.data['languages'][lang]['style']['default'].items():
            self.tags[tag] = self.text.tag_config(tag, foreground=val['color'])
        # Retag
        self.tag()
        # Refresh status
        if not init:
            self.notebook.jyx.update_status()

    #
    # Handling of state and deleting, writing, loading and saving
    #
    def save(self, filename=None, raw=False):
        filename = filename if filename is not None else self.filepath
        if filename is None:
            raise Exception("Impossible to save, no file name specified.")
        f = open(filename, mode='w', encoding='utf8')
        content = self.text.get('1.0', tk.END)
        f.write(content)
        f.close()
        if not raw: # skip updating the state if it is a "raw" save for executing file without to have to save it first
            self.dirty = False
            self.filepath = filename
            self.update_title()
    
    def load(self, filename, content):
        self.text.delete('1.0', tk.END)
        self.text.insert('1.0', content)
        self.text.edit_reset()
        self.dirty = False
        self.filepath = filename
        self.tag()
        self.text.see(tk.INSERT)
        self.update_title()
    
    def write(self, content, at=tk.INSERT):
        self.text.insert(at, content)
        self.text.edit_separator()
        self.dirty = True
        self.update_title()

    def delete(self, first, last=None):
        self.text.delete(first, last)
        self.text.edit_separator()
        self.dirty = True
        self.update_title()

    def undo(self):
        try:
            self.text.edit_undo()
            self.dirty = True
            self.update_title()
        except tk.TclError:
            self.notebook.jyx.log.info("Nothing to undo")

    def redo(self):
        try:
            self.text.edit_redo()
            self.dirty = True
            self.update_title()
        except tk.TclError:
            self.notebook.jyx.log.info("Nothing to redo")

    #
    # Handling of selection: deleting, getting, selecting and unselecting
    #
    def selection_delete(self):
        self.delete(tk.SEL_FIRST, tk.SEL_LAST)
        self.selection_clear()

    def selection_get(self):
        return self.text.get(tk.SEL_FIRST, tk.SEL_LAST)

    def selection_set(self, index1, index2):
        if self.text.compare(index1, '<', index2):
            self.text.tag_add(tk.SEL, f'{index1}', f'{index2}')
        else:
            self.text.tag_add(tk.SEL, f'{index2}', f'{index1}')

    def selection_clear(self):
        self.text.tag_remove(tk.SEL, '1.0', tk.END)

    def has_selection(self):
        return len(self.text.tag_ranges('sel')) > 0

    #
    # Basic functions (called from menu without event)
    #
    def paste(self, event=None):
        content = self.notebook.jyx.root.clipboard_get()
        if self.has_selection():
            self.selection_delete()
        self.text.insert(tk.INSERT, content)
        self.text.see(tk.INSERT)
        return 'break'

    def cut(self, event=None):
        self.copy(event)
        self.selection_delete()
        self.text.see(tk.INSERT)
        return 'break'

    def copy(self, event=None):
        if self.has_selection():
            self.notebook.jyx.root.clipboard_clear()
            self.notebook.jyx.root.clipboard_append(self.selection_get())
        return 'break'

    def select_all(self, event=None):
        self.selection_clear()
        self.selection_set('1.0', tk.END)
        self.text.mark_set(tk.INSERT, tk.END)
        self.text.see(tk.INSERT)
        return 'break'

    def clear(self, event=None):
        self.select_all(event)
        self.selection_delete()

    def control_pressed(self, state):
        return state in [JyxNote.MOD_CONTROL_LIN, JyxNote.MOD_CONTROL_WIN]

    def alt_left_pressed(self, state):
        return state in [JyxNote.MOD_ALT_LEFT_LIN, JyxNote.MOD_ALT_LEFT_WIN]

    def alt_right_pressed(self, state):
        return state in [JyxNote.MOD_ALT_RIGHT_LIN, JyxNote.MOD_ALT_RIGHT_WIN]

    #
    # React to key events
    #
    def update_text_before(self, event):
        text = event.widget
        #print(f'{event.state:08b} {platform.system()}')
        if self.control_pressed(event.state):
            pass
            #print(f'ctrl {event.state:08b} {platform.system()}')
        if self.alt_right_pressed(event.state):
            pass
            #print(f'alt right {event.state:08b} {platform.system()}')
        if self.alt_left_pressed(event.state):
            pass
            #print(f'alt left {event.state:08b} {platform.system()}')
        if JyxNote.MOD_CAPS_LOCK & event.state:
            pass
            #print(f'caps lock')
        if self.control_pressed(event.state):
            #print('update_text_before:', event.keysym)
            if event.keysym == 'a':
                self.select_all()
            elif event.keysym in ['n', 't']:
                self.notebook.new_tab()
            elif event.keysym == 'z':
                self.undo()
            elif event.keysym == 'y':
                self.redo()
            elif event.keysym == 'c':
                self.copy()
            elif event.keysym == 'x':
                self.cut()
            elif event.keysym == 'v':
                self.paste()
            elif event.keysym == 'p':
                self.notebook.jyx.treeview.rebuild()
            elif event.keysym == 's':
                self.notebook.jyx.save()
            else:
                self.notebook.jyx.log.info(f'Event not handled: {event.keysym} with state={event.state}')
            return 'break'
        elif event.keysym == 'Control_L':
            return 'break'
        elif event.keysym in ['Left', 'Right', 'Up', 'Down', 'End', 'Home']: # 37, 39
            codes = {
                'Left': 'insert-1c',
                'Right': 'insert+1c',
                'Up': 'insert-1l',
                'Down': 'insert+1l',
                'End': 'insert lineend',
                'Home': 'insert linestart'
            }
            nex = codes[event.keysym]
            if self.has_selection():
                self.selection_clear()
            else:
                self.start = text.index(tk.INSERT)
            if JyxNote.MOD_SHIFT & event.state:
                self.selection_set(nex, self.start)
            text.mark_set(tk.INSERT, f'{nex}')
            text.see(tk.INSERT)
            self.notebook.jyx.update_status()
            return 'break'
        elif event.keysym == 'BackSpace':
            if len(text.tag_ranges('sel')) > 0:
                self.selection_delete()
            else:
                if self.notebook.jyx.options['tabasspaces'].get():
                    col = int(self.text.index("insert").split('.')[1]);
                    nb = col % 4
                    nb = 4 if nb == 0 else nb
                    if self.text.get('insert-%dc' % (nb,), tk.INSERT).isspace():
                        self.delete('insert-%dc' % (nb,), tk.INSERT)
                    else:
                        self.delete('insert-1c', tk.INSERT)
                    #text.mark_set(tk.INSERT, 'insert-%dc' % (nb,))
                else:
                    self.delete('insert-1c', tk.INSERT)
            self.notebook.jyx.update_status()
            return 'break'
        elif event.keysym == 'Delete':
            if len(text.tag_ranges('sel')) > 0:
                self.selection_delete()
            elif text.index(tk.END) != text.index(tk.INSERT):
                self.delete(tk.INSERT)
            self.notebook.jyx.update_status()
            return 'break'
        elif event.keysym == 'Escape':
            self.selection_clear()
            self.notebook.jyx.update_status()
            return 'break'
        elif event.keysym == 'Return':
            if self.notebook.jyx.options['tabasspaces'].get():
                line = self.text.get('insert linestart', 'insert lineend')
                decal = len(line) - len(line.lstrip())
                if decal > 0:
                    content = '\n' + ' ' * decal
                else:
                    content = '\n'
            else:
                content = '\n'
        elif event.char == '\r':
            content = '\n'
        elif event.char == '\t':
            if self.notebook.jyx.options['tabasspaces'].get():
                col = int(self.text.index("insert").split('.')[1]);
                content = ' ' * (4 - (col % 4))
            else:
                content = '\t'
        elif event.keysym == 'space':
            content = ' '
        elif event.char.isprintable(): #isalnum()
            #info self.notebook.jyx.log.info(event)
            content = event.char
        else:
            self.notebook.jyx.log.info(f'Unknown: {event}')
            return 'break'
        if len(text.tag_ranges('sel')) > 0:
            self.selection_delete()
        self.write(content)
        self.tag(self.text.index("insert linestart"), self.text.index("insert lineend"))
        text.see(tk.INSERT)
        self.notebook.jyx.update_status()
        return 'break'

    #def update_text_after(self, event):
        #self.tag()
        #res = event.widget.search('--> ', "insert linestart", "insert lineend")
        #while res != '':
        #    self.notebook.jyx.log.info(res)
        #    self.delete(res, res + '+4c')
        #    self.write(res, '→ ')
        #    res = event.widget.search('--> ', res, "insert lineend")
        #return 'break'

    #
    # Tag
    #
    def tag(self, start='1.0', end=tk.END):
        if not self.notebook.jyx.has(f"languages.{self.lang}.support", "tokenize") or self.lang not in LEXERS:
            return
        # Clear all tags
        for tag in self.text.tag_names():
            if tag == 'sel':
                continue # sans cela, bug du selection_delete qui ne supprime pas le 1er caractere ! XXX
            self.text.tag_remove(tag, start, end)
        content = self.text.get(start, end)
        res = LEXERS[self.lang]().lex(content)
        for t in res:
            t_start = self.text.index("%s+%d chars" % (start, t.index))
            t_end = self.text.index("%s+%d chars" % (start, t.end))
            self.text.tag_add(t.kind, t_start, t_end)

#-------------------------------------------------------------------------------

class ParserJSON:

    def __init__(self):
        pass

    def parse(self, content):
        tokens = LexerJSON().lex(content, ['newline'])
        return self.read(deque(tokens))

    def read(self, tokens):
        #print('read', tokens[0], len(tokens))
        if len(tokens) == 0:
            print(tokens)
            raise Exception("No token")
        token = tokens[0]
        if token.kind == 'separator' and token.value == '{':
            return self.read_object(tokens)
        elif token.kind == 'separator' and token.value == '[':
            return self.read_array(tokens)
        else:
            return self.read_terminal(tokens)

    def read_object(self, tokens):
        #print('read_object', tokens[0], len(tokens))
        at = tokens[0].index
        tokens.popleft()
        elements = self.read_keyvalue(tokens)
        return ListNode(at, elements, '{}')

    def read_keyvalue(self, tokens):
        #print('read_keyvalue', tokens[0], len(tokens))
        if len(tokens) == 0:
            raise Exception('Malformed object literal: unfinished')
        token = tokens[0]
        if token.kind == 'separator' and token.value == '}':
            tokens.popleft()
            return []
        elif token.kind == 'separator' and token.value == ',':
            tokens.popleft()
            token = tokens[0]
        if token.kind != 'key':
            raise Exception('Malformed object literal on token: ' + str(token) + ' -> not a key')
        if len(tokens) < 2:
                raise Exception('Malformed object literal on token: ' + str(token) + ' -> key without :')
        if len(tokens) < 3:
                raise Exception('Malformed object literal on token: ' + str(token) + ' -> key without value')
        tokens.popleft()
        tokens.popleft()
        n = KeyValueElementNode(token.index, token.value, self.read(tokens))
        return [n] + self.read_keyvalue(tokens)

    def read_array(self, tokens):
        #print('read_array', tokens[0], len(tokens))
        at = tokens[0].index
        tokens.popleft()
        elements = self.read_item(tokens)
        return ListNode(at, elements, '[]')

    def read_item(self, tokens):
        #print('read_item', tokens[0], len(tokens))
        if len(tokens) == 0:
            raise Exception('Malformed array literal: unfinished')
        token = tokens[0]
        if token.kind == 'separator' and token.value == ']':
            tokens.popleft()
            return []
        elif token.kind == 'separator' and token.value == ',':
            tokens.popleft()
        n = self.read(tokens)
        return [n] + self.read_item(tokens)

    def read_terminal(self, tokens):
        #print('read_terminal', tokens[0], len(tokens))
        token = tokens[0]
        tokens.popleft()
        if token.kind == 'string':
            return LiteralNode(token.index, token.kind, token.value)
        elif token.kind == 'number':
            return LiteralNode(token.index, token.kind, token.value)
        elif token.kind == 'boolean':
            return LiteralNode(token.index, token.kind, token.value)
        else:
            raise Exception("Kind not known: " + str(token.kind))   


class NodeIterator:

    def __init__(self, obj):
        self.obj = obj
        self.count = -1

    def __next__(self):
        self.count += 1
        if self.count >= len(self.obj.children):
            raise StopIteration
        return self.obj.children[self.count]


class Node:

    def __init__(self, msg, at):
        self.msg = msg
        self.at = at

    def __repr__(self):
        return self.msg

    def __str__(self):
        return self.msg

    def __iter__(self):
        return NodeIterator(self)

    def explore(self, lvl=0):
        print(f"{'    ' * lvl}{self.msg}")

    def get_children(self):
        return []


class IfNode(Node):

    def __init__(self, at, condition, if_true, if_false):
        Node.__init__(self, 'if', at)
        self.condition = condition
        self.if_true = if_true
        self.if_false = if_false
        self.at = at


class WhileNode(Node):

    def __init__(self, at, condition, action):
        Node.__init__(self, 'while', at)
        self.condition = condition
        self.action = action
        self.at = at


class LiteralNode(Node):

    def __init__(self, at, kind, value):
        Node.__init__(self, f'{value} : {kind}', at)
        self.kind = kind
        self.value = value
        self.at = at


class ListNode(Node):

    def __init__(self, at, elements, kind=None):
        if kind is not None:
            msg = kind
        elif len(elements) > 0 and type(elements[0]) == KeyValueElementNode:
            msg = 'dict'
        else:
            msg = 'list'
        Node.__init__(self, msg, at)
        self.children = elements

    def explore(self, lvl=0):
        Node.explore(self, lvl)
        for c in self.children:
            c.explore(lvl + 1)

    def get_children(self):
        return self.children


class KeyValueElementNode(Node):

    def __init__(self, at, key, value):
        Node.__init__(self, 'key-value', at)
        self.key = key
        self.value = value

    def __str__(self):
        return f"{self.key} : {self.value.msg}"

    def explore(self, lvl=0):
        Node.explore(self, lvl)
        print(f"{'    ' * (lvl + 1)}{self.key}")
        self.value.explore(lvl + 1)

    def get_children(self):
        # We skip the {} step in order to present directly the elements of {}
        if type(self.value) == ListNode:
            return self.value.get_children()
        elif type(self.value) == LiteralNode:
            return [] # no more dispay
        else:
            return [self.value]

#-------------------------------------------------------------------------------

class LexerJSON:

    def __init__(self):
        pass

    def lex(self, content, discard=None):
        res = []
        line = 0
        index = 0
        discard = discard if discard is not None else []
        while index < len(content):
            c = content[index]
            if c in ['{', '}', '[', ']', ',', ':']:
                res.append(Token('separator', c, line, index))
                if c == ':' and len(res) > 1 and res[-2].kind == 'string':
                    res[-2].kind = 'key'
            elif c == '"':
                s = '"'
                j = index + 1
                while j < len(content):
                    s += content[j]
                    if content[j] == '"':
                        if j > 1 and content[j-1] == '\\' and content[j-2] == '\\':
                            break
                        elif j > 0 and content[j-1] != '\\':
                            break
                    j += 1
                res.append(Token('string', s, line, index))
                index += len(s) - 1
            elif c in ['\\r', '\\n']:
                if len(content) > i+1 and content[i+1] in ['\\r', '\\n']:
                    if 'newline' not in discard:
                        res.append(Token, 'newline', content[index, index+1], line, index)
                    index += 1
                else:
                    if 'newline' not in discard:
                        res.append(Token, 'newline', s, line, index)
                line += 1
            elif c in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                s = c
                j = index + 1
                while j < len(content):
                    if content[j] not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                        break
                    s += content[j]
                    j += 1
                res.append(Token('number', s, line, index))
                index += len(s) - 1
            elif c.isalpha():
                s = c
                j = index + 1
                while j < len(content):
                    if not content[j].isalpha() and c not in ['_']:
                        break
                    s += content[j]
                    j += 1
                    if s in ['false', 'true']:
                        res.append(Token('boolean', s, line, index))
                index += len(s) - 1
            elif c in [' ', '\t']:
                pass
            index += 1
        return res

class Token:

    def __init__(self, kind, value, line, index):
        self.kind = kind
        self.value = value
        self.line = line
        self.index = index
        self.end = self.index + len(self.value)

    def __repr__(self):
        return f"{self.value}:{self.kind}"

    def __str__(self):
        return f"({self.value}:{self.kind}@{self.line,self.index}#{len(self.value)})"

LEXERS = {'json': LexerJSON}
PARSERS = {'json': ParserJSON}

#
# Main
#

if __name__ == '__main__':
    Jyx()
